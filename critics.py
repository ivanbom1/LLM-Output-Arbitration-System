from llm_connect import groq_client
from schema import CritiqueReportForm
from config import GROQ_MODEL_ACCURACY, GROQ_MODEL_LOGIC, GROQ_MODEL_COMPLETENESS
from prompts import *

def run_critic(eval_system_prompt: str, tested_llm_output: str, model: str) -> CritiqueReportForm:
    
    return groq_client.chat.completions.create(
        model=model,
        response_model=CritiqueReportForm,
        messages=[
            {"role": "system", "content": eval_system_prompt}, # eval_system_prompt - API's system role: the critic's identity and instructions
            {"role": "user", "content": tested_llm_output}, # tested_llm_output - API's user role: the content being judged, not responded to
        ],
    )
    
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
