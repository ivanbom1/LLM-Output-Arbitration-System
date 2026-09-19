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
    
def logic_node(state: ArbitrationState) -> dict:
    try:
            
            report = run_logic_eval(state["output_text"])
            return {"logic_report": report}
        
    except Exception as e:
        return {
            "logic_report": None,
            "disagreements": [{"type": "critique_failute", "critic": "logic", "error": str(e)}],
        }
        
def completeness_node(state: ArbitrationState) -> dict:
    try:
        report = run_completeness_eval(state["output_text"], state["question"])
        return {"completeness_report": report}
    
    except Exception as e:
        return {
            "completeness_report": None,
            "disagreements": [{"type": "critic_failure", "critic": "completeness", "error": str(e)}],
        }
        
def collect_critiques_node(state: ArbitrationState) -> dict:
    """
    Empty-node which `collects` critic's reports after complteion on the same stage of the graph
    """
    return {}

def detect_disagreements_node(state: ArbitrationState) -> dict:
    # disagreements detection algorithms based on the score 
    raise NotImplementedError

def adjudicate_node(state: ArbitrationState) -> dict:
    
    raise NotImplementedError

def synthesize_verdict_node(state: ArbitrationState) -> dict:
    
    raise NotImplementedError
