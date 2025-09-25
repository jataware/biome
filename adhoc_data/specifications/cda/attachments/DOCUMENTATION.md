# CDA Python API Documentation

This document provides comprehensive API documentation for the `cdapython` library, a Python interface for accessing and analyzing cancer research data through the Cancer Data Aggregator (CDA) REST API.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Core Concepts](#core-concepts)
- [Data Access Functions](#data-access-functions)
- [Discovery Functions](#discovery-functions)
- [Summarization Functions](#summarization-functions)
- [Data Processing Functions](#data-processing-functions)
- [Configuration Functions](#configuration-functions)
- [Filter String Syntax](#filter-string-syntax)
- [Examples](#examples)

## Installation

```bash
pip install cdapython
```

## Quick Start

```python
import cdapython as cda

# List available functions
cda.cda_functions()

# Get available tables
tables = cda.tables()

# Get column metadata
columns = cda.columns()

# Get file data with filters
files = cda.get_file_data(match_all=['sex = female', 'age_at_diagnosis >= 50'])

# Summarize subject data
summary = cda.summarize_subjects(match_any=['primary_site = Breast', 'primary_site = Lung'])
```

## Core Concepts

### Data Sources
The CDA aggregates data from multiple sources:
- **GDC**: Genomic Data Commons
- **PDC**: Proteomic Data Commons
- **IDC**: Imaging Data Commons
- **CDS**: Cancer Data Service
- **ICDC**: Integrated Canine Data Commons

### Tables
Two main data tables are available:
- **file**: Information about data files (genomic, imaging, etc.)
- **subject**: Information about research subjects/patients

### Return Formats
Most functions support multiple return formats:
- `'dataframe'`: pandas DataFrame (default)
- `'tsv'`: Tab-separated file output
- `'list'`: Python list
- `'dict'`: Python dictionary
- `'json'`: JSON file output

## Data Access Functions

### get_file_data()

Retrieve file-level data matching specified criteria.

```python
def get_file_data(
    *,
    match_all=None,
    match_any=None,
    match_from_file={'input_file': '', 'input_column': '', 'cda_column_to_match': ''},
    data_source=None,
    add_columns=None,
    exclude_columns=None,
    collate_results=False,
    return_data_as='dataframe',
    output_file=''
)
```

**Parameters:**
- `match_all` (str/list): All conditions must be met
- `match_any` (str/list): At least one condition must be met
- `match_from_file` (dict): Filter using values from a TSV file
- `data_source` (str/list): Restrict to specific data sources
- `add_columns` (str/list): Additional columns to include
- `exclude_columns` (str/list): Columns to exclude
- `collate_results` (bool): Return related data as DataFrames vs lists
- `return_data_as` (str): Output format ('dataframe' or 'tsv')
- `output_file` (str): Path for TSV output

**Returns:** pandas DataFrame with file metadata and associated data

**Example:**
```python
# Get breast cancer files from GDC
files = cda.get_file_data(
    match_all=['primary_site = Breast', 'data_format = BAM'],
    data_source='GDC',
    add_columns=['subject.age_at_diagnosis', 'subject.sex']
)

# Get files using ID list from file
files = cda.get_file_data(
    match_from_file={
        'input_file': 'my_file_ids.tsv',
        'input_column': 'file_id',
        'cda_column_to_match': 'file_id'
    }
)
```

### get_subject_data()

Retrieve subject-level data matching specified criteria.

```python
def get_subject_data(
    *,
    match_all=None,
    match_any=None,
    match_from_file={'input_file': '', 'input_column': '', 'cda_column_to_match': ''},
    data_source=None,
    add_columns=None,
    exclude_columns=None,
    collate_results=False,
    include_external_refs=False,
    return_data_as='dataframe',
    output_file=''
)
```

**Parameters:** Same as `get_file_data()` plus:
- `include_external_refs` (bool): Include external resource references

**Returns:** pandas DataFrame with subject metadata and associated data

**Example:**
```python
# Get lung cancer subjects with specific age range
subjects = cda.get_subject_data(
    match_all=['primary_site = Lung', 'age_at_diagnosis >= 40', 'age_at_diagnosis <= 70'],
    add_columns=['file.data_format', 'file.file_size'],
    collate_results=True
)

# Get subjects from multiple data sources
subjects = cda.get_subject_data(
    match_any=['primary_site = *cancer*'],
    data_source=['GDC', 'PDC']
)
```

### get_data()

Core function used by `get_file_data()` and `get_subject_data()`.

```python
def get_data(
    table=None,  # Required: 'file' or 'subject'
    *,
    # ... same parameters as above
)
```

**Example:**
```python
# Equivalent to get_file_data()
files = cda.get_data(table='file', match_all=['sex = female'])

# Equivalent to get_subject_data()
subjects = cda.get_data(table='subject', match_all=['sex = female'])
```

## Discovery Functions

### tables()

Get list of available CDA tables.

```python
def tables()
```

**Returns:** List of table names

**Example:**
```python
available_tables = cda.tables()
print(available_tables)  # ['file', 'subject']
```

### columns()

Get metadata about searchable columns.

```python
def columns(
    *,
    return_data_as='',
    output_file='',
    sort_by='',
    **filter_arguments
)
```

**Filter Arguments:**
- `table` (str/list): Filter by table name
- `column` (str/list): Filter by column name
- `data_type` (str/list): Filter by data type
- `nullable` (bool): Filter by nullable status
- `description` (str/list): Filter by description text
- `exclude_table` (str/list): Exclude specific tables

**Returns:** DataFrame with columns: table, column, data_type, nullable, description

**Example:**
```python
# Get all columns
all_columns = cda.columns()

# Get file table columns only
file_columns = cda.columns(table='file')

# Get numeric columns
numeric_columns = cda.columns(data_type=['integer', 'numeric', 'bigint'])

# Get columns containing 'age' in name or description
age_columns = cda.columns(column='*age*', description='age')
```

### column_values()

Get distinct values and counts for a specific column.

```python
def column_values(
    column='',  # Required
    *,
    return_data_as='',
    output_file='',
    sort_by='',
    filters=None,
    data_source='',
    force=False
)
```

**Parameters:**
- `column` (str): Column name to analyze
- `filters` (str/list): Value filters with wildcard support
- `data_source` (str): Restrict to specific data source
- `force` (bool): Force execution for high-cardinality columns
- `sort_by` (str): 'count', 'value', 'count:desc', 'value:desc'

**Returns:** DataFrame with column values and counts

**Example:**
```python
# Get all primary sites
sites = cda.column_values('primary_site')

# Get primary sites containing 'lung'
lung_sites = cda.column_values('primary_site', filters=['*lung*'])

# Get file formats from GDC only
formats = cda.column_values('data_format', data_source='GDC', sort_by='count:desc')
```

### release_metadata()

Get information about the current CDA data release.

```python
def release_metadata()
```

**Returns:** List of metadata dictionaries

**Example:**
```python
metadata = cda.release_metadata()
for source_info in metadata:
    print(f"Source: {source_info['data_source']}, Version: {source_info['version']}")
```

### cda_functions()

List all available cdapython functions.

```python
def cda_functions()
```

**Returns:** List of function names

**Example:**
```python
functions = cda.cda_functions()
# Use help() to get details about any function
help(cda.get_file_data)
```

## Summarization Functions

### summarize_files()

Generate summary statistics for file data matching criteria.

```python
def summarize_files(
    *,
    match_all=None,
    match_any=None,
    match_from_file={'input_file': '', 'input_column': '', 'cda_column_to_match': ''},
    data_source=None,
    add_columns=None,
    exclude_columns=None,
    return_data_as='',
    output_file=''
)
```

**Returns:** Summary tables showing value counts for each column

**Example:**
```python
# Summary of breast cancer files
summary = cda.summarize_files(
    match_all=['primary_site = Breast'],
    add_columns=['subject.sex', 'subject.race']
)

# Returns dictionary with summary tables for each column
for column, stats in summary.items():
    print(f"\n{column}:")
    print(stats.head())
```

### summarize_subjects()

Generate summary statistics for subject data matching criteria.

```python
def summarize_subjects(
    *,
    # ... same parameters as summarize_files()
)
```

**Example:**
```python
# Summary of lung cancer subjects
summary = cda.summarize_subjects(
    match_all=['primary_site = Lung'],
    data_source=['GDC', 'PDC']
)
```

## Data Processing Functions

### expand_file_results()

Expand nested DataFrames in file results into flat tables.

```python
def expand_file_results(results_dataframe, column_to_expand)
```

**Parameters:**
- `results_dataframe`: DataFrame from `get_file_data()`
- `column_to_expand` (str): Column containing nested DataFrames

**Returns:** Flattened DataFrame with file_id preserved

**Example:**
```python
# Get files with collated subject data
files = cda.get_file_data(
    match_all=['primary_site = Breast'],
    add_columns=['subject.*'],
    collate_results=True
)

# Expand the nested subject data
expanded = cda.expand_file_results(files, 'subject_data')
```

### expand_subject_results()

Expand nested DataFrames in subject results into flat tables.

```python
def expand_subject_results(results_dataframe, column_to_expand)
```

**Example:**
```python
# Get subjects with collated file data
subjects = cda.get_subject_data(
    match_all=['sex = female'],
    add_columns=['file.*'],
    collate_results=True
)

# Expand the nested file data
expanded = cda.expand_subject_results(subjects, 'file_data')
```

### intersect_file_results()

Find files present in all input DataFrames.

```python
def intersect_file_results(*result_dfs_to_merge, ignore_added_columns=False)
```

**Parameters:**
- `*result_dfs_to_merge`: Multiple DataFrames from `get_file_data()`
- `ignore_added_columns` (bool): Only merge core file columns

**Returns:** DataFrame with files present in all inputs

**Example:**
```python
# Get breast cancer files from different sources
gdc_files = cda.get_file_data(match_all=['primary_site = Breast'], data_source='GDC')
pdc_files = cda.get_file_data(match_all=['primary_site = Breast'], data_source='PDC')

# Find files present in both sources
common_files = cda.intersect_file_results(gdc_files, pdc_files)
```

### intersect_subject_results()

Find subjects present in all input DataFrames.

```python
def intersect_subject_results(*result_dfs_to_merge, ignore_added_columns=False)
```

**Example:**
```python
# Find subjects with both genomic and proteomic data
genomic_subjects = cda.get_subject_data(add_columns=['file.data_category'],
                                       match_all=['file.data_category = Genomics'])
proteomic_subjects = cda.get_subject_data(add_columns=['file.data_category'],
                                         match_all=['file.data_category = Proteomics'])

common_subjects = cda.intersect_subject_results(genomic_subjects, proteomic_subjects)
```

## Configuration Functions

### API Configuration

```python
# Get current API URL
current_url = cda.get_api_url()

# Set custom API URL
cda.set_api_url('https://my-cda-instance.org')
```

### Logging Configuration

```python
# Check available log levels
levels = cda.get_valid_log_levels()  # {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}

# Set log level
cda.set_log_level('DEBUG')

# Get current log level
current_level = cda.get_log_level()

# Control output destinations
cda.enable_console_logging()   # Default: enabled
cda.disable_console_logging()
cda.enable_file_logging('my_log.txt')
cda.disable_file_logging()  # Default: disabled
```

## Filter String Syntax

Filter strings use the format: `"COLUMN_NAME OP VALUE"`

### Operators

- **Comparison**: `<`, `<=`, `>`, `>=` (numeric columns only)
- **Equality**: `=`, `!=` (all column types)
- **NULL matching**: `= NULL`, `!= NULL`

### String Wildcards

Use `*` for partial string matches:
- `diagnosis = *carcinoma*` (contains)
- `sex = F*` (starts with)
- `race = *american` (ends with)

### Data Types

- **Text**: Strings with optional wildcards
- **Numeric**: integers, decimals (`age_at_diagnosis >= 50`)
- **Boolean**: `true`/`false`, `t`/`f` (`vital_status = true`)

### Examples

```python
# Numeric comparisons
filters = ['age_at_diagnosis >= 40', 'age_at_diagnosis <= 70']

# String matching with wildcards
filters = ['primary_site = *Breast*', 'histological_type = *carcinoma*']

# Boolean values
filters = ['vital_status = true', 'tumor_grade != null']

# Multiple conditions
cda.get_file_data(
    match_all=['primary_site = Lung', 'file_size > 1000000'],
    match_any=['data_format = BAM', 'data_format = VCF']
)
```

### Ternary Comparisons

For range queries, use ternary syntax: `MIN_VALUE OP COLUMN OP MAX_VALUE`

```python
# Age between 40 and 70
files = cda.get_file_data(match_all=['40 <= age_at_diagnosis <= 70'])

# File size range
files = cda.get_file_data(match_all=['1000000 < file_size < 50000000'])
```

## Examples

### Basic Data Access

```python
import cdapython as cda

# Get all breast cancer files
breast_files = cda.get_file_data(match_all=['primary_site = Breast'])
print(f"Found {len(breast_files)} breast cancer files")

# Get female lung cancer subjects with age info
subjects = cda.get_subject_data(
    match_all=['sex = female', 'primary_site = Lung'],
    add_columns=['file.data_format', 'file.file_size']
)
```

### Data Exploration

```python
# Explore available data
print("Available tables:", cda.tables())

# Get column information
file_columns = cda.columns(table='file', return_data_as='list')
subject_columns = cda.columns(table='subject', return_data_as='list')

# Examine column values
primary_sites = cda.column_values('primary_site', sort_by='count:desc')
data_formats = cda.column_values('data_format', sort_by='count:desc')
```

### Complex Filtering

```python
# Multiple data sources and complex filters
files = cda.get_file_data(
    match_all=['primary_site = Breast', 'file_size > 1000000'],
    match_any=['data_format = BAM', 'data_format = VCF', 'data_format = MAF'],
    data_source=['GDC', 'PDC'],
    add_columns=['subject.age_at_diagnosis', 'subject.race', 'subject.ethnicity'],
    collate_results=True
)

# Filter using file-based criteria
patient_files = cda.get_file_data(
    match_from_file={
        'input_file': 'patient_ids.tsv',
        'input_column': 'submitter_id',
        'cda_column_to_match': 'subject.submitter_id'
    }
)
```

### Data Integration

```python
# Get overlapping subjects between data sources
gdc_subjects = cda.get_subject_data(data_source='GDC', match_all=['primary_site = Breast'])
pdc_subjects = cda.get_subject_data(data_source='PDC', match_all=['primary_site = Breast'])

# Find subjects with data in both sources
overlap = cda.intersect_subject_results(gdc_subjects, pdc_subjects)
print(f"Found {len(overlap)} subjects with data in both GDC and PDC")

# Expand nested data for analysis
expanded_data = cda.expand_subject_results(
    cda.get_subject_data(
        match_all=['primary_site = Lung'],
        add_columns=['file.*'],
        collate_results=True
    ),
    'file_data'
)
```

### Summary Analysis

```python
# Generate comprehensive summaries
file_summary = cda.summarize_files(
    match_all=['primary_site = Breast'],
    add_columns=['subject.race', 'subject.ethnicity', 'subject.age_at_diagnosis']
)

# Display summary statistics
for column_name, summary_df in file_summary.items():
    print(f"\n=== {column_name} ===")
    print(summary_df.head(10))

subject_summary = cda.summarize_subjects(
    match_any=['primary_site = Lung', 'primary_site = Breast'],
    return_data_as='dict'
)
```

### Output to Files

```python
# Export large datasets to files
cda.get_file_data(
    match_all=['primary_site = Breast'],
    return_data_as='tsv',
    output_file='breast_cancer_files.tsv'
)

# Export summaries as JSON
cda.summarize_subjects(
    match_all=['sex = female'],
    return_data_as='json',
    output_file='female_subjects_summary.json'
)
```

This documentation provides a comprehensive guide to using the cdapython API for accessing and analyzing cancer research data through the CDA platform. For additional help with any function, use Python's built-in `help()` function: `help(cda.function_name)`.