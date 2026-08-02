"""
Configuration for the ITS_LIVE data pipeline.
"""

# =============================================================================
# Glacier Selection
# =============================================================================

GLACIER_ID = "RGI2000-v7.0-G-14-08488"


# =============================================================================
# Search Parameters
# =============================================================================

# Match the Sentinel-2 temporal range.
START_DATE = "2021-01-01"
END_DATE = "2024-12-31"


# =============================================================================
# Output
# =============================================================================

OUTPUT_DIRECTORY = "data/raw/itslive"

COLLECTION_NAME = "itslive-granules"

START_DATE = "2021-01-01"
END_DATE = "2024-12-31"

MAX_ITEMS = 10

STAC_URL = "https://stac.itslive.cloud"

COLLECTION_NAME = "itslive-granules"

START_DATE = "2021-01-01"

END_DATE = "2024-12-31"

MAX_ITEMS = 1