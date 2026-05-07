import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import urllib.request
import os
import zipfile

print("1. Loading the 2023 NYPD Crime Data...")
nypd_df = pd.read_csv('NYPD_2023_Crimes_Only.csv', usecols=['Latitude', 'Longitude'])
nypd_df = nypd_df.dropna()

print("Fixing the comma decimals...")
nypd_df['Longitude'] = nypd_df['Longitude'].astype(str).str.replace(',', '.').astype(float)
nypd_df['Latitude'] = nypd_df['Latitude'].astype(str).str.replace(',', '.').astype(float)

print(f"Loaded {len(nypd_df):,} crimes. Converting coordinates to map points...")
geometry = [Point(xy) for xy in zip(nypd_df['Longitude'], nypd_df['Latitude'])]
crimes_geo = gpd.GeoDataFrame(nypd_df, geometry=geometry, crs="EPSG:4326")

# ==========================================
# THE FINAL UNZIP FIX
# ==========================================
print("2. Downloading and extracting the NYC Taxi Zone map...")
taxi_zones_url = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zones.zip"
local_zip_path = "taxi_zones.zip"
extract_folder = "taxi_zones_extracted"

# Download the file if you haven't already
if not os.path.exists(local_zip_path):
    print("Downloading map file to your hard drive...")
    urllib.request.urlretrieve(taxi_zones_url, local_zip_path)

# Extract the zip file safely so GeoPandas can read it normally
if not os.path.exists(extract_folder):
    print("Extracting zip file...")
    with zipfile.ZipFile(local_zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)

# Now we point GeoPandas directly to the .shp file inside the extracted folder
shp_path = os.path.join(extract_folder, "taxi_zones", "taxi_zones.shp")
zones_geo = gpd.read_file(shp_path)
zones_geo = zones_geo.to_crs("EPSG:4326")
# ==========================================

print("3. Dropping the pins! (Performing the Spatial Join)...")
crimes_with_zones = gpd.sjoin(crimes_geo, zones_geo, how="inner", predicate='intersects')

print("4. Tallying the danger scores...")
zone_danger_scores = crimes_with_zones['LocationID'].value_counts().reset_index()
zone_danger_scores.columns = ['PULocationID', 'Total_Crimes']
zone_danger_scores['PULocationID'] = zone_danger_scores['PULocationID'].astype(int)

print("\nTop 5 Most Dangerous Taxi Zones in 2023:")
print(zone_danger_scores.head())

zone_danger_scores.to_csv('Zone_Danger_Scores.csv', index=False)
print("\nSuccess! Saved to 'Zone_Danger_Scores.csv'.")