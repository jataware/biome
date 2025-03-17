# Examples

## Example 1: Search for nutrients for raw acerola juice

```
import requests
import os

# Define the API endpoint and parameters
url = 'https://api.nal.usda.gov/fdc/v1/foods/search'

api_key = os.environ.get("API_USDA_FDC")

params = {'query': 'raw acerola juice', 'api_key': api_key}

# Make the request to the USDA FoodData Central API
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    # Extract the first food item from the results
    food_item = data['foods'][0]
    food_item
```

