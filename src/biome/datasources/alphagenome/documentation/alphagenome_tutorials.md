# AlphaGenome Tutorials and Examples

## Tutorial Overview

AlphaGenome provides comprehensive tutorials to help users get started with genomic analysis. Each tutorial is designed to demonstrate specific capabilities and provide practical examples.

## Available Tutorials

### 1. Visualizing Predictions - Modality Tour
**Purpose**: Comprehensive tour of different visualization modalities supported by AlphaGenome.

**Key Learning Objectives**:
- Understanding different visualization types
- Multi-track genomic plotting
- Transcript annotation display
- Customizing plot appearance and labels
- Overlaying multiple data types

**Supported Visualization Types**:
- **RNA-seq Expression**: Gene expression levels across the genome
- **CAGE**: Transcription start site identification and quantification
- **ATAC-seq**: Chromatin accessibility patterns
- **ChIP-seq**: Histone modifications and transcription factor binding
- **DNase-seq**: DNase hypersensitivity sites

**Advanced Visualization Workflow**:
```python
from alphagenome.visualization import plot_components
import matplotlib.pyplot as plt

# Create comprehensive multi-track visualization
plot_components.plot([
    # Add transcript annotations
    plot_components.TranscriptAnnotation(longest_transcripts),
    
    # RNA-seq expression track
    plot_components.Tracks(
        tdata=output.rna_seq,
        ylabel_template='RNA_SEQ: {biosample_name}'
    ),
    
    # CAGE transcription start sites
    plot_components.Tracks(
        tdata=output.cage,
        ylabel_template='CAGE: {biosample_name}'
    ),
    
    # Chromatin accessibility
    plot_components.Tracks(
        tdata=output.atac,
        ylabel_template='ATAC: {biosample_name}'
    ),
    
    # Overlaid tracks for comparison
    plot_components.OverlaidTracks(
        tdata={
            'REF': reference_data,
            'ALT': alternate_data,
        },
        colors={'REF': 'dimgrey', 'ALT': 'red'},
    ),
], interval=genomic_interval)
plt.title("Multi-Modal Genomic Prediction Visualization")
plt.tight_layout()
plt.show()
```

**Customization Options**:
- Custom color schemes for different tracks
- Flexible ylabel templates with biosample information
- Interval-specific zooming and panning
- Export to various formats (PNG, PDF, SVG)

### 2. Scoring and Visualizing a Single Variant
**Purpose**: A comprehensive tool for scoring and visualizing variants across multiple modalities.

**Key Learning Objectives**:
- Single variant analysis workflow
- Multi-modal prediction interpretation
- Variant effect quantification
- Clinical relevance assessment

**Example Workflow**:
```python
from alphagenome.data import genome
from alphagenome.models import dna_client

# Define variant
variant = genome.Variant(
    chromosome='chr22',
    position=36201698,
    reference_bases='A',
    alternate_bases='C',
)

# Score variant across multiple outputs
outputs = model.predict_variant(
    interval=interval,
    variant=variant,
    ontology_terms=['UBERON:0001157'],
    requested_outputs=[
        dna_client.OutputType.RNA_SEQ,
        dna_client.OutputType.SPLICING,
        dna_client.OutputType.CHROMATIN
    ],
)
```

### 3. Navigating Data Ontologies
**Purpose**: A tool for fetching ontology IDs for specific tissues and biological contexts.

**Key Learning Objectives**:
- Understanding biological ontologies
- Tissue-specific analysis
- Ontology term selection
- Context-specific predictions

**Common Ontology Terms**:
- `UBERON:0001157` - Liver tissue
- `UBERON:0002048` - Lung tissue
- `UBERON:0000955` - Brain tissue
- `UBERON:0000948` - Heart tissue

### 4. Batch Variant Scoring
**Purpose**: Efficiently score multiple variants simultaneously for large-scale genomic analysis.

**Key Learning Objectives**:
- VCF file processing workflows
- Batch processing optimization
- Progress tracking for large datasets
- Multi-modal scoring configuration
- Result aggregation and interpretation

**Input Requirements**:
- Tab-separated VCF file with columns: `variant_id`, `CHROM`, `POS`, `REF`, `ALT`
- Supports both human and mouse genome builds
- Flexible sequence length selection (2KB to 1MB)

**Advanced Batch Processing Workflow**:
```python
import pandas as pd
from tqdm import tqdm
from alphagenome.data import genome
from alphagenome.models import dna_client

# Load VCF file
vcf = pd.read_csv('variants.vcf', sep='\t')

# Configure scoring types
scoring_types = [
    dna_client.OutputType.RNA_SEQ,
    dna_client.OutputType.CAGE,
    dna_client.OutputType.ATAC,
    dna_client.OutputType.DNASE,
    dna_client.OutputType.HISTONE_MARKS,
    dna_client.OutputType.TF_BINDING
]

# Process variants with progress tracking
results = []
for i, vcf_row in tqdm(vcf.iterrows(), total=len(vcf), desc="Processing variants"):
    variant = genome.Variant(
        chromosome=str(vcf_row.CHROM),
        position=int(vcf_row.POS),
        reference_bases=vcf_row.REF,
        alternate_bases=vcf_row.ALT,
        name=vcf_row.variant_id,
    )
    
    try:
        # Score variant across multiple modalities
        output = model.predict_variant(
            interval=interval,
            variant=variant,
            ontology_terms=tissue_terms,
            requested_outputs=scoring_types,
        )
        
        # Extract quantitative scores
        scores = {
            'variant_id': variant.name,
            'rna_seq_score': output.alternate.rna_seq.values.mean(),
            'cage_score': output.alternate.cage.values.mean(),
            'atac_score': output.alternate.atac.values.mean(),
            # Add other modality scores...
        }
        results.append(scores)
        
    except Exception as e:
        print(f"Error processing {variant.name}: {e}")
        continue

# Convert to DataFrame for analysis
results_df = pd.DataFrame(results)
print(f"Successfully processed {len(results_df)} variants")
```

**Optimization Tips**:
- Use `tqdm` for progress tracking on large datasets
- Implement error handling for failed predictions
- Consider memory management for very large VCF files
- Cache results for repeated analyses

### 5. Example Analysis Workflow: TAL1 Locus
**Purpose**: Comprehensive real-world analysis of oncogenic variants in the TAL1 locus.

**Key Learning Objectives**:
- Complete genomic analysis workflow
- Oncology research application
- Integration of multiple prediction types
- Biological interpretation of results
- GENCODE annotation integration

**TAL1 Locus Background**:
The TAL1 (T-cell acute lymphocytic leukemia 1) gene is a critical transcription factor involved in hematopoiesis. Oncogenic variants near this locus can lead to TAL1 upregulation and contribute to leukemogenesis.

**Complete Analysis Workflow**:
```python
import pandas as pd
from alphagenome.data import genome
from alphagenome.models import dna_client
from alphagenome.visualization import plot_components

# 1. Load and prepare gene annotations
gencode = pd.read_csv('gencode_annotations.gtf', sep='\t')
protein_coding = gencode[gencode['gene_type'] == 'protein_coding']
longest_transcripts = protein_coding.groupby('gene_id').apply(
    lambda x: x.loc[x['transcript_length'].idxmax()]
)

# 2. Define TAL1 locus region
tal1_interval = genome.Interval(
    chromosome='chr1',
    start=47200000,
    end=47300000  # 100kb region around TAL1
)

# 3. Load oncogenic variants
oncogenic_variants = [
    genome.Variant(chr='chr1', pos=47240000, ref='G', alt='A', name='TAL1_variant_1'),
    genome.Variant(chr='chr1', pos=47245000, ref='C', alt='T', name='TAL1_variant_2'),
    genome.Variant(chr='chr1', pos=47250000, ref='A', alt='G', name='TAL1_variant_3'),
]

# 4. Analyze variants in relevant cell context (CD34+ stem cells)
cd34_ontology = 'CL:0000037'  # CD34+ stem cell

results = {}
for variant in oncogenic_variants:
    # Predict variant effects across multiple modalities
    output = model.predict_variant(
        interval=tal1_interval,
        variant=variant,
        ontology_terms=[cd34_ontology],
        requested_outputs=[
            dna_client.OutputType.RNA_SEQ,
            dna_client.OutputType.ATAC,
            dna_client.OutputType.HISTONE_MARKS,
        ]
    )
    
    # Calculate effect sizes
    rna_effect = (output.alternate.rna_seq.values.mean() - 
                  output.reference.rna_seq.values.mean()) / output.reference.rna_seq.values.mean()
    
    atac_effect = (output.alternate.atac.values.mean() - 
                   output.reference.atac.values.mean()) / output.reference.atac.values.mean()
    
    results[variant.name] = {
        'rna_expression_effect': rna_effect,
        'chromatin_accessibility_effect': atac_effect,
        'predicted_oncogenic_potential': abs(rna_effect) > 0.2  # Threshold for significance
    }

# 5. Visualization of variant effects
for variant_name, result in results.items():
    if result['predicted_oncogenic_potential']:
        print(f"{variant_name}: High oncogenic potential")
        print(f"  RNA effect: {result['rna_expression_effect']:.3f}")
        print(f"  ATAC effect: {result['chromatin_accessibility_effect']:.3f}")
        
        # Create visualization
        plot_components.plot([
            plot_components.TranscriptAnnotation(longest_transcripts),
            plot_components.OverlaidTracks(
                tdata={
                    'REF': output.reference.rna_seq,
                    'ALT': output.alternate.rna_seq,
                },
                colors={'REF': 'blue', 'ALT': 'red'},
            ),
        ], interval=tal1_interval)
        plt.title(f"TAL1 Locus Analysis: {variant_name}")
        plt.show()

# 6. Biological interpretation
print("\nBiological Summary:")
print("- Variants with high RNA expression effects likely disrupt regulatory elements")
print("- Chromatin accessibility changes indicate altered transcription factor binding")
print("- Combined effects suggest mechanism of TAL1 upregulation in leukemogenesis")
```

**Key Insights from Analysis**:
- **Convergent Mechanisms**: Multiple variants converge on TAL1 oncogene upregulation
- **Regulatory Disruption**: Non-coding variants alter regulatory element function
- **Cell-Type Specificity**: Effects are analyzed in relevant hematopoietic cell context
- **Predictive Power**: Computational predictions help understand molecular mechanisms

**Clinical Relevance**:
- Identifies potential therapeutic targets
- Provides mechanistic insights for drug development
- Supports precision medicine approaches for leukemia treatment

## Common Analysis Patterns

### Basic Prediction Workflow
```python
from alphagenome.data import genome
from alphagenome.models import dna_client
import os

# Setup
API_KEY = os.environ.get("ALPHAGENOME_API_KEY")
model = dna_client.create(API_KEY)

# Define genomic region
interval = genome.Interval(
    chromosome='chr22',
    start=35677410,
    end=36725986
)

# Make prediction
outputs = model.predict(
    interval=interval,
    ontology_terms=['UBERON:0001157'],
    requested_outputs=[dna_client.OutputType.RNA_SEQ],
)
```

### Variant Effect Analysis
```python
# Compare reference vs alternate
variant = genome.Variant(
    chromosome='chr22',
    position=36201698,
    reference_bases='A',
    alternate_bases='C',
)

outputs = model.predict_variant(
    interval=interval,
    variant=variant,
    ontology_terms=['UBERON:0001157'],
    requested_outputs=[dna_client.OutputType.RNA_SEQ],
)

# Access reference and alternate predictions
ref_expression = outputs.reference.rna_seq
alt_expression = outputs.alternate.rna_seq
```

### Multi-Tissue Analysis
```python
tissue_terms = [
    'UBERON:0001157',  # Liver
    'UBERON:0002048',  # Lung
    'UBERON:0000955',  # Brain
    'UBERON:0000948',  # Heart
]

tissue_results = {}
for tissue in tissue_terms:
    outputs = model.predict(
        interval=interval,
        ontology_terms=[tissue],
        requested_outputs=[dna_client.OutputType.RNA_SEQ],
    )
    tissue_results[tissue] = outputs
```

## Best Practices

### 1. Resource Management
- Use appropriate interval sizes for your analysis
- Consider computational costs for large-scale analyses
- Implement proper error handling and retry logic

### 2. Data Interpretation
- Always consider biological context
- Validate predictions with experimental data when possible
- Use multiple prediction types for comprehensive analysis

### 3. Visualization Guidelines
- Use consistent color schemes across plots
- Include appropriate annotations and legends
- Consider accessibility in visualization design

### 4. Performance Optimization
- Batch similar queries when possible
- Cache results for repeated analyses
- Use appropriate output types for your specific needs

## Troubleshooting Common Issues

### API Connection Problems
- Verify API key is correctly set
- Check internet connectivity
- Ensure proper authentication

### Memory and Performance Issues
- Reduce interval sizes for large analyses
- Use batch processing for multiple variants
- Consider computational resource limitations

### Visualization Issues
- Ensure matplotlib is properly installed
- Check data format compatibility
- Verify coordinate systems match

## Next Steps

After completing these tutorials, users should be able to:
- Set up and configure AlphaGenome
- Perform basic genomic predictions
- Analyze variant effects
- Create informative visualizations
- Interpret results in biological context

For advanced usage patterns and specific research applications, consult the API reference documentation and consider joining the AlphaGenome community forum for additional support and collaboration opportunities.