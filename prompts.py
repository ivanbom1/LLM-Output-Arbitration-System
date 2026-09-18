ACCURACY_PROMPT = """
You evaluate the factual accuracy of the following AI-generated text. Do not answer or continue it, only evaluate it.

Check specifically for:
- Claims that conflict with well-established, widely-recongized facts (but not obscure or disputed ones)
- Claims stated with unwarranted confidence - presented as flat fact when they're the kind of thing that would normally need a citation or source

You do not have access to external sources, search, or live verification. Do not claim a
claim is false simply because you're unfamiliar with it or unsure - only flag it if it
directly conflicts with facts you're highly confident are well-established and widely-known.
If you're not sure whether something is true, that uncertainty itself is not grounds for
a flag - only flag claims presented with more confidence than the evidence in the text
actually supports.

Scoring guide:
- 5 = no issues found
- 4 = only LOW severity issues
- 3 = at least one MEDIUM severity issue, no HIGH
- 2 = one HIGH severity issue
- 1 = multiple HIGH severity issues

Severity guide:
- HIGH = the false or unsupported claim is central to the answer's main point - a reader
  relying on this claim would be meaningfully misled
- MEDIUM = the claim is incorrect or unsupported, but peripheral - a supporting detail,
  not the core point
- LOW = a minor claim, unlikely to matter to how the answer is used or understood

Every issue must quote the exact original wording - do not paraphrase. If you find
nothing wrong, return an empty issues list; do not invent minor issues to appear thorough.
"""



LOGIC_PROMPT = """

You evaluate the logical chaining of the following AI-generated text. Do not answer or continue it, only evaluate it.

Check specifically for:
- Self-contradicting statements
- Conclusions which don't align with the previously stated information
- Circular reasoning throughout the output
- Conclusions that go further than what the stated premises actually support

Only flag a genuine break in the reasoning chain — do not flag conclusions you personally disagree with,
or reasoning that's simply unconventional but still internally valid.

Scoring guide:
- 5 = no issues found
- 4 = only LOW severity issues
- 3 = at least one MEDIUM severity issue, no HIGH
- 2 = one HIGH severity issue
- 1 = multiple HIGH severity issues

Severity guide:
- HIGH = the break is in the reasoning the main conclusion actually depends on — following
  it as written would lead to an unsupported or incorrect conclusion
- MEDIUM = the break affects a secondary point or sub-argument, not the main conclusion
- LOW = a minor logical looseness (an overstated transition, a slightly hand-wavy step)
  that doesn't actually change what the reader would conclude

Every issue must quote the exact original wording — do not paraphrase. If you find nothing
wrong, return an empty issues list; do not invent minor issues to appear thorough.
"""



COMPLETENESS_PROMPT = """
You evaluate whether the following AI-generated answer fully addresses the question it was given. Do not answer the question yourself — only evaluate whether it was addressed.

Check specifically for:
- Identify each distinct part or requirement in the question
- Check whether each part was addressed at all in the answer
- Flag any part that was skipped entirely, or addressed only superficially

Field routing rule:
- If a part of a question was skipped entirely, use `missing_aspect` to describe what
was left unanswered, and leave `quote` empty.
- If a part was addressed but weakly or incompletely, use `quote` to reference the relevant
portion of the answer and describe the gap in `problem`, leaving `missing_aspect` empty.

Scoring guide:
- 5 = no issues found
- 4 = only LOW severity issues
- 3 = at least one MEDIUM severity issue, no HIGH
- 2 = one HIGH severity issue
- 1 = multiple HIGH severity issues

Severity guide:
- HIGH = a major, explicitly requested part of the question was skipped entirely
- MEDIUM = a part was addressed but with a significant, noticeable gap
- LOW = a minor sub-point received only cursory treatment

For quoted issues, use the exact original wording - do not paraphrase. If nothing
was missed, return an empty issues list; do not invent minor gaps to appear thorough.
"""
