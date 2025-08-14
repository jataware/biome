# Querying ClinVar with E-utilities

## Basic Gene Query
To search for all variants in a gene:
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=EGFR[gene]&retmode=json
```

## Specific Variant Queries
There are several ways to look up specific variants:

### 1. By HGVS notation
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=NM_005228.5(EGFR):c.2369C>T
```

### 2. By gene and amino acid change
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=EGFR[gene]+AND+T790M
```

### 3. By rs number
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=rs121434569
```

### 4. By genomic location
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=7:55181378[Chromosome]+AND+EGFR[gene]
```

## Getting Detailed Information
Once you have a variant ID, you can get detailed information using:
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=clinvar&id=16613&retmode=json
```

The detailed information includes:
- Clinical significance
- Genomic location
- Protein change
- Population frequencies
- Associated conditions
- Cross-references to other databases

## Example Response Data
We've saved example EGFR variant data in `egfr_clinvar_variants.json`, which contains:
- List of variant IDs
- Total count of variants
- Query metadata

## Tips for Using E-utilities
1. Always URL encode special characters in the query
2. Use `retmode=json` for easier parsing
3. Consider using `retmax` parameter to limit results
4. Include gene context when searching for specific variants 

## Concrete Example: Looking up EGFR L883S

### 1. Search for the variant
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=EGFR[gene]+AND+L883S&retmode=json
```

Response shows one result:
```json
{
  "esearchresult": {
    "count": "1",
    "retmax": "1",
    "idlist": ["1050891"]
  }
}
```

### 2. Get detailed information
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=clinvar&id=1050891&retmode=json
```

Key findings:
- **Variant Details**:
  - ClinVar ID: VCV001050891.8
  - HGVS: NM_005228.5(EGFR):c.2648T>C (p.Leu883Ser)
  - dbSNP: rs1787457693
- **Clinical Significance**: Uncertain significance (last evaluated: Dec 12, 2023)
- **Genomic Location**: 
  - GRCh38: Chr7:55192788
  - GRCh37: Chr7:55260481
- **Population Frequency**: 0.00001 (gnomAD)
- **Associated Condition**: EGFR-related lung cancer 

### 3. Supporting Submission Details
You can get detailed information about the clinical submissions using:
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=clinvar&id=RCV001358850,RCV004998848&rettype=clinvarset
```

Key findings from submissions:
```json
{
  "variant_details": {
    "name": "EGFR L883S",
    "hgvs": "NM_005228.5(EGFR):c.2648T>C (p.Leu883Ser)",
    "submissions": [
      {
        "submitter": "Labcorp Genetics (formerly Invitae)",
        "date_evaluated": "2023-12-12",
        "classification": "Uncertain significance",
        "evidence_summary": "This sequence change replaces leucine, which is neutral and non-polar, with serine, which is neutral and polar, at codon 883 of the EGFR protein. This variant is not present in population databases (gnomAD no frequency). This variant has not been reported in the literature in individuals affected with EGFR-related conditions. Advanced modeling indicates that this missense variant is expected to disrupt EGFR protein function with a positive predictive value of 80%."
      },
      {
        "submitter": "Quest Diagnostics Nichols Institute",
        "date_evaluated": "2023-11-09",
        "classification": "Uncertain significance",
        "evidence_summary": "The variant has not been reported in individuals with EGFR-related conditions in the published literature. The frequency in gnomAD is 0.0000066 (1/152186 chromosomes). Bioinformatics tools predict this variant is damaging."
      }
    ],
    "population_frequency": {
      "gnomAD": "0.00001"
    },
    "genomic_location": {
      "GRCh38": "Chr7:55192788",
      "GRCh37": "Chr7:55260481"
    }
  }
}
```

This example demonstrates:
1. How to find a specific variant
2. How to get its basic information
3. How to retrieve detailed clinical interpretations from multiple submitters
4. The format of evidence summaries provided by clinical laboratories 