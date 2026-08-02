"""
Data models used by the ITS_LIVE pipeline.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GranuleInfo:
    """
    Metadata describing an ITS_LIVE velocity granule.
    """

    id: str

    url: str

    bbox: tuple[float, float, float, float]

    datetime: str | None
    start_datetime: str | None
    end_datetime: str | None

    platform: str | None
    projection: str | None
    percent_valid_pixels: float | None
    version: str | None
    scene_1_id: str | None
    scene_2_id: str | None

    @property
    def filename(self) -> str:
        """Filename of the NetCDF granule."""
        return Path(self.url).name

    @property
    def mission(self) -> str:
        """Return the satellite mission."""
        if self.platform is None:
            return "Unknown"

        if self.platform.startswith("S1"):
            return "Sentinel-1"

        if self.platform.startswith("S2"):
            return "Sentinel-2"

        return "Unknown"