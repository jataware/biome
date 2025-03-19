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
