#import xarray as xr
#import rioxarray
#from pathlib import Path
#import xarray as xr

# ds = xr.open_dataset("data/raw/itslive/S1A_IW_SLC__1SSV_20241230T130605_20241230T130626_057222_0709C1_50D2_X_S1A_IW_SLC__1SSV_20250111T130604_20250111T130625_057397_0710AB_0B76_G0120V02_P095.nc")
#path = next(Path("data/processed/itslive").glob("*.nc"))

#print(path)

#ds = xr.open_dataset(path)

#print(ds.data_vars)
#print(ds.data_vars)
from pathlib import Path
import xarray as xr

path = next(Path("data/clipped/itslive").glob("*.nc"))

ds = xr.open_dataset(path)

print(ds)
print(ds.sizes)