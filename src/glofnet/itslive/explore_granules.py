"""
Explore the ITS_LIVE granule STAC collection.

This script is for exploratory purposes only. It helps us understand the
structure of ITS_LIVE velocity granules before implementing the production
search and download pipeline.

Workflow
--------
1. Load the glacier from the RGI inventory.
2. Compute its bounding box.
3. Connect to the ITS_LIVE STAC catalog.
4. Search the ITS_LIVE granule collection.
5. Inspect one STAC Item.
"""

from pystac_client import Client

from glofnet.common.console import (
    print_header,
    print_section,
    print_key_value,
    print_success,
    print_warning,
)
from glofnet.common.find_glacier import load_glacier
from glofnet.itslive.config import (
    GLACIER_ID,
    STAC_URL,
    COLLECTION_NAME,
    START_DATE,
    END_DATE,
    MAX_ITEMS,
)


def connect_to_catalog():
    """Connect to the ITS_LIVE STAC catalog."""

    print_section("Connecting to ITS_LIVE STAC")

    catalog = Client.open(STAC_URL)

    print_success("Connected successfully")

    return catalog


def compute_bbox(glacier):
    """
    Compute the glacier bounding box.

    Returns
    -------
    list[float]
        Bounding box in STAC format:
        [west, south, east, north]
    """

    west, south, east, north = glacier.total_bounds

    print_section("Bounding Box")

    print_key_value("West", west)
    print_key_value("South", south)
    print_key_value("East", east)
    print_key_value("North", north)

    return [west, south, east, north]


def search_granules(catalog, bbox):
    """
    Search the ITS_LIVE granule collection.
    """

    print_section("Searching ITS_LIVE Granules")

    search = catalog.search(
        collections=[COLLECTION_NAME],
        bbox=bbox,
        datetime=f"{START_DATE}/{END_DATE}",
        max_items=MAX_ITEMS,
    )

    items = list(search.items())

    print_key_value("Matching Granules", len(items))

    return items


def print_summary(item):
    """Print a summary of the STAC Item."""

    print_section("Granule Summary")

    print_key_value("ID", item.id)
    print_key_value("Collection", item.collection_id)
    print_key_value("Geometry", item.geometry["type"])
    print_key_value("BBox", item.bbox)


def print_assets(item):
    """Print all assets."""

    print_section("Assets")

    for name, asset in item.assets.items():

        print_key_value("Asset", name)
        print_key_value("Title", asset.title)
        print_key_value("Media Type", asset.media_type)
        print_key_value("Href", asset.href)

        print()


def print_properties(item):
    """Print all STAC properties."""

    print_section("Properties")

    for key, value in sorted(item.properties.items()):
        print_key_value(key, value)


def main():

    print_header("ITS_LIVE Granule Exploration")

    glacier = load_glacier(GLACIER_ID)

    print_success("Glacier loaded")

    print_key_value("Glacier ID", GLACIER_ID)

    bbox = compute_bbox(glacier)

    catalog = connect_to_catalog()

    items = search_granules(catalog, bbox)

    if not items:

        print_warning("No matching granules found.")

        return

    item = items[0]

    print_summary(item)

    print_assets(item)

    print_properties(item)


if __name__ == "__main__":
    main()