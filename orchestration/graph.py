from langgraph.graph import StateGraph, START, END
from .state import ArbitrationState


def build_graph():
    graph = StateGraph(ArbitrationState)
    
    #......
    
    return graph.compile()