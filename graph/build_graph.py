from rich import print as rprint

from langgraph.graph import StateGraph, END
from graph.state import GraphState
from graph.nodes import (
    initialize_debate,
    agent_turn,
    check_round_completion,
    generate_closing_statements,
    moderator_judgment,
)

AGENT_SEQUENCE = ["Optimist", "Skeptic", "Analyst"]

def build_debate_graph() -> StateGraph:
    builder = StateGraph(GraphState)

    # Step 1: Add agent turn nodes
    for agent_name in AGENT_SEQUENCE:
        builder.add_node(f"{agent_name}_Turn", agent_turn(agent_name))

    # Step 2: Add check + closing nodes
    builder.add_node("CheckIfDone", check_round_completion)
    builder.add_node("GenerateClosings", generate_closing_statements)
    builder.add_node("ModeratorJudgment", moderator_judgment)

    # Step 3: Conditional edge from check
    builder.add_conditional_edges(
        source="CheckIfDone",
        path=lambda state: state.routing_decision,
        path_map={
            # "continue": lambda x: f"{AGENT_SEQUENCE[0]}_Turn",
            "continue": f"{AGENT_SEQUENCE[0]}_Turn",
            "closing": "GenerateClosings",
        }
    )

    builder.add_edge("GenerateClosings", "ModeratorJudgment")

    # Step 4: Final edge
    builder.add_edge("ModeratorJudgment", END)

    # Step 5: Link agent turns to next step
    for i in range(len(AGENT_SEQUENCE)):
        current = f"{AGENT_SEQUENCE[i]}_Turn"
        next_node = (
            "CheckIfDone" if i == len(AGENT_SEQUENCE) - 1
            else f"{AGENT_SEQUENCE[i + 1]}_Turn"
        )
        print(f"edge: {current} -> {next_node}")
        builder.add_edge(current, next_node)

    # Step 6: Entry point
    builder.set_entry_point(f"{AGENT_SEQUENCE[0]}_Turn")


    graph = builder.compile()

    print("\n[GRAPH] Nodes:")
    rprint(graph.get_graph().nodes)

    print("\n[GRAPH] Transitions:")
    rprint(graph.get_graph().edges)



    return graph# builder.compile()
