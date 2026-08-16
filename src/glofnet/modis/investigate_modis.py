from pathlib import Path

import pandas as pd

from glofnet.common.find_glacier import load_glacier
from glofnet.sentinel.config import GLACIER_ID


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

# 2. Rebuilds the path cleanly using Path components (retaining the specific space)
csv_path = (
    PROJECT_ROOT 
    / "data" 
    / "raw" 
    / "modis" 
    / "64_point _shisper_lst_data" 
    / "64-grid-points-lst-data-shisper-MOD11A1-061-results.csv"
)


# --------------------------------------------------
# Load the exact Shishper polygon used by
# our Sentinel-2 pipeline
# --------------------------------------------------

glacier = load_glacier(GLACIER_ID)

min_lon, min_lat, max_lon, max_lat = (
    glacier.total_bounds
)

print("\n========================================")
print("SHISHPER REFERENCE")
print("========================================")

print("RGI ID:", glacier.iloc[0]["rgi_id"])
print("Name:", glacier.iloc[0]["glac_name"])
print("CRS:", glacier.crs)

print(
    f"Longitude: {min_lon} → {max_lon}"
)

print(
    f"Latitude : {min_lat} → {max_lat}"
)


# --------------------------------------------------
# Inspect MODIS CSV
# --------------------------------------------------

print("\n========================================")
print("MODIS CSV")
print("========================================")

print("File:", csv_path)

# Read only the first few rows initially.
sample = pd.read_csv(
    csv_path,
    nrows=5
)

print("\nColumns:")
for column in sample.columns:
    print("  -", column)

print("\nFirst 5 rows:")
print(sample.to_string(index=False))


# --------------------------------------------------
# Get basic file information
# --------------------------------------------------

print("\n========================================")
print("MODIS FILE INFORMATION")
print("========================================")

# Read the complete file.
# This should be reasonable for a 64-point dataset.
df = pd.read_csv(csv_path)

print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nData types:")
print(df.dtypes)

import geopandas as gpd

# Get the 64 unique spatial points
points_df = df[
    ["Latitude", "Longitude"]
].drop_duplicates()

print("\nNumber of unique MODIS points:", len(points_df))

# Convert to GeoDataFrame
points = gpd.GeoDataFrame(
    points_df,
    geometry=gpd.points_from_xy(
        points_df["Longitude"],
        points_df["Latitude"]
    ),
    crs="EPSG:4326"
)

# Test whether each point is inside Shishper
points["inside_shishper"] = points.geometry.within(
    glacier.geometry.iloc[0]
)

print("\n===== EXACT SHISHPER TEST =====")
print(
    "Points inside Shishper:",
    points["inside_shishper"].sum()
)
print(
    "Points outside Shishper:",
    (~points["inside_shishper"]).sum()
)

print("\nMODIS points:")
print(
    points[
        ["Latitude", "Longitude", "inside_shishper"]
    ].to_string(index=False)
)

# --------------------------------------------------
# Identify possible coordinate columns
# --------------------------------------------------

print("\n========================================")
print("POSSIBLE COORDINATE COLUMNS")
print("========================================")

coordinate_keywords = [
    "lat",
    "latitude",
    "lon",
    "longitude",
    "x",
    "y",
    "point",
]

for column in df.columns:

    column_lower = column.lower()

    if any(
        keyword in column_lower
        for keyword in coordinate_keywords
    ):
        print(column)


# --------------------------------------------------
# Print unique values for likely coordinate columns
# --------------------------------------------------

print("\n========================================")
print("COORDINATE INFORMATION")
print("========================================")

for column in df.columns:

    column_lower = column.lower()

    if (
        "lat" in column_lower
        or "latitude" in column_lower
        or "lon" in column_lower
        or "longitude" in column_lower
    ):

        print(f"\n{column}")

        print("  Unique values:",
              df[column].nunique())

        print("  Minimum:",
              df[column].min())

        print("  Maximum:",
              df[column].max())

        if df[column].nunique() <= 100:
            print(
                "  Values:",
                sorted(df[column].dropna().unique())
            )


# --------------------------------------------------
# Summary
# --------------------------------------------------

print("\n========================================")
print("INVESTIGATION COMPLETE")
print("========================================")

print(
    "\nNext step: compare the MODIS coordinate "
    "range with the Shishper RGI bounds above."
)