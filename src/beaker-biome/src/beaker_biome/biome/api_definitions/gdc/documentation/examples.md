# Examples

## Example 1: search based on disease type and gene mutation

```
import requests
import json

# Define the endpoint and filters
endpoint = "https://api.gdc.cancer.gov/ssms"
filters = {
    "op": "and",
    "content": [
        {
            "op": "regexp",
            "content": {
                "field": "cases.diagnoses.primary_diagnosis",
                "value": ".*acute myeloid leukemia.*"
            }
        },
        {
            "op": "in",
            "content": {
                "field": "consequence.transcript.gene.symbol",
                "value": ["JAK2"]
            }
        }
    ]
}

# Define the fields to be returned
fields = [
    "ssm_id",
    "consequence.transcript.gene.symbol",
    "mutation_type",
    "genomic_dna_change",
    "consequence.transcript.aa_change",
    "consequence.transcript.consequence_type",
    "occurrence.case.project.project_id",
    "occurrence.case.submitter_id"
]

# Construct the request parameters
params = {
    "filters": json.dumps(filters),
    "fields": ",".join(fields),
    "format": "JSON",
    "size": "100"
}

# Send the request
response = requests.get(endpoint, params=params)

# Check for successful response
if response.status_code == 200:
    data = response.json()
    # Extract and display the mutation data
    mutations = data["data"]["hits"]
    print(f"Found {len(mutations)} JAK2 mutations in AML cases:")
    for i, mutation in enumerate(mutations[:10]):  # Display the first 10 mutations
        print(f"\nMutation {i+1}:")
        print(f"    Mutation ID: {mutation['ssm_id']}")
        print(f"    Gene: {mutation['consequence'][0]['transcript']['gene']['symbol']}")
        print(f"    Mutation Type: {mutation['mutation_type']}")
        print(f"    Genomic Change: {mutation['genomic_dna_change']}")
        print(f"    Amino Acid Change: {mutation['consequence'][0]['transcript'].get('aa_change', 'Not available')}")
        print(f"    Consequence Type: {mutation['consequence'][0]['transcript'].get('consequence_type', 'Not available')}")
        print(f"    Project ID: {mutation['occurrence'][0]['case']['project']['project_id']}")
        print(f"    Case ID: {mutation['occurrence'][0]['case'].get('submitter_id', 'Not available')}")
else:
    print(f"Error: {response.status_code} - {response.text}")
```

## Example 2: search based on disease type and gene mutation

```
import requests
import json

# Define the endpoint and filters
endpoint = "https://api.gdc.cancer.gov/ssms"
filters = {
    "op": "and",
    "content": [
        {
            "op": "regexp",
            "content": {
                "field": "cases.diagnoses.primary_diagnosis",
                "value": ".*acute myeloid leukemia.*"
            }
        },
        {
            "op": "in",
            "content": {
                "field": "consequence.transcript.gene.symbol",
                "value": ["JAK2"]
            }
        }
    ]
}

# Define the fields to be returned
fields = [
    "ssm_id",
    "consequence.transcript.gene.symbol",
    "mutation_type",
    "genomic_dna_change",
    "consequence.transcript.aa_change",
    "consequence.transcript.consequence_type",
    "occurrence.case.project.project_id",
    "occurrence.case.submitter_id"
]

# Construct the request parameters
params = {
    "filters": json.dumps(filters),
    "fields": ",".join(fields),
    "format": "JSON",
    "size": "100"
}

# Send the request
response = requests.get(endpoint, params=params)

# Check for successful response
if response.status_code == 200:
    data = response.json()
    # Extract and display the mutation data
    mutations = data["data"]["hits"]
    print(f"Found {len(mutations)} JAK2 mutations in AML cases:")
    for i, mutation in enumerate(mutations[:10]):  # Display the first 10 mutations
        print(f"\nMutation {i+1}:")
        print(f"    Mutation ID: {mutation['ssm_id']}")
        print(f"    Gene: {mutation['consequence'][0]['transcript']['gene']['symbol']}")
        print(f"    Mutation Type: {mutation['mutation_type']}")
        print(f"    Genomic Change: {mutation['genomic_dna_change']}")
        print(f"    Amino Acid Change: {mutation['consequence'][0]['transcript'].get('aa_change', 'Not available')}")
        print(f"    Consequence Type: {mutation['consequence'][0]['transcript'].get('consequence_type', 'Not available')}")
        print(f"    Project ID: {mutation['occurrence'][0]['case']['project']['project_id']}")
        print(f"    Case ID: {mutation['occurrence'][0]['case'].get('submitter_id', 'Not available')}")
else:
    print(f"Error: {response.status_code} - {response.text}")
```

## Example 3: Get total count of specific mutations for a specific disease type in GDC

```
import requests
import json
from collections import Counter

# Define the endpoint and filters
endpoint = "https://api.gdc.cancer.gov/ssms"
filters = {
    "op": "and",
    "content": [
        {
            "op": "regexp",
            "content": {
                "field": "cases.diagnoses.primary_diagnosis",
                "value": ".*acute myeloid leukemia.*"
            }
        },
        {
            "op": "in",
            "content": {
                "field": "consequence.transcript.gene.symbol",
                "value": ["JAK2"]
            }
        }
    ]
}

# Define the fields to be returned
fields = [
    "ssm_id",
    "consequence.transcript.gene.symbol",
    "mutation_type",
    "consequence.transcript.aa_change",
    "consequence.transcript.consequence_type"
]

# First, get the total count
params = {
    "filters": json.dumps(filters),
    "fields": ",".join(fields),
    "format": "JSON",
    "size": "0"  # Set size to 0 to just get the total
}

response = requests.get(endpoint, params=params)

if response.status_code == 200:
    total_mutations = response.json()["data"]["pagination"]["total"]
    print(f"\nTotal number of JAK2 mutations in AML cases: {total_mutations}")
    
    # Now get all mutations to analyze types
    params["size"] = str(total_mutations)  # Get all mutations
    response = requests.get(endpoint, params=params)
    data = response.json()
    mutations = data["data"]["hits"]
    
    # Analyze mutation types
    consequence_types = []
    for mutation in mutations:
        if mutation.get('consequence'):
            cons_type = mutation['consequence'][0]['transcript'].get('consequence_type', 'Unknown')
            consequence_types.append(cons_type)
    
    # Count frequency of each type
    type_counts = Counter(consequence_types)
    
    print("\nBreakdown of mutation types:")
    for mut_type, count in type_counts.most_common():
        percentage = (count / len(consequence_types)) * 100
        print(f"    {mut_type}: {count} mutations ({percentage:.1f}%)")
        
else:
    print(f"Error: {response.status_code} - {response.text}")
```

## Example 4: Query somatic gene mutations for lung cancer cases in males under age 45 who never smoked using the Genomics Data Commons API.

```
import requests
import json

# Define the endpoint and filters
endpoint = "https://api.gdc.cancer.gov/ssms"
filters = {
    "op": "and",
    "content": [
        {
            "op": "in",
            "content": {
                "field": "cases.primary_site",
                "value": ["Bronchus and lung"]
            }
        },
        {
            "op": "in",
            "content": {
                "field": "cases.demographic.gender",
                "value": ["male"]
            }
        },
        {
            "op": "<",
            "content": {
                "field": "cases.diagnoses.age_at_diagnosis",
                "value": 16436 # 45 years in days
            }
        },
        {
            "op": "in",
            "content": {
                "field": "cases.exposures.tobacco_smoking_status",
                "value": ["Lifelong Non-smoker"]
            }
        }
    ]
}

# Define the fields to be returned
fields = [
    "ssm_id",
    "consequence.transcript.gene.symbol",
    "mutation_type",
    "genomic_dna_change",
    "consequence.transcript.aa_change",
    "consequence.transcript.consequence_type",
    "occurrence.case.project.project_id",
    "occurrence.case.submitter_id"
]

# Construct the request parameters
params = {
    "filters": json.dumps(filters),
    "fields": ",".join(fields),
    "format": "JSON",
    "size": "100"
}

# Send the request
response = requests.get(endpoint, params=params)

# Check for successful response
if response.status_code == 200:
    data = response.json()
    # Extract and display the mutation data
    mutations = data["data"]["hits"]
    print(f"Found {len(mutations)} mutations in lung cancer cases for males under 45 who never smoked:")
    for i, mutation in enumerate(mutations[:10]):  # Display the first 10 mutations
        print(f"\nMutation {i+1}:")
        print(f"    Mutation ID: {mutation['ssm_id']}")
        print(f"    Gene: {mutation['consequence'][0]['transcript']['gene']['symbol']}")
        print(f"    Mutation Type: {mutation['mutation_type']}")
        print(f"    Genomic Change: {mutation['genomic_dna_change']}")
        print(f"    Amino Acid Change: {mutation['consequence'][0]['transcript'].get('aa_change', 'Not available')}")
        print(f"    Consequence Type: {mutation['consequence'][0]['transcript'].get('consequence_type', 'Not available')}")
        print(f"    Project ID: {mutation['occurrence'][0]['case']['project']['project_id']}")
        print(f"    Case ID: {mutation['occurrence'][0]['case'].get('submitter_id', 'Not available')}")
else:
    print(f"Error: {response.status_code} - {response.text}")
```

## Example 5: Paginate through results to retrieve all somatic gene mutations for lung cancer cases in males under age 45 who never smoked using GDC API.

```
import requests
import json

# Define the endpoint and filters
endpoint = "https://api.gdc.cancer.gov/ssms"
filters = {
    "op": "and",
    "content": [
        {
            "op": "in",
            "content": {
                "field": "cases.primary_site",
                "value": ["Bronchus and lung"]
            }
        },
        {
            "op": "in",
            "content": {
                "field": "cases.demographic.gender",
                "value": ["male"]
            }
        },
        {
            "op": "<",
            "content": {
                "field": "cases.diagnoses.age_at_diagnosis",
                "value": 16436  # 45 years in days
            }
        },
        {
            "op": "in",
            "content": {
                "field": "cases.exposures.tobacco_smoking_status",
                "value": ["Lifelong Non-smoker"]
            }
        }
    ]
}

# Define the fields to be returned
fields = [
    "ssm_id",
    "case.submitter_id",
    "consequence.transcript.gene.symbol",
    "mutation_type",
    "genomic_dna_change",
    "consequence.transcript.aa_change",
    "consequence.transcript.consequence_type"
]

# Initialize variables for pagination
all_mutations = []
current_page = 0
page_size = 100

while True:
    # Construct the request parameters
    params = {
        "filters": json.dumps(filters),
        "fields": ",".join(fields),
        "format": "JSON",
        "size": str(page_size),
        "from": str(current_page * page_size)
    }

    # Send the request
    response = requests.get(endpoint, params=params)

    # Check for successful response
    if response.status_code == 200:
        data = response.json()
        # Extract the mutation data
        mutations = data["data"]["hits"]
        all_mutations.extend(mutations)
        
        # Break if no more mutations are found
        if len(mutations) < page_size:
            break
        
        # Increment the page
        current_page += 1
    else:
        print(f"Error: {response.status_code} - {response.text}")
        break

print(f"Found a total of {len(all_mutations)} mutations in lung cancer cases for males under 45 who never smoked")
```


## Example 6: Query GDC API for lung cancer cases with specific clinical characteristics (age, gender, smoking status) and associated mutation data. This example demonstrates how to:
1. Set up complex filters for multiple clinical criteria
2. Request specific fields including clinical data and associated files
3. Process and display the results in a readable format
4. Handle cases where certain data fields might be missing

```
import requests
import json

# Define the fields we want to retrieve
fields = [
    "submitter_id",
    "case_id",
    "primary_site",
    "disease_type",
    "diagnoses.age_at_diagnosis",
    "demographic.gender",
    "exposures.tobacco_smoking_status",
    "files.file_id",
    "files.file_name",
    "files.data_type",
    "files.experimental_strategy"
]

fields = ','.join(fields)

cases_endpt = "https://api.gdc.cancer.gov/cases"

# Define filters for:
# - Lung cancer cases
# - Male patients
# - Under 45 years old
filters = {
    "op": "and",
    "content":[
        {
        "op": "in",
        "content":{
            "field": "primary_site",
            "value": ["Bronchus and lung"]
            }
        },
        {
        "op": "in",
        "content":{
            "field": "demographic.gender",
            "value": ["male"]
            }
        },
        {
        "op": "<",
        "content":{
            "field": "diagnoses.age_at_diagnosis",
            "value": 16436  # 45 years in days
            }
        }
    ]
}

# Set up the API request parameters
params = {
    "filters": json.dumps(filters),
    "fields": fields,
    "format": "JSON",
    "expand": "files",  # Include associated files
    "size": "100"
}

# Make the API request
response = requests.post(cases_endpt, headers = {"Content-Type": "application/json"}, json = params)
response_data = response.json()

# Print results
print(f"Total cases found: {response_data['data']['pagination']['total']}")

# Process and display the results
for case in response_data['data']['hits']:
    print("\nCase Details:")
    print(f"Case ID: {case['case_id']}")
    print(f"Disease Type: {case['disease_type']}")
    age_in_years = round(case['diagnoses'][0]['age_at_diagnosis'] / 365.25, 1) if 'diagnoses' in case else "Not specified"
    print(f"Age at Diagnosis (years): {age_in_years}")
    print(f"Gender: {case['demographic']['gender']}")
    
    # Print smoking status if available
    if 'exposures' in case and len(case['exposures']) > 0:
        print(f"Smoking Status: {case['exposures'][0].get('tobacco_smoking_status', 'Not specified')}")
    else:
        print("Smoking Status: Not available")
    
    # Print mutation files if available
    if 'files' in case:
        mutation_files = [f for f in case['files'] if f.get('data_type') == "Simple Somatic Mutation"]
        if mutation_files:
            print("Mutation Files Available:")
            for file in mutation_files:
                print(f"  - {file['file_name']} ({file['data_type']})")
    print("-" * 50)
```


## Example 7: Query the GDC API for somatic gene mutations in lung cancer patients who are men under age 45 at diagnosis and never smoked.

```
import requests
import json

# Define the endpoint and filters
endpoint = "https://api.gdc.cancer.gov/ssms"
filters = {
    "op": "and",
    "content": [
        {
            "op": "in",
            "content": {
                "field": "cases.primary_site",
                "value": ["Bronchus and lung"]
            }
        },
        {
            "op": "in",
            "content": {
                "field": "cases.demographic.gender",
                "value": ["male"]
            }
        },
        {
            "op": "<",
            "content": {
                "field": "cases.diagnoses.age_at_diagnosis",
                "value": 16436 # 45 years in days
            }
        },
        {
            "op": "in",
            "content": {
                "field": "cases.exposures.tobacco_smoking_status",
                "value": ["Lifelong Non-smoker"]
            }
        }
    ]
}

# Define the fields to be returned
fields = [
    "ssm_id",
    "consequence.transcript.gene.symbol",
    "mutation_type",
    "genomic_dna_change",
    "consequence.transcript.aa_change",
    "consequence.transcript.consequence_type",
    "occurrence.case.project.project_id",
    "occurrence.case.submitter_id"
]

# Construct the request parameters
params = {
    "filters": json.dumps(filters),
    "fields": ",".join(fields),
    "format": "JSON",
    "size": "100"
}

# Send the request
response = requests.get(endpoint, params=params)

# Check for successful response
if response.status_code == 200:
    data = response.json()
    # Extract and display the mutation data
    mutations = data["data"]["hits"]
    print(f"Found {len(mutations)} mutations in lung cancer cases for males under 45 who never smoked:")
    for i, mutation in enumerate(mutations[:10]):  # Display the first 10 mutations
        print(f"\nMutation {i+1}:")
        print(f"    Mutation ID: {mutation['ssm_id']}")
        print(f"    Gene: {mutation['consequence'][0]['transcript']['gene']['symbol']}")
        print(f"    Mutation Type: {mutation['mutation_type']}")
        print(f"    Genomic Change: {mutation['genomic_dna_change']}")
        print(f"    Amino Acid Change: {mutation['consequence'][0]['transcript'].get('aa_change', 'Not available')}")
        print(f"    Consequence Type: {mutation['consequence'][0]['transcript'].get('consequence_type', 'Not available')}")
        print(f"    Project ID: {mutation['occurrence'][0]['case']['project']['project_id']}")
        print(f"    Case ID: {mutation['occurrence'][0]['case'].get('submitter_id', 'Not available')}")
else:
    print(f"Error: {response.status_code} - {response.text}")
```
