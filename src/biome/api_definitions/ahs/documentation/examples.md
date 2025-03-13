
## Example 1: Use the codebook to get the meaning of the codes for the OMB13CBSA variable, by first finding the row in the codebook for that variable.

```
import pandas as pd

# Read codebook to get metro area meanings
# ensure to set index_col=False, since the codebook has no index column
codebook = pd.read_csv('/jupyter/data/census-ahs-2021/codebook.csv', dtype=str, index_col=False)

# Find the row for OMB13CBSA
ombs_row = codebook[codebook['Variable'] == 'OMB13CBSA']

# Return the Response Codes column
ombs_row['Response Codes']
```

## Example 2: Use the codebook to get the meaning of the codes for the OMB13CBSA variable, matching one code to the meaning by creating a dictionary of code:meaning pairs and returning the statistical metro area name for a given code.

```
import pandas as pd

def get_code_name(code):
    # Read codebook to get metro area meanings
    # ensure to set index_col=False, since the codebook has no index column
    codebook = pd.read_csv('/jupyter/data/census-ahs-2021/codebook.csv', dtype=str, index_col=False)

    # Find the row for OMB13CBSA
    ombs_row = codebook[codebook['Variable'] == 'OMB13CBSA']

    response_codes_text = ombs_row['Response Codes'].iloc[0]  # Get the string value from the Series
    code_pairs = response_codes_text.split("||")

    code_pairs_dict = {k.strip(): v.strip() for k, v in (code_pair.split(":") for code_pair in code_pairs)}

    return code_pairs_dict.get(code)
```

## Example 3: I wonder if there are any trends for metro areas in Florida, US in which mold presence increased between years 2001 and 2011? Can you get the data for matching mold presence?

```
import pandas as pd

data_dir =  "/jupyter/data/census-ahs"


def get_florida_mold_data():
    # Store results
    florida_mold_data = []
    
    # Years to analyze
    years = range(2001, 2012, 2)
    
    for year in years:
        try:
            # Read data file for year
            file_path = os.path.join(data_dir, f'survey_{year}.csv')
            
            df = pd.read_csv(file_path, dtype=str, index_col=False)
            
            # Find mold-related columns
            mold_cols = [col for col in df.columns if 'mold' in col.lower()]
            
            # Find geographic identifier columns
            geo_cols = [col for col in df.columns if col in ['SMSA', 'METRO3', 'OMB13CBSA', 'DIVISION']]
            
            if len(mold_cols) == 0:
                continue
                
            if len(geo_cols) == 0:
                continue
            
            # Select relevant columns
            cols_to_use = geo_cols + mold_cols
            df_subset = df[cols_to_use]
            
            # Read codebook to identify Florida metro areas
            codebook_path = os.path.join(data_dir, 'census_ahs_codebook.csv')
            
            # ensure to pass index_col=False, else sometimes data shifts
            codebook = pd.read_csv(codebook_path, dtype=str, index_col=False)
            
            # Get Florida metro codes for the geographic identifier being used
            geo_col = geo_cols[len(geo_cols) - 1]
            
            geo_codes = codebook[codebook['Variable'] == geo_col]
            if geo_codes.empty:
                continue
                
            florida_codes = [code.split(':')[0].strip() 
                            for code in geo_codes['Response Codes'].iloc[0].split('||')
                            if 'FL' in code.upper()]
            
            # Filter for Florida metros using substring matching
            df_fl = df_subset[df_subset[geo_col].apply(lambda x: any(code in str(x) for code in florida_codes))]
            
            # Add year column
            df_fl.loc[:, 'YEAR'] = year
            
            florida_mold_data.append(df_fl)
            
        except Exception as e:
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            continue
    
    # Combine all years
    if florida_mold_data:
        combined_data = pd.concat(florida_mold_data, ignore_index=True)
        
        # Replace values in the 'MOLD' columns with number to string mappings
        # where MOLD columns are columns that contain MOLD in the column name (substring match)
        mold_cols = [col for col in combined_data.columns if 'mold' in col.lower()]
        
        for col in mold_cols:
            def convert_value(x):
                # Remove any extra quotes that might be present
                # many times codes are wrapped in quotes..
                x_str = str(x).strip().strip("'\"")
                if x_str in ['Y', '1', '1.0']:
                    return "Yes"
                elif x_str in ['N', '2', '2.0']:
                    return "No"
                elif x_str in ['-6', '-6.0', 'N/A', 'NA', '']:
                    return "N/A"
                else:
                    return x
            
            # Remember that this example converts to "Yes" / "No" / "N/A"
            # if you plot it, you'll want to "count" these text ocurrences
            # also remember that values soemtimes are wrapped in quotes, such as "'6'",
            # that is why we strip them or sometimes compare to substrings
            combined_data[col] = combined_data[col].apply(convert_value)
        
        return combined_data
    else:
        return pd.DataFrame()

```