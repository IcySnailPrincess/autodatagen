"Typed schema for Planning-Agent output."
from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, Field, ValidationError
from typing import List, Literal


class NodeType(str, Enum):
    source = "Source"
    transform = "Transform"
    filter = "Filter"


class NodeSpec(BaseModel):
    id: str                      = Field(..., pattern=r"^[a-zA-Z0-9_]+$")
    type: NodeType
    desc: str                    = Field(..., min_length=3, max_length=200)
    params: dict | None = None   # passed to Coding Agent later


class PipelineSpec(BaseModel):
    nodes: List[NodeSpec]
    edges: List[tuple[str, str]]  # (parent_id, child_id)

    def sanity_check(self) -> None:
        # every id appears in nodes
        ids = {n.id for n in self.nodes}
        for a, b in self.edges:
            assert a in ids and b in ids, f"Edge {a}->{b} uses unknown id"
