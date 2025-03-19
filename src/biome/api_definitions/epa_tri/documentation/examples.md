# Examples

## Example 1: Open the TRI data file with index_col=False, since otherwise columns are shifted, and find data for Orange County, FL.
```
import pandas as pd

# Always the TRI csv with index_col=False param, since pandas is inferring the wrong index column and shifting the data without it
df = pd.read_csv('{DATASET_FILES_BASE_PATH}/epa-tri/EPA_TRI_Toxics_2014_2023.csv', dtype=str, index_col=False)

# Filter for any entries containing 'Orange' in the County column
# sample name without the county suffix, all uppercase and with correct spacing
# In general, check contains/case=False instead of exact matches
orange_county = df[df['County'].str.contains('ORANGE, FL', case=False, na=False)]

# Display results
print(f"Found {len(orange_county)} toxic release records containing 'ORANGE, FL' in the County name.")
print("\nSample of the data:")
print(orange_county.head())
```

## Example 2: Capture any asthma-respiratory related hazard incident from the TRI- EPA's Toxic Release Inventory data- you have access to this api. FOr now focus on problems in 2022, in the county of Harris, TX.


```
import pandas as pd

# Load the TRI data
tri_data = pd.read_csv('{DATASET_FILES_BASE_PATH}/epa-tri/EPA_TRI_Toxics_2014_2023.csv', index_col=False)

# Define respiratory/asthma related chemicals
# Updated to match the actual format in the dataset (with CAS numbers)
respiratory_chemicals = [
    'Ammonia (7664-41-7)',
    'Chlorine (7782-50-5)',
    'Sulfuric acid (7664-93-9)',
    'Hydrochloric acid (7647-01-0)',
    'Nitric acid (7697-37-2)',
    'Ozone',  # Keep checking if this has a CAS number format
    'Toluene (108-88-3)',
    'Benzene (71-43-2)',
    'Formaldehyde (50-00-0)',
    'Methanol (67-56-1)'
]

# Filter data for:
# - Year 2022
# - Harris County (case-insensitive match)
# - Respiratory chemicals
respiratory_incidents = tri_data[
    (tri_data['Year'] == 2022) &
    (tri_data['County'].str.upper() == 'HARRIS, TX') &
    (tri_data['Chemical'].isin(respiratory_chemicals))
]

# Convert 'Releases (lb)' to numeric, coercing errors to NaN since ascending= on sort_values messes with it
respiratory_incidents['Releases (lb)'] = pd.to_numeric(respiratory_incidents['Releases (lb)'], errors='coerce')

# Sort by release amount
respiratory_incidents = respiratory_incidents.sort_values('Releases (lb)', ascending=False)

# Select relevant columns
result = respiratory_incidents[[
    'TRI Facility Name',
    'Chemical',
    'Releases (lb)',
    'RSEI Hazard',
    'Latitude',
    'Longitude'
]]

result
```

## Example 3: When not finding results for a combined query, try a more systematic approach by finding items and counting length by one by one, in order to discover if there is matching data, but the query is not returning any results. This is to discover amonia references for the county of "HARRIS, TX".

```
import pandas as pd

# Load the data
tri_data = pd.read_csv('{DATASET_FILES_BASE_PATH}/epa-tri/EPA_TRI_Toxics_2014_2023.csv', index_col=False)

print("Sample of County values:")
print(tri_data['County'].unique()[:10])  # Print first 10 unique county values

print("\nSample of Chemical values containing 'Ammonia':")
ammonia_chemicals = [chem for chem in tri_data['Chemical'].unique() if 'Ammonia' in str(chem)]
print(ammonia_chemicals)

# Try a more flexible approach
print("\nTrying a more flexible filter:")
filtered_data = tri_data[
    tri_data['Chemical'].str.contains('Ammonia', case=False, na=False)
]

print(f"Found {len(filtered_data)} records for any Ammonia")

# Now try to find Harris county with a flexible approach
print("\nLooking for Harris county:")
harris_data = tri_data[
    tri_data['County'].str.contains('Harris', case=False, na=False)
]

print(f"Found {len(harris_data)} records for Harris county")
print("Sample county values in Harris results:")
print(harris_data['County'].unique())

# Now try the combined filter with the correct formats
print("\nTrying combined filter with formats from the dataset:")
final_filtered = tri_data[
    tri_data['County'].str.contains('Harris', case=False, na=False) &
    tri_data['Chemical'].str.contains('Ammonia', case=False, na=False)
]

print(f"Found {len(final_filtered)} records for Ammonia in Harris county")
if len(final_filtered) > 0:
    # Select relevant columns and sort by release amount
    result = final_filtered[['TRI Facility Name', 'Chemical', 'Releases (lb)', 'RSEI Hazard', 'Latitude', 'Longitude']]
    result['Releases (lb)'] = pd.to_numeric(result['Releases (lb)'], errors='coerce')
    result = result.sort_values('Releases (lb)', ascending=False)
    print("\nResults:")
    print(result.head())
```


## Example 4: Query to retrieve asthma-respiratory related hazard incidents from the EPA's TRI for the year 2022 in Harris County, TX.

```
import pandas as pd

# Load the TRI data
tri_data = pd.read_csv('/jupyter/data/epa-tri/EPA_TRI_Toxics_2014_2023.csv', index_col=False)

# List of respiratory-related chemicals
respiratory_chemicals = [
    'Ammonia',
    'Chlorine',
    'Sulfuric acid',
    'Hydrochloric acid',
    'Hydrogen fluoride',
    'Nitric acid',
    'Ozone',
    'Phosgene',
    'Toluene diisocyanate',
    'Methylene diphenyl diisocyanate'
]

# Filter the data
respiratory_incidents = tri_data[
    (tri_data['Year'] == 2022) &
    (tri_data['County'] == 'HARRIS, TX') &
    (tri_data['Chemical'].str.contains('|'.join(respiratory_chemicals), case=False, na=False))
]

# Sort by release amount
respiratory_incidents = respiratory_incidents.sort_values('Releases (lb)', ascending=False)

# Select relevant columns
result = respiratory_incidents[[
    'TRI Facility Name',
    'Chemical',
    'Releases (lb)',
    'RSEI Hazard'
]]

print(result)
```
