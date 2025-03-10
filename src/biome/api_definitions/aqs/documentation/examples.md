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
# codes can be fetched from /list/parametersByClass?email=redacted&key=redacted&pc=ALL
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