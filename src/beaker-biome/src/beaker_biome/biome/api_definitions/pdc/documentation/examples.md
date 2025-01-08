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

## Example 3: Load samples into a pandas dataframe

```
import requests
import json
import pandas as pd

url = 'https://pdc.cancer.gov/graphql'

# Updated query with correct schema
query = """
query ($gene_name: String!) {
  getPaginatedUIGeneAliquotSpectralCount(
    gene_name: $gene_name,
    offset: 0,
    limit: 100  # Increased limit to get more samples
  ) {
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
      study_submitter_id
    }
  }
}
"""

def get_protein_data(gene_name):
    response = requests.post(url, json={'query': query, 'variables': {'gene_name': gene_name}})
    response.raise_for_status()
    data = response.json()
    
    if 'data' in data and 'getPaginatedUIGeneAliquotSpectralCount' in data['data']:
        results = data['data']['getPaginatedUIGeneAliquotSpectralCount']
        samples = results['uiGeneAliquotSpectralCounts']
        
        # Convert to DataFrame
        df = pd.DataFrame(samples)
        # Add gene name column
        df['gene_name'] = gene_name
        return df
    return None

try:
    # Get data for both proteins
    stat5a_df = get_protein_data('STAT5A')
    stat5b_df = get_protein_data('STAT5B')
    
    # Combine the dataframes
    combined_df = pd.concat([stat5a_df, stat5b_df], ignore_index=True)
    
    # Display basic information about the dataset
    print("DataFrame Info:")
    print(combined_df.info())
    
    print("\nFirst few rows of the dataset:")
    print(combined_df.head())
    
    print("\nSummary statistics:")
    print(combined_df.describe())
    
    # Save the DataFrame for later use
    combined_df.to_csv('stat5_protein_data.csv', index=False)
    print("\nData has been saved to 'stat5_protein_data.csv'")
    
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
    if hasattr(e, 'response') and e.response is not None:
        print("Response content:", e.response.text)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON response: {e}")
    print("Response content:", response.text)
```

## Example 4: Query the Proteomics Data Commons (PDC) to find studies with primary site 'Lung' or 'Bronchus and lung' using separate queries and combining results.

```
import requests
import json

# Define the GraphQL endpoint
url = "https://pdc.cancer.gov/graphql"

# Define the GraphQL query to filter for studies with primary site "Lung" or "Bronchus and lung"
query_lung = '''
{
  getPaginatedUIStudy(primary_site: "Lung") {
    uiStudies {
      study_id
      submitter_id_name
      pdc_study_id
      disease_type
      primary_site
    }
  }
}
'''

query_bronchus_and_lung = '''
{
  getPaginatedUIStudy(primary_site: "Bronchus and lung") {
    uiStudies {
      study_id
      submitter_id_name
      pdc_study_id
      disease_type
      primary_site
    }
  }
}
'''

# Send the request for "Lung"
response_lung = requests.post(url, json={'query': query_lung})

# Send the request for "Bronchus and lung"
response_bronchus_and_lung = requests.post(url, json={'query': query_bronchus_and_lung})

lung_cancer_studies = []

# Check for successful response for "Lung"
if response_lung.status_code == 200:
    data_lung = response_lung.json()
    lung_cancer_studies.extend(data_lung['data']['getPaginatedUIStudy']['uiStudies'])
else:
    print(f"Error: {response_lung.status_code} - {response_lung.text}")

# Check for successful response for "Bronchus and lung"
if response_bronchus_and_lung.status_code == 200:
    data_bronchus_and_lung = response_bronchus_and_lung.json()
    lung_cancer_studies.extend(data_bronchus_and_lung['data']['getPaginatedUIStudy']['uiStudies'])
else:
    print(f"Error: {response_bronchus_and_lung.status_code} - {response_bronchus_and_lung.text}")

# Remove duplicates
lung_cancer_studies = {study['study_id']: study for study in lung_cancer_studies}.values()

print(f"Found {len(lung_cancer_studies)} studies with primary site 'Lung' or 'Bronchus and lung'.")
# Display the first few studies
for study in list(lung_cancer_studies)[:5]:
    print(study)
```


## Example 5: Fetch all cases based on a study name

```
import requests
import json

# Define the GraphQL endpoint
url = "https://pdc.cancer.gov/graphql"

# Define the GraphQL query to get cases for the Georgetown Lung Cancer Proteomics Study using study name
query = '''
{
  getPaginatedUICase(study_name: "Georgetown Lung Cancer Proteomics Study") {
    uiCases {
      case_id
      case_submitter_id
      disease_type
      primary_site
    }
  }
}
'''

# Send the request for cases
response = requests.post(url, json={'query': query})

# Check for successful response for cases
if response.status_code == 200:
    data_cases = response.json()
    cases_info = data_cases['data']['getPaginatedUICase']['uiCases']
    print("Cases information for the Georgetown Lung Cancer Proteomics Study:")
    print(json.dumps(cases_info, indent=2))
else:
    print(f"Error: {response.status_code} - {response.text}")
```


## Example 6: Fetch detailed information about a case using its case ID in the Proteomics Data Commons (PDC).

```
import requests
import json

# Define the GraphQL endpoint
url = "https://pdc.cancer.gov/graphql"

# Define the GraphQL query to get detailed information about a case
query = '''
{
  case(case_id: "9e8e8f51-d732-11ea-b1fd-0aad30af8a83") {
    case_id
    case_submitter_id
    disease_type
    primary_site
    demographics {
      gender
      race
      ethnicity
      age_at_index
    }
    diagnoses {
      diagnosis_id
      diagnosis_submitter_id
      tumor_stage
      tumor_grade
    }
    samples {
      sample_id
      sample_submitter_id
      sample_type
    }
  }
}
'''

# Send the request
response = requests.post(url, json={'query': query})

# Check for successful response
if response.status_code == 200:
    data = response.json()
    case_info = data['data']['case']
    print("Detailed information about the case:")
    print(json.dumps(case_info, indent=2))
else:
    print(f"Error: {response.status_code} - {response.text}")
```


## Example 7: Fetch raw mass spec data for a specific study using study name, data category, and file type in the Proteomics Data Commons (PDC).

```
import requests
import json

# Define the GraphQL endpoint
url = "https://pdc.cancer.gov/graphql"

# Define the GraphQL query to get raw mass spec data for the Georgetown Lung Cancer Proteomics Study
query = '''
{
  getPaginatedUIFile(
    study_name: "Georgetown Lung Cancer Proteomics Study",
    data_category: "Raw Mass Spectra",
    file_type: "Proprietary"
  ) {
    uiFiles {
      file_id
      file_name
      file_type
      file_size
      md5sum
      downloadable
    }
  }
}
'''

# Send the request
response = requests.post(url, json={'query': query})

# Check for successful response
if response.status_code == 200:
    data = response.json()
    file_info = data['data']['getPaginatedUIFile']['uiFiles']
    print("Raw mass spec data for the Georgetown Lung Cancer Proteomics Study:")
    print(json.dumps(file_info, indent=2))
else:
    print(f"Error: {response.status_code} - {response.text}")
```


## Example 8: Retrieve a signed URL for downloading a specific file (e.g. raw mass spec file) in a study using the Proteomics Data Commons (PDC) API.

```
import requests
import json

# Define the GraphQL endpoint
url = "https://pdc.cancer.gov/graphql"

# Define the GraphQL query to get the signed URL for the file
query = '''
query FilesDataQuery($file_name: String!, $study_id: String!) {
  uiFilesPerStudy(file_name: $file_name, study_id: $study_id) {
    file_id
    file_name
    signedUrl {
      url
    }
  }
}
'''

# Set the variables for the query
variables = {
    "file_name": "Ctrl_1-set_1-label_113-frac_2-F9.wiff",
    "study_id": "17d5bccf-d028-11ea-b1fd-0aad30af8a83"
}

# Send the request
response = requests.post(url, json={'query': query, 'variables': variables})

# Check for successful response
if response.status_code == 200:
    data = response.json()
    signed_url = data['data']['uiFilesPerStudy'][0]['signedUrl']['url']
    print(f"Signed URL for the file: {signed_url}")
else:
    print(f"Error: {response.status_code} - {response.text}")
```


## Example 9: Retrieve open standard data files for a specific study using the Proteomics Data Commons (PDC) API.

```
import requests
import json

# Define the GraphQL endpoint
url = "https://pdc.cancer.gov/graphql"

# Define the GraphQL query to get open standard data for a study
query = '''
{
  getPaginatedUIFile(
    study_name: "Georgetown Lung Cancer Proteomics Study",
    file_type: "Open Standard"
  ) {
    uiFiles {
      file_id
      file_name
      file_type
      file_size
      md5sum
      downloadable
    }
  }
}
'''

# Send the request
response = requests.post(url, json={'query': query})

# Check for successful response
if response.status_code == 200:
    data = response.json()
    file_info = data['data']['getPaginatedUIFile']['uiFiles']
    print("Open standard data for the study:")
    print(json.dumps(file_info, indent=2))
else:
    print(f"Error: {response.status_code} - {response.text}")
```


## Example 10: This example demonstrates how to find lung cancer studies in the Proteomics Data Commons by querying for studies with primary sites 'Lung' and 'Bronchus and lung', and combining the results.

```
import requests
import json

# Define the GraphQL endpoint
url = "https://pdc.cancer.gov/graphql"

# Define the GraphQL query to filter for studies with primary site "Lung"
query_lung = '''
{
  getPaginatedUIStudy(primary_site: "Lung") {
    uiStudies {
      study_id
      submitter_id_name
      pdc_study_id
      disease_type
      primary_site
    }
  }
}
'''

# Define the GraphQL query to filter for studies with primary site "Bronchus and lung"
query_bronchus_and_lung = '''
{
  getPaginatedUIStudy(primary_site: "Bronchus and lung") {
    uiStudies {
      study_id
      submitter_id_name
      pdc_study_id
      disease_type
      primary_site
    }
  }
}
'''

# Send the request for "Lung"
response_lung = requests.post(url, json={'query': query_lung})

# Send the request for "Bronchus and lung"
response_bronchus_and_lung = requests.post(url, json={'query': query_bronchus_and_lung})

# Combine the results from both queries
lung_cancer_studies = []

if response_lung.status_code == 200:
    data_lung = response_lung.json()
    lung_cancer_studies.extend(data_lung['data']['getPaginatedUIStudy']['uiStudies'])
else:
    print(f"Error: {response_lung.status_code} - {response_lung.text}")

if response_bronchus_and_lung.status_code == 200:
    data_bronchus_and_lung = response_bronchus_and_lung.json()
    lung_cancer_studies.extend(data_bronchus_and_lung['data']['getPaginatedUIStudy']['uiStudies'])
else:
    print(f"Error: {response_bronchus_and_lung.status_code} - {response_bronchus_and_lung.text}")

# Remove duplicates
lung_cancer_studies = {study['study_id']: study for study in lung_cancer_studies}.values()

# Print the number of studies found and the first 5 studies
print(f"Found {len(lung_cancer_studies)} studies with primary site 'Lung' or 'Bronchus and lung'.")
print(list(lung_cancer_studies)[:5])
```


## Example 11: This example demonstrates how to query the Proteomics Data Commons for studies with open standard data for processed mass spec using the getPaginatedUIFile query.

```
import requests
import json

# Define the GraphQL endpoint
url = "https://pdc.cancer.gov/graphql"

# Define the GraphQL query to find studies with open standard data for processed mass spec
query = '''
{
  getPaginatedUIFile(
    data_category: "Processed Mass Spectra",
    file_type: "Open Standard",
    offset: 0,
    limit: 10
  ) {
    uiFiles {
      file_id
      file_name
      study_id
      pdc_study_id
    }
  }
}
'''

# Send the request
response = requests.post(url, json={'query': query})

# Check for successful response
if response.status_code == 200:
    data = response.json()
    files = data['data']['getPaginatedUIFile']['uiFiles']
    print("Studies with open standard data for processed mass spec:")
    print(json.dumps(files, indent=2))
else:
    print(f"Error: {response.status_code} - {response.text}")
```

## Example 12: Query PDC to find studies with a specific disease type (in this case 'Acute Myeloid Leukemia')

```
import requests
import json

url = 'https://pdc.cancer.gov/graphql'

query = """
{
  getPaginatedUIStudy(disease_type: "Acute Myeloid Leukemia") {
    uiStudies {
      study_id
      submitter_id_name
      pdc_study_id
      disease_type
      primary_site
    }
  }
}
"""

try:
    response = requests.post(url, json={'query': query})
    response.raise_for_status()

    # Process the response data
    data = response.json()
    studies = data['data']['getPaginatedUIStudy']['uiStudies']

    # Output the results
    print(f"Found {len(studies)} studies related to Acute Myeloid Leukemia.")
    for study in studies[:5]:  # Print the first 5 studies
        print(study)

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
```

## Example 13: Fetch all available metadata for a study using its PDC Study ID.

```
import requests
import json

url = 'https://pdc.cancer.gov/graphql'
study_id = 'PDC000478'  # Using the PDC Study ID instead

query = """
query getStudyMetadata($pdc_study_id: String!) {
  getPaginatedUIStudy(pdc_study_id: $pdc_study_id) {
    uiStudies {
      study_id
      pdc_study_id
      submitter_id_name
      study_description
      program_name
      project_name
      disease_type
      primary_site
      analytical_fraction
      experiment_type
      embargo_date
      cases_count
      aliquots_count
      filesCount {
        file_type
        data_category
        files_count
      }
      supplementaryFilesCount {
        data_category
        file_type
        files_count
      }
      nonSupplementaryFilesCount {
        data_category
        file_type
        files_count
      }
      contacts {
        name
        institution
        email
        url
      }
      versions {
        number
      }
    }
  }
}
"""

variables = {
  "pdc_study_id": study_id
}

try:
  response = requests.post(url, json={'query': query, 'variables': variables})
  response.raise_for_status()
  data = response.json()
  # Print a subset of the data
  print(json.dumps(data['data']['getPaginatedUIStudy']['uiStudies'][0], indent=2))

except requests.exceptions.RequestException as e:
  print(f"An error occurred: {e}")
  if hasattr(e, 'response') and e.response is not None:
    print("Response content:", e.response.text)
except json.JSONDecodeError as e:
  print(f"Error decoding JSON response: {e}")
  print("Response content:", response.text)
```


## Example 14: Retrieve quantitative mass spectrometry data for STAT5A and STAT5B proteins using the getPaginatedUIGeneAliquotSpectralCount query.

```
import requests
import json

url = 'https://pdc.cancer.gov/graphql'

query = """
query ($gene_name: String!, $offset: Int, $limit: Int) {
  getPaginatedUIGeneAliquotSpectralCount(gene_name: $gene_name, offset: $offset, limit: $limit) {
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

variables_stat5a = {
    "gene_name": "STAT5A",
    "offset": 0,
    "limit": 10  # Retrieve the first 10 results
}

variables_stat5b = {
    "gene_name": "STAT5B",
    "offset": 0,
    "limit": 10  # Retrieve the first 10 results
}

try:
    response_stat5a = requests.post(url, json={'query': query, 'variables': variables_stat5a})
    response_stat5a.raise_for_status()
    data_stat5a = response_stat5a.json()

    response_stat5b = requests.post(url, json={'query': query, 'variables': variables_stat5b})
    response_stat5b.raise_for_status()
    data_stat5b = response_stat5b.json()

    print("STAT5A Protein Expression Data (First 10 Results):")
    print(json.dumps(data_stat5a['data']['getPaginatedUIGeneAliquotSpectralCount']['uiGeneAliquotSpectralCounts'], indent=2))

    print("\nSTAT5B Protein Expression Data (First 10 Results):")
    print(json.dumps(data_stat5b['data']['getPaginatedUIGeneAliquotSpectralCount']['uiGeneAliquotSpectralCounts'], indent=2))

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON response: {e}")
    print("Response content:", response_stat5a.text)
    print("Response content:", response_stat5b.text)
```
