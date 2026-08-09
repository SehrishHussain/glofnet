"""
Reduce ITS_LIVE datasets to the variables required by CryoFusion.
"""

from pathlib import Path

import xarray as xr

from glofnet.common.paths import (
    ITSLIVE_PROCESSED_DIRECTORY,
    ITSLIVE_RAW_DIRECTORY,
)
from glofnet.itslive.config import ITSLIVE_VARIABLES


def preprocess_granule(path: Path) -> Path:
    """
    Reduce a single ITS_LIVE granule to the required variables.

    Parameters
    ----------
    path : Path
        Path to the raw ITS_LIVE NetCDF file.

    Returns
    -------
    Path
        Path to the reduced NetCDF file.
    """

    with xr.open_dataset(path) as ds:

        # --------------------------------------------------------------
        # Verify required variables exist.
        # --------------------------------------------------------------
        missing = [
            variable
            for variable in ITSLIVE_VARIABLES
            if variable not in ds.data_vars
        ]

        if missing:
            raise KeyError(
                "Missing ITS_LIVE variables: "
                f"{', '.join(missing)}"
            )

        # --------------------------------------------------------------
        # Keep only required variables.
        # --------------------------------------------------------------
        reduced = ds[ITSLIVE_VARIABLES]

        # --------------------------------------------------------------
        # Save.
        # --------------------------------------------------------------
        ITSLIVE_PROCESSED_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = (
            ITSLIVE_PROCESSED_DIRECTORY / path.name
        )

        reduced.to_netcdf(output_path)

        reduced.close()

    return output_path


def preprocess_all() -> list[Path]:
    """
    Reduce every raw ITS_LIVE dataset.

    Returns
    -------
    list[Path]
        Paths to the reduced datasets.
    """

    datasets = sorted(
        ITSLIVE_RAW_DIRECTORY.glob("*.nc")
    )

    if not datasets:
        raise FileNotFoundError(
            "No ITS_LIVE datasets found."
        )

    processed_files: list[Path] = []

    for dataset in datasets:
        processed_files.append(
            preprocess_granule(dataset)
        )

    return processed_files


def main():

    processed = preprocess_all()

    print("\nReduced datasets:\n")

    for dataset in processed:
        print(dataset)


if __name__ == "__main__":
    main()