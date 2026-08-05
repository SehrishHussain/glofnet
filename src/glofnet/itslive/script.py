from pathlib import Path
import xarray as xr

path = next(Path("../data/raw/itslive").glob("*.nc"))

print(path.stat().st_size)

ds = xr.open_dataset(path)
print(ds)
ds.close()