from pathlib import Path

import geopandas as gpd

# ----------------------------------------------------
# Configuration
# ----------------------------------------------------

SHAPEFILE = Path(
    "data/reference/RGI/RGI2000-v7.0-G-14_south_asia_west/RGI2000-v7.0-G-14_south_asia_west.shp"
)

GLACIER_ID = "RGI2000-v7.0-G-14-08488"

# ----------------------------------------------------
# Load glacier inventory
# ----------------------------------------------------

gdf = gpd.read_file(SHAPEFILE)

print(f"Loaded {len(gdf)} glacier polygons")

# ----------------------------------------------------
# Find glacier by RGI ID
# ----------------------------------------------------

glacier = gdf[gdf["rgi_id"] == GLACIER_ID]

# ----------------------------------------------------
# Function
# ----------------------------------------------------

def load_glacier(glacier_id):
    """
    Returns the glacier polygon for a given RGI ID.
    """

    glacier = gdf[gdf["rgi_id"] == glacier_id]

    if glacier.empty:
        raise ValueError(f"Glacier '{glacier_id}' not found.")

    return glacier

# ----------------------------------------------------
# Verify glacier exists
# ----------------------------------------------------

if glacier.empty:
    print(f"Glacier {GLACIER_ID} not found.")
    exit()

# ----------------------------------------------------
# Test the function
# ----------------------------------------------------

if __name__ == "__main__":

    print(f"Loaded {len(gdf)} glacier polygons")

    glacier = load_glacier(GLACIER_ID)

    print("\nGlacier Found\n")

    print("RGI ID:", glacier.iloc[0]["rgi_id"])
    print("Name:", glacier.iloc[0]["glac_name"])
    print("Area (km²):", glacier.iloc[0]["area_km2"])
    print("Center Longitude:", glacier.iloc[0]["cenlon"])
    print("Center Latitude:", glacier.iloc[0]["cenlat"])
