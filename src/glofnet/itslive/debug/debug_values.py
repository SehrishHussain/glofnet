"""
Inspect ITS_LIVE velocity values around the glacier.

This script checks whether the downloaded ITS_LIVE granule contains
valid velocity measurements around the glacier centroid before any
preprocessing or clipping.
"""

from pathlib import Path

import numpy as np
import xarray as xr

from glofnet.common.find_glacier import load_glacier
from glofnet.common.geospatial import (
    get_dataset_crs,
    reproject_geometry,
)
from glofnet.common.paths import ITSLIVE_RAW_DIRECTORY
from glofnet.itslive.config import GLACIER_ID


WINDOW_RADIUS = 10  # pixels


def inspect_variable(ds: xr.Dataset, variable: str) -> None:
    """
    Inspect one variable around the glacier centroid.
    """

    glacier = load_glacier(GLACIER_ID)

    dataset_crs = get_dataset_crs(ds)

    glacier = reproject_geometry(glacier, dataset_crs)

    centroid = glacier.geometry.iloc[0].centroid

    print("\n" + "=" * 70)
    print(variable)
    print("=" * 70)

    print(f"Centroid X : {centroid.x:.2f}")
    print(f"Centroid Y : {centroid.y:.2f}")

    # ------------------------------------------------------------
    # Find nearest pixel
    # ------------------------------------------------------------

    x_index = int(np.abs(ds.x.values - centroid.x).argmin())
    y_index = int(np.abs(ds.y.values - centroid.y).argmin())

    print(f"Nearest x index : {x_index}")
    print(f"Nearest y index : {y_index}")

    # ------------------------------------------------------------
    # Extract window
    # ------------------------------------------------------------

    window = ds[variable].isel(
        time=0,
        x=slice(
            max(0, x_index - WINDOW_RADIUS),
            min(ds.sizes["x"], x_index + WINDOW_RADIUS + 1),
        ),
        y=slice(
            max(0, y_index - WINDOW_RADIUS),
            min(ds.sizes["y"], y_index + WINDOW_RADIUS + 1),
        ),
    )

    values = window.values

    total = values.size
    valid = np.count_nonzero(~np.isnan(values))
    missing = np.count_nonzero(np.isnan(values))

    print(f"Window size : {values.shape}")
    print(f"Total pixels: {total}")
    print(f"Valid pixels: {valid}")
    print(f"Missing     : {missing}")

    if valid > 0:
        print(f"Minimum : {np.nanmin(values):.2f}")
        print(f"Maximum : {np.nanmax(values):.2f}")
        print(f"Mean    : {np.nanmean(values):.2f}")
    else:
        print("No valid values in this window.")


def main():

    path = next(ITSLIVE_RAW_DIRECTORY.glob("*.nc"))

    print(f"Dataset: {path.name}")

    ds = xr.open_dataset(path)

    for variable in [
        "vx",
        "vy",
        "v",
        "v_error",
    ]:
        inspect_variable(ds, variable)

    ds.close()


if __name__ == "__main__":
    main()