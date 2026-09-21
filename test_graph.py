from orchestration.graph import build_graph

app = build_graph()

QUESTION = "What is compound interest, how does it differ from simple interest, and if I invest $1000 at 5% annual compound interest, roughly how much will I have after 10 years?"

ANSWER = (
    "Compound interest is interest calculated only on the original principal amount, "
    "never on the interest that has already accumulated. If you invest $1000 at 5% for "
    "10 years, you'll end up with exactly $1500, since 5% of $1000 is $50 per year over 10 years."
)

result = app.invoke({"question": QUESTION, "output_text": ANSWER})
verdict = result["verdict"]

print("=== VERDICT ===")
print(f"overall_score: {verdict.overall_score}  confidence: {verdict.confidence:.2f}")
print(f"summary: {verdict.summary}")

print(f"\nconfirmed_issues ({len(verdict.confirmed_issues)}):")
for i, issue in enumerate(verdict.confirmed_issues, 1):
    print(f"  {i}. [{issue.source_critic.value}] severity={issue.severity.name}")
    print(f"     problem:  {issue.problem}")
    print(f"     evidence: {issue.evidence}")

print(f"\ndismissed_flags ({len(verdict.dismissed_flags)}):")
for i, flag in enumerate(verdict.dismissed_flags, 1):
    print(f"  {i}. [{flag.source_critic.value}]")
    print(f"     original:  {flag.original_problem}")
    print(f"     reasoning: {flag.reasoning}")

print("\n=== DISAGREEMENTS DETECTED ===")
for d in result["disagreements"]:
    print(f"  {d}")