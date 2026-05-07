import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("1. Loading Data...")
danger_df = pd.read_csv('Zone_Danger_Scores_Felonies.csv')
cols_to_load = ['payment_type', 'tip_amount', 'total_amount', 'DOLocationID']
taxi_df = pd.read_csv('2023_Yellow_Taxi_Trip_Data_20260415.csv', usecols=cols_to_load, low_memory=False)

print("2. Isolating the Extremes...")
# Sort zones by felonies
danger_df = danger_df.sort_values(by='Total_Felonies')

# Get the 10 safest and 10 most dangerous zones
safest_zones = danger_df.head(10).copy()
safest_zones['Category'] = 'Top 10 Safest Zones'

danger_zones = danger_df.tail(10).copy()
danger_zones['Category'] = 'Top 10 Most Dangerous Zones'

# Combine them into one tiny dataframe
extremes_df = pd.concat([safest_zones, danger_zones])
extremes_df.rename(columns={'PULocationID': 'DOLocationID'}, inplace=True)

print("3. Cleaning Taxi Data...")
for col in cols_to_load:
    taxi_df[col] = pd.to_numeric(taxi_df[col], errors='coerce')
taxi_df = taxi_df.dropna()

taxi_df = taxi_df[taxi_df['payment_type'] == 1] 
pre_tip_total = taxi_df['total_amount'] - taxi_df['tip_amount']
taxi_df = taxi_df[pre_tip_total > 0]
taxi_df['tip_percent'] = (taxi_df['tip_amount'] / pre_tip_total) * 100
taxi_df = taxi_df[taxi_df['tip_percent'] <= 100] 

print("4. Merging and Calculating Averages...")
# Merge ONLY the rides that ended in those 20 extreme zones
merged_df = pd.merge(taxi_df, extremes_df, on='DOLocationID', how='inner')

# Calculate the average tip for the Safe vs. Dangerous groups
extreme_tips = merged_df.groupby('Category', observed=True)['tip_percent'].mean().reset_index()

print("\n--- THE EXTREMES TEST RESULTS ---")
print(extreme_tips)
print("---------------------------------")

print("\n5. Generating Plot...")
plt.figure(figsize=(8, 6))
ax = sns.barplot(x='Category', y='tip_percent', data=extreme_tips, palette=['#C44E52', '#55A868'])

plt.title('The Extremes: Safest vs. Most Dangerous Drop-offs', fontsize=14, pad=15)
plt.ylabel('Average Tip Percentage (%)', fontsize=12)
plt.xlabel('')
plt.ylim(0, 25) 

for p in ax.patches:
    ax.annotate(f'{p.get_height():.2f}%', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='bottom', fontsize=14, fontweight='bold', xytext=(0, 5), textcoords='offset points')

plt.tight_layout()
plt.savefig('Extremes_Test_To.png', dpi=300)
plt.show()