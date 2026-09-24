# LLM Output Arbitration System

A multi-agent pipeline that takes an LLM-generated output, routes it to three
independent critics (accuracy, logic, completeness), detects disagreements
between them, and resolves conflicts through an adjudicator to produce a
single confidence-scored verdict.

**Status:** Phases 1–3 complete (critics, LangGraph orchestration, adjudicator).
Phases 4–6 (UI, API, portfolio polish) in progress.




All three critics and the adjudicator run on [Groq](https://console.groq.com)
(free tier) — no paid API keys required to run this project.

## Prerequisites

- Python 3.11+ (tested on 3.12)
- A free [Groq API key](https://console.groq.com/keys)
- WSL2 Ubuntu if on Windows (or any Linux/macOS shell)

## Installation

```bash
git clone <your-repo-url>
cd LLM-Output-Arbitration-System

python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

If `requirements.txt` isn't present yet, install directly:
```bash
pip install pydantic instructor openai anthropic python-dotenv langgraph
```

## Configuration

Copy the example env file and fill in your key:
```bash
cp .env.example .env
```

Edit `.env`:
```
GROQ_API_KEY=your_actual_key_here

# Optional — override the model per critic. Falls back to GROQ_MODEL if unset.
GROQ_MODEL=llama-3.1-8b-instant
GROQ_MODEL_ACCURACY=llama-3.3-70b-versatile
GROQ_MODEL_LOGIC=llama-3.3-70b-versatile
GROQ_MODEL_COMPLETENESS=llama-3.1-8b-instant
GROQ_MODEL_ADJUDICATOR=llama-3.3-70b-versatile

# Optional — evaluation scale, "5" or "10". Defaults to 5.
EVAL_SCALE=5
```

> Model IDs shift over time. Confirm what's currently live for your account
> at `console.groq.com/docs/models` before running, or check via:
> `curl https://api.groq.com/openai/v1/models -H "Authorization: Bearer $GROQ_API_KEY"`

## Usage

**Test individual critics** (Phase 1 — no orchestration, just the three
critic functions called directly):
```bash
python test_smoke.py
```

**Run the full graph** (Phase 2/3 — parallel dispatch, disagreement
detection, adjudication, final verdict):
```bash
python test_graph.py
```

Both scripts use a fixed test fixture with deliberately planted flaws — edit
the `QUESTION`/`ANSWER` variables at the top of either file to test your own
input.

## Project structure

```
.
├── .env.example
├── requirements.txt
│
├── config.py            # env var loading, per-critic/adjudicator model config
├── llm_connect.py        # Groq client, instructor-patched
├── schema.py             # CritiqueReportForm and related types (Phase 1)
├── verdict_schema.py     # Verdict, ConfirmedIssue, DismissedFlag (Phase 3)
├── eval_options.py       # 1-5 / 1-10 scoring scale presets
├── prompts.py            # all four system prompts (3 critics + adjudicator)
├── critics.py             # run_accuracy_eval / run_logic_eval / run_completeness_eval
├── adjudicator.py         # run_adjudication
│
├── orchestration/
│   ├── state.py           # ArbitrationState (shared graph state)
│   ├── nodes.py            # all graph node functions
│   └── graph.py            # build_graph() — wires nodes into the LangGraph pipeline
│
├── test_smoke.py          # Phase 1 smoke test (individual critics)
└── test_graph.py          # Phase 2/3 end-to-end test (full graph)
```

## How it works, briefly

1. **Three critics** (`critics.py`) independently evaluate the output for
   factual accuracy, logical consistency, and completeness, each returning a
   structured `CritiqueReportForm` (score, issues, confidence) enforced via
   `instructor`.
2. **LangGraph** (`orchestration/graph.py`) dispatches all three critics in
   parallel, then runs rule-based disagreement detection (score gaps,
   coverage gaps between critics).
3. If everything's clean, the graph **short-circuits** straight to the final
   verdict. Otherwise, an **adjudicator** (`adjudicator.py`) reviews every
   issue from all three reports, resolves disagreements using a
   dimension-specific method, deduplicates overlapping findings across
   critics, and confirms or dismisses each one with reasoning.
4. The final `Verdict` (`verdict_schema.py`) — overall score, confidence,
   confirmed issues, dismissed flags, and a summary — is what the pipeline
   returns.

## Known limitations

- No live fact-checking — critics and the adjudicator reason over the given
  text only, with no external verification (by design; see project notes).
- Well-formedness/coherence (e.g. a truncated or incoherent sentence) isn't
  covered by any of the three critic dimensions — an accepted, documented gap.
- Severity/score assignment can vary run-to-run on identical input — inherent
  model variance, mitigated but not eliminated by deterministic score
  computation from assigned severities.