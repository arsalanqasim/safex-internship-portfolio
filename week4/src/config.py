"""Configuration constants and path resolvers for Week 4 workspace."""

from pathlib import Path
from dotenv import load_dotenv

WEEK4_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = WEEK4_DIR / "outputs"
DATA_DIR = WEEK4_DIR / "data"
DOCS_DIR = WEEK4_DIR / "docs"

# Load environment variables
load_dotenv(WEEK4_DIR / ".env")
load_dotenv(WEEK4_DIR.parent / ".env")

# Create directories if they do not exist
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)
