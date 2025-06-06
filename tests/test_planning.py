import json, builtins
from unittest.mock import patch
from agents.planning import Agent
from specs import PipelineSpec

FAKE_JSON = {
    "nodes": [
        {"id": "src1", "type": "Source", "desc": "dummy source"},
        {"id": "tfm1", "type": "Transform", "desc": "dummy tfm"}
    ],
    "edges": [["src1", "tfm1"]]
}
FAKE_REPLY = f"```pipeline_spec\n{json.dumps(FAKE_JSON, indent=2)}\n```"

@patch("openai.ChatCompletion.create")
def test_planner_creates_valid_spec(mock_create):
    mock_create.return_value = {
        "choices": [{"message": {"content": FAKE_REPLY}}]
    }
    agent = Agent(model_name="gpt-4o-mini")  # model name irrelevant to mock
    spec = agent("generate cat images")
    assert isinstance(spec, PipelineSpec)
    assert spec.nodes[0].id == "src1"
