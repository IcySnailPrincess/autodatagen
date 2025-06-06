import json, re, openai
from typing import Dict, Any
from agents.utils import build_planner_prompt, read_api_key, OPENAI_MODEL
from specs import PipelineSpec, ValidationError


class Agent:
    """
    Phase-1 PlanningAgent.
    • Builds a prompt from target description T
    • Calls OpenAI chat completion
    • Extracts & validates JSON spec
    """

    def __init__(self, model_name: str = OPENAI_MODEL):
        openai.api_key = read_api_key()
        self.model = model_name

    def __call__(self, T: str, d_boot: str | None = None) -> PipelineSpec:
        prompt = build_planner_prompt(T)
        if d_boot:
            prompt += f"\nBootstrapping data path: {d_boot}\n"

        resp = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )
        content = resp["choices"][0]["message"]["content"]

        json_txt = self._extract_json(content)
        data: Dict[str, Any] = json.loads(json_txt)

        try:
            spec = PipelineSpec(**data)
            spec.sanity_check()
        except ValidationError as e:
            raise RuntimeError(f"Spec invalid: {e}")

        return spec

    @staticmethod
    def _extract_json(text: str) -> str:
        match = re.search(r"```(?:pipeline_spec)?\s*(\{.*\})\s*```", text, re.S)
        if not match:
            raise RuntimeError("Could not find JSON fence in model output")
        return match.group(1)
