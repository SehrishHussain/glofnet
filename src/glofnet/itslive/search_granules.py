"""
Search the ITS_LIVE STAC granule collection for velocity granules
intersecting a glacier.
"""

from pystac_client import Client

from glofnet.common.find_glacier import load_glacier
from glofnet.itslive.config import (
    GLACIER_ID,
    STAC_URL,
    COLLECTION_NAME,
    START_DATE,
    END_DATE,
    MAX_ITEMS,
)
from glofnet.itslive.models import GranuleInfo


def connect_to_catalog():
    """Connect to the ITS_LIVE STAC catalog."""
    return Client.open(STAC_URL)


def compute_bbox(glacier):
    """
    Compute the glacier bounding box.

    Returns
    -------
    list[float]
        [west, south, east, north]
    """
    west, south, east, north = glacier.total_bounds
    return [west, south, east, north]


def search_granules() -> list[GranuleInfo]:
    """
    Search ITS_LIVE granules for the configured glacier.

    Returns
    -------
    list[GranuleInfo]
    """

    glacier = load_glacier(GLACIER_ID)

    bbox = compute_bbox(glacier)

    catalog = connect_to_catalog()

    search = catalog.search(
        collections=[COLLECTION_NAME],
        bbox=bbox,
        datetime=f"{START_DATE}/{END_DATE}",
        max_items=MAX_ITEMS,
    )

    granules: list[GranuleInfo] = []

    for item in search.items():

        # Find the NetCDF asset
        asset = item.assets.get("data")

        if asset is None:
            continue

        granules.append(
            GranuleInfo(
                id=item.id,
                url=asset.href,
                bbox=tuple(item.bbox),

                datetime=item.properties.get("datetime"),
                start_datetime=item.properties.get("start_datetime"),
                end_datetime=item.properties.get("end_datetime"),

                platform=item.properties.get("platform"),

                projection=item.properties.get("proj:code"),

                percent_valid_pixels=item.properties.get("percent_valid_pixels"),

                version=item.properties.get("version"),

                scene_1_id=item.properties.get("scene_1_id"),
                scene_2_id=item.properties.get("scene_2_id"),
            )
        )

    return granules


def main():

    granules = search_granules()

    print(f"\nFound {len(granules)} granules.\n")
    if not granules:
        raise RuntimeError("No ITS_LIVE granules found.")

    for granule in granules[:5]:

        for granule in granules[:5]:

            print(f"ID        : {granule.id}")
            print(f"Platform  : {granule.platform}")
            print(f"Datetime  : {granule.datetime}")
            print(f"Quality   : {granule.percent_valid_pixels}%")
            print(f"File      : {granule.filename}")
            print()
            print()


if __name__ == "__main__":
    main()