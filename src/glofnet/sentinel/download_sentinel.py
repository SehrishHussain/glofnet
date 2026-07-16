import ee
import geemap
import webbrowser

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
    clipped_image = first_image.clip(ee_polygon)
    rgb = clipped_image.select(["B4", "B3", "B2"])

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