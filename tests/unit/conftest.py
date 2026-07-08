"""Unit test configuration."""

import sys
from pathlib import Path

# Add unit directory to Python path so imports work
unit_dir = Path(__file__).parent
sys.path.insert(0, str(unit_dir))
