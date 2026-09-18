from critics import run_accuracy_eval, run_logic_eval, run_completeness_eval

# One fixed test fixture with planted flaws for all three critics:
# - accuracy: wrong year (Wall fell in 1989, not 1987)
# - logic: non-sequitur ("this proves..." doesn't follow from the premise)
# - completeness: the question asks for causes, the answer never gives any

QUESTION = "What does HTTP stand for, what port does it typically use by default, and what does HTTPS add on top of it?"
ANSWER = (
    "HTTP stands for HyperText Transfer Protocol, and it typically communicates using "
    "port 11434 by default."
)


def print_report(label, report):
    print(f"\n=== {label} ===")
    print(f"score: {report.score}  confidence: {report.confidence}")
    if not report.issues:
        print("no issues flagged")
        return
    for i, issue in enumerate(report.issues, 1):
        print(f"  issue {i}  severity={issue.severity.name}")
        print(f"    quote:           {issue.quote!r}")
        print(f"    missing_aspect:  {issue.missing_aspect!r}")
        print(f"    problem:         {issue.problem}")


if __name__ == "__main__":
    print_report("ACCURACY", run_accuracy_eval(ANSWER))
    print_report("LOGIC", run_logic_eval(ANSWER))
    print_report("COMPLETENESS", run_completeness_eval(ANSWER, QUESTION))