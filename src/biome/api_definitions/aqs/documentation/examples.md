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