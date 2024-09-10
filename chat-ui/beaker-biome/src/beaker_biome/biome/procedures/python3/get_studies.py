import requests

# Function to get all studies
response = requests.get('https://www.cbioportal.org/api/studies', params=dict({{request_input}}))
if response.status_code == 200:
    studies = response.json()
else:
    print(f'Failed to retrieve studies. HTTP Status code: {response.status_code}')

{{target_var}} = studies

request_input = {{request_input}}