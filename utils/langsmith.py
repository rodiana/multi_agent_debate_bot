from langchain_core.prompts import PromptTemplate
from langsmith import Client
import os

def load_prompt_from_hub(prompt_name: str) -> PromptTemplate:

    client = Client(api_key=os.getenv("LANGCHAIN_API_KEY"),api_url=os.getenv("LANGCHAIN_ENDPOINT"))

    try:
        prompt = client.pull_prompt(prompt_name)
        if prompt is None:
            raise ValueError(f"Prompt '{prompt_name}' not found or empty.")
        return prompt
    except Exception as e:
        raise RuntimeError(f"Failed to load prompt '{prompt_name}': {e}")
