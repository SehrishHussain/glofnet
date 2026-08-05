

from pathlib import Path

import xarray as xr

from glofnet.common.paths import (
    RAW_DIRECTORY,
    PROCESSED_DIRECTORY,
)
from glofnet.itslive.config import ITSLIVE_VARIABLES


RAW_DIRECTORY = RAW_DIRECTORY / "itslive"
PROCESSED_DIRECTORY = PROCESSED_DIRECTORY / "itslive"


def preprocess_granule(path: Path) -> Path:
    """
    Preprocess one ITS_LIVE granule.

    Parameters
    ----------
    path : Path
        Path to the downloaded NetCDF file.

    Returns
    -------
    Path
        Path to the processed NetCDF.
    """

    ds = xr.open_dataset(path)


    # Verify that all required variables exist.
    missing = [
        variable
        for variable in ITSLIVE_VARIABLES
        if variable not in ds.data_vars
    ]

    if missing:
        ds.close()
        raise KeyError(
            f"Missing ITS_LIVE variables: {', '.join(missing)}"
        )

    # Keep only the required variables.
    processed = ds[ITSLIVE_VARIABLES]

    # Create output directory if needed.
    PROCESSED_DIRECTORY.mkdir(parents=True, exist_ok=True)

    output_path = PROCESSED_DIRECTORY / path.name

    # Save the reduced dataset.
    processed.to_netcdf(output_path)

    processed.close()
    ds.close()

    return output_path
def preprocess_all() -> list[Path]:
    """
    Reduce variables for all downloaded ITS_LIVE granules.
    """

    granules = sorted(RAW_DIRECTORY.glob("*.nc"))

    if not granules:
        raise FileNotFoundError(
            "No downloaded ITS_LIVE granules found."
        )

    processed_files: list[Path] = []

    for granule in granules:
        processed_files.append(
            preprocess_granule(granule)
        )

    return processed_files


def main():

    processed = preprocess_all()

    print("\nProcessed files:\n")

    for file in processed:
        print(file)


if __name__ == "__main__":
    main()