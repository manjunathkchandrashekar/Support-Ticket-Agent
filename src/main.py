import argparse
from pathlib import Path
from src.agents.policy_agent import PolicyAgent
from src.agents.rag_agent import RAGAgent
from src.agents.response_agent import ResponseAgent
from src.agents.sentiment_agent import SentimentAgent
from src.agents.triage_agent import TriageAgent
from src.graph.support_graph import SupportGraph
from src.retrieval.document_loader import load_documents
from src.retrieval.retriever import Retriever
from src.retrieval.vector_store import LexicalVectorStore
from src.utils.helpers import load_json
from src.utils.schemas import Ticket


def build_agent(root: Path):
    chunks = load_documents(root / "data" / "knowledge_base")
    retriever = Retriever(LexicalVectorStore(chunks))
    return TriageAgent(RAGAgent(retriever), PolicyAgent(), SentimentAgent(), ResponseAgent())


def main():
    parser = argparse.ArgumentParser(description="AI-powered support ticket triage agent")
    parser.add_argument("--input", default="data/tickets/sample_ticket_batch.json")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    agent = build_agent(root)
    tickets = [Ticket(**item) for item in load_json(root / args.input)]
    for ticket in tickets:
        decision = SupportGraph(agent).invoke(ticket)
        print(f"{ticket.ticket_id}: {decision.action.value} ({decision.confidence:.2f})")
        print(f"  {decision.response}")
        print(f"  Rationale: {decision.rationale}; sources: {', '.join(decision.sources) or 'none'}")


if __name__ == "__main__":
    main()
