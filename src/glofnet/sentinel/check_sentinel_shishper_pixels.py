from pathlib import Path

import geopandas as gpd
import rasterio
from rasterio.mask import mask

from src.glofnet.common.find_glacier import load_glacier
from src.glofnet.sentinel.config import GLACIER_ID


SENTINEL_DIR = Path(
    "data/raw/sentinel/"
    "Glacier_images_dataset-20260812T234814Z-1-001/"
    "Glacier_images_dataset/"
    "GEE_Sentinel"
)

TIF_PATH = SENTINEL_DIR / "2018-12-17.tif"


# --------------------------------------------------
# Load Shishper
# --------------------------------------------------

glacier = load_glacier(GLACIER_ID)

print("\n===== SHISHPER =====")
print("RGI ID:", glacier.iloc[0]["rgi_id"])
print("CRS:", glacier.crs)


# --------------------------------------------------
# Open Sentinel image
# --------------------------------------------------

with rasterio.open(TIF_PATH) as src:

    print("\n===== SENTINEL IMAGE =====")
    print("File:", TIF_PATH.name)
    print("CRS:", src.crs)
    print("Size:", src.width, "x", src.height)
    print("Bands:", src.count)
    print("NoData:", src.nodata)
    print("Dtype:", src.dtypes)

    # Convert glacier to image CRS
    glacier_image_crs = glacier.to_crs(src.crs)

    geometry = [
        glacier_image_crs.geometry.iloc[0]
    ]

    # Mask raster to Shishper polygon
    masked_data, masked_transform = mask(
        src,
        geometry,
        crop=True,
        filled=False,
    )

    print("\n===== SHISHPER PIXELS =====")

    print(
        "Masked raster shape:",
        masked_data.shape
    )

    # Count valid pixels for each band
    for band_number in range(1, src.count + 1):

        band = masked_data[band_number - 1]

        valid_pixels = (~band.mask).sum()
        total_pixels = band.size

        percentage = (
            valid_pixels / total_pixels * 100
        )

        print(
            f"Band {band_number}: "
            f"{valid_pixels:,} valid / "
            f"{total_pixels:,} total "
            f"({percentage:.2f}%)"
        )