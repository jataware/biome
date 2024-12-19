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
