import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("1. Loading the Danger Scores...")
danger_df = pd.read_csv('Zone_Danger_Scores.csv')

# Divide the neighborhoods into 3 equal buckets based on crime volume
danger_df['Danger_Level'] = pd.qcut(danger_df['Total_Crimes'], q=3, labels=['Low Crime', 'Medium Crime', 'High Crime'])

print("2. Loading the 5GB Taxi Data (Memory Efficient Mode)...")
cols_to_load = ['payment_type', 'tip_amount', 'total_amount', 'PULocationID']
taxi_df = pd.read_csv('2023_Yellow_Taxi_Trip_Data_20260415.csv', usecols=cols_to_load, low_memory=False)

print("3. Cleaning Taxi Data & Calculating Tips...")
# Force numeric data types
for col in cols_to_load:
    taxi_df[col] = pd.to_numeric(taxi_df[col], errors='coerce')
taxi_df = taxi_df.dropna()

# Keep only Credit Card payments
taxi_df = taxi_df[taxi_df['payment_type'] == 1] 

# Calculate the precise tip percentage
pre_tip_total = taxi_df['total_amount'] - taxi_df['tip_amount']
taxi_df = taxi_df[pre_tip_total > 0]
taxi_df['tip_percent'] = (taxi_df['tip_amount'] / pre_tip_total) * 100

# Remove crazy outliers (e.g., people tipping over 100% by accident)
taxi_df = taxi_df[taxi_df['tip_percent'] <= 100] 

print("4. Merging the Datasets...")
# Match every single taxi ride to the Danger Level of its pickup location
merged_df = pd.merge(taxi_df, danger_df, on='PULocationID', how='inner')

print("5. Calculating the 'Danger Tip'...")
# Group by our 3 Danger Levels and find the exact average tip for each
danger_tips = merged_df.groupby('Danger_Level', observed=True)['tip_percent'].mean().reset_index()
print("\n--- RESULTS ---")
print(danger_tips)
print("---------------")

print("\n6. Generating the Final Plot...")
plt.figure(figsize=(8, 6))

# Plot the 3 bars using a green -> orange -> red color palette
ax = sns.barplot(x='Danger_Level', y='tip_percent', data=danger_tips, palette=['#55A868', '#F1A340', '#C44E52'])

plt.title('Do New Yorkers Tip More in High-Crime Areas?', fontsize=14, pad=15)
plt.xlabel('Pickup Neighborhood Danger Level', fontsize=12)
plt.ylabel('Average Tip Percentage (%)', fontsize=12)

# Lock the y-axis to 25 so differences are visible but not exaggerated
plt.ylim(0, 25) 

# Add the exact percentages on top of the bars
for p in ax.patches:
    ax.annotate(f'{p.get_height():.2f}%', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='bottom', fontsize=12, fontweight='bold', xytext=(0, 5), textcoords='offset points')

plt.tight_layout()
plt.savefig('Final_Danger_Tip_Plot.png', dpi=300)
plt.show()

print("All Done! Check your folder for the final plot.")