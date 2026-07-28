"""
Search for the ITS_LIVE velocity cube corresponding to a glacier.
"""

from pystac_client import Client

from glofnet.itslive.config import (
    STAC_URL,
    COLLECTION_NAME,
    MAX_ITEMS,
)
from glofnet.itslive.models import CubeInfo


def connect_to_catalog():
    """
    Connect to the ITS_LIVE STAC catalog.

    Returns
    -------
    pystac_client.Client
        Connected STAC client.
    """
    return Client.open(STAC_URL)


def compute_bbox(glacier):
    """
    Compute the glacier bounding box.

    Parameters
    ----------
    glacier : GeoDataFrame
        Single glacier polygon.

    Returns
    -------
    list[float]
        Bounding box in STAC format:
        [west, south, east, north]
    """
    west, south, east, north = glacier.total_bounds
    return [west, south, east, north]


def find_cube(glacier):
    """
    Find the ITS_LIVE cube intersecting a glacier.

    Parameters
    ----------
    glacier : GeoDataFrame
        Glacier polygon.

    Returns
    -------
    CubeInfo
        Metadata describing the ITS_LIVE cube.

    Raises
    ------
    RuntimeError
        If no cube or multiple cubes are found.
    """

    catalog = connect_to_catalog()

    bbox = compute_bbox(glacier)

    search = catalog.search(
        collections=[COLLECTION_NAME],
        bbox=bbox,
        max_items=MAX_ITEMS,
    )

    items = list(search.items())

    if len(items) == 0:
        raise RuntimeError("No ITS_LIVE cube found for glacier.")

    if len(items) > 1:
        raise RuntimeError(
            f"Expected one cube but found {len(items)}."
        )

    item = items[0]

    return CubeInfo(
        id=item.id,
        zarr_url=item.assets["zarr"].href,
        epsg=item.properties["proj:code"],
        bbox=tuple(item.bbox),
        start_datetime=item.properties["start_datetime"],
        end_datetime=item.properties["end_datetime"],
        granule_count=item.properties["granule_count"],
    )

def get_cube(glacier):
    """
    Convenience wrapper for find_cube().

    Parameters
    ----------
    glacier : GeoDataFrame

    Returns
    -------
    CubeInfo
    """
    return find_cube(glacier)