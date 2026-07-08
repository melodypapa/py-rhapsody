"""Integration test configuration."""

import sys
from pathlib import Path

# Add unit directory to Python path so imports from unit tests work
unit_dir = Path(__file__).parent.parent / "unit"
sys.path.insert(0, str(unit_dir))
