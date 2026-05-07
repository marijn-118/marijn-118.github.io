import pandas as pd

# The massive file you just downloaded
input_file = 'NYPD_Complaint_Data_Historic_20260421.csv' 
# The new, tiny file we are going to create
output_file = 'NYPD_2023_Crimes_Only.csv'

# We only load the 4 columns we actually care about to save memory
columns_to_keep = ['CMPLNT_FR_DT', 'LAW_CAT_CD', 'Latitude', 'Longitude']

print("Sifting through 9.5 million rows. This might take 3-5 minutes...")

first_chunk = True
total_2023_crimes = 0

# chunksize=100000 means we load 100,000 rows at a time, process them, and forget them!
for chunk in pd.read_csv(input_file, usecols=columns_to_keep, chunksize=100000, low_memory=False):
    
    # Drop rows where the date is missing
    chunk = chunk.dropna(subset=['CMPLNT_FR_DT'])
    
    # Fast filtering: Keep only rows where the date string contains '2023'
    chunk_2023 = chunk[chunk['CMPLNT_FR_DT'].str.contains('2023', na=False)]
    
    if not chunk_2023.empty:
        total_2023_crimes += len(chunk_2023)
        
        # If it's the first chunk, create the file and write the headers
        if first_chunk:
            chunk_2023.to_csv(output_file, index=False)
            first_chunk = False
        # Otherwise, just append the new data to the bottom of the file
        else:
            chunk_2023.to_csv(output_file, mode='a', header=False, index=False)

print(f"\nDone! We extracted {total_2023_crimes:,} crimes from 2023.")
print(f"They are safely saved in '{output_file}'. You can now delete the massive 5GB file if you want!")