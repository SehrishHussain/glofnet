from datetime import date

import itslive


bbox = [-25, 64, -19, 67]

print("Searching known ITS_LIVE granule area...")

results = itslive.velocity_pairs.find(
    bbox=bbox,
    engine="duckdb",
    partition_type="h3",
    resolution=2,
)

print(f"Found {len(results)} pairs")

for url in results[:10]:
    print(url)