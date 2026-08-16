from pathlib import Path

import geopandas as gpd
import rasterio
from shapely.geometry import box

from src.glofnet.common.find_glacier import load_glacier
from src.glofnet.sentinel.config import GLACIER_ID


# --------------------------------------------------
# Paths
# --------------------------------------------------

SENTINEL_DIR = Path(
    "data/raw/sentinel/"
    "Glacier_images_dataset-20260812T234814Z-1-001/"
    "Glacier_images_dataset/"
    "GEE_Sentinel"
)


# --------------------------------------------------
# Load the exact Shishper polygon used by our
# Sentinel-2 pipeline
# --------------------------------------------------

glacier = load_glacier(GLACIER_ID)

# Make sure the glacier is in geographic coordinates
glacier = glacier.to_crs("EPSG:4326")

shishper = glacier.geometry.iloc[0]

print("\n========================================")
print("SHISHPER REFERENCE")
print("========================================")

print("RGI ID:", glacier.iloc[0]["rgi_id"])
print("CRS:", glacier.crs)

min_lon, min_lat, max_lon, max_lat = shishper.bounds

print(f"Longitude: {min_lon} → {max_lon}")
print(f"Latitude : {min_lat} → {max_lat}")


# --------------------------------------------------
# Find TIFF files
# --------------------------------------------------

tif_files = sorted(SENTINEL_DIR.glob("*.tif"))

print("\n========================================")
print("READY-MADE SENTINEL DATA")
print("========================================")

print("Directory:", SENTINEL_DIR)
print("TIFF files found:", len(tif_files))

if not tif_files:
    raise FileNotFoundError(
        f"No .tif files found in {SENTINEL_DIR}"
    )


# --------------------------------------------------
# Inspect every TIFF
# --------------------------------------------------

results = []

for tif_path in tif_files:

    print("\n----------------------------------------")
    print("File:", tif_path.name)

    with rasterio.open(tif_path) as src:

        print("CRS:", src.crs)
        print("Size:", src.width, "x", src.height)
        print("Bands:", src.count)
        print("Resolution:", src.res)
        print("Bounds:", src.bounds)

        # Raster footprint in its own CRS
        raster_polygon = box(
            src.bounds.left,
            src.bounds.bottom,
            src.bounds.right,
            src.bounds.top,
        )

        raster_gdf = gpd.GeoDataFrame(
            geometry=[raster_polygon],
            crs=src.crs,
        )

        # Convert raster footprint to WGS84
        raster_wgs84 = raster_gdf.to_crs("EPSG:4326")

        footprint = raster_wgs84.geometry.iloc[0]

        # Exact intersection with Shishper
        intersects = footprint.intersects(shishper)

        # Area of intersection
        intersection = footprint.intersection(shishper)

        intersection_area = intersection.area

        results.append({
            "file": tif_path.name,
            "crs": str(src.crs),
            "intersects_shishper": intersects,
            "intersection_area_deg2": intersection_area,
        })

        print(
            "Intersects Shishper:",
            intersects
        )

        print(
            "Intersection area:",
            intersection_area
        )


# --------------------------------------------------
# Summary
# --------------------------------------------------

print("\n========================================")
print("SUMMARY")
print("========================================")

results_df = gpd.pd.DataFrame(results)

print(results_df.to_string(index=False))

print("\nTIFFs intersecting Shishper:")

shishper_files = results_df[
    results_df["intersects_shishper"]
]

print(
    shishper_files[
        ["file", "intersects_shishper"]
    ].to_string(index=False)
)

print(
    f"\nTotal TIFFs intersecting Shishper: "
    f"{len(shishper_files)}"
)