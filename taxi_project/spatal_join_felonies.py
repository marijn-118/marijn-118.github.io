import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import urllib.request
import os
import zipfile

print("1. Loading the 2023 NYPD Crime Data...")
# Notice we are now loading the LAW_CAT_CD column too!
nypd_df = pd.read_csv('NYPD_2023_Crimes_Only.csv', usecols=['Latitude', 'Longitude', 'LAW_CAT_CD'])
nypd_df = nypd_df.dropna()

print(f"Total crimes loaded: {len(nypd_df):,}")

# ==========================================
# THE NEXT-LEVEL FILTER
# ==========================================
print("Filtering for FELONIES only (True Danger)...")
# We make sure the text is uppercase and has no weird spaces, just in case
nypd_df['LAW_CAT_CD'] = nypd_df['LAW_CAT_CD'].astype(str).str.strip().str.upper()
nypd_df = nypd_df[nypd_df['LAW_CAT_CD'] == 'FELONY']

print(f"Severe crimes (Felonies) remaining: {len(nypd_df):,}")
# ==========================================

print("Fixing the comma decimals...")
nypd_df['Longitude'] = nypd_df['Longitude'].astype(str).str.replace(',', '.').astype(float)
nypd_df['Latitude'] = nypd_df['Latitude'].astype(str).str.replace(',', '.').astype(float)

print("Converting coordinates to map points...")
geometry = [Point(xy) for xy in zip(nypd_df['Longitude'], nypd_df['Latitude'])]
crimes_geo = gpd.GeoDataFrame(nypd_df, geometry=geometry, crs="EPSG:4326")

print("2. Loading the extracted NYC Taxi Zone map...")
# Since you already downloaded and extracted it last time, we can skip downloading!
extract_folder = "taxi_zones_extracted"
shp_path = os.path.join(extract_folder, "taxi_zones", "taxi_zones.shp")

zones_geo = gpd.read_file(shp_path)
zones_geo = zones_geo.to_crs("EPSG:4326")

print("3. Dropping the pins! (Performing the Spatial Join)...")
crimes_with_zones = gpd.sjoin(crimes_geo, zones_geo, how="inner", predicate='intersects')

print("4. Tallying the new TRUE danger scores...")
zone_danger_scores = crimes_with_zones['LocationID'].value_counts().reset_index()
zone_danger_scores.columns = ['PULocationID', 'Total_Felonies']
zone_danger_scores['PULocationID'] = zone_danger_scores['PULocationID'].astype(int)

print("\nTop 5 Most Dangerous Taxi Zones (Felonies Only):")
print(zone_danger_scores.head())

zone_danger_scores.to_csv('Zone_Danger_Scores_Felonies.csv', index=False)
print("\nSuccess! Saved to 'Zone_Danger_Scores_Felonies.csv'.")