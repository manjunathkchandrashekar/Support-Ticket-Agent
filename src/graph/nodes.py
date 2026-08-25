from src.graph.graph_state import GraphState


def retrieve_node(state: GraphState, rag_agent):
    state.evidence = rag_agent.retrieve(state.ticket)
    return state


def triage_node(state: GraphState, triage_agent):
    state.decision = triage_agent.process(state.ticket)
    return state


def sentiment_node(state: GraphState, sentiment_agent):
    state.sentiment = sentiment_agent.analyze(state.ticket.message)
    return state
