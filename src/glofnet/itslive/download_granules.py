"""
Download ITS_LIVE velocity granules.
"""

from pathlib import Path

import requests

from glofnet.itslive.config import OUTPUT_DIRECTORY
from glofnet.itslive.search_granules import search_granules


def download_granule(granule):

    output_dir = Path(OUTPUT_DIRECTORY)
    output_dir.mkdir(parents=True, exist_ok=True)

    destination = output_dir / granule.filename

    if destination.exists():
        print(f"Already exists: {destination.name}")
        return destination

    print(f"Downloading {granule.filename}")

    response = requests.get(granule.url, stream=True)
    response.raise_for_status()

    with open(destination, "wb") as file:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            if chunk:
                file.write(chunk)

    print("Finished.")

    return destination


def main():

    granule = search_granules()[0]

    download_granule(granule)


if __name__ == "__main__":
    main()