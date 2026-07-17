import ee
import geemap
import webbrowser
import requests
from pathlib import Path

from glofnet.common.find_glacier import load_glacier

from glofnet.sentinel.config import (
    GLACIER_ID,
    START_DATE,
    END_DATE,
    MAX_CLOUD_PERCENTAGE,
)


def main():

    ee.Initialize()

    glacier = load_glacier(GLACIER_ID)

    polygon = glacier.geometry.iloc[0]

    coords = [
        [x, y]
        for x, y, *_ in polygon.exterior.coords
    ]

    ee_polygon = ee.Geometry.Polygon([coords])

    print("Earth Engine polygon created successfully.")
    collection = (
    ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
    .filterBounds(ee_polygon)
    .filterDate(START_DATE, END_DATE)
    .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", MAX_CLOUD_PERCENTAGE))
)

    count = collection.size().getInfo()

    first_image = collection.first()

    glacier_id = glacier.iloc[0]["rgi_id"]

    image_date = ee.Date(first_image.get("system:time_start")).format("YYYY-MM-dd").getInfo()

    filename = f"{glacier_id}_{image_date}.tif"

    print(filename)
    output_dir = Path("data/raw/sentinel")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / filename

    #print(geemap.image_date)
    clipped_image = first_image.clip(ee_polygon)
    rgb = clipped_image.select([ "B2",   # Blue
    "B3",   # Green
    "B4",   # Red
    "B8",   # NIR
    "B11",  # SWIR-1
    "B12",  # SWIR-2
    ])
    download_url = rgb.getDownloadURL(
    {
        "scale": 10,
        "region": ee_polygon,
        "format": "GEO_TIFF",
    }
)
    print(glacier.columns)
   # print(download_url)
    response = requests.get(download_url)
    with open(output_file, "wb") as f:
        f.write(response.content)

    print(f"GeoTIFF saved to: {output_file}")
    
    print("GeoTIFF downloaded successfully.")

    Map = geemap.Map()

    Map.centerObject(ee_polygon, 12)

    
   # print(first_image.getInfo())

    print(f"Found {count} Sentinel-2 images after cloud filtering.")
    Map.addLayer(
    rgb,
    {
        "bands": ["B4", "B3", "B2"],
        "min": 0,
        "max": 3000,
    },
    "Sentinel RGB",
)
    

    Map.addLayer(
        ee_polygon,
        {"color": "red"},
        "Passu Glacier",
    )
    Map.to_html("passu_map.html")

    webbrowser.open("passu_map.html")

if __name__ == "__main__":
    main()