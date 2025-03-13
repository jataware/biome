# Example 1: Can you tell me which medication have the highest adverse effects reported from all of the available?

```
import requests
import os
import pandas as pd

# Base URL for the API
base_url = "https://api.fda.gov/drug/event.json?api_key=" + os.environ.get('API_OPENFDA')

# Query parameters
params = {
    'count': 'patient.drug.medicinalproduct.exact',
    'limit': 100  # Get top 100 medications by report count
}

# Make API request
response = requests.get(base_url, params=params)

# Convert to DataFrame
results = response.json()['results']
df = pd.DataFrame(results, columns=['term', 'count'])

# Sort by count in descending order
df = df.sort_values('count', ascending=False)

# Display top medications with highest adverse event counts
print("Top medications by adverse event count:")
print(df.head(10))

# Get medication with highest count
top_med = df.iloc[0]
print(f"\nMedication with highest number of adverse events:")
print(f"{top_med['term']}: {top_med['count']} reports")
```