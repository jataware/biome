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


## Example 4: Fetch and filter studies related to Acute Myeloid Leukemia (AML) from cBioPortal API.

```
import requests
import pandas as pd

def fetch_aml_studies():
    # Base URL for cBioPortal API
    base_url = "https://www.cbioportal.org/api"
    
    # Get all studies
    response = requests.get(f"{base_url}/studies")
    
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}")
    
    # Get all studies as JSON
    studies = response.json()
    
    # Filter for AML related studies
    aml_studies = []
    for study in studies:
        # Convert all fields to lowercase for case-insensitive search
        study_id = study.get('studyId', '').lower()
        name = study.get('name', '').lower()
        cancer_type = study.get('cancerTypeId', '').lower()
        description = study.get('description', '').lower()
        
        # Check if 'aml' appears in any of the relevant fields
        if any('aml' in field for field in [study_id, name, cancer_type, description]):
            aml_studies.append({
                'studyId': study['studyId'],
                'name': study['name'],
                'description': study.get('description', 'N/A'),
                'cancerTypeId': study.get('cancerTypeId', 'N/A'),
                'sampleCount': study.get('allSampleCount', 0),
                'status': study.get('status', 'N/A'),
                'publicStudy': study.get('publicStudy', False)
            })
    
    # Convert to DataFrame for better display
    df = pd.DataFrame(aml_studies)
    
    # Sort by sample count descending
    df = df.sort_values('sampleCount', ascending=False)
    
    return df

# Execute the function
aml_studies_df = fetch_aml_studies()
print(f"Found {len(aml_studies_df)} AML-related studies")
print(aml_studies_df)
```


## Example 5: This example demonstrates how to fetch and analyze mutation data for a specific study in cBioPortal. It shows:
1. How to properly construct the API endpoint URL with sample list ID
2. How to fetch mutation data for a study
3. How to get gene symbol information using entrez IDs
4. How to create a comprehensive mutation analysis including:
   - Total mutation counts
   - Gene frequency analysis
   - Mutation type distribution
   - Sample statistics
The example uses the TARGET AML (GDC) study but can be modified for any study by changing the study_id.

```
import requests
import pandas as pd
from collections import Counter
import numpy as np

# Base URL for cBioPortal API
base_url = "https://www.cbioportal.org/api"
study_id = "aml_target_gdc"  # Example study ID

# Get mutations using the sample list ID
mutations_url = f"{base_url}/molecular-profiles/{study_id}_mutations/mutations?sampleListId={study_id}_all"
mutations_response = requests.get(mutations_url)

if mutations_response.status_code == 200:
    mutations_data = mutations_response.json()
    mutations_df = pd.DataFrame(mutations_data)
    
    # Get gene information for the entrez IDs
    entrez_ids = [int(x) for x in mutations_df['entrezGeneId'].unique()]  # Convert to regular Python integers
    genes_url = f"{base_url}/genes/fetch"
    genes_response = requests.post(genes_url, json=entrez_ids)
    
    if genes_response.status_code == 200:
        genes_data = genes_response.json()
        gene_map = {gene['entrezGeneId']: gene['hugoGeneSymbol'] for gene in genes_data}
        
        # Add gene symbols to mutations dataframe
        mutations_df['gene_symbol'] = mutations_df['entrezGeneId'].map(gene_map)
        
        # Print summary statistics
        print(f"Total mutations found: {len(mutations_df)}")
        print(f"Number of affected genes: {len(mutations_df['gene_symbol'].unique())}")
        
        print("\nMost frequently mutated genes:")
        print(mutations_df['gene_symbol'].value_counts().head(10))
        
        print("\nMutation types distribution:")
        print(mutations_df['mutationType'].value_counts())
        
        print("\nSample of mutations (first 5 rows):")
        display_cols = ['gene_symbol', 'sampleId', 'mutationType', 'proteinChange', 'chr', 'startPosition', 'variantType']
        print(mutations_df[display_cols].head())
        
        # Calculate sample statistics
        samples_with_mutations = len(mutations_df['sampleId'].unique())
        print(f"\nNumber of samples with mutations: {samples_with_mutations}")
        
        avg_mutations_per_sample = len(mutations_df) / samples_with_mutations
        print(f"Average mutations per sample: {avg_mutations_per_sample:.2f}")
else:
    print(f"Error fetching mutations: {mutations_response.status_code}")
    print("Response:", mutations_response.text)
```


## Example 6: Retrieve and analyze mutation data from multiple AML studies, including data processing and summary statistics. This example demonstrates how to fetch mutations across multiple studies, handle the nested JSON response, and create a comprehensive mutation dataset with key information.

```
import requests
import pandas as pd
import json

# Base URL
BASE_URL = "https://www.cbioportal.org/api"

# List of AML studies
AML_STUDIES = [
    'aml_target_2018_pub',
    'aml_ohsu_2018', 
    'aml_ohsu_2022',
    'laml_tcga',
    'laml_tcga_pan_can_atlas_2018',
    'laml_tcga_gdac',
    'aml_target_gdc',
    'washu_pdi_2016',
    'laml_tcga_pub'
]

# Function to get mutations for a study
def get_study_mutations(study_id):
    print(f"\nProcessing study: {study_id}")
    
    # Get the molecular profile ID
    molecular_profile_id = f"{study_id}_mutations"
    
    # Get the sample list ID
    sample_list_id = f"{study_id}_all"
    
    # Fetch mutations
    mutations_response = requests.get(
        f"{BASE_URL}/molecular-profiles/{molecular_profile_id}/mutations",
        params={"sampleListId": sample_list_id, "projection": "DETAILED"}
    )
    
    if mutations_response.status_code == 200:
        mutations = mutations_response.json()
        print(f"Found {len(mutations)} mutations")
        
        # Convert to DataFrame
        mutations_df = pd.DataFrame(mutations)
        
        # Extract gene symbols from the nested dictionary
        mutations_df['gene_symbol'] = mutations_df['gene'].apply(lambda x: x['hugoGeneSymbol'])
        
        # Create a more focused DataFrame with key columns
        focused_df = mutations_df[[
            'gene_symbol',
            'sampleId',
            'proteinChange',
            'mutationType',
            'chr',
            'startPosition',
            'endPosition',
            'referenceAllele',
            'variantAllele'
        ]]
        
        return focused_df
    else:
        print(f"Error fetching mutations: {mutations_response.text}")
        return None

# Process all studies
all_mutations_dfs = []

for study_id in AML_STUDIES:
    study_df = get_study_mutations(study_id)
    if study_df is not None:
        study_df['study_id'] = study_id  # Add study ID column
        all_mutations_dfs.append(study_df)

# Combine all mutations
if all_mutations_dfs:
    combined_df = pd.concat(all_mutations_dfs, ignore_index=True)
    
    print("\nOverall mutation data summary:")
    print(f"Total number of mutations: {len(combined_df)}")
    print(f"Number of unique genes: {combined_df['gene_symbol'].nunique()}")
    print(f"Number of unique samples: {combined_df['sampleId'].nunique()}")
    
    print("\nTop 20 most frequently mutated genes across all studies:")
    print(combined_df['gene_symbol'].value_counts().head(20))
    
    print("\nDistribution of mutation types:")
    print(combined_df['mutationType'].value_counts())
    
    print("\nNumber of mutations by study:")
    print(combined_df['study_id'].value_counts())
    
    # Save to CSV
    combined_df.to_csv('all_aml_mutations.csv', index=False)
```


## Example 7: Example showing how to retrieve and analyze the molecular profiles available for multiple studies from cBioPortal. The code demonstrates how to fetch metadata on the molecular profiles, organize them into DataFrames, and analyze specific information about each profile like the types of profiles available such as RNA expression.

```
import requests
import pandas as pd
from typing import List, Dict

def get_molecular_profiles(study_ids: List[str]) -> Dict[str, pd.DataFrame]:
    """
    Retrieve molecular profiles for multiple studies from cBioPortal.
    
    Args:
        study_ids: List of cBioPortal study IDs
        
    Returns:
        Dictionary mapping study IDs to DataFrames containing their molecular profiles
    """
    # Base URL for cBioPortal's web API
    base_url = "https://www.cbioportal.org/api"
    
    # Dictionary to store results
    results = {}
    
    print("Fetching molecular profiles...")
    for study_id in study_ids:
        print(f"\nStudy: {study_id}")
        print("-" * 40)
        
        # Get molecular profiles for this study
        response = requests.get(f"{base_url}/studies/{study_id}/molecular-profiles")
        
        if response.status_code == 200:
            profiles = response.json()
            
            # Create a summary DataFrame
            profile_data = []
            for profile in profiles:
                profile_data.append({
                    'molecularProfileId': profile['molecularProfileId'],
                    'name': profile['name'],
                    'datatype': profile['datatype'],
                    'molecularAlterationType': profile['molecularAlterationType'],
                    'description': profile.get('description', 'N/A')
                })
            
            if profile_data:
                df = pd.DataFrame(profile_data)
                results[study_id] = df
                print(f"Found {len(df)} molecular profiles")
                
                # Display summary of profile types
                print("\nProfile types:")
                type_summary = df.groupby('molecularAlterationType')['molecularProfileId'].count()
                print(type_summary)
            else:
                print("No molecular profiles found")
                results[study_id] = pd.DataFrame()
        else:
            print(f"Error accessing study: {response.status_code}")
            results[study_id] = pd.DataFrame()
    
    return results

# Example usage with AML studies
aml_studies = [
    'aml_target_2018_pub',
    'aml_ohsu_2018', 
    'aml_ohsu_2022',
    'laml_tcga',
    'laml_tcga_pan_can_atlas_2018',
    'aml_target_gdc',
    'mnm_washu_2016'
]

# Get molecular profiles for all studies
profiles_by_study = get_molecular_profiles(aml_studies)

# Example of how to work with the results - get RNA expression profiles for first study
first_study = list(profiles_by_study.keys())[0]
if not profiles_by_study[first_study].empty:
    rna_profiles = profiles_by_study[first_study][
        profiles_by_study[first_study]['molecularAlterationType'] == 'MRNA_EXPRESSION'
    ]
    print(f"\nRNA expression profiles for {first_study}:")
    print(rna_profiles[['molecularProfileId', 'name', 'datatype']].to_string())
```


## Example 8: Example of how to fetch RNA-seq z-scores for STAT5A and STAT5B across multiple AML studies. This example demonstrates:
1. How to properly fetch sample IDs for each study
2. How to use these sample IDs when requesting molecular data
3. How to handle large requests by processing samples in chunks
4. How to combine data from multiple studies into a single dataframe
5. How to create both long and wide format versions of the data

Key points:
- Must provide explicit sample IDs in the molecular data request
- Z-scores are pre-calculated by cBioPortal for each study
- Different studies may use different measurement types (TPM, RPKM, RSEM)
- Processing in chunks helps avoid timeouts with large datasets

```
import requests
import pandas as pd
import time

# Configuration
BASE_URL = "https://www.cbioportal.org/api"

# Define studies and their RNA-seq profiles
STUDY_PROFILES = {
    'aml_target_gdc': {
        'name': 'TARGET-AML (GDC)',
        'profile': 'aml_target_gdc_mrna_seq_tpm_Zscores',
        'type': 'TPM'
    },
    'aml_ohsu_2022': {
        'name': 'OHSU AML 2022',
        'profile': 'aml_ohsu_2022_mrna_median_Zscores',
        'type': 'RPKM'
    }
    # ... other studies ...
}

# Define STAT5 genes with their Entrez IDs
STAT5_GENES = {
    6776: 'STAT5A',
    6777: 'STAT5B'
}

# Function to get RNA-seq samples for a study
def get_rna_seq_samples(study_id):
    """Get list of sample IDs that have RNA-seq data for a study."""
    url = f"{BASE_URL}/studies/{study_id}/sample-lists"
    response = requests.get(url)
    if response.status_code == 200:
        sample_lists = response.json()
        # Find RNA-seq sample list
        rna_list = next((sl['sampleListId'] for sl in sample_lists 
                        if sl['category'] == 'all_cases_with_mrna_rnaseq_data'), None)
        if rna_list:
            # Get sample IDs from the list
            url = f"{BASE_URL}/sample-lists/{rna_list}/sample-ids"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
    return None

# Function to get expression data
def get_expression_data(profile_id, gene_ids, sample_ids):
    """Fetch expression z-scores for specific genes and samples."""
    url = f"{BASE_URL}/molecular-profiles/{profile_id}/molecular-data/fetch"
    # IMPORTANT: Must provide sample IDs explicitly
    data = {
        "sampleIds": sample_ids,  # List of specific sample IDs
        "entrezGeneIds": gene_ids  # List of Entrez gene IDs
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    return None

# Process each study
all_study_data = []

for study_id, study_info in STUDY_PROFILES.items():
    print(f"\nProcessing {study_info['name']}...")
    
    # First get the sample IDs for the study
    sample_ids = get_rna_seq_samples(study_id)
    
    if sample_ids:
        print(f"Found {len(sample_ids)} RNA-seq samples")
        
        # Process samples in chunks to avoid large requests
        chunk_size = 100
        study_data = []
        
        for i in range(0, len(sample_ids), chunk_size):
            chunk = sample_ids[i:i + chunk_size]
            print(f"Fetching data for samples {i+1}-{i+len(chunk)}...")
            
            # Get expression data for this chunk of samples
            expression_data = get_expression_data(
                study_info['profile'], 
                list(STAT5_GENES.keys()), 
                chunk
            )
            
            if expression_data:
                study_data.extend(expression_data)
            time.sleep(0.2)  # Small delay between requests
        
        if study_data:
            # Convert to DataFrame
            df = pd.DataFrame(study_data)
            
            # Add metadata
            df['gene_symbol'] = df['entrezGeneId'].map(STAT5_GENES)
            df['study_id'] = study_id
            df['study_name'] = study_info['name']
            df['measurement_type'] = study_info['type']
            
            # Select and rename columns
            df = df[[
                'study_id', 'study_name', 'measurement_type',
                'gene_symbol', 'sampleId', 'value'
            ]]
            df.columns = [
                'study_id', 'study_name', 'measurement_type',
                'gene', 'sample_id', 'zscore'
            ]
            
            all_study_data.append(df)

# Combine all data
if all_study_data:
    # Create long format
    combined_df = pd.concat(all_study_data, ignore_index=True)
    
    # Create wide format (samples as rows, genes as columns)
    combined_wide = combined_df.pivot_table(
        index=['study_id', 'study_name', 'measurement_type', 'sample_id'],
        columns='gene',
        values='zscore'
    ).reset_index()
    
    # Save both versions
    stat5_all_studies = combined_df  # Long format
    stat5_all_studies_wide = combined_wide  # Wide format

# Example of the resulting data structure:
print("\nLong format example (first few rows):")
print(stat5_all_studies.head())

print("\nWide format example (first few rows):")
print(stat5_all_studies_wide.head())
```
