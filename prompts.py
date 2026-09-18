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
[same five-part structure, once designed]
"""

COMPLETENESS_PROMPT = """
[same five-part structure, plus the missing_aspect vs quote routing rule]
"""