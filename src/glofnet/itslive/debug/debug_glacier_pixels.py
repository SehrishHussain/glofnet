"""
Inspect velocity values inside the glacier polygon.

This script clips the RAW ITS_LIVE granule in memory and reports
how many valid pixels exist within the glacier.
"""

import numpy as np
import rioxarray  # noqa: F401
import xarray as xr

from glofnet.common.find_glacier import load_glacier
from glofnet.common.geospatial import (
    get_dataset_crs,
    reproject_geometry,
)
from glofnet.common.paths import ITSLIVE_RAW_DIRECTORY
from glofnet.itslive.config import GLACIER_ID


def inspect_variable(ds: xr.Dataset, variable: str) -> None:
    """
    Print statistics for one variable.
    """

    data = ds[variable].values

    total = data.size
    valid = np.count_nonzero(~np.isnan(data))
    missing = np.count_nonzero(np.isnan(data))

    print("\n" + "=" * 70)
    print(variable)
    print("=" * 70)

    print(f"Total pixels : {total:,}")
    print(f"Valid pixels : {valid:,}")
    print(f"Missing      : {missing:,}")

    if valid == 0:
        print("\nNo valid values inside glacier.")
        return

    print(f"\nMinimum : {np.nanmin(data):.2f}")
    print(f"Maximum : {np.nanmax(data):.2f}")
    print(f"Mean    : {np.nanmean(data):.2f}")
    print(f"Std Dev : {np.nanstd(data):.2f}")


def main():

    path = next(ITSLIVE_RAW_DIRECTORY.glob("*.nc"))

    print(f"\nDataset:\n{path.name}")

    ds = xr.open_dataset(path)

    # ------------------------------------------------------------------
    # Attach CRS
    # ------------------------------------------------------------------

    crs = get_dataset_crs(ds)

    ds = ds.rio.write_crs(crs)

    # ------------------------------------------------------------------
    # Load glacier
    # ------------------------------------------------------------------

    glacier = load_glacier(GLACIER_ID)

    glacier = reproject_geometry(glacier, crs)

    # ------------------------------------------------------------------
    # Clip IN MEMORY
    # ------------------------------------------------------------------

    clipped = ds.rio.clip(
        glacier.geometry.values,
        glacier.crs,
        drop=True,
    )

    print("\nClipped dimensions")
    print(dict(clipped.sizes))

    print("\nVariables")
    print(list(clipped.data_vars))

    # ------------------------------------------------------------------
    # Inspect velocity variables
    # ------------------------------------------------------------------

    for variable in [
        "vx",
        "vy",
        "v",
        "v_error",
    ]:
        inspect_variable(clipped, variable)

    # ------------------------------------------------------------------
    # Interpolation mask
    # ------------------------------------------------------------------

    print("\n" + "=" * 70)
    print("interp_mask")
    print("=" * 70)

    mask = clipped["interp_mask"].values

    unique, counts = np.unique(mask, return_counts=True)

    for value, count in zip(unique, counts):
        print(f"{value}: {count:,}")

    ds.close()
    clipped.close()


if __name__ == "__main__":
    main()