from llm_connect import groq_client
from config import GROQ_MODEL_ADJUDICATOR
from prompts import ADJUDICATION_PROMPT
from verdict_schema import AdjudicationResult

def format_report(name: str, report) -> str:
    if report is None:
        return f"{name.upper()} REPORT: FAILED - this critic didn't return a result"
    
    lines = [f"{name.upper()} REPORT (score={report.score}, confidence={report.confidence}):"]
    if not report.issues:
        lines.append(" no issue found")
    for i, issue in enumerate(report.issue, 1):
        lines.append(f"  issue {i} (severity={issue.severity.name})")
        if issue.quote:
            lines.append(f" quote: {issue.quote!r}")
        if issue.missing_aspect:
            lines.append(f" missing_aspect: {issue.missing_aspect!r}")
        lines.append(f" problem: {issue.problem}")
    return "\n".join(lines)

def format_disagreement(disagreements: list) -> str:
    if not disagreements:
        return "DISAGREEMENTS: \n none detected"
    lines = ["DISAGREEMENTS:"]
    for d in disagreements:
        lines.append(f"  - {d}")
    return "\n".join(lines)

