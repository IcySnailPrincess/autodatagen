import json, os, textwrap
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()                       # picks up .env if present

OPENAI_MODEL = "gpt-4o-mini"

def read_api_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("Set OPENAI_API_KEY in your environment or .env")
    return key

def build_planner_prompt(T: str) -> str:
    """Return a chat prompt that asks the model for a JSON spec."""
    return textwrap.dedent(f"""
    You are an expert ML data-pipeline planner.

    GOAL: design a pipeline (DAG) that produces synthetic data matching:
    {T}

    OUTPUT FORMAT (JSON, no commentary):
    ```
    {{
      "nodes":[{{"id": "...", "type":"Source|Transform|Filter", "desc":"...", "params":{{}} }}, ...],
      "edges":[["parent_id","child_id"], ...]
    }}
    ```
    First think step-by-step. Then emit JSON under a ```pipeline_spec``` fence.
    """)
