from importlib import import_module
def load_agent(name: str):
    mod = import_module(f"agents.{name}")
    return getattr(mod, "Agent")
