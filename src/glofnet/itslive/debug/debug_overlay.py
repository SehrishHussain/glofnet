from pathlib import Path

import matplotlib.pyplot as plt
import rioxarray  # noqa: F401
import xarray as xr

from glofnet.common.find_glacier import load_glacier
from glofnet.common.geospatial import (
    get_dataset_crs,
    reproject_geometry,
)
from glofnet.common.paths import ITSLIVE_RAW_DIRECTORY
from glofnet.itslive.config import GLACIER_ID


# ---------------------------------------------------------------------
# Load raw ITS_LIVE dataset
# ---------------------------------------------------------------------

path = next(ITSLIVE_RAW_DIRECTORY.glob("*.nc"))

ds = xr.open_dataset(path)

crs = get_dataset_crs(ds)
ds = ds.rio.write_crs(crs)


# ---------------------------------------------------------------------
# Load glacier
# ---------------------------------------------------------------------

glacier = load_glacier(GLACIER_ID)
glacier = reproject_geometry(glacier, crs)

centroid = glacier.geometry.iloc[0].centroid


# ---------------------------------------------------------------------
# Debug information
# ---------------------------------------------------------------------

print("=" * 70)
print("GLACIER")
print("=" * 70)

print("\nNumber of features")
print(len(glacier))

print("\nGeometry types")
print(glacier.geometry.geom_type.value_counts())

geometry = glacier.geometry.iloc[0]

print("\nGeometry summary")
print(f"Type      : {geometry.geom_type}")
print(f"Area      : {geometry.area:.2f} m²")
print(f"Perimeter : {geometry.length:.2f} m")

print("\nGlacier bounds")
print(glacier.total_bounds)

print("\nCentroid")
print(f"X: {centroid.x:.2f}")
print(f"Y: {centroid.y:.2f}")


print("\n" + "=" * 70)
print("RASTER")
print("=" * 70)

print("\nCRS")
print(ds.rio.crs)

print("\nDataset bounds")
print(ds.rio.bounds())

print("\nRaster X range")
print(f"{float(ds.x.min()):.2f} -> {float(ds.x.max()):.2f}")

print("\nRaster Y range")
print(f"{float(ds.y.min()):.2f} -> {float(ds.y.max()):.2f}")

print("\nDataset dimensions")
print(dict(ds.sizes))

print("\nVariables")
print(list(ds.data_vars))


# ---------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------

fig, ax = plt.subplots(figsize=(8, 8))

ds["v"].isel(time=0).plot(
    ax=ax,
    cmap="viridis",
    robust=True,
)

glacier.boundary.plot(
    ax=ax,
    edgecolor="red",
    linewidth=2,
)

ax.scatter(
    centroid.x,
    centroid.y,
    color="yellow",
    edgecolors="black",
    linewidths=2,
    marker="*",
    s=300,
    zorder=100,
    label="Centroid",
)

xmin, ymin, xmax, ymax = glacier.total_bounds

pad = 2000  # metres

ax.set_xlim(xmin - pad, xmax + pad)
ax.set_ylim(ymin - pad, ymax + pad)

ax.set_aspect("equal")

ax.set_title("Passu Glacier on Raw ITS_LIVE Velocity")
ax.legend(loc="upper right")

plt.tight_layout()
plt.show()

ds.close()