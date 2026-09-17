from llm_connect import groq_client
from config import GROQ_MODEL
from schema import CritiqueReportForm

def run_critic(eval_system_prompt: str, tested_llm_output: str, model: str = GROQ_MODEL) -> CritiqueReportForm:
    
    return groq_client.chat.completions.create(
        model=model,
        response_model=CritiqueReportForm,
        messages=[
            {"role": "system", "content": eval_system_prompt}, # eval_system_prompt - API's system role: the critic's identity and instructions
            {"role": "user", "content": tested_llm_output}, # tested_llm_output - API's user role: the content being judged, not responded to
        ],
    )
    
def run_accuracy_eval(tested_llm_output: str) -> CritiqueReportForm:
    return run_critic("Accuracy evaluation instructions placeholder", tested_llm_output)

def run_logic_eval(tested_llm_output: str) -> CritiqueReportForm:
    return run_critic("Logic evaluation instructions placeholder", tested_llm_output)

def run_completeness_eval(tested_llm_output: str) -> CritiqueReportForm:
    return run_critic("Completemess evaluation instructions placeholder", tested_llm_output)
