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