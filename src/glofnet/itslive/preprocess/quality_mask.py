"""
Apply quality masking to clipped ITS_LIVE datasets.

Workflow
--------
1. Open a clipped ITS_LIVE dataset.
2. Remove interpolated velocity pixels.
3. Preserve metadata.
4. Save the quality-controlled dataset.
"""

from pathlib import Path

import xarray as xr

from glofnet.common.paths import (
    ITSLIVE_CLIPPED_DIRECTORY,
    ITSLIVE_QUALITY_DIRECTORY,
)


VELOCITY_VARIABLES = [
    "vx",
    "vy",
    "v",
    "v_error",
]


def quality_mask_granule(path: Path) -> Path:
    """
    Apply quality masking to one clipped ITS_LIVE dataset.

    Parameters
    ----------
    path : Path
        Path to the clipped NetCDF dataset.

    Returns
    -------
    Path
        Path to the quality-controlled dataset.
    """

    with xr.open_dataset(path) as ds:

        # --------------------------------------------------------------
        # Keep only measured pixels.
        #
        # interp_mask == 0  -> measured
        # interp_mask == 1  -> interpolated
        # --------------------------------------------------------------

        valid_pixels = ds["interp_mask"] == 0

        masked = ds.copy()

        for variable in VELOCITY_VARIABLES:
            masked[variable] = ds[variable].where(valid_pixels)

        # --------------------------------------------------------------
        # Save.
        # --------------------------------------------------------------

        ITSLIVE_QUALITY_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = (
            ITSLIVE_QUALITY_DIRECTORY / path.name
        )

        masked.to_netcdf(output_path)

        masked.close()

    return output_path


def quality_mask_all() -> list[Path]:
    """
    Apply quality masking to every clipped ITS_LIVE dataset.

    Returns
    -------
    list[Path]
        Paths to the quality-controlled datasets.
    """

    datasets = sorted(
        ITSLIVE_CLIPPED_DIRECTORY.glob("*.nc")
    )

    if not datasets:
        raise FileNotFoundError(
            "No clipped ITS_LIVE datasets found."
        )

    outputs: list[Path] = []

    for dataset in datasets:
        outputs.append(
            quality_mask_granule(dataset)
        )

    return outputs


def main():

    outputs = quality_mask_all()

    print("\nQuality-controlled datasets:\n")

    for dataset in outputs:
        print(dataset)


if __name__ == "__main__":
    main()