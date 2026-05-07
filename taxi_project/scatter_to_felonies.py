import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("1. Loading the TRUE Danger Scores (Felonies Only)...")
danger_df = pd.read_csv('Zone_Danger_Scores_Felonies.csv')

print("2. Loading the Taxi Data...")
# Load DOLocationID instead of PULocationID
cols_to_load = ['payment_type', 'tip_amount', 'total_amount', 'DOLocationID']
taxi_df = pd.read_csv('2023_Yellow_Taxi_Trip_Data_20260415.csv', usecols=cols_to_load, low_memory=False)

print("3. Cleaning Taxi Data & Calculating Tips...")
for col in cols_to_load:
    taxi_df[col] = pd.to_numeric(taxi_df[col], errors='coerce')
taxi_df = taxi_df.dropna()

taxi_df = taxi_df[taxi_df['payment_type'] == 1] 

pre_tip_total = taxi_df['total_amount'] - taxi_df['tip_amount']
taxi_df = taxi_df[pre_tip_total > 0]
taxi_df['tip_percent'] = (taxi_df['tip_amount'] / pre_tip_total) * 100

taxi_df = taxi_df[taxi_df['tip_percent'] <= 100] 

print("4. Calculating Average Tip per Neighborhood...")
# Group by DOLocationID
zone_tips = taxi_df.groupby('DOLocationID')['tip_percent'].mean().reset_index()

print("5. Merging TRUE Danger Scores with Tip Averages...")
# Rename the danger column so it matches Drop-off location
danger_df.rename(columns={'PULocationID': 'DOLocationID'}, inplace=True)
merged_df = pd.merge(zone_tips, danger_df, on='DOLocationID', how='inner')

print("6. Generating Scatter Plot and Trendline...")
plt.figure(figsize=(10, 6))

sns.regplot(
    data=merged_df, 
    x='Total_Felonies', 
    y='tip_percent', 
    scatter_kws={'alpha':0.6, 'color': '#4C72B0'}, 
    line_kws={'color': '#C44E52', 'linewidth': 2}
)

plt.title('Correlation: TRUE Danger (Felonies) vs. Average Tip % (Drop-offs)', fontsize=14, pad=15)
plt.xlabel('Total Felonies in Drop-off Zone (2023)', fontsize=12)
plt.ylabel('Average Tip Percentage (%)', fontsize=12)

correlation = merged_df['Total_Felonies'].corr(merged_df['tip_percent'])
plt.annotate(f'Correlation (r): {correlation:.3f}', 
             xy=(0.05, 0.95), xycoords='axes fraction', 
             fontsize=12, fontweight='bold', 
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", lw=1))

plt.tight_layout()
plt.savefig('Scatter_TRUE_Danger_Tip_Dropoffs.png', dpi=300)
plt.show()

print(f"All Done! The new correlation coefficient is {correlation:.3f}.")