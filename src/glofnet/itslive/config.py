"""
Configuration for the ITS_LIVE data pipeline.

This module centralizes all configuration values used by the ITS_LIVE
pipeline. Other modules should import settings from here rather than
hard-coding them.
"""

# =============================================================================
# Glacier Selection
# =============================================================================

# Reuse the glacier selected for the entire GLOFNet pipeline.
# This should match the glacier used by the Sentinel-2 pipeline.
GLACIER_ID = "RGI2000-v7.0-G-14-08488"


# =============================================================================
# ITS_LIVE STAC API
# =============================================================================

# Official ITS_LIVE STAC Catalog
STAC_URL = "https://stac.itslive.cloud"

# Collection containing cloud-optimized Zarr velocity cubes
COLLECTION_NAME = "itslive-cubes"

# Maximum number of search results to retrieve.
#
# We intentionally request two items so that we can detect
# ambiguous searches (multiple matching cubes).
MAX_ITEMS = 2


# =============================================================================
# Output
# =============================================================================

# Directory for downloaded velocity products
OUTPUT_DIRECTORY = "data/raw/itslive"