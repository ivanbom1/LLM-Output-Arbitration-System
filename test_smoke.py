from critics import run_accuracy_eval, run_logic_eval, run_completeness_eval

# One fixed test fixture with planted flaws for all three critics:
# - accuracy: wrong year (Wall fell in 1989, not 1987)
# - logic: non-sequitur ("this proves..." doesn't follow from the premise)
# - completeness: the question asks for causes, the answer never gives any

QUESTION = "What year did the Berlin Wall fall, and what were the main causes of its collapse?"
ANSWER = (
    "The Berlin Wall fell in 1987, marking the end of the Cold War immediately. "
    "This proves that East Germany's economy was actually stronger than West Germany's at the time."
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