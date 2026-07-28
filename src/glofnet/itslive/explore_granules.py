"""
Explore the ITS_LIVE Python API.

This script searches for velocity granules intersecting the configured glacier
and prints information about the returned objects.
"""

from datetime import date

import itslive

from glofnet.common.find_glacier import load_glacier
from glofnet.itslive.config import (
    GLACIER_ID,
    START_DATE,
    END_DATE,
)


def glacier_to_geojson(glacier):
    """
    Convert a single glacier polygon into a GeoJSON geometry.

    Parameters
    ----------
    glacier : GeoDataFrame

    Returns
    -------
    dict
        GeoJSON geometry dictionary.
    """
    return glacier.geometry.iloc[0].__geo_interface__


def main():

    glacier = load_glacier(GLACIER_ID)

    geometry = glacier_to_geojson(glacier)

    print("Searching ITS_LIVE granules...\n")

    results = itslive.velocity_pairs.find(
        geojson=geometry,
        start=date.fromisoformat(START_DATE),
        end=date.fromisoformat(END_DATE),
    )

    print("=" * 70)
    print("SEARCH RESULTS")
    print("=" * 70)

    print(f"Returned object : {type(results)}")
    print(f"Number found    : {len(results)}")

    if len(results) == 0:
        print("\nNo granules found.")
        return

    first = results[0]

    print("\nFIRST RESULT")
    print("=" * 70)

    print(type(first))
    print(first)


if __name__ == "__main__":
    main()