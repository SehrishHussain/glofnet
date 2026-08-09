"""
ITS_LIVE preprocessing pipeline.

This module orchestrates preprocessing of a single ITS_LIVE
velocity granule.

Workflow
--------
1. Reduce the dataset to the required variables.
2. Clip the dataset to the glacier boundary.
3. Apply quality masking.
"""

from pathlib import Path

from glofnet.itslive.preprocess.clip import clip_granule
from glofnet.itslive.preprocess.quality_mask import quality_mask_granule
from glofnet.itslive.preprocess.reduce_variables import preprocess_granule


def run_pipeline(raw_granule: Path) -> Path:
    """
    Execute the ITS_LIVE preprocessing pipeline.

    Parameters
    ----------
    raw_granule : Path
        Path to the raw ITS_LIVE NetCDF file.

    Returns
    -------
    Path
        Path to the final quality-controlled dataset.
    """

    print("=" * 70)
    print("ITS_LIVE PREPROCESSING PIPELINE")
    print("=" * 70)

    # --------------------------------------------------------------
    # Reduce variables
    # --------------------------------------------------------------

    print("\n[1/3] Reducing variables...")

    reduced = preprocess_granule(raw_granule)

    print(f"✓ Reduced dataset:")
    print(reduced)

    # --------------------------------------------------------------
    # Clip to glacier
    # --------------------------------------------------------------

    print("\n[2/3] Clipping to glacier...")

    clipped = clip_granule(reduced)

    print(f"✓ Clipped dataset:")
    print(clipped)

    # --------------------------------------------------------------
    # Apply quality mask
    # --------------------------------------------------------------

    print("\n[3/3] Applying quality mask...")

    masked = quality_mask_granule(clipped)

    print(f"✓ Quality-controlled dataset:")
    print(masked)

    print("\nPipeline completed successfully.")

    return masked


def main():
    raise RuntimeError(
        "This module processes a single dataset. "
        "Run it from glofnet.itslive.pipeline instead."
    )


if __name__ == "__main__":
    main()