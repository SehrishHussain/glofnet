# GLOFNet Reproduction

This project reproduces the data engineering pipeline described in the paper:

**GLOFNet: A Multimodal Dataset for GLOF Monitoring and Prediction**

## Current Progress

- ✅ Python environment configured
- ✅ Google Earth Engine authentication
- ✅ Randolph Glacier Inventory (RGI) integration
- ✅ Glacier lookup module implemented

## Planned Pipeline

1. Glacier identification
2. Sentinel-2 acquisition
3. ITS_LIVE acquisition
4. MODIS acquisition
5. Data preprocessing
6. Dataset harmonization
7. AI-ready dataset generation

## Tech Stack

- Python
- GeoPandas
- Google Earth Engine
- Shapely
- QGIS

# Running the Project

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.11 or later
- Git
- Google Earth Engine account
- Google Cloud Project with the Earth Engine API enabled
- Randolph Glacier Inventory (RGI v7.0)

---

## 1. Clone the Repository

Clone the repository and navigate to the project directory.

```bash
git clone https://github.com/<username>/<repository>.git
cd <repository>
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

Install all required Python packages.

```bash
pip install -r requirements.txt
```

If the project does not yet contain a `requirements.txt` file, generate one using:

```bash
pip freeze > requirements.txt
```

---

## 4. Authenticate Google Earth Engine

Authenticate your Google Earth Engine account.

```bash
earthengine authenticate
```

A browser window will open where you can sign in with your Google account.

---

## 5. Configure Google Earth Engine

Google Earth Engine now requires a Google Cloud Project.

### Create a Google Cloud Project

1. Go to the Google Cloud Console.
2. Create a new project (or use an existing one).
3. Enable the **Earth Engine API** for your project.
4. Register the project for Earth Engine use.

### Initialize Earth Engine

Update your initialization code to include your project ID.

```python
ee.Initialize(project="YOUR_PROJECT_ID")
```

Replace `YOUR_PROJECT_ID` with your Google Cloud Project ID.

---

## 6. Download the Randolph Glacier Inventory (RGI)

Download **RGI Version 7.0** and place the files in the following directory structure.

```
data/
└── reference/
    └── RGI/
        └── RGI2000-v7.0-G-14_south_asia_west/
            ├── RGI2000-v7.0-G-14_south_asia_west.shp
            ├── RGI2000-v7.0-G-14_south_asia_west.dbf
            ├── RGI2000-v7.0-G-14_south_asia_west.shx
            ├── RGI2000-v7.0-G-14_south_asia_west.prj
            └── ...
```

---

## 7. Configure the Project

Open:

```
src/glofnet/sentinel/config.py
```

Update the configuration values.

```python
GLACIER_ID = "RGI2000-v7.0-G-14-08488"

START_DATE = "2017-01-01"

END_DATE = "2024-12-31"

MAX_CLOUD_PERCENTAGE = 80
```

Modify these values according to the glacier and date range you wish to process.

---

## 8. Run the Pipeline

From the project root directory, run:

```bash
python -m glofnet.sentinel.download_sentinel
```

---

# Expected Output

After execution, the pipeline will:

- Load the glacier polygon from the RGI shapefile.
- Convert the glacier boundary into an Earth Engine geometry.
- Query Sentinel-2 imagery.
- Filter imagery by date and cloud coverage.
- Download Sentinel-2 GeoTIFF images.
- Save downloaded images in:

```
data/raw/sentinel/
```

- Generate an interactive visualization:

```
passu_map.html
```

The HTML map will automatically open in your default web browser.

---

# Project Structure

```
project/
│
├── data/
│   ├── raw/
│   │   └── sentinel/
│   └── reference/
│       └── RGI/
│
├── src/
│   └── glofnet/
│       ├── common/
│       └── sentinel/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Troubleshooting

## Earth Engine Authentication Error

If authentication expires or fails, run:

```bash
earthengine authenticate
```

---

## Earth Engine Project Error

If you encounter an error similar to:

```
Project XXXXX is not registered to use Earth Engine.
```

Verify that:

- Your Google Cloud Project has the Earth Engine API enabled.
- The project has been registered for Earth Engine access.
- You initialize Earth Engine using:

```python
ee.Initialize(project="YOUR_PROJECT_ID")
```

---

## ModuleNotFoundError

Always run the project from the repository root using:

```bash
python -m glofnet.sentinel.download_sentinel
```

Do **not** execute the script directly:

```bash
python download_sentinel.py
```

---

# Notes

- The project currently supports downloading Sentinel-2 imagery for glaciers contained in the Randolph Glacier Inventory (RGI).
- Images are clipped to the glacier boundary before being downloaded.
- The download pipeline supports downloading either the complete image collection or a limited number of images for testing using the `max_images` parameter.