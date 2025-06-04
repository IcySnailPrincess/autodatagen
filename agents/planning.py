class Agent:
    """PlanningAgent stub — to be implemented in Phase 1.2."""
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.model = model_name
    def __call__(self, T: str, d_boot: str | None = None) -> dict:
        raise NotImplementedError
