# Examples

## Example 1: Check the existing columns in the dataset to see if the screentime variable and which geo columns are included.

```
import pandas as pd

df_2023 = pd.read_sas("{DATASET_FILES_BASE_PATH}/census-nsch/2023e_topical.sas7bdat", format="sas7bdat")

existing_cols = df_2023.columns.tolist()
print(existing_cols)
```


## Example 2: Check the codebook columns head and available columns
```
import pandas as pd

# Read codebook with explicit parameters

# Ensure index_col=FALSE, if not first column values disappear and the whole dataframe is shifted!
codebook = pd.read_csv("{DATASET_FILES_BASE_PATH}/census-nsch/nsch_dictionary_codebook.csv", index_col=False)  
# Display the first few rows
print(codebook.head())

# and columns if needed
print(codebook.columns.tolist())
```

## Example 3: Query to retrieve health conditions reported in the National Survey of Children's Health, including ADHD, autism, and asthma.

```
import pandas as pd
import numpy as np

# Read the codebook
codebook = pd.read_csv("/jupyter/data/census-nsch/nsch_dictionary_codebook.csv", index_col=False)

# Read 2023 data 
df = pd.read_sas("/jupyter/data/census-nsch/2023e_topical.sas7bdat", format="sas7bdat")

# Find condition-related variables from codebook
conditions = codebook[
    (codebook['Variable'].str.contains('adhd|autism|asth', case=False, na=False)) &
    (codebook['Source'] == 'Topical')
][['Variable', 'Question', 'Response Code']]

# Get condition variables that exist in our dataset
condition_vars = [var for var in conditions['Variable'] if var in df.columns]

# Calculate prevalence for each condition
results = []
for var in condition_vars:
    condition_info = conditions[conditions['Variable'] == var].iloc[0]
    
    # Get counts and percentages
    counts = df[var].value_counts()
    total = counts.sum()
    percentages = (counts / total * 100).round(2)
    
    # Add to results
    results.append({
        'Condition': condition_info['Question'],
        'Total_Responses': total,
        'Yes_Count': counts.get(1, 0),  # Assuming 1 = Yes
        'Percentage': percentages.get(1, 0)
    })

# Create results dataframe
results_df = pd.DataFrame(results)
results_df = results_df.sort_values('Percentage', ascending=False)

print(results_df)
```
