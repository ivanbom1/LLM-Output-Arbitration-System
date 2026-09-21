from .state import ArbitrationState
from critics import run_accuracy_eval, run_logic_eval, run_completeness_eval
from eval_options import ACTIVE_SCALE
import time

from adjudicator import run_adjudication
from schema import Dimension
from verdict_schema import ConfirmedIssue, Verdict

def call_with_retry(fnc, *args, max_attempts: int = 3, delay_sec: float = 2.0, **kwargs):
    
    last_err = None
    for a in range(1, max_attempts + 1):
        try:
            return fnc(*args, **kwargs)
        except Exception as e:
            last_err = e
            if a < max_attempts:
                time.sleep(delay_sec)
        
    raise last_err

def parse_input_node(state: ArbitrationState) -> dict:
    """
    Parser function for now blindly trusts to the input data and stands only as a
    START node in this pipeline
    """
    
    return {}

def accuracy_node(state: ArbitrationState) -> dict:
    try:
        
        report = call_with_retry(run_accuracy_eval, state["output_text"])
        return {"accuracy_report": report}
    
    except Exception as e:
        return {
            "accuracy_report": None,
            "disagreements": [{"type": "critique_failute", "critic": "accuracy", "error": str(e)}],
        }
    
def logic_node(state: ArbitrationState) -> dict:
    try:
            
            report = call_with_retry(run_logic_eval, state["output_text"])
            return {"logic_report": report}
        
    except Exception as e:
        return {
            "logic_report": None,
            "disagreements": [{"type": "critique_failute", "critic": "logic", "error": str(e)}],
        }
        
def completeness_node(state: ArbitrationState) -> dict:
    try:
        report = call_with_retry(run_completeness_eval, state["output_text"], state["question"])
        return {"completeness_report": report}
    
    except Exception as e:
        return {
            "completeness_report": None,
            "disagreements": [{"type": "critic_failure", "critic": "completeness", "error": str(e)}],
        }
        
def collect_critiques_node(state: ArbitrationState) -> dict:
    """
    Empty-node which `collects` critic's reports after complteion on the same stage of the graph
    """
    return {}

def detect_disagreements_node(state: ArbitrationState) -> dict:
    # disagreements detection algorithms based on the score difference
    reports = {
        "acurracy": state["accuracy_report"],
        "logic": state["logic_report"],
        "completeness": state["completeness_report"]
    }

    reports = {k: v for k, v in reports.items() if v is not None}
    
    disagreements:list = []
    gap_threshold = ACTIVE_SCALE["disagreement_gap"]
    
    names = list(reports.keys())
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = reports[names[i]], reports[names[j]]
            if abs(a.score - b.score) > gap_threshold:
                disagreements.append({
                    "type": "score_gap",
                    "critics": [names[i], names[j]],
                    "detail": f"{names[i]}={a.score} vs {names[j]}={b.score}",
                })
                
    issue_counts = {name: len(r.issues) for name, r in reports.items()}
    if any(issue_counts.values()) and not all(issue_counts.values()):
        disagreements.append({
            "type": "coverage_gap",
            "detail": issue_counts
        })
    return {"disagreements": disagreements}

def adjudicate_node(state: ArbitrationState) -> dict:
    
    try:
        result = call_with_retry(
            run_adjudication,
            state["question"],
            state["output_text"],
            state["accuracy_report"],
            state["logic_report"],
            state["completeness_report"],
            state["disagreements"]
        )
        return {"adjudication": result}

    except Exception as e:
        return {
            "adjudication": None,
            "disagreements": [{"type": "adjudicator_failure", "error": str(e)}],
        }
        
def compute_overall_score(confirmed_issues: list) -> int:
    if not confirmed_issues:
        return 10

    highs = sum(1 for i in confirmed_issues if i.severity.name == "HIGH")
    meds = sum(1 for i in confirmed_issues if i.severity.name == "MEDIUM")
    if highs >= 2:
        return 2
    if  highs == 1:
        return 4
    if meds >= 1:
        return 6
    
    return 8 # if only low issues confirmed

def compute_confidence(reports: list) -> float:
    available = [r.confidence for r in reports if r is not None]
    return sum(available / len(available) if available else 0.5)

def build_summary(confirmed_issues: list, dismissed_flags: list) -> str:
    if not confirmed_issues:
        return ("All three critics evaluated this output and, after review no confirmed"
                "issues were found accross accuracy, logic, or completeness.")
    
    highs = sum(1 for i in confirmed_issues if i.severity.name == "HIGH")
    parts = [f"{len(confirmed_issues)} issue(s) were confirmed after adjudication"]
    if highs:
        parts.append(f"including {highs} high-severity issue(s)")
    if dismissed_flags:
        parts.append(f"{len(dismissed_flags)} additional critic flag(s) were reviewed and dismissed")
        
    return ", ".join(parts) + "."
    
def synthesize_verdict_node(state: ArbitrationState) -> dict:
    
    adjudication = state.get("adjudication")
    disagreements = state.get("disagreements") or []
    reports = {
        "accuracy": state["accuracy_report"],
        "logic" : state["logic_report"],
        "completeness": state["completeness"],
    }
    
    adjudicator_fail = any(d.get("type") == "adjudicator_failure" for d in disagreements)
    
    if adjudication is not None:
        
        confirmed = adjudication.confirmed_issues
        dismissed = adjudication.dismissed_flags
        
    elif adjudicator_fail:
        
        confirmed = [
            ConfirmedIssue(
                source_critic=Dimension(name),
                problem=issue.problem,
                severity=issue.severity,
                evidence="Adjudicator unavailable — auto-confirmed from critic report without review.",
            )
            for name, report in reports.items() if report is not None
            for issue in report.issues
        ]
        dismissed = []
    else:
        # True short-circuit: every critic came back clean, adjudicate never ran.
        confirmed = []
        dismissed = []
 
    confidence = compute_confidence(list(reports.values()))
    if adjudicator_fail:
        confidence *= 0.5  # penalize - nothing here was genuinely reviewed
 
    verdict = Verdict(
        overall_score=compute_overall_score(confirmed),
        confidence=confidence,
        confirmed_issues=confirmed,
        dismissed_flags=dismissed,
        summary=build_summary(confirmed, dismissed),
    )
    return {"verdict": verdict} 
