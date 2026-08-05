"""
Common geospatial utilities.

This module contains reusable helper functions for working with
coordinate reference systems (CRS) across the GLOFNet data pipelines.
"""

from geopandas import GeoDataFrame
from pyproj import CRS


import xarray as xr

def get_dataset_crs(ds: xr.Dataset) -> CRS:
    """
    Return the CRS of an xarray dataset.

    ITS_LIVE stores CRS information in the ``mapping`` variable rather
    than attaching it directly to the dataset. This helper extracts the
    EPSG code and returns it as a ``pyproj.CRS`` object.

    Parameters
    ----------
    ds : xarray.Dataset
        Open ITS_LIVE dataset.

    Returns
    -------
    pyproj.CRS
        Coordinate reference system of the dataset.

    Raises
    ------
    KeyError
        If the dataset does not contain a mapping variable or the EPSG
        code is missing.
    """

    if "mapping" not in ds:
        raise KeyError("Dataset does not contain a 'mapping' variable.")

    mapping = ds["mapping"]

    if "spatial_epsg" not in mapping.attrs:
        raise KeyError(
            "Dataset mapping variable does not contain 'spatial_epsg'."
        )

    epsg = int(mapping.attrs["spatial_epsg"])

    return CRS.from_epsg(epsg)

def reproject_geometry(
    geometry: GeoDataFrame,
    target_crs: CRS,
) -> GeoDataFrame:
    """
    Reproject a GeoDataFrame to the target CRS.

    Parameters
    ----------
    geometry : GeoDataFrame
        Input geometry.
    target_crs : pyproj.CRS
        Target coordinate reference system.

    Returns
    -------
    GeoDataFrame
        Reprojected geometry.
    """

    return geometry.to_crs(target_crs)