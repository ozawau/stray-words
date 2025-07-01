from pathlib import Path

# Determine project root based on the script's location
try:
    # This works when running as a script
    SCRIPT_DIR = Path(__file__).resolve().parent
except NameError:
    # Fallback for interactive environments or when __file__ is not defined
    SCRIPT_DIR = Path.cwd()

PROJECT_ROOT = SCRIPT_DIR.parent.parent
WORDLISTS_DIR = PROJECT_ROOT / "wordlists"