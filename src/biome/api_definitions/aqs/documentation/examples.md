# Examples

## Example 1: Query annual air pollution data for Seminole County, Florida for the year 2000. Use pollutants relating to asthma.

```
import requests
import os

# Get API credentials from environment variables
email = os.environ.get("API_EPA_AQS_EMAIL")
key = os.environ.get("API_EPA_AQS")

# Define the API endpoint and parameters
state_code = 12 # "Florida"
county_code = 117 # "Seminole" county
year = 2000
# codes can be fetched from /list/parametersByClass?email={email}&key={key}&pc=ALL
# These are asthma related pollutant/parameter codes:
pollutant_codes = [
    '44201', # ozone
    '81102', # PM10
    '81104', # PM2.5
    '42602', # Nitrogen dioxide (NO2)
    '42401', # Sulfur dioxide
    '42101', # Carbon monoxide
]

bdate = f"{year}0501"
edate = f"{year}0501"

# Construct the API URL
param_string = ','.join(pollutant_codes)

url = f'https://aqs.epa.gov/data/api/annualData/byCounty?email={email}&key={key}&param={param_string}&bdate={bdate}&edate={edate}&state={state_code}&county={county_code}'

# Make the API request
response = requests.get(url)

data = None
# Check if the request was successful
if response.status_code == 200:
    data = response.json()

data
```

## Example 2: Collect historical air quality data from the EPA Air Quality System (AQS) for Orange County, FL.

```
import requests
import os

# Get API credentials from environment variables
email = os.environ.get("API_EPA_AQS_EMAIL")
key = os.environ.get("API_EPA_AQS")

# Define parameters
state_code = "12"  # Florida
county_code = "095" # Orange County
param_codes = [
    "44201",  # Ozone
    "42401",  # SO2
    "42101",  # CO 
    "42602",  # NO2
    "88101"   # PM2.5
]

# Use annual data API endpoint since we want historical data
# Sample every 5 years from 1980-2020 to avoid too many API calls
years = range(1980, 2021, 5)

# Initialize list to store results
all_data = []

# Make API requests for each year
for year in years:
    bdate = f"{year}0101"
    edate = f"{year}1231"
    
    url = f"https://aqs.epa.gov/data/api/annualData/byCounty"
    params = {
        "email": email,
        "key": key,
        "param": ",".join(param_codes),
        "bdate": bdate,
        "edate": edate,
        "state": state_code,
        "county": county_code
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if "Data" in data:
            all_data.extend(data["Data"])
        else:
            print(f"No data found for year {year}")
    else:
        print(f"Error {response.status_code}: {response.text}")

# Check the structure of the collected data
if all_data:
    print(all_data[0])  # Print the first entry to see the structure
    df = pd.DataFrame(all_data)
    
    # Clean up the DataFrame
    if not df.empty:
        # Select relevant columns
        # parameter_name doesn't exist- use `parameter` or `parameter_code`:
        cols = ['parameter', 'year', 'arithmetic_mean',  
                'first_max_value', 'first_max_datetime',
                'observation_count']
        df = df[cols]
        
        # Sort by year and parameter
        df = df.sort_values(['year', 'parameter'])
        
        # Convert year to int
        df['year'] = df['year'].astype(int)
        
        # Display first few rows
        print(df.head())
    else:
        print("No data found for the specified parameters")
else:
    print("No data collected.")
```

## Example 3: Inspect API response change by generating a schema from an API response so that we don't inspect the raw data and blow up the context window.

```
import requests
from genson import SchemaBuilder
import os

# Get API credentials from environment variables
email = os.environ.get("API_EPA_AQS_EMAIL")
key = os.environ.get("API_EPA_AQS")

# Define parameters
state_code = "48"  # Texas
county_code = "201" # Harris County
param_codes = [
    "44201",  # Ozone
    "42401",  # SO2
    "42101",  # CO 
    "42602",  # NO2
    "88101", # PM2.5
    "81102"  # PM10
]

# Sample one year to inspect the response structure
year = 2020
bdate = f"{year}0101"
edate = f"{year}1231"

url = f"https://aqs.epa.gov/data/api/annualData/byCounty"
params = {
    "email": email,
    "key": key,
    "param": ",".join(param_codes),
    "bdate": bdate,
    "edate": edate,
    "state": state_code,
    "county": county_code
}

response = requests.get(url, params=params)
response_data = response.json()

# annual data by county can include a lot of data, especially if we specify a broad date range and a county with a lot of data- lets generate a schema and inspect that instead of inspecting the raw data
builder = SchemaBuilder()
builder.add_object(response_data)
schema = builder.to_schema()

print(schema["properties"])
```

## Example 4: Retrieve daily air quality data for ozone, CO, NO2, and PM2.5 in Harris County, TX for each month of the year 2022.

```
import os
import requests
import pandas as pd
from datetime import datetime
import calendar

# API configuration
base_url = "https://aqs.epa.gov/data/api"
email = os.environ.get("API_EPA_AQS_EMAIL")
key = os.environ.get("API_EPA_AQS")

# Define parameters
parameters = {
    'Ozone': 44201,
    'CO': 42101, 
    'NO2': 42602,
    'PM2.5': 88101
}

# Harris County, TX codes
state_code = '48'
county_code = '201'
year = 2022

def get_monthly_data(param_code, month):
    # Get number of days in month
    num_days = calendar.monthrange(year, month)[1]
    
    params = {
        'email': email,
        'key': key,
        'param': param_code,
        'bdate': f'{year}{month:02d}01',
        'edate': f'{year}{month:02d}{num_days}',
        'state': state_code,
        'county': county_code
    }
    
    response = requests.get(f"{base_url}/dailyData/byCounty", params=params)
    return response.json()

# Initialize empty list to store all data
all_data = []

# Loop through each parameter and month
for param_name, param_code in parameters.items():
    for month in range(1, 13):
        try:
            data = get_monthly_data(param_code, month)
            
            if 'Data' in data:
                for record in data['Data']:
                    all_data.append({
                        'date': record['date_local'],
                        'parameter': param_name,
                        'value': record['arithmetic_mean'],
                        'units': record['units_of_measure'],
                        'site': record['site_number'],
                        'latitude': record['latitude'],
                        'longitude': record['longitude']
                    })
        except Exception as e:
            print(f"Error fetching data for {param_name} in month {month}: {str(e)}")

# Convert to DataFrame
df = pd.DataFrame(all_data)

# Convert date string to datetime
df['date'] = pd.to_datetime(df['date'])

# Sort by date and parameter
df = df.sort_values(['date', 'parameter'])

# Save to CSV
df.to_csv('harris_county_air_quality_2022.csv', index=False)
```

## Example 5: Here's a reusable function for retrieving and processing data for multiple pollutants:

```
def get_pollutant_data(state_code, county_code, param_code, year, pollutant_name):
    """
    Get and process data for a specific pollutant
    
    Parameters:
    -----------
    state_code : str
        Two-digit state code
    county_code : str
        Three-digit county code
    param_code : str
        Parameter code for the pollutant
    year : str
        Year to retrieve data for
    pollutant_name : str
        Name of the pollutant (for display purposes)
        
    Returns:
    --------
    pandas.DataFrame or None
        DataFrame containing the processed data, or None if the request failed
    """
    print(f"Retrieving daily {pollutant_name} data for Harris County, TX for {year}...")
    
    bdate = f"{year}0101"  # January 1st of the year
    edate = f"{year}1231"  # December 31st of the year
    
    data_response = get_aqs_data("dailyData/byCounty", {
        "state": state_code,
        "county": county_code,
        "param": param_code,
        "bdate": bdate,
        "edate": edate
    })
    
    if data_response and data_response.get('Header', [{}])[0].get('status') == 'Success':
        data = data_response.get('Data', [])
        df = pd.DataFrame(data)
        
        # Convert date_local to datetime
        df['date'] = pd.to_datetime(df['date_local'])
        
        # Group by site and date to get daily averages for each site
        site_daily_avg = df.groupby(['local_site_name', 'date'])['arithmetic_mean'].mean().reset_index()
        
        # Get the overall daily average across all sites
        daily_avg = site_daily_avg.groupby('date')['arithmetic_mean'].mean().reset_index()
        
        # Rename the arithmetic_mean column to the pollutant name for clarity
        daily_avg = daily_avg.rename(columns={'arithmetic_mean': pollutant_name.lower()})
        
        return daily_avg, df['units_of_measure'].iloc[0]
    else:
        print(f"Failed to retrieve {pollutant_name} data")
        return None, None
```

## Example 6: Retrieving and exploring parameter classes and codes for air quality research. This example demonstrates how to get a list of parameter classes, then retrieve specific parameters within the CRITERIA class, which contains the most important air pollutants for health research. It also identifies key parameter codes relevant to asthma research.

```
import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Get authentication details from environment variables
email = os.environ.get("API_EPA_AQS_EMAIL")
api_key = os.environ.get("API_EPA_AQS")

# Base URL for the EPA AQS API
base_url = "https://aqs.epa.gov/data/api"

# Function to make API requests
def get_aqs_data(endpoint, params=None):
    """
    Make a request to the EPA AQS API
    
    Parameters:
    -----------
    endpoint : str
        The API endpoint to query
    params : dict
        Additional parameters for the request
        
    Returns:
    --------
    dict
        The JSON response from the API
    """
    # Add authentication parameters
    if params is None:
        params = {}
    params['email'] = email
    params['key'] = api_key
    
    # Make the request
    url = f"{base_url}/{endpoint}"
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Get list of parameter classes
classes_response = get_aqs_data("list/classes")

# Check if we got a valid response for classes
if classes_response and classes_response.get('Header', [{}])[0].get('status') == 'Success':
    # Convert to DataFrame for easier viewing
    classes_data = classes_response.get('Data', [])
    classes_df = pd.DataFrame(classes_data)
    
    print("Parameter Classes:")
    print(classes_df)
    
    # Now get parameters for the CRITERIA class (most relevant to air quality standards)
    criteria_params_response = get_aqs_data("list/parametersByClass", {"pc": "CRITERIA"})
    
    if criteria_params_response and criteria_params_response.get('Header', [{}])[0].get('status') == 'Success':
        # Convert to DataFrame for easier viewing
        criteria_params_data = criteria_params_response.get('Data', [])
        criteria_params_df = pd.DataFrame(criteria_params_data)
        
        print(f"\nFound {len(criteria_params_data)} criteria pollutant parameters")
        print("\nCriteria pollutant parameters:")
        print(criteria_params_df)
        
        # Create a dictionary of key parameter codes for asthma research
        asthma_param_codes = {
            'Ozone': '44201',
            'PM2.5': '88101',
            'PM10': '81102',
            'NO2': '42602',
            'SO2': '42401',
            'CO': '42101'
        }
        
        print("\nKey parameter codes for asthma research:")
        for pollutant, code in asthma_param_codes.items():
            print(f"{pollutant}: {code}")
    else:
        print("Failed to retrieve criteria parameters data")
else:
    print("Failed to retrieve parameter classes data")
```


## Example 7: Multi-pollutant correlation analysis for air quality research. This example demonstrates how to retrieve data for multiple pollutants (Ozone, PM2.5, NO2, and SO2), process the data to get daily averages, merge the datasets, and analyze correlations between different pollutants. It includes a visualization of the correlation matrix using a heatmap.

```
import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set the style for our plots
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Get authentication details from environment variables
email = os.environ.get("API_EPA_AQS_EMAIL")
api_key = os.environ.get("API_EPA_AQS")

# Base URL for the EPA AQS API
base_url = "https://aqs.epa.gov/data/api"

# Function to make API requests
def get_aqs_data(endpoint, params=None):
    """
    Make a request to the EPA AQS API
    
    Parameters:
    -----------
    endpoint : str
        The API endpoint to query
    params : dict
        Additional parameters for the request
        
    Returns:
    --------
    dict
        The JSON response from the API
    """
    # Add authentication parameters
    if params is None:
        params = {}
    params['email'] = email
    params['key'] = api_key
    
    # Make the request
    url = f"{base_url}/{endpoint}"
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Function to get and process data for a specific pollutant
def get_pollutant_data(state_code, county_code, param_code, year, pollutant_name):
    """
    Get and process data for a specific pollutant
    
    Parameters:
    -----------
    state_code : str
        Two-digit state code
    county_code : str
        Three-digit county code
    param_code : str
        Parameter code for the pollutant
    year : str
        Year to retrieve data for
    pollutant_name : str
        Name of the pollutant (for display purposes)
        
    Returns:
    --------
    pandas.DataFrame or None
        DataFrame containing the processed data, or None if the request failed
    """
    print(f"Retrieving daily {pollutant_name} data for {year}...")
    
    bdate = f"{year}0101"  # January 1st of the year
    edate = f"{year}1231"  # December 31st of the year
    
    data_response = get_aqs_data("dailyData/byCounty", {
        "state": state_code,
        "county": county_code,
        "param": param_code,
        "bdate": bdate,
        "edate": edate
    })
    
    if data_response and data_response.get('Header', [{}])[0].get('status') == 'Success':
        data = data_response.get('Data', [])
        df = pd.DataFrame(data)
        
        print(f"\nFound {len(data)} daily {pollutant_name} records for {year}")
        
        # Convert date_local to datetime
        df['date'] = pd.to_datetime(df['date_local'])
        
        # Extract month and day of week for analysis
        df['month'] = df['date'].dt.month
        df['month_name'] = df['date'].dt.month_name()
        
        # Group by site and date to get daily averages for each site
        site_daily_avg = df.groupby(['local_site_name', 'date'])['arithmetic_mean'].mean().reset_index()
        
        # Get the overall daily average across all sites
        daily_avg = site_daily_avg.groupby('date')['arithmetic_mean'].mean().reset_index()
        
        # Rename the arithmetic_mean column to the pollutant name for clarity
        daily_avg = daily_avg.rename(columns={'arithmetic_mean': pollutant_name.lower()})
        
        return daily_avg, df['units_of_measure'].iloc[0]
    else:
        print(f"Failed to retrieve {pollutant_name} data")
        return None, None

# Set up parameters
state_code = "48"  # Texas
county_code = "201"  # Harris County
year = "2022"

# Define pollutants to retrieve
pollutants = {
    'Ozone': '44201',
    'PM2.5': '88101',
    'NO2': '42602',
    'SO2': '42401'
}

# Get data for each pollutant
pollutant_data = {}
units = {}

for pollutant_name, param_code in pollutants.items():
    daily_avg, unit = get_pollutant_data(state_code, county_code, param_code, year, pollutant_name)
    if daily_avg is not None:
        pollutant_data[pollutant_name.lower()] = daily_avg
        units[pollutant_name.lower()] = unit

# Merge all pollutant data on date
merged_df = None

for pollutant_name, daily_avg in pollutant_data.items():
    if merged_df is None:
        merged_df = daily_avg
    else:
        merged_df = pd.merge(merged_df, daily_avg[['date', pollutant_name]], on='date', how='outer')

# Calculate correlations between pollutants
if merged_df is not None:
    print("\nCorrelations between pollutants:")
    correlation_matrix = merged_df.drop('date', axis=1).corr()
    print(correlation_matrix)
    
    # Plot correlation heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0)
    plt.title(f'Correlation Matrix of Air Pollutants ({year})', fontsize=16)
    plt.tight_layout()
    plt.show()
```


## Example 8: Spatial and temporal analysis of air quality data. This example demonstrates how to analyze air quality data (specifically ozone) across different dimensions: by monitoring site location, by month, and by day of week. It includes visualizations for each type of analysis, helping researchers identify spatial and temporal patterns in air pollution that could affect respiratory health.

```
import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set the style for our plots
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Get authentication details from environment variables
email = os.environ.get("API_EPA_AQS_EMAIL")
api_key = os.environ.get("API_EPA_AQS")

# Base URL for the EPA AQS API
base_url = "https://aqs.epa.gov/data/api"

# Function to make API requests
def get_aqs_data(endpoint, params=None):
    """
    Make a request to the EPA AQS API
    
    Parameters:
    -----------
    endpoint : str
        The API endpoint to query
    params : dict
        Additional parameters for the request
        
    Returns:
    --------
    dict
        The JSON response from the API
    """
    # Add authentication parameters
    if params is None:
        params = {}
    params['email'] = email
    params['key'] = api_key
    
    # Make the request
    url = f"{base_url}/{endpoint}"
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# Set up parameters
state_code = "48"  # Texas
county_code = "201"  # Harris County
param_code = "44201"  # Ozone
year = "2022"
bdate = f"{year}0101"  # January 1st of the year
edate = f"{year}1231"  # December 31st of the year

print(f"Retrieving daily ozone data for {year}...")

# Get daily ozone data
daily_data_response = get_aqs_data("dailyData/byCounty", {
    "state": state_code,
    "county": county_code,
    "param": param_code,
    "bdate": bdate,
    "edate": edate
})

if daily_data_response and daily_data_response.get('Header', [{}])[0].get('status') == 'Success':
    daily_data = daily_data_response.get('Data', [])
    daily_df = pd.DataFrame(daily_data)
    
    print(f"\nFound {len(daily_data)} daily ozone records for {year}")
    
    # Convert date_local to datetime
    daily_df['date'] = pd.to_datetime(daily_df['date_local'])
    
    # Extract month and day of week for analysis
    daily_df['month'] = daily_df['date'].dt.month
    daily_df['day_of_week'] = daily_df['date'].dt.dayofweek
    daily_df['month_name'] = daily_df['date'].dt.month_name()
    daily_df['day_name'] = daily_df['date'].dt.day_name()
    
    # Analyze by monitoring site
    site_avg = daily_df.groupby('local_site_name')['arithmetic_mean'].mean().reset_index()
    site_avg = site_avg.sort_values('arithmetic_mean', ascending=False)
    
    print("\nAverage ozone levels by monitoring site:")
    print(site_avg.head(10))
    
    # Plot monitoring sites with highest ozone levels
    plt.figure(figsize=(14, 8))
    sns.barplot(data=site_avg.head(10), x='arithmetic_mean', y='local_site_name')
    plt.title(f'Average Ozone Levels by Monitoring Site ({year})', fontsize=16)
    plt.xlabel('Ozone Concentration (ppm)', fontsize=12)
    plt.ylabel('Monitoring Site', fontsize=12)
    plt.tight_layout()
    plt.show()
    
    # Analyze by month
    monthly_avg = daily_df.groupby('month_name')['arithmetic_mean'].mean().reset_index()
    # Reorder months chronologically
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    monthly_avg['month_name'] = pd.Categorical(monthly_avg['month_name'], categories=month_order, ordered=True)
    monthly_avg = monthly_avg.sort_values('month_name')
    
    # Plot monthly averages
    plt.figure(figsize=(12, 6))
    sns.barplot(data=monthly_avg, x='month_name', y='arithmetic_mean')
    plt.title(f'Monthly Average Ozone Levels ({year})', fontsize=16)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Ozone Concentration (ppm)', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    # Analyze by day of week
    dow_avg = daily_df.groupby('day_name')['arithmetic_mean'].mean().reset_index()
    # Reorder days of week
    dow_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_avg['day_name'] = pd.Categorical(dow_avg['day_name'], categories=dow_order, ordered=True)
    dow_avg = dow_avg.sort_values('day_name')
    
    # Plot day of week averages
    plt.figure(figsize=(10, 6))
    sns.barplot(data=dow_avg, x='day_name', y='arithmetic_mean')
    plt.title(f'Average Ozone Levels by Day of Week ({year})', fontsize=16)
    plt.xlabel('Day of Week', fontsize=12)
    plt.ylabel('Ozone Concentration (ppm)', fontsize=12)
    plt.tight_layout()
    plt.show()
else:
    print("Failed to retrieve ozone data")
```
