"""Configuration for the LLM Council.

The council runs entirely on models that are already configured inside
opencode. There is no model provider API key anywhere in this project.
"""

import os
from dotenv import load_dotenv

load_dotenv(override=True)

# --- opencode server connection -------------------------------------------
# Both values are auto-detected when unset. See opencode_client.discover_*.

# Override if the auto-detection cannot find the server.
OPENCODE_SERVER_URL = os.getenv("OPENCODE_SERVER_URL")

# Override if the auto-detection cannot find the password.
OPENCODE_SERVER_PASSWORD = os.getenv("OPENCODE_SERVER_PASSWORD")

# The directory council sessions operate in. Also the repo the council may read.
OPENCODE_WORKSPACE = os.getenv("OPENCODE_WORKSPACE", os.getcwd())

# --- council composition ---------------------------------------------------

# Council members are discovered at runtime from opencode's model list, so
# there is no hardcoded roster to maintain. These are the defaults used when
# the user has not overridden them in the UI.

# Restrict the roster to specific "provider/model" ids. Empty = use everything.
COUNCIL_MODELS: list[str] = [
    m.strip() for m in os.getenv("COUNCIL_MODELS", "").split(",") if m.strip()
]

# Chairman synthesizes the final verdict. None = auto-pick the model with the
# largest context window.
CHAIRMAN_MODEL = os.getenv("CHAIRMAN_MODEL") or None

# Number of open debate rounds between the position and review stages.
DEBATE_ROUNDS = int(os.getenv("DEBATE_ROUNDS", "2"))

# Initial compression level for the model-to-model exchange: off, lite, full,
# ultra, max. Overridable at any time from the UI, including mid-run.
# See backend/caveman.py for what these mean and where the rules come from.
DEBATE_MODE = os.getenv("DEBATE_MODE", "full")

# Per-model timeout in seconds. Free-tier models with web research are slow.
PER_MODEL_TIMEOUT = float(os.getenv("PER_MODEL_TIMEOUT", "300"))

# Council members run under this opencode agent. "plan" is built-in and
# read-only by design, which combined with the session-level permission
# ruleset in opencode_client.council_permissions() keeps members from ever
# modifying your files. Set to "" to use the default agent.
#
# Note: custom agents defined in a project-level opencode.json register but do
# not run in opencode 2.0.18, so we deliberately use a built-in one.
COUNCIL_AGENT = os.getenv("COUNCIL_AGENT", "plan")

# --- storage ---------------------------------------------------------------

# Data directory for conversation storage
DATA_DIR = "data/conversations"
