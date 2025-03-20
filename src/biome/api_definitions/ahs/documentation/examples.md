# Examples

## Example 1: Use the codebook to get the meaning of the codes for the OMB13CBSA variable, by first finding the row in the codebook for that variable.

```
import pandas as pd

# Read codebook to get metro area meanings
# ensure to set index_col=False, since the codebook has no index column
codebook = pd.read_csv('{{DATASET_FILES_BASE_PATH}}/census-ahs/census_ahs_codebook.csv', index_col=False)

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
    codebook = pd.read_csv('{{DATASET_FILES_BASE_PATH}}/census-ahs/census_ahs_codebook.csv', index_col=False)

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

data_dir =  "{{DATASET_FILES_BASE_PATH}}/census-ahs"

def get_florida_mold_data():
    # Store results
    florida_mold_data = []
    
    # Years to analyze
    years = range(2001, 2012, 2)
    
    for year in years:
        try:
            # Read data file for year
            file_path = os.path.join(data_dir, f'survey_{year}.csv')
            
            df = pd.read_csv(file_path, index_col=False)
            
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
            codebook = pd.read_csv(codebook_path, index_col=False)
            
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

## Example 4: Analyzing and visualizing the relationship between housing conditions (mold, water leaks) and the presence of children in households using the 2023 American Housing Survey data. This code creates a horizontal bar chart comparing the prevalence of various housing conditions in homes with and without children, and generates a summary table of the differences.

```
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import PercentFormatter

# Load a sample of the AHS dataset (2023)
file_path = '{{DATASET_FILES_BASE_PATH}}/census-ahs/survey_2023.csv'

# Define columns of interest based on our exploration
geo_cols = ['OMB13CBSA']
mold_cols = ['MOLDBASEM', 'MOLDBATH', 'MOLDBEDRM', 'MOLDKITCH', 'MOLDLROOM', 'MOLDOTHER']
leak_cols = ['LEAKI', 'LEAKO']
child_cols = ['NUMOLDKIDS', 'NUMYNGKIDS']

# Combine all columns of interest
cols_of_interest = geo_cols + mold_cols + leak_cols + child_cols

# Load a sample of the data with only the columns we need
sample_size = 10000  # Adjust based on memory constraints
ahs_sample = pd.read_csv(file_path, usecols=cols_of_interest, nrows=sample_size)

# Clean the data by removing quotes from string values
for col in ahs_sample.columns:
    if ahs_sample[col].dtype == 'object':
        ahs_sample[col] = ahs_sample[col].str.replace("'", "")

# Create a binary variable for presence of children
ahs_sample['has_children'] = ((ahs_sample['NUMOLDKIDS'] > 0) | (ahs_sample['NUMYNGKIDS'] > 0)).astype(int)

# Convert categorical variables to numeric for analysis
for col in mold_cols + leak_cols:
    # Convert '1' (Yes) to 1, '2' (No) to 0, and others to NaN
    ahs_sample[col] = ahs_sample[col].apply(
        lambda x: 1 if x == '1' else (0 if x == '2' else np.nan)
    )

# Create a more descriptive mapping for the variables
variable_descriptions = {
    'MOLDBASEM': 'Mold in Basement',
    'MOLDBATH': 'Mold in Bathroom',
    'MOLDBEDRM': 'Mold in Bedroom',
    'MOLDKITCH': 'Mold in Kitchen',
    'MOLDLROOM': 'Mold in Living Room',
    'MOLDOTHER': 'Mold in Other Areas',
    'LEAKI': 'Inside Water Leaks',
    'LEAKO': 'Outside Water Leaks'
}

# Prepare data for visualization
conditions = []
with_children_vals = []
without_children_vals = []
sample_sizes = []

for condition in mold_cols + leak_cols:
    valid_data = ahs_sample.dropna(subset=[condition, 'has_children'])
    
    if len(valid_data) > 0:
        with_children_val = valid_data[valid_data['has_children'] == 1][condition].mean() * 100
        without_children_val = valid_data[valid_data['has_children'] == 0][condition].mean() * 100
        
        if not np.isnan(with_children_val) and not np.isnan(without_children_val):
            conditions.append(variable_descriptions.get(condition, condition))
            with_children_vals.append(with_children_val)
            without_children_vals.append(without_children_val)
            sample_sizes.append(len(valid_data))

# Create a DataFrame for plotting
plot_data = pd.DataFrame({
    'Condition': conditions,
    'With Children (%)': with_children_vals,
    'Without Children (%)': without_children_vals,
    'Sample Size': sample_sizes
})

# Sort by prevalence in homes with children
plot_data = plot_data.sort_values(by='With Children (%)', ascending=False)

# Create a horizontal bar chart
plt.figure(figsize=(12, 10))
sns.set_style("whitegrid")

# Create the horizontal bar chart
ax = sns.barplot(
    x='With Children (%)', 
    y='Condition', 
    data=plot_data, 
    color='#3498db',
    label='Homes with Children'
)

sns.barplot(
    x='Without Children (%)', 
    y='Condition', 
    data=plot_data, 
    color='#e74c3c',
    label='Homes without Children'
)

# Add percentage labels to the bars
for i, (with_val, without_val) in enumerate(zip(plot_data['With Children (%)'], plot_data['Without Children (%)'])):
    if with_val > without_val:
        ax.text(with_val + 0.5, i, f'{with_val:.1f}%', va='center')
        ax.text(without_val - 2.5, i, f'{without_val:.1f}%', va='center', color='white')
    else:
        ax.text(with_val - 2.5, i, f'{with_val:.1f}%', va='center', color='white')
        ax.text(without_val + 0.5, i, f'{without_val:.1f}%', va='center')

# Add sample size information to the y-axis labels
labels = [f"{condition}\n(n={size:,})" for condition, size in zip(plot_data['Condition'], plot_data['Sample Size'])]
ax.set_yticklabels(labels)

# Format the x-axis as percentages
ax.xaxis.set_major_formatter(PercentFormatter())

# Add a title and labels
plt.title('Housing Conditions by Presence of Children\nAmerican Housing Survey (2023)', fontsize=16, pad=20)
plt.xlabel('Prevalence (%)', fontsize=12)
plt.ylabel('Housing Condition', fontsize=12)
plt.legend(title='Household Type', loc='lower right')

# Add a note about the data
plt.figtext(0.5, 0.01, 
            "Note: Data from 2023 American Housing Survey. Sample sizes vary by condition.\n"
            "Percentages represent the proportion of households reporting each condition.", 
            ha='center', fontsize=10, style='italic')

plt.tight_layout(rect=[0, 0.03, 1, 0.97])
plt.show()

# Create a summary table of the results
summary_table = plot_data.copy()
summary_table['Difference (percentage points)'] = summary_table['With Children (%)'] - summary_table['Without Children (%)']
summary_table = summary_table.sort_values(by='Difference (percentage points)', ascending=False)

print("Summary of Housing Conditions by Presence of Children:")
print(summary_table[['Condition', 'With Children (%)', 'Without Children (%)', 'Difference (percentage points)', 'Sample Size']].to_string(index=False, float_format=lambda x: f"{x:.1f}"))
```


## Example 5: Analyzing the relationship between housing conditions, asthma, and the presence of children using the 2023 American Housing Survey data. This code calculates and compares the prevalence of various housing conditions (mold, water leaks) in homes with and without reported asthma cases, and also examines the prevalence of asthma in households with and without children.

```
import pandas as pd
import numpy as np

# Load the AHS dataset (2023) with asthma-related variables
file_path = '{{DATASET_FILES_BASE_PATH}}/census-ahs/survey_2023.csv'

# Define variables of interest
asthma_vars = ['HHLDASTHMA']  # Household member ever diagnosed with asthma
housing_vars = [
    'MOLDBASEM', 'MOLDBATH', 'MOLDBEDRM', 'MOLDKITCH', 'MOLDLROOM', 'MOLDOTHER',  # Mold
    'LEAKI', 'LEAKO'                                                               # Water leaks
]
child_vars = ['NUMOLDKIDS', 'NUMYNGKIDS']
geo_vars = ['OMB13CBSA']

# Combine all variables of interest
cols_of_interest = asthma_vars + housing_vars + child_vars + geo_vars

# Load a sample of the data
sample_size = 10000  # Adjust based on memory constraints
ahs_sample = pd.read_csv(file_path, usecols=cols_of_interest, nrows=sample_size)

# Clean the data by removing quotes from string values
for col in ahs_sample.columns:
    if ahs_sample[col].dtype == 'object':
        ahs_sample[col] = ahs_sample[col].str.replace("'", "")

# Create a binary variable for presence of children
ahs_sample['has_children'] = ((ahs_sample['NUMOLDKIDS'] > 0) | (ahs_sample['NUMYNGKIDS'] > 0)).astype(int)

# Convert asthma variable to binary (Yes/No)
ahs_sample['asthma'] = ahs_sample['HHLDASTHMA'].apply(
    lambda x: 1 if x == '1' else (0 if x == '2' else np.nan)
)

# Convert housing condition variables to binary (Yes/No)
for col in housing_vars:
    ahs_sample[col + '_binary'] = ahs_sample[col].apply(
        lambda x: 1 if x == '1' else (0 if x == '2' else np.nan)
    )

# Analyze relationship between housing conditions and asthma
print("Relationship between asthma and housing conditions:")
for col in housing_vars:
    binary_col = col + '_binary'
    valid_data = ahs_sample.dropna(subset=['asthma', binary_col])
    
    if len(valid_data) > 0:
        with_asthma = valid_data[valid_data['asthma'] == 1][binary_col].mean() * 100
        without_asthma = valid_data[valid_data['asthma'] == 0][binary_col].mean() * 100
        
        if not np.isnan(with_asthma) and not np.isnan(without_asthma):
            print(f"\n{col}:")
            print(f"  - Homes with asthma: {with_asthma:.1f}%")
            print(f"  - Homes without asthma: {without_asthma:.1f}%")
            print(f"  - Difference: {with_asthma - without_asthma:.1f} percentage points")

# Calculate the prevalence of asthma in households with and without children
asthma_by_children = ahs_sample.dropna(subset=['asthma', 'has_children']).groupby('has_children')['asthma'].mean() * 100
print("\nAsthma Prevalence by Presence of Children:")
print(f"Households with children: {asthma_by_children.get(1, 'N/A'):.1f}%")
print(f"Households without children: {asthma_by_children.get(0, 'N/A'):.1f}%")
print(f"Difference: {asthma_by_children.get(1, 0) - asthma_by_children.get(0, 0):.1f} percentage points")
```


## Example 6: Analyzing housing conditions in Houston, TX using the 2007 American Housing Survey data. This code identifies Houston records using the SMSA code, analyzes the prevalence of water leaks and pest problems, and compares these conditions between larger households (3+ persons, likely to have children) and smaller households (1-2 persons).

```
import pandas as pd
import numpy as np

# Load the 2007 AHS dataset with Houston data
file_path = '{{DATASET_FILES_BASE_PATH}}/census-ahs/survey_2007.csv'

# Define Houston SMSA code
houston_smsa = '3360'

# Define housing condition variables based on our exploration
housing_vars = [
    'LEAK', 'ILEAK',                                        # Water leaks
    'RATS', 'MICE'                                          # Pests
]

# Define household size variable
household_var = 'PER'

# Combine all columns of interest
cols_of_interest = ['SMSA'] + housing_vars + [household_var]

# Load the Houston data
houston_data = pd.read_csv(file_path, usecols=cols_of_interest)

# Clean the data by removing quotes if needed
for col in houston_data.columns:
    if houston_data[col].dtype == 'object':
        houston_data[col] = houston_data[col].str.replace("'", "")

# Filter for Houston
houston_data = houston_data[houston_data['SMSA'] == houston_smsa]

print(f"Loaded {len(houston_data)} Houston records from 2007 survey")

# Create a binary variable for households likely to have children (3+ persons)
# This is a proxy since we don't have direct child indicators
houston_data['likely_has_children'] = houston_data[household_var].apply(
    lambda x: 1 if x not in ['-6', '-9'] and int(x) >= 3 else 0
)

print(f"\nHouseholds likely to have children (3+ persons): {houston_data['likely_has_children'].sum()} ({houston_data['likely_has_children'].mean()*100:.1f}% of Houston sample)")

# Convert housing condition variables to binary (Yes/No)
for col in housing_vars:
    houston_data[col + '_binary'] = houston_data[col].apply(
        lambda x: 1 if x == '1' else (0 if x == '2' else np.nan)
    )

# Analyze housing conditions
print("\nPrevalence of housing conditions in Houston (2007):")
for col in housing_vars:
    binary_col = col + '_binary'
    valid_data = houston_data.dropna(subset=[binary_col])
    if len(valid_data) > 0:
        yes_pct = valid_data[binary_col].mean() * 100
        print(f"{col}: {yes_pct:.1f}% reported 'Yes' (based on {len(valid_data)} valid responses)")

# Analyze relationship between household size and housing conditions
print("\nRelationship between household size and housing conditions in Houston (2007):")
for col in housing_vars:
    binary_col = col + '_binary'
    valid_data = houston_data.dropna(subset=[binary_col, 'likely_has_children'])
    
    if len(valid_data) > 0:
        with_children = valid_data[valid_data['likely_has_children'] == 1][binary_col].mean() * 100
        without_children = valid_data[valid_data['likely_has_children'] == 0][binary_col].mean() * 100
        
        if not np.isnan(with_children) and not np.isnan(without_children):
            print(f"\n{col}:")
            print(f"  - Households with 3+ persons: {with_children:.1f}%")
            print(f"  - Households with 1-2 persons: {without_children:.1f}%")
            print(f"  - Difference: {with_children - without_children:.1f} percentage points")
```


## Example 7: Exploring the American Housing Survey codebook to identify variables related to asthma, respiratory health, and housing conditions. This code searches the codebook for terms related to asthma, air quality, pests, and HVAC systems, and provides a summary of available variables that could be relevant for analyzing the relationship between housing conditions and respiratory health.

```
import pandas as pd
import numpy as np

# Load the codebook to find information about variables
codebook_path = '{{DATASET_FILES_BASE_PATH}}/census-ahs/census_ahs_codebook.csv'
codebook = pd.read_csv(codebook_path, dtype=str, index_col=False)

# Define search terms related to asthma and respiratory health
asthma_terms = [
    'asthma', 'allerg', 'respir', 'breath', 'lung', 'air', 'ventil', 
    'humid', 'mold', 'mildew', 'dust', 'smoke', 'pest', 'roach', 'rodent', 
    'insect', 'heat', 'cool', 'toxic', 'pollut', 'chemical', 'lead'
]

# Search for variables related to these terms
asthma_vars = []
for term in asthma_terms:
    term_vars = codebook[
        (codebook['Description'].str.contains(term, case=False, na=False)) |
        (codebook['Question Text'].str.contains(term, case=False, na=False)) |
        (codebook['Variable'].str.contains(term, case=False, na=False))
    ]
    if not term_vars.empty:
        for _, row in term_vars.iterrows():
            var_info = {
                'Variable': row['Variable'],
                'Description': row['Description'] if 'Description' in row and not pd.isna(row['Description']) else 'No description',
                'Question_Text': row['Question Text'] if 'Question Text' in row and not pd.isna(row['Question Text']) else 'No question text',
                'Survey_Years': row['Survey Years'] if 'Survey Years' in row and not pd.isna(row['Survey Years']) else 'Unknown',
                'Response_Codes': row['Response Codes'] if 'Response Codes' in row and not pd.isna(row['Response Codes']) else 'No codes'
            }
            # Check if this variable is already in our list
            if not any(v['Variable'] == var_info['Variable'] for v in asthma_vars):
                asthma_vars.append(var_info)

# Create a DataFrame for easier viewing
asthma_vars_df = pd.DataFrame(asthma_vars)

# Check if we have any variables specifically about asthma
asthma_specific = asthma_vars_df[
    asthma_vars_df['Description'].str.contains('asthma', case=False, na=False) |
    asthma_vars_df['Question_Text'].str.contains('asthma', case=False, na=False)
]

print(f"Found {len(asthma_vars_df)} variables potentially related to asthma and respiratory health")
print(f"Found {len(asthma_specific)} variables specifically mentioning asthma")

# Display the asthma-specific variables if any
if not asthma_specific.empty:
    print("\nVariables specifically mentioning asthma:")
    for _, row in asthma_specific.head(5).iterrows():  # Show first 5 for brevity
        print(f"\nVariable: {row['Variable']}")
        print(f"Description: {row['Description']}")
        print(f"Question Text: {row['Question_Text']}")
        print(f"Survey Years: {row['Survey_Years']}")

# Check for variables related to indoor air quality
air_quality = asthma_vars_df[
    asthma_vars_df['Description'].str.contains('air quality|ventil|humid', case=False, na=False) |
    asthma_vars_df['Question_Text'].str.contains('air quality|ventil|humid', case=False, na=False)
]

print(f"\nFound {len(air_quality)} variables related to indoor air quality")

# Check for variables related to pests
pest_vars = asthma_vars_df[
    asthma_vars_df['Description'].str.contains('pest|roach|rodent|insect|rat|mice|mouse', case=False, na=False) |
    asthma_vars_df['Question_Text'].str.contains('pest|roach|rodent|insect|rat|mice|mouse', case=False, na=False)
]

print(f"\nFound {len(pest_vars)} variables related to pests")

# Check for variables related to heating and cooling systems
hvac_vars = asthma_vars_df[
    asthma_vars_df['Description'].str.contains('heat|cool|air condition|hvac', case=False, na=False) |
    asthma_vars_df['Question_Text'].str.contains('heat|cool|air condition|hvac', case=False, na=False)
]

print(f"\nFound {len(hvac_vars)} variables related to heating and cooling systems")
```
