#!/usr/bin/env python3
"""
Backward-compatible wrapper for SunRiseSet CLI.
Forwards execution to src.sunriseset.cli.
"""

import sys
import os

# Add src to sys.path so it works directly without pip install
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from sunriseset.cli import run

if __name__ == "__main__":
    sys.exit(run())
