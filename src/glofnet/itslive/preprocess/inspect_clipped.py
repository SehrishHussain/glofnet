"""
Inspect clipped ITS_LIVE datasets.

This utility verifies that clipping produced the expected output before
continuing to later preprocessing stages.
"""

from pathlib import Path

import numpy as np
import xarray as xr

from glofnet.common.paths import ITSLIVE_CLIPPED_DIRECTORY


def inspect_dataset(path: Path) -> None:
    """
    Print summary information for one clipped dataset.
    """

    ds = xr.open_dataset(path)

    print("=" * 70)
    print(path.name)
    print("=" * 70)

    # ------------------------------------------------------------------
    # Dataset summary
    # ------------------------------------------------------------------

    print("\nDataset")
    print(ds)

    # ------------------------------------------------------------------
    # Dimensions
    # ------------------------------------------------------------------

    print("\nDimensions")
    print(dict(ds.sizes))

    # ------------------------------------------------------------------
    # CRS
    # ------------------------------------------------------------------

    print("\nCRS")

    if "spatial_ref" in ds.coords:
        print(ds["spatial_ref"].attrs.get("crs_wkt", "Unknown"))
    elif "mapping" in ds:
        print(ds["mapping"].attrs.get("spatial_epsg", "Unknown"))
    else:
        print("None")

    # ------------------------------------------------------------------
    # Variables
    # ------------------------------------------------------------------

    print("\nVariables")
    print(list(ds.data_vars))

    # ------------------------------------------------------------------
    # Bounding box
    # ------------------------------------------------------------------

    print("\nBounding box")

    print(f"x min : {float(ds.x.min()):.2f}")
    print(f"x max : {float(ds.x.max()):.2f}")
    print(f"y min : {float(ds.y.min()):.2f}")
    print(f"y max : {float(ds.y.max()):.2f}")

    # ------------------------------------------------------------------
    # Valid pixels
    # ------------------------------------------------------------------

    print("\nValid pixels")

    for variable in ["vx", "vy", "v", "v_error"]:

        if variable not in ds:
            continue

        data = ds[variable].values

        valid = np.count_nonzero(~np.isnan(data))
        missing = np.count_nonzero(np.isnan(data))

        print(
            f"{variable:<8}"
            f" valid={valid:,}"
            f" missing={missing:,}"
        )

    # ------------------------------------------------------------------
    # Velocity statistics
    # ------------------------------------------------------------------

    print("\nVelocity statistics")

    for variable in ["vx", "vy", "v", "v_error"]:

        if variable not in ds:
            continue

        data = ds[variable].values

        print(f"\n{variable}")

        print(f"  Minimum : {np.nanmin(data):.2f}")
        print(f"  Maximum : {np.nanmax(data):.2f}")
        print(f"  Mean    : {np.nanmean(data):.2f}")
        print(f"  Std Dev : {np.nanstd(data):.2f}")

    # ------------------------------------------------------------------
    # Interpolation mask
    # ------------------------------------------------------------------

    if "interp_mask" in ds:

        print("\nInterpolation mask")

        values, counts = np.unique(
            ds["interp_mask"].values,
            return_counts=True,
        )

        for value, count in zip(values, counts):
            print(f"{value}: {count:,}")

    ds.close()


def main():

    datasets = sorted(
        ITSLIVE_CLIPPED_DIRECTORY.glob("*.nc")
    )

    if not datasets:
        raise FileNotFoundError(
            "No clipped ITS_LIVE datasets found."
        )

    for dataset in datasets:
        inspect_dataset(dataset)


if __name__ == "__main__":
    main()