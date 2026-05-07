import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("1. Loading Total Crimes Danger Scores...")
# Using the original All Crimes file
danger_df = pd.read_csv('Zone_Danger_Scores.csv')

print("2. Isolating the Extremes (Total Crimes)...")
danger_df = danger_df.sort_values(by='Total_Crimes')

safest_zones = danger_df.head(10).copy()
safest_zones['Category'] = 'Top 10 Safest Zones'

danger_zones = danger_df.tail(10).copy()
danger_zones['Category'] = 'Top 10 Most Dangerous Zones'

extremes_df_pu = pd.concat([safest_zones, danger_zones])
# Create a copy for Drop-offs and rename the ID column
extremes_df_do = extremes_df_pu.copy()
extremes_df_do.rename(columns={'PULocationID': 'DOLocationID'}, inplace=True)

print("3. Loading and Cleaning Taxi Data (This takes a moment)...")
# Loading BOTH pickup and drop-off columns so we only have to load the 5GB file once!
cols_to_load = ['payment_type', 'tip_amount', 'total_amount', 'PULocationID', 'DOLocationID']
taxi_df = pd.read_csv('2023_Yellow_Taxi_Trip_Data_20260415.csv', usecols=cols_to_load, low_memory=False)

for col in cols_to_load:
    taxi_df[col] = pd.to_numeric(taxi_df[col], errors='coerce')
taxi_df = taxi_df.dropna()

taxi_df = taxi_df[taxi_df['payment_type'] == 1] 
pre_tip_total = taxi_df['total_amount'] - taxi_df['tip_amount']
taxi_df = taxi_df[pre_tip_total > 0]
taxi_df['tip_percent'] = (taxi_df['tip_amount'] / pre_tip_total) * 100
taxi_df = taxi_df[taxi_df['tip_percent'] <= 100] 

print("\n4. Calculating Averages...")
# --- PICKUPS (FROM) ---
merged_pu = pd.merge(taxi_df, extremes_df_pu, on='PULocationID', how='inner')
extreme_tips_pu = merged_pu.groupby('Category', observed=True)['tip_percent'].mean().reset_index()
print("\n--- RESULTS: EXTREME PICKUPS (FROM) ---")
print(extreme_tips_pu)

# --- DROP-OFFS (TO) ---
merged_do = pd.merge(taxi_df, extremes_df_do, on='DOLocationID', how='inner')
extreme_tips_do = merged_do.groupby('Category', observed=True)['tip_percent'].mean().reset_index()
print("\n--- RESULTS: EXTREME DROP-OFFS (TO) ---")
print(extreme_tips_do)

print("\n5. Generating Side-by-Side Plot...")
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
palette_colors = ['#C44E52', '#55A868']

# Plot 1: Pickups
ax1 = sns.barplot(x='Category', y='tip_percent', data=extreme_tips_pu, palette=palette_colors, ax=axes[0])
axes[0].set_title('All Crimes: Safest vs. Most Dangerous Pickups', fontsize=14, pad=15)
axes[0].set_ylabel('Average Tip Percentage (%)', fontsize=12)
axes[0].set_xlabel('')
axes[0].set_ylim(0, 25)
for p in ax1.patches:
    ax1.annotate(f'{p.get_height():.2f}%', (p.get_x() + p.get_width() / 2., p.get_height()), 
                 ha='center', va='bottom', fontsize=12, fontweight='bold', xytext=(0, 5), textcoords='offset points')

# Plot 2: Drop-offs
ax2 = sns.barplot(x='Category', y='tip_percent', data=extreme_tips_do, palette=palette_colors, ax=axes[1])
axes[1].set_title('All Crimes: Safest vs. Most Dangerous Drop-offs', fontsize=14, pad=15)
axes[1].set_ylabel('')
axes[1].set_xlabel('')
axes[1].set_ylim(0, 25)
for p in ax2.patches:
    ax2.annotate(f'{p.get_height():.2f}%', (p.get_x() + p.get_width() / 2., p.get_height()), 
                 ha='center', va='bottom', fontsize=12, fontweight='bold', xytext=(0, 5), textcoords='offset points')

plt.tight_layout()
plt.savefig('Extremes_All_Crimes_Combined.png', dpi=300)
plt.show()

print("All Done! Check your folder for the combined plot.")