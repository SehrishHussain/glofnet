"""
Clip reduced ITS_LIVE datasets to the configured glacier geometry.

Workflow
--------
1. Open a reduced ITS_LIVE dataset.
2. Read the dataset CRS.
3. Attach the CRS to the dataset.
4. Load the glacier geometry.
5. Reproject the glacier to the dataset CRS.
6. Clip the dataset.
7. Save the clipped dataset.
"""

from pathlib import Path

import rioxarray  # noqa: F401
import xarray as xr

from glofnet.common.find_glacier import load_glacier
from glofnet.common.geospatial import (
    get_dataset_crs,
    reproject_geometry,
)
from glofnet.common.paths import (
    ITSLIVE_CLIPPED_DIRECTORY,
    ITSLIVE_PROCESSED_DIRECTORY,
)
from glofnet.itslive.config import GLACIER_ID


def clip_granule(path: Path) -> Path:
    """
    Clip a reduced ITS_LIVE dataset to the configured glacier.

    Parameters
    ----------
    path : Path
        Path to the reduced ITS_LIVE NetCDF file.

    Returns
    -------
    Path
        Path to the clipped NetCDF file.
    """

    with xr.open_dataset(path) as ds:

        # --------------------------------------------------------------
        # Attach CRS.
        # --------------------------------------------------------------

        crs = get_dataset_crs(ds)

        ds = ds.rio.write_crs(crs)

        # --------------------------------------------------------------
        # Load glacier geometry.
        # --------------------------------------------------------------

        glacier = load_glacier(GLACIER_ID)

        glacier = reproject_geometry(
            glacier,
            crs,
        )

        # --------------------------------------------------------------
        # Clip dataset.
        # --------------------------------------------------------------

        clipped = ds.rio.clip(
            glacier.geometry.values,
            glacier.crs,
            drop=True,
        )

        # --------------------------------------------------------------
        # Save.
        # --------------------------------------------------------------

        ITSLIVE_CLIPPED_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = (
            ITSLIVE_CLIPPED_DIRECTORY / path.name
        )

        clipped.to_netcdf(output_path)

        clipped.close()

    return output_path


def clip_all() -> list[Path]:
    """
    Clip every reduced ITS_LIVE dataset.

    Returns
    -------
    list[Path]
        Paths to the clipped datasets.
    """

    datasets = sorted(
        ITSLIVE_PROCESSED_DIRECTORY.glob("*.nc")
    )

    if not datasets:
        raise FileNotFoundError(
            "No reduced ITS_LIVE datasets found."
        )

    clipped_files: list[Path] = []

    for dataset in datasets:
        clipped_files.append(
            clip_granule(dataset)
        )

    return clipped_files


def main():

    clipped = clip_all()

    print("\nClipped datasets:\n")

    for dataset in clipped:
        print(dataset)


if __name__ == "__main__":
    main()