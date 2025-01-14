## Example 1: Query the GDC for cases of myeloid leukemia with a JAK2 somatic mutation and return the results as a pandas dataframe.

```
import pandas as pd
from pandas import json_normalize

import requests
import json

# Define the endpoint and filters
endpoint = "https://api.gdc.cancer.gov/ssm_occurrences"
filters = {
    "op": "and",
    "content": [
        {
            "op": "=",
            "content": {
                "field": "case.disease_type",
                "value": "*myeloid leukemia*"
            }
        },
        {
            "op": "in",
            "content": {
                "field": "ssm.consequence.transcript.gene.symbol",
                "value": ["JAK2"]
            }
        }
    ]
}

# Define the fields to be returned
fields = [
    "ssm_id",
    "ssm.consequence.transcript.gene.symbol",
    "ssm.mutation_type",
    "ssm.genomic_dna_change",
    "ssm.consequence.transcript.aa_change",
    "ssm.consequence.transcript.consequence_type",
    "case.project.project_id",
    "case.submitter_id",
    "case.case_id",
    "case.diagnoses.primary_diagnosis"
]

# Construct the request parameters
params = {
    "filters": json.dumps(filters),
    "fields": ",".join(fields),
    "format": "JSON",
    "size": "1000"
}

# Send the request
response = requests.get(endpoint, params=params)
print(f"total hits: {response.json()['data']['pagination']['total']}")
all_ssms = response.json()['data']['hits']

ssms = pd.DataFrame(json_normalize(all_ssms))
ssms.head()
```

## Example 2: Get all cases where disease type is myeloid leukemia from GDC and return the results as a pandas dataframe. Paginate through the results to fetch all available cases

```
import pandas as pd
from pandas import json_normalize

import requests
import json

# Define the endpoint and filters
endpoint = "https://api.gdc.cancer.gov/cases"
filters = {
    "op": "=",
    "content": {
        "field": "disease_type",
        "value": "*myeloid leukemia*"
    }
}

# Define the fields to be returned
fields = [
    "submitter_id",
    "case_id",
    "primary_site",
    "disease_type",
    "diagnoses.age_at_diagnosis",
    "diagnoses.primary_diagnosis",
    "demographic.gender",
    "exposures.tobacco_smoking_status",
    "files.file_id",
    "files.file_name",
    "files.data_type",
    "files.experimental_strategy"
]

# Initialize pagination variables
all_cases = []
current_page = 1
page_size = 1000

while True:
    # Construct the request parameters
    params = {
        "filters": json.dumps(filters),
        "fields": ",".join(fields),
        "format": "JSON",
        "size": page_size,
        "from": (current_page - 1) * page_size
    }

    # Send the request
    response = requests.get(endpoint, params=params)

    # Check for successful response
    if response.status_code == 200:
        data = response.json()
        cases = data["data"]["hits"]
        all_cases.extend(cases)
        if len(cases) < page_size:
            break
        current_page += 1
    else:
        print(f"Error: {response.status_code} - {response.text}")
        break

# Convert the results to a DataFrame
cases_df = pd.DataFrame(json_normalize(all_cases))
print(f"There are {len(cases_df)} cases in GDC for AML")
# Display the DataFrame
cases_df.head()
```

## Example 3: Get all cases from GDC with no filters. Fetch only the case ids and paginate through the results to fetch all available cases. Store the results as a dataframe

```
import requests
import json
import pandas as pd
from pandas import json_normalize

# Define the fields to be returned
fields = [
    "case_id",
]

# Initialize pagination variables
all_cases = []
current_page = 1
page_size = 1000

while True:
    # Construct the request parameters
    params = {
        "fields": ",".join(fields),
        "format": "JSON",
        "size": page_size,
        "from": (current_page - 1) * page_size
    }

    # Send the request
    response = requests.get(endpoint, params=params)

    # Check for successful response
    if response.status_code == 200:
        data = response.json()
        cases = data["data"]["hits"]
        all_cases.extend(cases)
        if len(cases) < page_size:
            break
        current_page += 1
    else:
        print(f"Error: {response.status_code} - {response.text}")
        break

# Convert the results to a DataFrame
all_cases_df = pd.DataFrame(json_normalize(all_cases))
print(f"There are {len(all_cases_df)} cases in GDC in total")
# Display the DataFrame
all_cases_df.head()
```

## Example 4: Get simple somatic mutation occurrences (cases) from GDC where the primary site is bronchus and lung, the gender is male, the age at diagnosis is less than 45 years old, and the patient is a lifelong non-smoker. Return the results as a pandas dataframe.

```
import pandas as pd
from pandas import json_normalize

import requests
import json

# Define the endpoint and filters
endpoint = "https://api.gdc.cancer.gov/ssm_occurrences"
filters = {
    "op": "and",
    "content": [
        {
            "op": "in",
            "content": {
                "field": "case.primary_site",
                "value": ["Bronchus and lung"]
            }
        },
        {
            "op": "in",
            "content": {
                "field": "case.demographic.gender",
                "value": ["male"]
            }
        },
        {
            "op": "<",
            "content": {
                "field": "case.diagnoses.age_at_diagnosis",
                "value": 16436 # 45 years in days
            }
        },
        {
            "op": "in",
            "content": {
                "field": "case.exposures.tobacco_smoking_status",
                "value": ["Lifelong Non-smoker"]
            }
        }
    ]
}

# Define the fields to be returned
fields = [
    "ssm_id",
    "ssm.consequence.transcript.gene.symbol",
    "ssm.mutation_type",
    "ssm.genomic_dna_change",
    "ssm.consequence.transcript.aa_change",
    "ssm.consequence.transcript.consequence_type",
    "case.project.project_id",
    "case.submitter_id",
    "case.case_id",
    "case.diagnoses.primary_diagnosis",
    "case.primary_site",
    "case.demographic.gender",
    "case.diagnoses.age_at_diagnosis",
    "case.exposures.tobacco_smoking_status"
]

# Construct the request parameters
params = {
    "filters": json.dumps(filters),
    "fields": ",".join(fields),
    "format": "JSON",
    "size": "1000"
}

# Send the request
response = requests.get(endpoint, params=params)

# Check for successful response
if response.status_code == 200:
    data = response.json()
    # Extract and display the mutation data
    mutations = data["data"]["hits"]
    print(f"Found {len(mutations)} mutations in lung cancer cases for males under 45 who never smoked:")
    lung_mutation_df = pd.DataFrame(json_normalize(mutations))
else:
    print(f"Error: {response.status_code} - {response.text}")
  
lung_mutation_df.head()
```