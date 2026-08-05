"""
Apply quality masking to clipped ITS_LIVE velocity datasets.

Workflow
--------
1. Open a clipped ITS_LIVE dataset.
2. Mask interpolated velocity pixels.
3. Preserve metadata.
4. Save the quality-controlled dataset.
"""

from pathlib import Path

import xarray as xr

from glofnet.common.paths import QUALITY_DIRECTORY, CLIPPED_DIRECTORY

QUALITY_DIRECTORY = QUALITY_DIRECTORY / "itslive"

CLIPPED_DIRECTORY = CLIPPED_DIRECTORY / "itslive"



def quality_mask_granule(path: Path) -> Path:
    """
    Apply quality masking to one clipped ITS_LIVE dataset.

    Parameters
    ----------
    path : Path
        Path to a clipped NetCDF dataset.

    Returns
    -------
    Path
        Path to the quality-controlled dataset.
    """

    ds = xr.open_dataset(path)

    # ------------------------------------------------------------
    # Mask interpolated pixels.
    #
    # interp_mask == 1  -> interpolated
    # interp_mask == 0  -> measured
    # ------------------------------------------------------------

    valid_pixels = ds["interp_mask"] == 0

    masked = ds.copy()

    for variable in ["vx", "vy", "v", "v_error"]:
        masked[variable] = ds[variable].where(valid_pixels)

    # ------------------------------------------------------------
    # Save.
    # ------------------------------------------------------------

    QUALITY_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = QUALITY_DIRECTORY / path.name

    masked.to_netcdf(output_path)

    masked.close()
    ds.close()

    return output_path


def quality_mask_all() -> list[Path]:
    """
    Apply quality masking to every clipped dataset.

    Returns
    -------
    list[Path]
        Paths to the quality-controlled datasets.
    """

    datasets = sorted(CLIPPED_DIRECTORY.glob("*.nc"))

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