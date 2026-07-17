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

def create_ee_polygon(glacier):
    """
    Convert a glacier polygon from a GeoDataFrame
    into an Earth Engine polygon.
    """

    polygon = glacier.geometry.iloc[0]

    coords = [
        [x, y]
        for x, y, *_ in polygon.exterior.coords
    ]

    return ee.Geometry.Polygon([coords])

def get_sentinel_collection(
    ee_polygon,
    start_date,
    end_date,
    max_cloud_percentage,
):
    """
    Return a cloud-filtered Sentinel-2 image collection
    for the specified area and date range.
    """

    return (
        ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
        .filterBounds(ee_polygon)
        .filterDate(start_date, end_date)
        .filter(
            ee.Filter.lt(
                "CLOUDY_PIXEL_PERCENTAGE",
                max_cloud_percentage,
            )
        )
    )

def download_collection(
        collection,
        glacier_id,
        ee_polygon,
        output_dir,
        max_images=None
    ):
        """
        Download the first few images from a Sentinel-2 collection.
        """
        
        collection_size = collection.size().getInfo()

        if max_images is None:
            images_to_download = collection_size
        else:
            images_to_download = min(collection_size, max_images)

        image_list = collection.toList(images_to_download)

        for i in range(images_to_download):
            image = ee.Image(image_list.get(i))

            output_file = download_image(
                image,
                glacier_id,
                ee_polygon,
                output_dir,
            )

            print(f"Downloaded to: {output_file}")
                     
           
def download_image(
    image,
    glacier_id,
    ee_polygon,
    output_dir,
):
    """
    Download a clipped Sentinel-2 image and save it
    as a GeoTIFF using the glacier ID and acquisition date.
    """

    image = image.clip(ee_polygon)

    image_date = (
        ee.Date(image.get("system:time_start"))
        .format("YYYY-MM-dd")
        .getInfo()
    )

    filename = f"{glacier_id}_{image_date}.tif"

    export_image = image.select(
        [
            "B2",   # Blue
            "B3",   # Green
            "B4",   # Red
            "B8",   # Near Infrared
            "B11",  # SWIR-1
            "B12",  # SWIR-2
        ]
    )

    download_url = export_image.getDownloadURL(
        {
            "scale": 10,
            "region": ee_polygon,
            "format": "GEO_TIFF",
        }
    )

    response = requests.get(download_url)
    response.raise_for_status()

    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / filename

    with open(output_file, "wb") as f:
        f.write(response.content)

    print(f"Downloaded {filename}")

    return output_file

def main():

    ee.Initialize()

    glacier = load_glacier(GLACIER_ID)

   
    ee_polygon = create_ee_polygon(glacier)
    print("Earth Engine polygon created successfully.")

    collection = get_sentinel_collection(
    ee_polygon,
    START_DATE,
    END_DATE,
    MAX_CLOUD_PERCENTAGE,
)
    

    count = collection.size().getInfo()

    first_image = collection.first()

    glacier_id = glacier.iloc[0]["rgi_id"]

    output_dir = Path("data/raw/sentinel")
    

    #print(f"GeoTIFF saved to: {output_file}")
    map_view = geemap.Map()

    map_view.centerObject(ee_polygon, 12)

    
   # print(first_image.getInfo())

    print(f"Found {count} Sentinel-2 images after cloud filtering.")
    rgb = (
    first_image
    .clip(ee_polygon)
    .select(["B4", "B3", "B2"])
)
    map_view.addLayer(
    rgb,
    {
        "bands": ["B4", "B3", "B2"],
        "min": 0,
        "max": 3000,
    },
    "Sentinel RGB",
)
    

    map_view.addLayer(
        ee_polygon,
        {"color": "red"},
        "Passu Glacier",
    )
    map_view.to_html("passu_map.html")

    webbrowser.open("passu_map.html")

    downloaded_files = download_collection(
    collection,
    glacier_id,
    ee_polygon,
    output_dir,
    max_images=5,
    
)

if __name__ == "__main__":
    main()