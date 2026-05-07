import pandas as pd

print("1. Loading Data...")
danger_df = pd.read_csv('Zone_Danger_Scores_Felonies.csv')

# We only need the Pickup Location ID to count the rides!
taxi_df = pd.read_csv('2023_Yellow_Taxi_Trip_Data_20260415.csv', usecols=['PULocationID'], low_memory=False)

print("2. Isolating the Extremes...")
# Sort zones by felonies
danger_df = danger_df.sort_values(by='Total_Felonies')

# Get the 10 safest and 10 most dangerous zones
safest_zones = danger_df.head(10).copy()
safest_zones['Category'] = 'Top 10 Safest Zones'

danger_zones = danger_df.tail(10).copy()
danger_zones['Category'] = 'Top 10 Most Dangerous Zones'

extremes_df = pd.concat([safest_zones, danger_zones])

print("3. Merging and Counting Rides...")
# Match the taxi rides to our 20 extreme zones
merged_df = pd.merge(taxi_df, extremes_df, on='PULocationID', how='inner')

# Count how many total rides happened in each category
ride_counts = merged_df['Category'].value_counts()

print("\n--- SAMPLE SIZE CHECK ---")
# Formatting with commas so the big numbers are easy to read
for category, count in ride_counts.items():
    print(f"{category}: {count:,} rides")
print("-------------------------")