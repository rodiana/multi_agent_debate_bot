# graph/nodes.py

from graph.state import GraphState, Message
from agents.optimist import OptimistAgent
from agents.skeptic import SkepticAgent
from agents.analyst import AnalystAgent
from agents.moderator import ModeratorAgent

from typing import Callable, Dict, Literal

MAX_ROUNDS = 2  # Customize how many rounds of debate you want

# Instantiate agents once
AGENT_REGISTRY: Dict[str, Callable[[], object]] = {
    "Optimist": OptimistAgent,
    "Skeptic": SkepticAgent,
    "Analyst": AnalystAgent,
}


def initialize_debate(topic: str) -> GraphState:
    """Start the graph with initial state."""
    return GraphState(
        topic=topic,
        round=1,
        history=[],
        closing_statements={},
        winner=None,
    )


def agent_turn(agent_name: str) -> Callable[[GraphState], GraphState]:
    """Returns a node function that allows the given agent to take a turn."""

    def _node(state: GraphState) -> GraphState:
        print(f"{agent_name} turn!")
        agent_cls = AGENT_REGISTRY[agent_name]
        agent = agent_cls()
        runnable = agent.get_runnable()

        # Convert history into a single string for the prompt
        history_text = "\n".join(
            [f"{m.agent}: {m.content}" for m in state.history]
        )


        input_data = {
            "topic": state.topic,
            "history": history_text,
        }

        output = runnable.invoke(input_data)

        # Append message to state history
        updated_history = state.history + [Message(agent=agent_name, content=output)]

        return state.copy(update={"history": updated_history})

    return _node

def check_round_completion(state: GraphState):
    """
    Decide whether to continue to next debate round or stop and close.
    Each round has 1 turn per agent.
    """
    print("[DEBUG] Entered CheckIfDone")
    num_agents = len(AGENT_REGISTRY)
    total_messages = len(state.history)
    
    if total_messages >= num_agents * MAX_ROUNDS:
        print('closing!')
        return state.copy(update={"routing_decision": "closing"})
    else:
        print('continuing!')
        return state.copy(update={"routing_decision": "continue"})

def generate_closing_statements(state: GraphState) -> GraphState:
    """
    Each agent gives a closing argument based on the full debate history.
    """
    print("[Graph] Entered generate_closing_statements")
    closing = {}

    history_text = "\n".join(
        [f"{m.agent}: {m.content}" for m in state.history]
    )

    for agent_name, agent_cls in AGENT_REGISTRY.items():
        agent = agent_cls()
        runnable = agent.get_runnable()

        input_data = {
            "topic": state.topic,
            "history": history_text,
        }

        output = runnable.invoke(input_data)
        closing[agent_name] = output

    print("[Graph] Generated closing statements for:", list(closing.keys()))
    return state.copy(update={"closing_statements": closing, "round": state.round + 1})

def moderator_judgment(state: GraphState) -> GraphState:
    """
    Invokes the ModeratorAgent to analyze closing statements and select a winner.
    """
    print("[Graph] Entered moderator_judgment")
    closings_text = "\n".join(
        [f"{agent}: {text}" for agent, text in state.closing_statements.items()]
    )

    input_data = {
        "topic": state.topic,
        "closings": closings_text,
    }

    agent = ModeratorAgent()
    result = agent.get_runnable().invoke(input_data)
    print("\n🧠 Moderator raw response:\n", result)


    # Extract winner from the result (basic string parsing for now)
    lines = result.strip().splitlines()
    winner_line = next((line for line in lines if line.startswith("Winner:")), None)

    winner = winner_line.split(":")[1].strip() if winner_line else "Unknown"

    return state.copy(update={"winner": winner})