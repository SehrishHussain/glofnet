from pathlib import Path

import matplotlib.pyplot as plt
import xarray as xr

from glofnet.common.find_glacier import load_glacier
from glofnet.common.geospatial import (
    get_dataset_crs,
    reproject_geometry,
)
from glofnet.common.paths import ITSLIVE_RAW_DIRECTORY
from glofnet.itslive.config import GLACIER_ID

path = next(ITSLIVE_RAW_DIRECTORY.glob("*.nc"))

ds = xr.open_dataset(path)

crs = get_dataset_crs(ds)

glacier = load_glacier(GLACIER_ID)
glacier = reproject_geometry(glacier, crs)
print("\nDataset bounds")
print(f"x: {float(ds.x.min()):.2f} -> {float(ds.x.max()):.2f}")
print(f"y: {float(ds.y.min()):.2f} -> {float(ds.y.max()):.2f}")

print("\nGlacier bounds")
minx, miny, maxx, maxy = glacier.total_bounds

print(f"x: {minx:.2f} -> {maxx:.2f}")
print(f"y: {miny:.2f} -> {maxy:.2f}")

fig, ax = plt.subplots(figsize=(10, 8))

ds["v"].isel(time=0).plot(
    ax=ax,
    cmap="viridis",
    robust=True,
)
ax.set_xlim(
    glacier.total_bounds[0] - 5000,
    glacier.total_bounds[2] + 5000,
)

ax.set_ylim(
    glacier.total_bounds[1] - 5000,
    glacier.total_bounds[3] + 5000,
)

glacier.boundary.plot(
    ax=ax,
    color="red",
    linewidth=2,
)

plt.title("ITS_LIVE velocity with Passu glacier")
plt.show()


ds.close()