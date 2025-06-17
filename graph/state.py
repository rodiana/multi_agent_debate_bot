# graph/state.py

from typing import List, Dict, Optional
from pydantic import BaseModel


class Message(BaseModel):
    agent: str
    content: str


class GraphState(BaseModel):
    topic: str
    round: int = 0  # default start
    history: List[Message] = []
    closing_statements: Dict[str, str] = {}
    winner: Optional[str] = None
    routing_decision: Optional[str] = None
