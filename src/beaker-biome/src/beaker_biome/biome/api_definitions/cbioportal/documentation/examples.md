# Examples


## Example 1: Query and display all colorectal cancer studies from cBioPortal. This example searches for studies with cancer type IDs 'coadread', 'coad', and 'read' (representing colorectal adenocarcinoma, colon adenocarcinoma, and rectal adenocarcinoma respectively). For each study, it displays the name, study ID, description, and cancer type ID.

```
import requests

url = "https://www.cbioportal.org/api/studies"
response = requests.get(url)

if response.status_code == 200:
    studies = response.json()
    colorectal_studies = [study for study in studies if study['cancerTypeId'].lower() in ['coadread', 'coad', 'read']]
    print(f"Found {len(colorectal_studies)} colorectal cancer studies.")
    print("\nStudy Details:")
    for study in colorectal_studies:
        print(f"\nName: {study['name']}")
        print(f"Study ID: {study['studyId']}")
        print(f"Description: {study['description']}")
        print(f"Cancer Type ID: {study['cancerTypeId']}")
        print("-" * 80)
```

## Example 2: Query mutation data from cBioPortal for a specific study (Genentech colorectal cancer study) and analyze mutations in key cancer genes (APC, TP53, KRAS, PIK3CA). The example demonstrates how to:
1. Get sample IDs for a study
2. Fetch mutation data using the molecular profiles endpoint
3. Filter and analyze mutations for specific genes
4. Count mutation types and protein changes
The code provides a detailed breakdown of mutation types and frequencies for each gene.

```
import requests
import json 

# Get samples for the study
study_id = "coadread_genentech"
samples_url = f"https://www.cbioportal.org/api/studies/{study_id}/samples"
samples_response = requests.get(samples_url)

if samples_response.status_code == 200:
    samples = json.loads(samples_response.content)
    sample_ids = [sample['sampleId'] for sample in samples]
    print(f"Found {len(sample_ids)} samples")
    
    # Get mutation data
    mutations_url = f"https://www.cbioportal.org/api/molecular-profiles/{study_id}_mutations/mutations/fetch"
    
    # Create the filter with sample IDs
    data = {
        "sampleIds": sample_ids
    }
    
    # Make the POST request
    mutations_response = requests.post(mutations_url, json=data)
    
    if mutations_response.status_code == 200:
        mutations = json.loads(mutations_response.content)
        print(f"\nRetrieved {len(mutations)} mutations")
        
        # Focus on key cancer genes
        key_genes = {
            'APC': 324,    # EntrezGeneID for APC
            'TP53': 7157,  # EntrezGeneID for TP53
            'KRAS': 3845,  # EntrezGeneID for KRAS
            'PIK3CA': 5290 # EntrezGeneID for PIK3CA
        }
        
        # Analyze mutations for these genes
        gene_details = {}
        for gene_symbol, gene_id in key_genes.items():
            gene_mutations = [m for m in mutations if m['entrezGeneId'] == gene_id]
            
            # Count mutation types
            mutation_types = {}
            protein_changes = []
            
            for mutation in gene_mutations:
                mut_type = mutation['mutationType']
                if mut_type in mutation_types:
                    mutation_types[mut_type] += 1
                else:
                    mutation_types[mut_type] = 1
                    
                if mutation['proteinChange']:
                    protein_changes.append(mutation['proteinChange'])
            
            gene_details[gene_symbol] = {
                'total_mutations': len(gene_mutations),
                'mutation_types': mutation_types,
                'protein_changes': protein_changes
            }
        
        # Print detailed analysis
        print("\nDetailed Analysis of Key Cancer Genes:\n")
        for gene, details in gene_details.items():
            print(f"\n{gene} Analysis:")
            print(f"Total mutations: {details['total_mutations']}")
            
            print("Mutation types:")
            for mut_type, count in details['mutation_types'].items():
                print(f"  - {mut_type}: {count}")
                
            print("Protein changes (top 5):")
            for change in details['protein_changes'][:5]:
                print(f"  - {change}")
            if len(details['protein_changes']) > 5:
                print(f"  ... and {len(details['protein_changes'])-5} more changes")
```


## Example 3: Query for studies related to colorectal cancer using the cancerTypeId 'coadread'.

```
import requests
import pandas as pd

# cBioPortal API base URL
base_url = "https://www.cbioportal.org/api"

# Endpoint to fetch studies
endpoint = "/studies"

# Parameters for the query
params = {"cancerTypeId": "coadread"}

# Make the API request
response = requests.get(base_url + endpoint, params=params)

# Check for successful response
response.raise_for_status()

# Parse the JSON response
studies = response.json()

# Create a pandas DataFrame from the results
df = pd.DataFrame(studies)

# Print the DataFrame
print(df)
```
