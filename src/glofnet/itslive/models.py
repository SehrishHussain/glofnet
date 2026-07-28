from dataclasses import dataclass


@dataclass(frozen=True)
class CubeInfo:
    """
    Metadata describing one ITS_LIVE velocity cube.
    """

    id: str
    zarr_url: str
    epsg: int
    bbox: tuple[float, float, float, float]
    start_datetime: str
    end_datetime: str
    granule_count: int