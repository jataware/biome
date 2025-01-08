

## Example 1: Retrieve literature evidence related to AML using MeSH term queries, including child terms, and summarize the findings.

```
import requests
import json

def get_mesh_literature():
    # API base URL
    base_url = "https://discovery.indra.bio/api/"

    # Get papers with evidence for AML MeSH term
    payload = {
        "mesh_term": ["MESH", "D015470"],
        "include_child_terms": True
    }

    # Make request to get evidences
    response = requests.post(
        base_url + "get_evidences_for_mesh",
        json=payload,
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        # Process and return results
        results = response.json()
        
        # Convert results to a more readable format
        evidence_by_statement = {}
        for stmt_hash, evidences in results.items():
            evidence_by_statement[stmt_hash] = {
                'pmids': list(set([ev['text_refs'].get('PMID') for ev in evidences if ev.get('text_refs', {}).get('PMID')])),
                'evidence_count': len(evidences)
            }
            
        return evidence_by_statement
    else:
        print(f"Error: {response.status_code}")
        return None

if __name__ == "__main__":
    evidence_data = get_mesh_literature()
    
    if evidence_data:
        # Print summary of findings
        print(f"Found {len(evidence_data)} statements with evidence")
        
        # Get total evidence count
        total_evidence = sum(data['evidence_count'] for data in evidence_data.values())
        print(f"Total evidence count: {total_evidence}")
        
        # Get unique PMIDs
        all_pmids = set()
        for data in evidence_data.values():
            all_pmids.update(data['pmids'])
        print(f"Total unique PMIDs: {len(all_pmids)}")
```
