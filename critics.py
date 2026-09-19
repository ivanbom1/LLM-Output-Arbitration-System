from llm_connect import groq_client
from schema import CritiqueReportForm, SeverityLevel
from config import GROQ_MODEL_ACCURACY, GROQ_MODEL_LOGIC, GROQ_MODEL_COMPLETENESS
from prompts import *

def compute_score(issues: list) -> int:
    """Deterministically derive the score from issue severities, per the scoring
    guide in each prompt — instead of trusting the model to do this arithmetic
    itself, which is unreliable. This always overrides whatever score the model
    returned, so the two can never disagree."""
    if not issues:
        return 5
    highs = sum(1 for i in issues if i.severity == SeverityLevel.HIGH)
    meds = sum(1 for i in issues if i.severity == SeverityLevel.MEDIUM)
    if highs >= 2:
        return 1
    if highs == 1:
        return 2
    if meds >= 1:
        return 3
    return 4  # only LOW-severity issues present

def run_critic(eval_system_prompt: str, tested_llm_output: str, model: str) -> CritiqueReportForm:
    
    report = groq_client.chat.completions.create(
        model=model,
        response_model=CritiqueReportForm,
        messages=[
            {"role": "system", "content": eval_system_prompt}, # eval_system_prompt - API's system role: the critic's identity and instructions
            {"role": "user", "content": tested_llm_output}, # tested_llm_output - API's user role: the content being judged, not responded to
        ],
    )
    report.score = compute_score(report.issues) #re-compute the severity level depended on number of issues
    return report
    
def run_accuracy_eval(tested_llm_output: str) -> CritiqueReportForm:
    
    return run_critic(
        ACCURACY_PROMPT, 
        tested_llm_output, 
        model=GROQ_MODEL_ACCURACY,
    )

def run_logic_eval(tested_llm_output: str) -> CritiqueReportForm:
    
    return run_critic(
        LOGIC_PROMPT, 
        tested_llm_output, 
        model=GROQ_MODEL_LOGIC,
    )

def run_completeness_eval(tested_llm_output: str, original_question: str) -> CritiqueReportForm:
    
    return run_critic(
        COMPLETENESS_PROMPT,
        f"Question: {original_question}\n\nAnswer: {tested_llm_output}",
        model=GROQ_MODEL_COMPLETENESS,
    )
