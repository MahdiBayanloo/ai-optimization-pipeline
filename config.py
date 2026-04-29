import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

CONFIG = {
    "api_key": os.getenv("ANTHROPIC_API_KEY"),
    "default_model": "claude-opus-4-5",
    "max_tokens": 4096,
    "max_repair_iterations": 3,
    "task_folder": None,  # set via CLI argument
    "agents": {
        "planner":               {"model": None},
        "generator":             {"model": None},
        "architecture_reviewer": {"model": None},
        "behavior_reviewer":     {"model": None},
        "repair":                {"model": None},
        "test_designer":         {"model": None},
    }
}
