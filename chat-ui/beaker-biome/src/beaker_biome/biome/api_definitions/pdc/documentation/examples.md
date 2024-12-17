# Examples

## Example 1: obtain quantitative mass spec data on a specific protein (STAT5)

```
import requests
import json

url = 'https://pdc.cancer.gov/graphql'

# Query for STAT5B protein expression data
query = """
query ($gene_name: String!) {
  getPaginatedUIGeneAliquotSpectralCount(gene_name: $gene_name, offset: 0, limit: 10) {
    total
    uiGeneAliquotSpectralCounts {
      aliquot_id
      plex
      experiment_type
      spectral_count
      distinct_peptide
      unshared_peptide
      precursor_area
      log2_ratio
    }
  }
}
"""

variables = {
    "gene_name": "STAT5B"
}

try:
    response = requests.post(url, json={'query': query, 'variables': variables})
    response.raise_for_status()
    data = response.json()
    print("STAT5B Protein Expression Data:")
    print(json.dumps(data, indent=2))
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON response: {e}")
    print("Response content:", response.text)
```

## Example 2: obtain quantitative data

```
import requests
import json

url = 'https://pdc.cancer.gov/graphql'

# Corrected query structure
query = """
query ($gene_name: String!) {
  getPaginatedUIGeneAliquotSpectralCount(
    gene_name: $gene_name,
    offset: 0,
    limit: 10
  ) {
    total
    uiGeneAliquotSpectralCounts {
      aliquot_id
      plex
      experiment_type
      spectral_count
      distinct_peptide
      unshared_peptide
      log2_ratio
      study_submitter_id
    }
  }
}
"""

def print_results(data, gene_name):
    if 'data' in data and 'getPaginatedUIGeneAliquotSpectralCount' in data['data']:
        results = data['data']['getPaginatedUIGeneAliquotSpectralCount']
        total = results['total']
        samples = results['uiGeneAliquotSpectralCounts']
        
        print(f"\n{gene_name} Results:")
        print(f"Total samples available: {total}")
        print("\nSample details (first 10 samples):")
        
        for i, sample in enumerate(samples):
            print(f"\nSample {i+1}:")
            print(f"  Study ID: {sample['study_submitter_id']}")
            print(f"  Experiment Type: {sample['experiment_type']}")
            print(f"  Spectral Count: {sample['spectral_count']}")
            print(f"  Distinct Peptides: {sample['distinct_peptide']}")
            print(f"  Unshared Peptides: {sample['unshared_peptide']}")
            print(f"  Log2 Ratio: {sample['log2_ratio']}")
            print(f"  Plex: {sample['plex']}")

try:
    # Query STAT5A
    response = requests.post(url, json={'query': query, 'variables': {'gene_name': 'STAT5A'}})
    response.raise_for_status()
    stat5a_data = response.json()
    print_results(stat5a_data, 'STAT5A')
    
    # Query STAT5B
    response = requests.post(url, json={'query': query, 'variables': {'gene_name': 'STAT5B'}})
    response.raise_for_status()
    stat5b_data = response.json()
    print_results(stat5b_data, 'STAT5B')
    
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
    if hasattr(e.response, 'text'):
        print("Response content:", e.response.text)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON response: {e}")
    print("Response content:", response.text)
```    