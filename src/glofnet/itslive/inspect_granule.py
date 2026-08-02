"""
Inspect an ITS_LIVE velocity granule.
"""

from pathlib import Path

import xarray as xr

from glofnet.itslive.config import OUTPUT_DIRECTORY


def inspect_granule(filename):

    path = Path(OUTPUT_DIRECTORY) / filename

    ds = xr.open_dataset(path)

    print("=" * 70)
    print("DATASET")
    print("=" * 70)

    print(ds)

    print("\nDimensions")
    print(ds.sizes)

    print("\nCoordinates")
    print(list(ds.coords))

    print("\nVariables")

    for variable in ds.data_vars:
        print(variable)

    print("\nAttributes")

    for key, value in ds.attrs.items():
        print(f"{key}: {value}")


def main():

    directory = Path(OUTPUT_DIRECTORY)

    files = sorted(directory.glob("*.nc"))

    if not files:
        raise FileNotFoundError("No granules downloaded.")

    inspect_granule(files[0].name)


if __name__ == "__main__":
    main()