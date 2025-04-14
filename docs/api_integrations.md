# API Loader

![loader-workflow](./loader-workflow.png)

## Global Loader Config

The global loader config defines settings for adhoc-api's agents (non-per-API) and provides a source for where to look for the APIs (`definitions_root`) and the **default cache body (`default_cache_body`).**

**For any API not specifying an overridden cache body, this will be used - and will interpolate the fields `documentation` and `instructions` into the cache body.**

Most of the time, you will only need to specify `instructions` for a new API to add.

Below is the default.

```yaml
definitions_root: ./datasources
drafter:
    model: models/gemini-1.5-pro-001
    ttl_seconds: 1800
finalizer:
    model: gpt-4o
default_cache_body: | 
    You will be given the entire API documentation. 
    When you write code against this API, you should avail yourself of the appropriate query parameters, 
    your understanding of the response model, and be cognizant that not all data is public and thus may require a token, etc.
    Unless you receive a 403 forbidden, assume the endpoints are unauthenticated.
    If the user says the API does not require authentication, OMIT code about tokens and token handling and token headers.
    When you are downloading, communicate via stdout that something has been downloaded.
    When you are doing complex things try to break them down step by step and implement appropriate exception handling.
    
    {instructions}
    
    Here is the documentation.
    
    {documentation}
```

## API Definitions

Each API is contained within it's own folder.

Within that folder is an `api.yaml` file (it must have that name) that contains API-specific details.

An example (PDC):  

```yaml
name: "Proteomics Data Commons"
description: |
    The objectives of the National Cancer Institute’s Proteomic Data Commons (PDC) are (1) to make cancer-related proteomic datasets easily accessible to the public, and (2) facilitate direct multiomics integration in support of precision medicine through interoperability with accompanying data resources (genomic and medical image datasets).
    The PDC was developed to advance our understanding of how proteins help to shape the risk, diagnosis, development, progression, and treatment of cancer. In-depth analysis of proteomic data allows us to study both how and why cancer develops and to devise ways of personalizing treatment for patients using precision medicine.
    The PDC is one of several repositories within the NCI Cancer Research Data Commons (CRDC), a secure cloud-based infrastructure featuring diverse data sets and innovative analytic tools – all designed to advance data-driven scientific discovery. The CRDC enables researchers to link proteomic data with other data sets (e.g., genomic and imaging data) and to submit, collect, analyze, store, and share data throughout the cancer data ecosystem.
    Access to highly curated and standardized biospecimen, clinical and proteomic data with direct integration of accompanying data resources (genomic and medical image datasets).
    
    Uses: 
    * Intuitive interface to filter, query, search, visualize and download the data and metadata.
    * A common data harmonization pipeline to uniformly analyze all PDC data and provide advanced visualization of the quantitative information.
    * Cloud based (Amazon Web Services) infrastructure facilitates interoperability with AWS based data analysis tools and platforms natively.
    * Application programming interface (API) provides cloud-agnostic data access and allows third parties to extend the functionality beyond the PDC.
    * A highly structured workspace that serves as a private user data store and also data submission portal.
    * Distributes controlled access data, such as the patient-specific protein fasta sequence databases, with dbGaP authorization and eRA Commons authentication.
documentation:
    file: "pdc_schema.graphql"
cache_key: "api_assistant_pdc_graphql"
instructions: |
    This API is through GraphQL. You will be provided the schema. 
    All requests go to the following URL: https://pdc.cancer.gov/graphql
    Make all GraphQL requests to that URL. 
```

### Cache Body

The main prompt and cache body can be specified and overridden, or use the default. 

Using default can be done one of two ways:

* Omitting the key (implicit)
* Explicitly setting `cache_body` as follows:

```yaml
cache_body:
    default: true
```

Both are identical.

If overridden, strings can be used and interpolation will be performed **last**, allowing you to safe use any other field.

```yaml
cache_body: |
  my prompt goes here
  {description}
  if my api defines a new key called 'facets'
  loaded from a file, i can use that here
  {facets}
``` 

### Required API keys 

The required API keys are metadata for usage.

#### `name`

The name of the API.

#### `description`

Description for how the agent should choose API.

#### `cache_key` 

Gemini cache key for drafting agent.

#### `instructions`

Instructions are fed to the second-agent proofreader (finalizer) via `adhoc-api`. 

In the default cache_body, instructions are interpolated into the prompt and included to the drafting agent as well. (see above in Global Loader Config)

Instructions is interpolated before cache_body and can safely use any other keys.

### Loading Files, Interpolation

`file:` directives in place of text will load files from disk into the yaml fields.

```yaml
documentation:
    file: filename.txt
```

------> at runtime...

```yaml
documentation: |
    these are the contents of filename.txt
```

### Defining New Keys

Arbitrary new keys can be defined.

> New keys are not themselves interpolated, but can be used for interpolation as in the example below (for either `instructions` or `description`).

```yaml
facets:
    file: facets.txt
license:
    file: license

instructions: |
    For this api, you should know the following
    {facets}
    This API is licensed as
    {license}
```
