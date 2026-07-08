"""Unit test configuration."""

from __future__ import annotations

import sys
from pathlib import Path

# Add unit directory to Python path so imports work
unit_dir = Path(__file__).parent
sys.path.insert(0, str(unit_dir))
