import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os

print("1. Loading the Taxi Zone Map...")
extract_folder = "taxi_zones_extracted"
shp_path = os.path.join(extract_folder, "taxi_zones", "taxi_zones.shp")
zones_geo = gpd.read_file(shp_path)

print("2. Loading the Felonies Danger Scores...")
danger_df = pd.read_csv('Zone_Danger_Scores_Felonies.csv')

# Ensure the columns match for the merge
danger_df.rename(columns={'PULocationID': 'LocationID'}, inplace=True)
danger_df['LocationID'] = danger_df['LocationID'].astype(int)
zones_geo['LocationID'] = zones_geo['LocationID'].astype(int)

print("3. Merging the Map with the Danger Scores...")
map_df = zones_geo.merge(danger_df, on='LocationID', how='left')

# Fill empty zones with 0 felonies
map_df['Total_Felonies'] = map_df['Total_Felonies'].fillna(0)

print("4. Generating the Heatmap...")
fig, ax = plt.subplots(1, 1, figsize=(12, 12))

# Plot the map, coloring by Total_Felonies
map_df.plot(column='Total_Felonies', 
            cmap='OrRd', 
            linewidth=0.5, 
            ax=ax, 
            edgecolor='0.8', 
            legend=True,
            legend_kwds={'label': "Total Felonies (2023)",
                         'orientation': "vertical",
                         'shrink': 0.7})

ax.set_title('Visual Proof: 2023 NYC Felonies by Taxi Zone', fontsize=16, fontweight='bold', pad=20)
ax.axis('off')

plt.tight_layout()
plt.savefig('Map_Visual_Check.png', dpi=300)
plt.show()

print("Check the map! Does it look accurate?")