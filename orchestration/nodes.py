from .state import ArbitrationState
from critics import run_accuracy_eval, run_logic_eval, run_completeness_eval
from eval_options import ACTIVE_SCALE
import time


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
    
    raise NotImplementedError

def synthesize_verdict_node(state: ArbitrationState) -> dict:
    
    raise NotImplementedError
