"""
Project-wide filesystem paths.
"""

from pathlib import Path

# Project root (Cryofusion/)
PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_DIRECTORY = PROJECT_ROOT / "data"

RAW_DIRECTORY = DATA_DIRECTORY / "raw"
PROCESSED_DIRECTORY = DATA_DIRECTORY / "processed"
CLIPPED_DIRECTORY = DATA_DIRECTORY / "clipped"

ITSLIVE_RAW_DIRECTORY = RAW_DIRECTORY / "itslive"
ITSLIVE_PROCESSED_DIRECTORY = PROCESSED_DIRECTORY / "itslive"
ITSLIVE_CLIPPED_DIRECTORY = CLIPPED_DIRECTORY / "itslive"