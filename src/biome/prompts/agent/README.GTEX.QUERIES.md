# Querying GTEx Expression Data

## Finding Gene ID from Symbol
To get the correct Gencode ID for your gene of interest:
```bash
# Get gene information including Gencode ID
curl "https://gtexportal.org/api/v2/reference/gene?geneId=EGFR" | jq '.'

# Example Response:
{
  "data": [{
    "gencodeId": "ENSG00000146648.17",
    "geneSymbol": "EGFR",
    "geneSymbolUpper": "EGFR",
    "chromosome": "chr7",
    "start": 55019021,
    "end": 55211628,
    "description": "epidermal growth factor receptor"
  }]
}
```
Use the `gencodeId` from this response in the expression queries below.

## Getting All Median Expression Values
To get median expression values for all tissues:
```bash
curl -H "Accept: application/json" "https://gtexportal.org/api/v2/expression/medianGeneExpression?gencodeId=ENSG00000146648.17&datasetId=gtex_v8" | jq '.'
```

## Getting Expression with Quartiles
To get full expression data including quartiles:
```bash
curl -H "Accept: application/json" "https://gtexportal.org/api/v2/expression/geneExpression?gencodeId=ENSG00000146648.17&filterTissues=all" | jq '.'
```

## Getting Top 10 Tissues by Expression
To get the top 10 tissues sorted by median expression:
```bash
curl -H "Accept: application/json" "https://gtexportal.org/api/v2/expression/medianGeneExpression?gencodeId=ENSG00000146648.17&datasetId=gtex_v8" | jq '.data | sort_by(-.median) | .[0:10]'
```

## Example Response Format

### Median Expression Response
```json
{
  "data": [
    {
      "median": 78.3374,
      "tissueSiteDetailId": "Skin_Sun_Exposed_Lower_leg",
      "geneSymbol": "EGFR",
      "unit": "TPM"
    }
  ]
}
```

### Full Expression with Quartiles Response
```json
{
  "data": [
    {
      "median": 78.3374,
      "quartile25": 65.2145,
      "quartile75": 95.4321,
      "tissueSiteDetailId": "Skin_Sun_Exposed_Lower_leg",
      "geneSymbol": "EGFR",
      "unit": "TPM"
    }
  ]
}
```

## For EGFR (Example)
Top 10 tissues by expression:
1. Skin (Sun Exposed): 78.34 TPM
2. Skin (Not Sun Exposed): 75.93 TPM
3. Cultured fibroblasts: 60.63 TPM
4. Nerve Tibial: 43.12 TPM
5. Vagina: 40.60 TPM
6. Subcutaneous Adipose: 39.73 TPM
7. Esophagus Gastroesophageal Junction: 34.63 TPM
8. Artery Tibial: 33.20 TPM
9. Breast Mammary Tissue: 32.94 TPM
10. Esophagus Muscularis: 31.80 TPM

## Parameters
- `gencodeId`: Ensembl gene ID (e.g., ENSG00000146648.17 for EGFR)
- `datasetId`: GTEx version (e.g., gtex_v8)
- `filterTissues`: Filter specific tissues or 'all'

## Notes
- Expression values are in TPM (Transcripts Per Million)
- Data is from GTEx v8 release
- Quartile data helps understand expression variation within tissues
- Some tissues may have different sample sizes

## Complete Workflow Example
To go from a gene symbol to expression data:

1. Get the Gencode ID:
```bash
curl "https://gtexportal.org/api/v2/reference/gene?geneId=EGFR" | jq -r '.data[0].gencodeId'
# Returns: ENSG00000146648.17
```

2. Use the ID to get expression data:
```bash
# Store the gene ID in a variable
GENE_ID=$(curl "https://gtexportal.org/api/v2/reference/gene?geneId=EGFR" | jq -r '.data[0].gencodeId')

# Get expression data using the ID
curl -H "Accept: application/json" "https://gtexportal.org/api/v2/expression/medianGeneExpression?gencodeId=$GENE_ID&datasetId=gtex_v8" | jq '.'
```

This workflow can be used for any gene symbol. Just replace 'EGFR' with your gene of interest. 