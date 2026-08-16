from pathlib import Path

import duckdb


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
    print("ITS_LIVE RAW CSV - GLOBAL SPATIAL SUMMARY")
    print("=" * 70)

    print("\nCSV:")
    print(CSV_PATH)

    con = duckdb.connect()

    query = """
        SELECT
            MIN(lon) AS min_lon,
            MAX(lon) AS max_lon,
            MIN(lat) AS min_lat,
            MAX(lat) AS max_lat,

            COUNT(*) AS observations,

            COUNT(
                DISTINCT
                CONCAT(
                    CAST(lon AS VARCHAR),
                    '_',
                    CAST(lat AS VARCHAR)
                )
            ) AS locations,

            MIN(mid_date) AS earliest,
            MAX(mid_date) AS latest

        FROM read_csv_auto(
            ?,
            sample_size=1000
        )
    """

    result = con.execute(
        query,
        [str(CSV_PATH)],
    ).fetchone()

    print("\nSpatial extent:")
    print(f"Longitude: {result[0]} → {result[1]}")
    print(f"Latitude : {result[2]} → {result[3]}")

    print("\nObservations:")
    print(f"{result[4]:,}")

    print("\nUnique locations:")
    print(f"{result[5]:,}")

    print("\nTemporal extent:")
    print(f"Earliest: {result[6]}")
    print(f"Latest  : {result[7]}")


if __name__ == "__main__":
    main()