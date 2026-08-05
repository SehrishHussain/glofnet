"""
ITS_LIVE preprocessing pipeline.

This module orchestrates the preprocessing workflow for downloaded
ITS_LIVE velocity granules.

Workflow
--------
1. Reduce the dataset to the required variables.
2. Clip each dataset to the glacier boundary.
3. Apply quality masking.
"""

from glofnet.itslive.preprocess.reduce_variables import preprocess_all
from glofnet.itslive.preprocess.clip import clip_all

from glofnet.itslive.preprocess.quality_mask import quality_mask_all


def run_pipeline() -> None:
    """
    Execute the complete ITS_LIVE preprocessing pipeline.
    """

    print("=" * 70)
    print("ITS_LIVE PREPROCESSING PIPELINE")
    print("=" * 70)

    print("\n[1/3] Reducing variables...")
    reduced = preprocess_all()
    print(f"✓ Reduced {len(reduced)} dataset(s)")

    print("\n[2/3] Clipping to glacier...")
    clipped = clip_all()
    print(f"✓ Clipped {len(clipped)} dataset(s)")

    print("\n[3/3] Quality masking...")
    masked = quality_mask_all()
    print(f"✓ Quality masked {len(masked)} dataset(s)")

    print("\nPipeline completed successfully.")


def main():
    run_pipeline()


if __name__ == "__main__":
    main()