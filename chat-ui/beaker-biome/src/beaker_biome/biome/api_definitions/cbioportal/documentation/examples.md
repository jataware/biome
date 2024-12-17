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
