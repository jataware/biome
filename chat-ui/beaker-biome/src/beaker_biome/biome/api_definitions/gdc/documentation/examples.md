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
```# Examples

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