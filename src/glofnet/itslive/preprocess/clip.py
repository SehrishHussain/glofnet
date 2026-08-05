"""
Clip reduced ITS_LIVE velocity datasets to the glacier geometry.

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

from glofnet.common.paths import (
    ITSLIVE_PROCESSED_DIRECTORY,
    ITSLIVE_CLIPPED_DIRECTORY,
)

import rioxarray  # noqa: F401
import xarray as xr

from glofnet.common.find_glacier import load_glacier
from glofnet.common.geospatial import (
    get_dataset_crs,
    reproject_geometry,
)
from glofnet.itslive.config import GLACIER_ID







def clip_granule(path: Path) -> Path:
    
    """
    Clip one reduced ITS_LIVE dataset to the glacier polygon.

    Parameters
    ----------
    path : Path
        Path to the reduced NetCDF file.

    Returns
    -------
    Path
        Path to the clipped NetCDF file.
    """

    ds = xr.open_dataset(path)
    #ds = xr.open_dataset(path)

    
    #print("Variables:", list(ds.data_vars))

    # ------------------------------------------------------------------
    # Read CRS from the dataset mapping variable.
    # ------------------------------------------------------------------

    crs = get_dataset_crs(ds)

    ds = ds.rio.write_crs(crs)

    #print("Dataset CRS:", ds.rio.crs)
    

    # ------------------------------------------------------------------
    # Load glacier geometry.
    # ------------------------------------------------------------------

    glacier = load_glacier(GLACIER_ID)

    glacier = reproject_geometry(glacier, crs)
    # print("Glacier CRS:", glacier.crs)

    # ------------------------------------------------------------------
    # Clip.
    # ------------------------------------------------------------------

    clipped = ds.rio.clip(
        glacier.geometry.values,
        glacier.crs,
        drop=True,
    )

    # ------------------------------------------------------------------
    # Save.
    # ------------------------------------------------------------------

    ITSLIVE_CLIPPED_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)

    output_path = ITSLIVE_CLIPPED_DIRECTORY / path.name

    clipped.to_netcdf(output_path)

    clipped.close()
    ds.close()

    return output_path


def clip_all() -> list[Path]:
    """
    Clip every reduced ITS_LIVE dataset.

    Returns
    -------
    list[Path]
        Paths to the clipped datasets.
    """
    print("Processed directory:", ITSLIVE_PROCESSED_DIRECTORY)
    print("Exists:", ITSLIVE_PROCESSED_DIRECTORY.exists())
    print("Files:", list(ITSLIVE_PROCESSED_DIRECTORY.glob("*.nc")))
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