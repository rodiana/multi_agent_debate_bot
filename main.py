# run_debate.py

from dotenv import load_dotenv
load_dotenv()

from graph.build_graph import build_debate_graph
from graph.nodes import initialize_debate

def run_debate(topic: str):
    print(f"\n🗣️ Starting debate on: \"{topic}\"\n{'='*60}")

    # 1. Build the graph
    graph = build_debate_graph()

    # 2. Initialize the state
    state = initialize_debate(topic)

    # 3. Run the full graph
    final_state = graph.invoke(state)

    # 4. Display history
    print("\n📝 Debate History:")
    for msg in final_state['history']:
        print(f"{msg.agent}: {msg.content}\n")

    # 5. Display closing statements
    print("\n🎤 Closing Statements:")
    for agent, text in final_state['closing_statements'].items():
        print(f"\n{agent}:\n{text}\n")

    # 6. Display winner
    print("🏆 Debate Winner:")
    print(final_state['winner'] or "No clear winner")


if __name__ == "__main__":
    run_debate("Will AGI be achievable by 2035?")
