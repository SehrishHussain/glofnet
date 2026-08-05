"""
Inspect an ITS_LIVE velocity granule.

This module inspects the structure of a downloaded ITS_LIVE NetCDF
granule before implementing the preprocessing pipeline.
"""

from pathlib import Path

import xarray as xr

from glofnet.itslive.config import OUTPUT_DIRECTORY


def open_granule(path: Path) -> xr.Dataset:
    """
    Open a downloaded ITS_LIVE granule.

    Parameters
    ----------
    path : Path
        Path to the NetCDF granule.

    Returns
    -------
    xarray.Dataset
    """
    return xr.open_dataset(path)


def print_dataset_summary(ds: xr.Dataset) -> None:
    """Print the dataset summary."""

    print("\n" + "=" * 70)
    print("DATASET")
    print("=" * 70)

    print(ds)


def print_dimensions(ds: xr.Dataset) -> None:
    """Print dataset dimensions."""

    print("\n" + "=" * 70)
    print("DIMENSIONS")
    print("=" * 70)

    for name, size in ds.sizes.items():
        print(f"{name:<20}{size}")


def print_coordinates(ds: xr.Dataset) -> None:
    """Print coordinate information."""

    print("\n" + "=" * 70)
    print("COORDINATES")
    print("=" * 70)

    for name, coord in ds.coords.items():

        print(f"\n{name}")
        print("-" * len(name))

        print(f"Dimensions : {coord.dims}")
        print(f"Shape      : {coord.shape}")
        print(f"Dtype      : {coord.dtype}")


def print_variables(ds: xr.Dataset) -> None:
    """Print all data variables."""

    print("\n" + "=" * 70)
    print("DATA VARIABLES")
    print("=" * 70)

    for name, variable in ds.data_vars.items():

        print(f"\n{name}")
        print("-" * len(name))

        print(f"Dimensions : {variable.dims}")
        print(f"Shape      : {variable.shape}")
        print(f"Dtype      : {variable.dtype}")

        print("Attributes")

        if variable.attrs:
            for key, value in variable.attrs.items():
                print(f"  {key}: {value}")
        else:
            print("  None")


def print_global_attributes(ds: xr.Dataset) -> None:
    """Print dataset metadata."""

    print("\n" + "=" * 70)
    print("GLOBAL ATTRIBUTES")
    print("=" * 70)

    if ds.attrs:
        for key, value in ds.attrs.items():
            print(f"{key}: {value}")
    else:
        print("None")


def inspect_granule(path: Path) -> None:
    """
    Inspect a downloaded ITS_LIVE granule.

    Parameters
    ----------
    path : Path
        Path to the NetCDF file.
    """

    ds = open_granule(path)

    print_dataset_summary(ds)
    print_dimensions(ds)
    print_coordinates(ds)
    print_variables(ds)
    print_global_attributes(ds)

    ds.close()


def main():

    output_dir = Path(OUTPUT_DIRECTORY)

    granules = sorted(output_dir.glob("*.nc"))

    if not granules:
        raise FileNotFoundError(
            "No downloaded ITS_LIVE granules found. "
            "Run download_granules.py first."
        )

    inspect_granule(granules[0])


if __name__ == "__main__":
    main()