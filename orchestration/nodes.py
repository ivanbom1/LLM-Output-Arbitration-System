from .state import ArbitrationState
from critics import run_accuracy_eval, run_logic_eval, run_completeness_eval
from eval_options import ACTIVE_SCALE

def parse_input_node(state: ArbitrationState) -> dict:
    """
    Parser function for now blindly trusts to the input data and stands only as a
    START node in this pipeline
    """
    
    return {}

def accuracy_node(state: ArbitrationState) -> dict:
    try:
        
        report = run_accuracy_eval(state["output_text"])
        return {"accuracy_report": report}
    
    except Exception as e:
        return {
            "accuracy_report": None,
            "disagreements": [{"type": "critique_failute", "critic": "accuracy", "error": str(e)}],
        }
    