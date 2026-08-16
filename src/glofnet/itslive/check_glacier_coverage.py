from pathlib import Path

import duckdb

from glofnet.common.find_glacier import load_glacier
from glofnet.itslive.config import GLACIER_ID


CSV_PATH = (
    Path(__file__).resolve().parents[3]
    / "data"
    / "raw"
    / "itslive"
    / "velocity_data_raw"
    / "df_raw.csv"
)


def main():

    print("=" * 70)
    print("ITS_LIVE - GLACIER VELOCITY SPATIAL DIAGNOSTIC")
    print("=" * 70)

    # ------------------------------------------------------------
    # Load glacier
    # ------------------------------------------------------------

    glacier = load_glacier(GLACIER_ID)
    geometry = glacier.geometry.iloc[0]

    min_lon, min_lat, max_lon, max_lat = geometry.bounds

    centroid = geometry.centroid

    print("\nGlacier:")
    print(GLACIER_ID)

    print("\nGlacier bbox:")
    print(
        f"{min_lon:.6f}, "
        f"{min_lat:.6f}, "
        f"{max_lon:.6f}, "
        f"{max_lat:.6f}"
    )

    print("\nGlacier centroid:")
    print(
        f"{centroid.x:.6f}, "
        f"{centroid.y:.6f}"
    )

    # ------------------------------------------------------------
    # Open CSV
    # ------------------------------------------------------------

    con = duckdb.connect()

    print("\nCSV:")
    print(CSV_PATH)

    if not CSV_PATH.exists():
        raise FileNotFoundError(CSV_PATH)

    # ------------------------------------------------------------
    # 1. Check exact glacier bbox
    # ------------------------------------------------------------

    print("\n" + "=" * 70)
    print("TEST 1 - EXACT GLACIER BBOX")
    print("=" * 70)

    query = """
        SELECT
            COUNT(*) AS observations,
            COUNT(DISTINCT
                CONCAT(
                    CAST(lon AS VARCHAR),
                    '_',
                    CAST(lat AS VARCHAR)
                )
            ) AS locations
        FROM read_csv_auto(
            ?,
            sample_size=1000
        )
        WHERE
            lon BETWEEN ? AND ?
            AND lat BETWEEN ? AND ?
    """

    result = con.execute(
        query,
        [
            str(CSV_PATH),
            min_lon,
            max_lon,
            min_lat,
            max_lat,
        ],
    ).fetchone()

    print("Observations:", f"{result[0]:,}")
    print("Locations   :", f"{result[1]:,}")

    # ------------------------------------------------------------
    # 2. Expanded bbox
    # ------------------------------------------------------------

    margin = 0.10

    expanded_min_lon = min_lon - margin
    expanded_max_lon = max_lon + margin
    expanded_min_lat = min_lat - margin
    expanded_max_lat = max_lat + margin

    print("\n" + "=" * 70)
    print("TEST 2 - EXPANDED BBOX")
    print("=" * 70)

    print(
        f"Longitude: "
        f"{expanded_min_lon:.6f} → "
        f"{expanded_max_lon:.6f}"
    )

    print(
        f"Latitude : "
        f"{expanded_min_lat:.6f} → "
        f"{expanded_max_lat:.6f}"
    )

    query = """
        SELECT
            COUNT(*) AS observations,
            COUNT(DISTINCT
                CONCAT(
                    CAST(lon AS VARCHAR),
                    '_',
                    CAST(lat AS VARCHAR)
                )
            ) AS locations
        FROM read_csv_auto(
            ?,
            sample_size=1000
        )
        WHERE
            lon BETWEEN ? AND ?
            AND lat BETWEEN ? AND ?
    """

    result = con.execute(
        query,
        [
            str(CSV_PATH),
            expanded_min_lon,
            expanded_max_lon,
            expanded_min_lat,
            expanded_max_lat,
        ],
    ).fetchone()

    print("\nObservations:", f"{result[0]:,}")
    print("Locations   :", f"{result[1]:,}")

    # ------------------------------------------------------------
    # 3. Spatial extent of velocity locations
    # ------------------------------------------------------------

    print("\n" + "=" * 70)
    print("TEST 3 - VELOCITY POINT EXTENT")
    print("=" * 70)

    query = """
        SELECT
            MIN(lon),
            MAX(lon),
            MIN(lat),
            MAX(lat),
            COUNT(DISTINCT
                CONCAT(
                    CAST(lon AS VARCHAR),
                    '_',
                    CAST(lat AS VARCHAR)
                )
            )
        FROM read_csv_auto(
            ?,
            sample_size=1000
        )
        WHERE
            lon BETWEEN ? AND ?
            AND lat BETWEEN ? AND ?
    """

    result = con.execute(
        query,
        [
            str(CSV_PATH),
            expanded_min_lon,
            expanded_max_lon,
            expanded_min_lat,
            expanded_max_lat,
        ],
    ).fetchone()

    print("\nVelocity locations:")
    print(f"Longitude: {result[0]:.6f} → {result[1]:.6f}")
    print(f"Latitude : {result[2]:.6f} → {result[3]:.6f}")
    print(f"Unique locations: {result[4]:,}")

    # ------------------------------------------------------------
    # 4. Find nearest velocity locations to glacier centroid
    # ------------------------------------------------------------

    print("\n" + "=" * 70)
    print("TEST 4 - NEAREST VELOCITY LOCATIONS")
    print("=" * 70)

    query = """
        SELECT
            lon,
            lat,
            SQRT(
                POWER(lon - ?, 2)
                +
                POWER(lat - ?, 2)
            ) AS distance_degrees
        FROM (
            SELECT DISTINCT
                lon,
                lat
            FROM read_csv_auto(
                ?,
                sample_size=1000
            )
            WHERE
                lon BETWEEN ? AND ?
                AND lat BETWEEN ? AND ?
        )
        ORDER BY distance_degrees
        LIMIT 20
    """

    rows = con.execute(
        query,
        [
            centroid.x,
            centroid.y,
            str(CSV_PATH),
            expanded_min_lon,
            expanded_max_lon,
            expanded_min_lat,
            expanded_max_lat,
        ],
    ).fetchall()

    print("\nNearest locations:")
    print("-" * 70)

    for lon, lat, distance in rows:
        print(
            f"lon={lon:.6f}, "
            f"lat={lat:.6f}, "
            f"distance={distance:.6f} degrees"
        )


if __name__ == "__main__":
    main()