# Examples

## Example 1: Open the TRI data file with index_col=False, since otherwise columns are shifted, and find data for Orange County, FL.
```
import pandas as pd

# Always the TRI csv with index_col=False param, since pandas is inferring the wrong index column and shifting the data without it
df = pd.read_csv('{{DATASET_FILES_BASE_PATH}}/epa-tri/EPA_TRI_Toxics_2014_2023.csv', dtype=str, index_col=False)

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
tri_data = pd.read_csv('{{DATASET_FILES_BASE_PATH}}/epa-tri/EPA_TRI_Toxics_2014_2023.csv', index_col=False)

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
tri_data = pd.read_csv('{{DATASET_FILES_BASE_PATH}}/epa-tri/EPA_TRI_Toxics_2014_2023.csv', index_col=False)

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
tri_data = pd.read_csv('{{DATASET_FILES_BASE_PATH}}/epa-tri/EPA_TRI_Toxics_2014_2023.csv', index_col=False)

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


## Example 5: Basic loading, cleaning, and summarizing of EPA TRI data for a specific county. This example demonstrates how to handle the comma-separated numeric values in the dataset, filter for a specific geographic area, and create a summary of facilities with their total releases, hazard scores, and chemical counts.

```
import pandas as pd

# Load the data
file_path = '{{DATASET_FILES_BASE_PATH}}/epa-tri/EPA_TRI_Toxics_2014_2023.csv'
tri_data = pd.read_csv(file_path, low_memory=False)

# Fix the numeric columns that might be stored as strings with commas
for col in ['Releases (lb)', 'Waste Managed (lb)', 'RSEI Hazard']:
    if tri_data[col].dtype == 'object':
        # Remove commas and convert to float
        tri_data[col] = tri_data[col].str.replace(',', '').astype(float)

# Filter for a specific county
harris_data = tri_data[(tri_data['County'] == 'HARRIS, TX') | 
                       (tri_data['County'] == 'HARRIS COUNTY, TX')]

# Create a summary of facilities
facility_summary = harris_data.groupby(['TRI Facility Name', 'Latitude', 'Longitude']).agg({
    'Releases (lb)': 'sum',
    'RSEI Hazard': 'sum',
    'Chemical': 'nunique',
    'Year': 'nunique'
}).reset_index()

facility_summary.columns = ['Facility Name', 'Latitude', 'Longitude', 'Total Releases (lb)', 
                           'Total RSEI Hazard', 'Number of Chemicals', 'Years Reported']

# Sort by total releases
facility_summary = facility_summary.sort_values('Total Releases (lb)', ascending=False)

print("Summary of Facilities:")
print(f"Total number of facilities: {len(facility_summary)}")
print(f"Total toxic releases: {facility_summary['Total Releases (lb)'].sum():,.2f} lb")
print(f"Total RSEI Hazard score: {facility_summary['Total RSEI Hazard'].sum():,.2f}")

# Print top 10 facilities by releases
print("\nTop 10 Facilities by Total Releases:")
for i, (name, lat, lon, releases, hazard, chemicals, years) in enumerate(facility_summary.head(10).values, 1):
    print(f"{i}. {name}: {releases:,.2f} lb, RSEI Hazard: {hazard:,.2f}, Chemicals: {chemicals}")
```


## Example 6: Analyzing and visualizing toxic releases by ZIP code. This example shows how to aggregate TRI data by geographic units (ZIP codes), calculate total releases and hazard scores, and create a bar chart visualization of the top areas with highest toxic releases.

```
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load and prepare data (assuming tri_data is already loaded and cleaned)
file_path = '{{DATASET_FILES_BASE_PATH}}/epa-tri/EPA_TRI_Toxics_2014_2023.csv'
tri_data = pd.read_csv(file_path, low_memory=False)

# Fix the numeric columns that might be stored as strings with commas
for col in ['Releases (lb)', 'Waste Managed (lb)', 'RSEI Hazard']:
    if tri_data[col].dtype == 'object':
        # Remove commas and convert to float
        tri_data[col] = tri_data[col].str.replace(',', '').astype(float)

# Filter for a specific county
county_data = tri_data[(tri_data['County'] == 'HARRIS, TX') | 
                       (tri_data['County'] == 'HARRIS COUNTY, TX')]

# Analyze data by ZIP code
zip_summary = county_data.groupby('ZIP Code').agg({
    'TRI Facility Name': 'nunique',
    'Releases (lb)': 'sum',
    'RSEI Hazard': 'sum'
}).reset_index()

zip_summary.columns = ['ZIP Code', 'Number of Facilities', 'Total Releases (lb)', 'Total RSEI Hazard']
zip_summary = zip_summary.sort_values('Total Releases (lb)', ascending=False)

print("Top 10 ZIP Codes by Total Releases:")
for i, (zipcode, facilities, releases, hazard) in enumerate(zip_summary.head(10).values, 1):
    print(f"{i}. ZIP {zipcode}: {facilities} facilities, {releases:,.2f} lb, RSEI Hazard: {hazard:,.2f}")

# Create a bar chart of top 10 ZIP codes by releases
plt.figure(figsize=(12, 6))
top_zips = zip_summary.head(10)
bars = plt.bar(top_zips['ZIP Code'].astype(str), top_zips['Total Releases (lb)'] / 1e6)
plt.title('Top 10 ZIP Codes by Total Toxic Releases')
plt.xlabel('ZIP Code')
plt.ylabel('Total Releases (Million lb)')
plt.xticks(rotation=45)
plt.grid(True, axis='y', linestyle='--', alpha=0.7)

# Add value labels on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f'{height:.1f}M', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('top_zips_by_releases.png')
plt.show()
```


## Example 7: Identifying and analyzing chemicals related to specific health conditions. This example demonstrates how to filter TRI data for chemicals associated with a particular health condition (like asthma), calculate their proportion of total releases, and analyze trends over time. This approach can be adapted for various health conditions by modifying the list of relevant chemicals.

```
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load and prepare data (assuming tri_data is already loaded and cleaned)
file_path = '{{DATASET_FILES_BASE_PATH}}/epa-tri/EPA_TRI_Toxics_2014_2023.csv'
tri_data = pd.read_csv(file_path, low_memory=False)

# Fix the numeric columns that might be stored as strings with commas
for col in ['Releases (lb)', 'Waste Managed (lb)', 'RSEI Hazard']:
    if tri_data[col].dtype == 'object':
        # Remove commas and convert to float
        tri_data[col] = tri_data[col].str.replace(',', '').astype(float)

# Filter for a specific county
county_data = tri_data[(tri_data['County'] == 'HARRIS, TX') | 
                       (tri_data['County'] == 'HARRIS COUNTY, TX')]

# List of chemicals known to potentially trigger or worsen a specific health condition (e.g., asthma)
condition_related_chemicals = [
    'Ammonia', 'Chlorine', 'Formaldehyde', 'Sulfuric acid', 'Hydrochloric acid',
    'Nitrogen oxides', 'Sulfur dioxide', 'Particulate matter', 'Isocyanates',
    'Toluene diisocyanate', 'Phthalates', 'Volatile organic compounds', 'VOCs',
    'Ozone', 'Acrolein', 'Benzene', 'Styrene', 'Xylene', 'Toluene'
]

# Create a function to check if a chemical is related to the health condition
def is_condition_related(chemical_name):
    for chem in condition_related_chemicals:
        if chem.lower() in chemical_name.lower():
            return True
    return False

# Add a column to identify condition-related chemicals
county_data['Condition_Related'] = county_data['Chemical'].apply(is_condition_related)

# Calculate total condition-related releases
condition_releases = county_data[county_data['Condition_Related']]['Releases (lb)'].sum()
total_releases = county_data['Releases (lb)'].sum()
condition_percentage = (condition_releases / total_releases) * 100

print(f"Total toxic releases: {total_releases:,.2f} lb")
print(f"Condition-related chemical releases: {condition_releases:,.2f} lb")
print(f"Percentage of condition-related releases: {condition_percentage:.2f}%")

# Analyze trends over time for condition-related chemicals
yearly_condition = county_data[county_data['Condition_Related']].groupby('Year')['Releases (lb)'].sum()
yearly_total = county_data.groupby('Year')['Releases (lb)'].sum()
yearly_percentage = (yearly_condition / yearly_total) * 100

# Create a time series plot
plt.figure(figsize=(12, 6))
plt.plot(yearly_condition.index, yearly_condition.values / 1e6, 'o-', color='red', 
         label='Condition-related Releases')
plt.plot(yearly_total.index, yearly_total.values / 1e6, 'o-', color='blue', 
         label='Total Releases')
plt.title('Yearly Trends in Toxic Releases')
plt.xlabel('Year')
plt.ylabel('Releases (Million lb)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('yearly_condition_trends.png')
plt.show()
```


## Example 8: Creating an interactive map of toxic release facilities. This example shows how to use the folium library to generate an interactive web map displaying the locations of facilities, with circle sizes proportional to release amounts and popup information showing detailed facility data. This visualization helps identify spatial patterns and hotspots of toxic releases.

```
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import numpy as np

# Load and prepare data (assuming tri_data is already loaded and cleaned)
file_path = '{{DATASET_FILES_BASE_PATH}}/epa-tri/EPA_TRI_Toxics_2014_2023.csv'
tri_data = pd.read_csv(file_path, low_memory=False)

# Fix the numeric columns that might be stored as strings with commas
for col in ['Releases (lb)', 'Waste Managed (lb)', 'RSEI Hazard']:
    if tri_data[col].dtype == 'object':
        # Remove commas and convert to float
        tri_data[col] = tri_data[col].str.replace(',', '').astype(float)

# Filter for a specific county
county_data = tri_data[(tri_data['County'] == 'HARRIS, TX') | 
                       (tri_data['County'] == 'HARRIS COUNTY, TX')]

# Create a summary of facilities
facility_summary = county_data.groupby(['TRI Facility Name', 'Latitude', 'Longitude']).agg({
    'Releases (lb)': 'sum',
    'RSEI Hazard': 'sum',
    'Chemical': 'nunique',
    'Year': 'nunique'
}).reset_index()

facility_summary.columns = ['Facility Name', 'Latitude', 'Longitude', 'Total Releases (lb)', 
                           'Total RSEI Hazard', 'Number of Chemicals', 'Years Reported']

# Sort by total releases
facility_summary = facility_summary.sort_values('Total Releases (lb)', ascending=False)

# Create an interactive map
# Center the map on the county
county_center = [29.7604, -95.3698]  # Houston coordinates as center
m = folium.Map(location=county_center, zoom_start=10, tiles='CartoDB positron')

# Add a marker cluster for better visualization
marker_cluster = MarkerCluster().add_to(m)

# Add markers for each facility
for i, row in facility_summary.iterrows():
    # Scale the circle size based on the log of releases (to make it more visible)
    radius = np.log1p(row['Total Releases (lb)']) * 0.5
    
    # Create popup content
    popup_content = f"""
    <b>{row['Facility Name']}</b><br>
    Total Releases: {row['Total Releases (lb)']:,.2f} lb<br>
    RSEI Hazard: {row['Total RSEI Hazard']:,.2f}<br>
    Number of Chemicals: {row['Number of Chemicals']}<br>
    Years Reported: {row['Years Reported']}
    """
    
    # Add a circle marker
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=radius,
        popup=folium.Popup(popup_content, max_width=300),
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.6,
        opacity=0.8
    ).add_to(marker_cluster)

# Save the map
map_file = 'facilities_map.html'
m.save(map_file)
print(f"Interactive map saved to: {map_file}")
```


## Example 9: Analyzing the relationship between release amounts and hazard scores. This example demonstrates how to investigate the correlation between the quantity of toxic releases and their associated RSEI Hazard scores using scatter plots, trend lines, and correlation statistics. This analysis helps understand whether larger releases necessarily correspond to higher health risks.

```
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import pearsonr

# Load and prepare data (assuming tri_data is already loaded and cleaned)
file_path = '{{DATASET_FILES_BASE_PATH}}/epa-tri/EPA_TRI_Toxics_2014_2023.csv'
tri_data = pd.read_csv(file_path, low_memory=False)

# Fix the numeric columns that might be stored as strings with commas
for col in ['Releases (lb)', 'Waste Managed (lb)', 'RSEI Hazard']:
    if tri_data[col].dtype == 'object':
        # Remove commas and convert to float
        tri_data[col] = tri_data[col].str.replace(',', '').astype(float)

# Filter for a specific county
county_data = tri_data[(tri_data['County'] == 'HARRIS, TX') | 
                       (tri_data['County'] == 'HARRIS COUNTY, TX')]

# Analyze data by Census Block Group
census_summary = county_data.groupby('Census Block Group').agg({
    'TRI Facility Name': 'nunique',
    'Releases (lb)': 'sum',
    'RSEI Hazard': 'sum',
    'Chemical': 'nunique'
}).reset_index()

census_summary.columns = ['Census Block Group', 'Number of Facilities', 
                         'Total Releases (lb)', 'Total RSEI Hazard', 'Number of Chemicals']

# Create a scatter plot of total releases vs RSEI Hazard by Census Block Group
plt.figure(figsize=(10, 8))
plt.scatter(
    np.log10(census_summary['Total Releases (lb)']), 
    np.log10(census_summary['Total RSEI Hazard'] + 1),  # Add 1 to avoid log(0)
    alpha=0.7,
    s=50,
    c='blue'
)
plt.title('Relationship Between Total Releases and RSEI Hazard Score (Log Scale)')
plt.xlabel('Log10(Total Releases in lb)')
plt.ylabel('Log10(RSEI Hazard Score)')
plt.grid(True, linestyle='--', alpha=0.7)

# Add a trend line
z = np.polyfit(np.log10(census_summary['Total Releases (lb)']), 
               np.log10(census_summary['Total RSEI Hazard'] + 1), 1)
p = np.poly1d(z)
plt.plot(np.log10(census_summary['Total Releases (lb)']), 
         p(np.log10(census_summary['Total Releases (lb)'])), 
         "r--", linewidth=2)

# Add correlation coefficient
corr, _ = pearsonr(np.log10(census_summary['Total Releases (lb)']), 
                  np.log10(census_summary['Total RSEI Hazard'] + 1))
plt.annotate(f"Correlation: {corr:.2f}", xy=(0.05, 0.95), xycoords='axes fraction', 
             fontsize=12, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

plt.tight_layout()
plt.savefig('releases_vs_hazard.png')
plt.show()
```
