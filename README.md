# 🧠 Multi-Agent Debate Bot

A multi-agent debate simulation powered by [LangGraph](https://www.langchain.com/langgraph) and open-source local LLMs via [Ollama](https://ollama.com/).

This project explores how agentic reasoning and conditional graph routing can be used to simulate structured debates among AI agents with distinct perspectives — an Optimist, a Skeptic, an Analyst, and a Moderator.

---

## 🧩 Key Concepts

- **Agent Turns** – each agent contributes one message per round
- **Conditional Routing** – control flow determines whether to continue debating or wrap up
- **State Tracking** – maintains history, round count, and final winner using a shared state object
- **Prompt Management** – all agent prompts are stored and versioned via [LangSmith](https://smith.langchain.com/) for better maintainability
- **Graph Introspection** – used `get_graph()` to inspect the structure at runtime and export a visual representation (PNG) using `graph.get_graph().draw_mermaid_png()`, making it easier to debug or analyze control flow

---

## 🔧 Tech Stack

- 🐍 Python
- ⚙️ [LangGraph](https://www.langchain.com/langgraph) for agent orchestration
- 🧱 [Pydantic](https://docs.pydantic.dev/) for typed state modeling
- 🤖 [Ollama](https://ollama.com/) for running local LLMs
- 🧠 [LangSmith](https://smith.langchain.com/) for managing and storing prompt templates
- ✍️ `BaseModel` for defining structured messages and state

---

## 🚀 How to Run
### ⚠️ Prerequisite
Before running the app, you’ll need to **create your own prompt templates** using [LangSmith](https://smith.langchain.com/) and set them to **public** or provide access via your API key.
Each agent (Optimist, Skeptic, Analyst, Moderator) loads its prompt from the LangSmith repository at runtime. You can either:
- Recreate your own versions of the prompts (with the same names), or
- Modify the code to point to your own prompt IDs

Make sure you also have your **LangSmith API key** set as an environment variable:

### Run via CLI

```bash
python main.py

## 📂 Project Structure
graph/
  ├─ build_graph.py       # Builds and compiles the LangGraph
  ├─ nodes.py             # All agent nodes + control logic
  ├─ state.py             # GraphState and Message definitions
agents/
  ├─ optimist.py
  ├─ skeptic.py
  ├─ analyst.py
  ├─ moderator.py
main.py                   # CLI runner


## 📝 Note
This codebase includes multiple print() statements intentionally left in place for debugging and educational purposes. They’re meant to assist others building similar LangGraph-based architectures by making execution flow and state transitions more transparent.