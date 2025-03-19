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
