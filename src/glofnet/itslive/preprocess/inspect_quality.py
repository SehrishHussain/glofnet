"""
Inspect quality-controlled ITS_LIVE datasets.

This module summarizes the contents of quality-masked ITS_LIVE datasets.
It is intended for diagnostics and validation, not preprocessing.
"""

from pathlib import Path

import xarray as xr


from glofnet.common.paths import QUALITY_DIRECTORY

QUALITY_DIRECTORY = QUALITY_DIRECTORY / "itslive"


def inspect_dataset(path: Path) -> None:
    """
    Inspect one quality-controlled ITS_LIVE dataset.

    Parameters
    ----------
    path : Path
        Path to a quality-controlled NetCDF dataset.
    """

    ds = xr.open_dataset(path)

    print("=" * 70)
    print(path.name)
    print("=" * 70)

    print("\nDimensions")
    print(ds.sizes)

    print("\nCRS")
    print(ds.rio.crs)

    print("\nVariables")
    print(list(ds.data_vars))

    print("\nVelocity statistics")

    for variable in ["vx", "vy", "v", "v_error"]:

        data = ds[variable]

        print(f"\n{variable}")
        print(f"  Min   : {float(data.min(skipna=True)):.3f}")
        print(f"  Max   : {float(data.max(skipna=True)):.3f}")
        print(f"  Mean  : {float(data.mean(skipna=True)):.3f}")

        valid = int(data.notnull().sum())
        total = data.size

        print(f"  Valid : {valid:,}")
        print(f"  Missing: {total - valid:,}")

    print("\nInterpolation mask")

    interpolated = int(ds["interp_mask"].sum())

    total_pixels = ds["interp_mask"].size

    print(f"Interpolated pixels : {interpolated:,}")
    print(f"Total pixels        : {total_pixels:,}")
    print(
        f"Interpolation rate  : "
        f"{100 * interpolated / total_pixels:.2f}%"
    )

    ds.close()


def inspect_all() -> None:
    """
    Inspect every quality-controlled dataset.
    """

    datasets = sorted(QUALITY_DIRECTORY.glob("*.nc"))

    if not datasets:
        raise FileNotFoundError(
            "No quality-controlled ITS_LIVE datasets found."
        )

    for dataset in datasets:
        inspect_dataset(dataset)


def main():

    inspect_all()


if __name__ == "__main__":
    main()