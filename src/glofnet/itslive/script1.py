import pandas as pd

csv_path = "data/raw/itslive/velocity_data_raw/df_raw.csv"


df = pd.read_csv(csv_path)

print(df.columns.tolist())
print(df.head())
print(df.shape)

print("\nLongitude:")
print(df["lon"].min(), df["lon"].max())

print("\nLatitude:")
print(df["lat"].min(), df["lat"].max())