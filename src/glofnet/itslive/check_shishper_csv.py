from pathlib import Path

import pandas as pd
import geopandas as gpd

from glofnet.common.find_glacier import load_glacier
from glofnet.sentinel.config import GLACIER_ID


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

# 3. Builds the absolute path to your CSV file
csv_path = PROJECT_ROOT / "data" / "raw" / "itslive" / "velocity_data_raw" / "df_raw.csv"


# --------------------------------------------------
# Load the exact same glacier polygon
# used by the Sentinel-2 pipeline
# --------------------------------------------------

glacier = load_glacier(GLACIER_ID)

print("\n===== SHISHPER =====")

print("RGI ID:", glacier.iloc[0]["rgi_id"])
print("Name:", glacier.iloc[0]["glac_name"])
print("CRS:", glacier.crs)

min_lon, min_lat, max_lon, max_lat = (
    glacier.total_bounds
)

print(
    f"Longitude: {min_lon} → {max_lon}"
)

print(
    f"Latitude : {min_lat} → {max_lat}"
)

print("====================")


# --------------------------------------------------
# Get ITS_LIVE CSV spatial extent
# WITHOUT loading the entire 73-million-row
# dataset into memory
# --------------------------------------------------

print("\nReading ITS_LIVE CSV...")

csv_min_lon = float("inf")
csv_max_lon = float("-inf")
csv_min_lat = float("inf")
csv_max_lat = float("-inf")

chunksize = 500_000

for chunk in pd.read_csv(
    csv_path,
    usecols=["lon", "lat"],
    chunksize=chunksize,
):

    csv_min_lon = min(
        csv_min_lon,
        chunk["lon"].min()
    )

    csv_max_lon = max(
        csv_max_lon,
        chunk["lon"].max()
    )

    csv_min_lat = min(
        csv_min_lat,
        chunk["lat"].min()
    )

    csv_max_lat = max(
        csv_max_lat,
        chunk["lat"].max()
    )


print("\n===== ITS_LIVE CSV =====")

print(
    f"Longitude: {csv_min_lon} → {csv_max_lon}"
)

print(
    f"Latitude : {csv_min_lat} → {csv_max_lat}"
)

print("========================")


# --------------------------------------------------
# Check whether bounding boxes overlap
# --------------------------------------------------

longitude_overlap = (
    csv_max_lon >= min_lon
    and
    csv_min_lon <= max_lon
)

latitude_overlap = (
    csv_max_lat >= min_lat
    and
    csv_min_lat <= max_lat
)

print("\n===== SPATIAL OVERLAP =====")

print(
    "Longitude overlap:",
    longitude_overlap
)

print(
    "Latitude overlap:",
    latitude_overlap
)

if longitude_overlap and latitude_overlap:

    print(
        "\nThe CSV bounding box overlaps "
        "the Shishper bounding box."
    )

else:

    print(
        "\nThe CSV bounding box does NOT "
        "overlap the Shishper bounding box."
    )

print("============================")