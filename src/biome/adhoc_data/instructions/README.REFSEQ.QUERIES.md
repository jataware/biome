# Querying RefSeq Data Starting with a Gene Symbol

## 1. Finding RefSeq Transcripts for a Gene

To get RefSeq transcripts for a human gene, use E-utilities with the following query structure:
```bash
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=nucleotide&term=GENE[Gene Name] AND RefSeq[Filter] AND human[Organism]&retmode=json"
```

For example, for EGFR:
```bash
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=nucleotide&term=EGFR[Gene%20Name]%20AND%20RefSeq[Filter]%20AND%20human[Organism]&retmode=json"
```

## 2. Getting Detailed Transcript Information

Once you have identified a RefSeq accession (e.g., NM_005228), get the full GenBank record:
```bash
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&id=NM_005228&rettype=gb&retmode=text"
```

## 3. Key Information in the GenBank Record

The GenBank record contains:

1. **Basic Transcript Information**
   - Accession number
   - Version
   - Definition line
   - Length of transcript

2. **Coding Sequence (CDS) Details**
   - Start and stop positions
   - Protein length
   - Translation
   - Signal peptides
   - Mature peptide regions

3. **UTR Information**
   - 5' UTR location
   - 3' UTR location
   - Polyadenylation signals

4. **Exon Structure**
   - Individual exon coordinates
   - Splice variants

## Example: EGFR Transcript Analysis

Using EGFR's primary transcript (NM_005228.5) as an example:

```
LOCUS       NM_005228               9905 bp    mRNA    linear   PRI
DEFINITION  Homo sapiens epidermal growth factor receptor (EGFR), transcript variant 1, mRNA.
```

Key Features:
1. **Transcript Length**: 9,905 bp
2. **Coding Sequence**:
   - Start: 262 bp
   - End: 3,894 bp
   - Length: 3,633 bp
   - Protein: 1,210 amino acids

3. **UTR Regions**:
   - 5' UTR: 1-261 bp
   - 3' UTR: 3,895-9,905 bp

4. **Polyadenylation Signals**:
   - First signal: 5,589-5,594
   - Second signal: 9,824-9,829
   - Third signal: 9,883-9,888

## Common Fields in GenBank Records

1. **LOCUS**: Basic sequence information
   - Accession
   - Length
   - Molecule type
   - Taxonomy

2. **FEATURES**: Detailed annotation
   - CDS (coding sequence)
   - Exons
   - UTRs
   - Signal peptides
   - Regulatory elements

3. **ORIGIN**: The actual sequence

## Tips for Parsing

1. Look for the `CDS` feature to find:
   - Coding sequence coordinates
   - Protein translation
   - Protein features

2. Check `exon` features for:
   - Splice structure
   - Alternative splicing

3. Look for `regulatory` features for:
   - Polyadenylation signals
   - Other regulatory elements

## Example Script to Extract Information

```python
import re

def parse_genbank_features(gb_text):
    # Find CDS coordinates
    cds_match = re.search(r'CDS\s+(\d+)\.\.(\d+)', gb_text)
    if cds_match:
        cds_start = int(cds_match.group(1))
        cds_end = int(cds_match.group(2))
        cds_length = cds_end - cds_start + 1
        
        return {
            'cds_start': cds_start,
            'cds_end': cds_end,
            'cds_length': cds_length,
            '5_utr_length': cds_start - 1,
            '3_utr_start': cds_end + 1
        }
    return None
```

## Notes

1. Always verify the version number of the RefSeq record
2. Check for multiple transcript variants
3. Consider using the NCBI E-utilities API for automated queries
4. Be aware of rate limits when making multiple requests 