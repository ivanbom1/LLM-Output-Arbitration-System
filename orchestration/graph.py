from langgraph.graph import StateGraph, START, END
from .state import ArbitrationState
from .nodes import (
    parse_input_node,
    accuracy_node,
    logic_node,
    completeness_node,
    collect_critiques_node,
    detect_disagreements_node,
    adjudicate_node,
    synthesize_verdict_node,
)


def route_after_disagreements(state: ArbitrationState) -> str:
    """Short-circuit routing: if every critic that actually ran came back
    with zero issues, skip adjudicate entirely and go straight to
    synthesize_verdict. A critic that failed (report is None) does NOT
    count as 'clean'"""
    reports = [state["accuracy_report"], state["logic_report"], state["completeness_report"]]
    all_present_and_clean = all(r is not None and not r.issues for r in reports)
    return "synthesize_verdict" if all_present_and_clean else "adjudicate"


def build_graph():
    graph = StateGraph(ArbitrationState)
    # add graph nodes
    graph.add_node("parse_input", parse_input_node)
    graph.add_node("accurate_critic", accuracy_node)
    graph.add_node("logic_critic", logic_node)
    graph.add_node("completeness_critic", completeness_node)
    graph.add_node("collect_critiques", collect_critiques_node)
    graph.add_node("detect_disagreements", detect_disagreements_node)
    graph.add_node("adjudicate", adjudicate_node)
    graph.add_node("synthesize_verdict", synthesize_verdict_node)
    
    # set a starting node
    graph.add_edge(START, "parse_input")
    
    # set concurrent start of three critics
    graph.add_edge("parse_input", "accurate_critic")
    graph.add_edge("parse_input", "logic_critic")
    graph.add_edge("parse_input", "completeness_critic")
    
    # start collect critiques only when all 3 are done
    graph.add_edge("accuracy_critic", "collect_critiques")
    graph.add_edge("logic_critic", "collect_critiques")
    graph.add_edge("completeness_critic", "collect_critiques")
    
    graph.add_edge("collect_critiques", "detect_disagreements")
    
    # shortcut - skip adjudicate if everything came back clean
    graph.add_conditional_edges(
        "detect_disagreements",
        route_after_disagreements,
        {"synthesize_verdict": "synthesize_verdict", "adjudicate": "adjudicate"}
    )
    
    graph.add_edge("adjudicate", "synthesize_verdict")
    graph.add_edge("synthesize_verdict", END)
    
    return graph.compile()
