"""
Inspect an ITS_LIVE velocity Zarr dataset.

This script explores the structure of the ITS_LIVE velocity cube before
implementing the production download and preprocessing pipeline.
"""

import xarray as xr

from glofnet.common.find_glacier import load_glacier
from glofnet.itslive.config import GLACIER_ID
from glofnet.itslive.search_cube import find_cube


def open_dataset():
    """
    Locate the ITS_LIVE cube for the configured glacier and open it as an
    xarray Dataset.

    Returns
    -------
    xarray.Dataset
    """

    glacier = load_glacier(GLACIER_ID)

    cube = find_cube(glacier)

    print(f"\nOpening Zarr dataset:")
    print(cube.zarr_url)

    return xr.open_zarr(cube.zarr_url)


def print_dataset_summary(ds):
    """Print a high-level dataset summary."""

    print("\n" + "=" * 70)
    print("DATASET SUMMARY")
    print("=" * 70)

    print(ds)


def print_dimensions(ds):
    """Print dataset dimensions."""

    print("\n" + "=" * 70)
    print("DIMENSIONS")
    print("=" * 70)

    for name, size in ds.dims.items():
        print(f"{name:<20}{size}")


def print_coordinates(ds):
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

        values = coord.values

        if len(values) > 0:
            print(f"First      : {values[0]}")
            print(f"Last       : {values[-1]}")


def print_variables(ds):
    """Print available data variables."""

    print("\n" + "=" * 70)
    print("DATA VARIABLES")
    print("=" * 70)

    for name in ds.data_vars:
        print(name)


def print_variable_details(ds):
    """Print detailed information for each variable."""

    print("\n" + "=" * 70)
    print("VARIABLE DETAILS")
    print("=" * 70)

    for name, da in ds.data_vars.items():

        print(f"\n{name}")
        print("-" * len(name))

        print(f"Dimensions : {da.dims}")
        print(f"Shape      : {da.shape}")
        print(f"Dtype      : {da.dtype}")
        print(f"Chunks     : {da.chunks}")

        print("\nAttributes")

        if da.attrs:
            for key, value in da.attrs.items():
                print(f"  {key}: {value}")
        else:
            print("  None")

        if da.dtype.kind in {"f", "i", "u"}:

            print("\nStatistics")

            print(f"  Min     : {da.min().item()}")
            print(f"  Max     : {da.max().item()}")
            print(f"  Mean    : {da.mean().item()}")
            print(f"  Missing : {da.isnull().sum().item()}")


def print_global_attributes(ds):
    """Print dataset-level metadata."""

    print("\n" + "=" * 70)
    print("GLOBAL ATTRIBUTES")
    print("=" * 70)

    for key, value in ds.attrs.items():
        print(f"{key}: {value}")


def main():

    ds = open_dataset()

    print_dataset_summary(ds)

    print_dimensions(ds)

    print_coordinates(ds)

    print_variables(ds)

    print_variable_details(ds)

    print_global_attributes(ds)

    ds.close()


if __name__ == "__main__":
    main()