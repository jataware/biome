<a href="https://colab.research.google.com/github/ImagingDataCommons/IDC-Tutorials/blob/master/notebooks/labs/idc_rsna2023.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# Getting started with IDC using `idc-index` python package

---


## Summary

This notebook is introducing NCI Imaging Data Commons to the users who want to interact with IDC programmatically using [`idc-index` python package](https://github.com/ImagingDataCommons/idc-index).

In this notebook you will be introduced into how IDC organizes the metadata accompanying images available in IDC, and how that metadata can be used to define subsets of data. This documentation page complements this notebook with the more detailed discussion of the metadata organization in IDC: https://learn.canceridc.dev/data/organization-of-data/files-and-metadata.

Please note that it is important that you run each cell of this notebook in sequence the first time you go over the notebook. Out of order execution may result in runtime errors.

---
Initial version: Nov 2023

## What is IDC?

NCI Imaging Data Commons (IDC) is a cloud-based environment containing publicly available cancer imaging data co-located with the analysis and exploration tools and resources. IDC is a node within the broader NCI Cancer Research Data Commons (CRDC) infrastructure that provides secure access to a large, comprehensive, and expanding collection of cancer research data.

## IDC metadata search: why, what and how

**Why?**

Think of IDC as a library. Image files are books, and we have ~45 TB of those. When you go to a library, you want to check out just the books that you want to read. In order to find a book in a large library you need a catalog. Without a good catalog it is difficult to make use of a library, or any other resource containing significant amount of information.

**What?**

Just as in the library, IDC maintains a catalog that indexes a variety of metadata fields describing the files we curate. That metadata catalog is accessible in a large database table that you should be using to search and subset the images. All of the data in IDC is in DICOM format, and DICOM format is all about metadata! A typical DICOM image will contain dozens if not hundreds of attributes describing its content.

We extract all of the DICOM attributes, and store the result in a large table, where each row of that table corresponds to a file (and most often, one slice of a CT or MR image corresponds to one DICOM file), and each column corresponds to a metadata attribute. IDC catalog of all the metadata is enormous: as of writing, for IDC release v16, this table contains >42M rows and 869 columns! We will refer to this gigantic catalog as _IDC BigQuery index_ (you can learn how to use this index in another tutorial).

The issue is, _IDC BigQuery index_ is very large, requires rather powerful resources to search it, can be intimidating to the novice IDC users, and is not necessary for most common search tasks. This is why we developed a small index of IDC data that contains just a fraction of the metadata attributes. Since this index is small, it can be distributed and searched easily. The downside of course is that you cannot search all of the metadata.

We wrapped the IDC "mini" index into the `idc-index` python package, which we will be focusing on in this tutorial.

**How?**

When you search, or _query_ IDC catalog, you specify what criteria should the metadata describing the selected files satisfy.

Queries can be as simple as

* "_everything in collection X_",

or as complex as

* "_files corresponding to CT images of female patients that are accompanied by annotations of lung tumors that are larger than 1500 mm^3 in volume_".

Although it would be very nice to just state what you need in free form (and let AI write the query for you - which is becoming more and more feasible - see one such early results in [this preprint](https://arxiv.org/abs/2305.07637)!), in practice most often queries need to be written in a formal way.

To query IDC index, you can utilize Standard Query Language (SQL). You can use SQL with both the IDC BigQuery index, and with the IDC "mini" index available in the `idc-index` python package.

In the following steps of the tutorial we will use just a few of the attributes (SQL table columns) to get started. You will be able to use the same principles and SQL queries to extend your search criteria to include any of the other attributes indexed by IDC.

## Prerequisites

Prerequisites for using IDC "mini" index are very simple: use `pip` to install the `idc-index` package! In the cell below we use a fixed (currently, latest) version of the package for the sake of reproducibility.

Note how we install the specific version of the package. We do this because `idc-index` is in the early stages of development, and its API and capabilities are evolving. By fixing the release version we ensure that the notebook remains functional even if the package API changes in a breaking manner.

Once the package is installed, we instantiate `IDCClient` class that is a wrapper around the "mini" index.


```python
!pip install idc-index --upgrade

from idc_index import index

client = index.IDCClient()
```

## First query

As the very first query, let's get the list of all the image collections available in IDC. Here is that query:

```sql
SELECT
  DISTINCT(collection_id)
FROM
  index
```

Let's look into how this query works:

* `SELECT` defines the list of columns that should be returned by the query,
* `DISTINCT` indicates that we want to see the distinct values encountered in the selected column,
* `FROM` defines which table should be queried. Here, `index` is the internal table availabe within the `idc-index` package.

Next, let's execute that query using the `client` instantiated earlier. The `sql_query` function will return a `pandas` `DataFrame` with the result.


```python
# formatting is not required, but makes queries easier to read!
query = """
SELECT
  DISTINCT(collection_id)
FROM
  index
"""
client.sql_query(query)
```

What other attributes are available in this "mini" index?


```python
print(client.index.columns)
```

## Summarizing the content of the individual collections

Before discussing what each of those attributes means, let's consider a bit more complicated query that utilizes the `Modality` and `BodyPartExamined` to create summary of the collections available in IDC.

In the query above, we use the familiar operators `SELECT` and `FROM`, but also couple of new ones:

* `GROUP BY` in the end of the query indicates that we want to get a single row per the distinct value of the `collection_id`
* `STRING_AGG` and `DISTINCT` indicate how the values of the selected columns should be aggregated while combining into single row per collection_id: we take all the distinct values per individual `collection_id`, and the concatenate them into a single string


```python
query = """
SELECT
  collection_id,
  STRING_AGG(DISTINCT(Modality)) as modalities,
  STRING_AGG(DISTINCT(BodyPartExamined)) as body_parts
FROM
  index
GROUP BY
  collection_id
ORDER BY
  collection_id ASC
"""
client.sql_query(query)
```

As you look at the result of the query, consider that ...
* `Modality` abbreviations are disambiguated in this part of the standard: https://dicom.nema.org/medical/dicom/current/output/chtml/part03/sect_C.7.3.html#sect_C.7.3.1.1.1
* the values of `BodyPartExamined` were curated by IDC to improve conformance to the value set prescribed by the standard (you can see it here: https://dicom.nema.org/medical/dicom/current/output/chtml/part16/chapter_L.html#chapter_L)
* Slide Microscopy modality (`SM`) does not use `BodyPartExamined`, and therefore it is expected that the values of this attribute are blank for the slide microscopy collections.

## Selecting collections based on the specific characteristics

In the following query, we use several of the attributes in the index to select collections that meet specific search criteria: those that contain MR modality, and have Liver as the body part examined.

Note that standard compliant values of `BodyPartExamined` are ALL CAPS! If you wanted to make the search case-insensitive, you could use `UPPER(BodyPartExamined)`.


```python
query = """
SELECT
  DISTINCT(collection_id)
FROM
  index
WHERE
  Modality = 'MR'
  AND BodyPartExamined = 'LIVER'
"""
client.sql_query(query)
```

## DICOM data model: Patients, studies, series and instances

Up to now we searched the data at the granularity of the collections. In practice, we often want to know how many patients meet our search criteria, or what are the specific images that we need to download.

IDC is using DICOM for data representation, and in the DICOM data model, patients (identified by `PatientID`) undergo imaging exams (or _studies_, in DICOM nomenclature).

Each patient will have one or more studies, with each study identified uniquely by the attribute `StudyInstanceUID`. During each of the imaging studies one or more imaging _series_ will be collected. As an example, a Computed Tomography (CT) imaging study may include a volume sweep before and after administration of the contrast agent. Imaging series are uniqiely identified by `SeriesInstanceUID`.

Finally, each imaging series contains one or more _instances_, where each instance corresponds to a file. Most often, one instance corresponds to a single slice from a cross-sectional image. Individual instances are identified by unique `SOPInstanceUID` values.

The figure below, borrowed from the DICOM standard [here](http://dicom.nema.org/medical/dicom/current/output/chtml/part03/chapter_7.html), captures the discussed data model.

![DICOM data model](https://2103490465-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2F-MCTG4fXybYgGMalZnmf-2668963341%2Fuploads%2Fgit-blob-0f639d56e22ae53a03c2ca59c96306c5db51b158%2FPS3.3_7-1a-DICOM_model.png?alt=media)

**image description**: DICOM data model representing the following relationships:
```yaml
entities:
- Patient:
    relationships:
        - makes: 
            target: Study
            cardinality: "1-n"
        - has: 
            target: Study
            cardinality: "1-n"

- Study:
    relationships:
        - comprised_of: 
            target: Modality_Performed_Procedure_Step
            cardinality: "1-n"
        - includes: 
            target: Modality_Performed_Procedure_Step
            cardinality: "1-n"
        - contains: 
            target: Series
            cardinality: "1-n"

- Modality_Performed_Procedure_Step:
    relationships:
        - includes: 
            target: Series
            cardinality: "1-n"

- Equipment:
    relationships:
        - creates: 
            target: Series
            cardinality: "1-n"

- Frame_of_Reference:
    relationships:
        - spatially_defines:
            target: Series
            cardinality: "0-1"
        - spatially_defines:
            target: Registration
            cardinality: "1-n"

- Series:
    relationships:
        - contains:
            target:
            - Presentation_State
            - MR_Spectroscopy
            - Radiotherapy_Objects
            - Encapsulated_Document
            - Real_World_Value_Mapping
            - Stereometric_Relationship
            - Measurements
            - Tractography_Results
            - Registration
            - Fiducials
            - Image
            - Raw_Data
            - Waveform
            - SR_Document
            - Surface
            - Annotations
            cardinality: "0-n"
        - contains: 
            target: Registration
            cardinality: "0-n"

- Presentation_State:
    relationships: []

- MR_Spectroscopy:
    relationships: []

- Radiotherapy_Objects:
    relationships: []

- Encapsulated_Document:
    relationships: []

- Real_World_Value_Mapping:
    relationships: []

- Stereometric_Relationship:
    relationships: []

- Measurements:
    relationships: []

- Tractography_Results:
    relationships: []

- Registration:
    relationships:
        - spatially_defines:
            target: Frame_of_Reference
            cardinality: "1-n"

- Fiducials:
    relationships: []

- Image:
    relationships: []

- Raw_Data:
    relationships: []

- Waveform:
    relationships: []

- SR_Document:
    relationships: []

- Surface:
    relationships: []

- Annotations:
    relationships: []
```

## `idc-index` organization

Having reviewed the DICOM data model, it is time to go over the attributes (columns) included in `idc-index`.

But first, it is important to know that **`idc-index` is series-based**, i.e, it has one row per DICOM series. AI analysis is most often performed at the granularity of the individual series, and therefore selection of the series is a task we address with `idc-index`.

We "compressed" the IDC BigQuery index (which is instance-based) for the sake of efficiency to support basic search capabilities. The convention followed in naming the columns is that every column that is named in CamelCase notation corresponds one-for-one to the DICOM attribute with the same name. Columns starting with a lower-case letter are those that were introduced by the IDC team as part of curation, and do do not fit the DICOM data model. For each of those series our "mini" index contains the following columns.

* non-DICOM attributes assigned/curated by IDC:
  * `collection_id`: short string with the identifier of the collection the series belongs to
  * `analysis_result_id`: this string is not empty if the specific series is part of an analysis results collection; analysis results can be added to a given collection over time
  * `source_DOI`: Digital Object Identifier of the dataset that contains the given series; note that a given collection can include one or more DOIs, since analysis results added to the collection would typically have independent DOI values!
  * `instanceCount`: number of files in the series (typically, this matches the number of slices in cross-sectional modalities)
  * `license_short_name`: short name of the license that governs the use of the files corresponding to the series
  * `series_aws_url`: location of the series files in a public AWS bucket
  * `series_size_MB`: total disk size needed to store the series
* DICOM attributes extracted from the files
  * `PatientID`: identifier of the patient
  * `PatientAge` and `PatientSex`: attributes containing patient age and sex
  * `StudyInstanceUID`: unique identifier of the DICOM study
  * `StudyDescription`: textual description of the study content
  * `StudyDate`: date of the study (note that those dates are shifted, and are not real dates when images were acquired, to protect patient privacy)
  * `SeriesInstanceUID`: unique identifier of the DICOM series
  * `SeriesDate`: date when the series was acquired
  * `SeriesDescription`: textual description of the series content
  * `SeriesNumber`: series number
  * `BodyPartExamined`: body part imaged
  * `Modality`: acquisition modality
  * `Manufacturer`: manufacturer of the equipment that generated the series
  * `ManufacturerModelName`: model name of the equipment

  Similar to how we searched collections, we can filter suitable DICOM series with SQL queries. In the following query we search for MR series that have "PROSTATE" as the `BodyPartExamined`, and list the collections that contain those series, along with the total number of patients, studies, series count, manufacturer values and size on disk in GB.



```python
selection_query = """
SELECT
  collection_id,
  COUNT(DISTINCT(PatientID)) as patient_count,
  COUNT(DISTINCT(StudyInstanceUID)) as study_count,
  COUNT(DISTINCT(SeriesInstanceUID)) as series_count,
  STRING_AGG(DISTINCT(Manufacturer)) as manufacturers,
  SUM(series_size_MB)/1000 as total_size_GB
FROM
  index
WHERE
  Modality = 'MR'
  AND BodyPartExamined = 'PROSTATE'
GROUP BY
  collection_id
ORDER BY
  patient_count DESC
"""
client.sql_query(selection_query)
```

Instead of creating a collection-level summary, we can instead get the list of series that match our selection criteria.


```python
selection_query = """
SELECT
  SeriesInstanceUID,
  SeriesDescription,
  series_aws_url,
  license_short_name,
  source_DOI
FROM
  index
WHERE
  Modality = 'MR'
  AND BodyPartExamined = 'PROSTATE'
"""
client.sql_query(selection_query)
```

# Key operations with IDC cohorts

A "cohort"? What cohort?

In IDC, a _cohort_ is set of objects stored in IDC that share certain characteristics as defined by metadata. In the previous section we defined a query that selects all MR series of the prostate. You can think of that selection as a cohort.

We will show you how to download the series in your cohort, but first - let's learn what you can do without having to download anything!

## Checking licenses and attribution requirements

IDC collects data from various data coordination centers and program. It is important to appreciate that different components of IDC data are covered by different licenses and have attribution requirements that you must follow when using the data!

To get information about license check the `license_short_name`. Most of the data in IDC is covered by the CC-BY (Creative Commons By Attribution).


To make sure you properly comply with the attribution clause, use `source_DOI`. If we prepend `source_DOI` with "https://doi.org/", we will get a URL that you can open to learn more about the dataset that contains the specific series.

If you use data from IDC, we would also appreciate if you acknowledge IDC by citing one of the publications below:

> Fedorov, A., Longabaugh, W. J. R., Pot, D., Clunie, D. A., Pieper, S. D., Gibbs, D. L., Bridge, C., Herrmann, M. D., Homeyer, A., Lewis, R., Aerts, H. J. W., Krishnaswamy, D., Thiriveedhi, V. K., Ciausu, C., Schacherer, D. P., Bontempi, D., Pihl, T., Wagner, U., Farahani, K., Kim, E. & Kikinis, R. _National Cancer Institute Imaging Data Commons: Toward Transparency, Reproducibility, and Scalability in Imaging Artificial Intelligence_. RadioGraphics (2023). https://doi.org/10.1148/rg.230180


```python
from IPython.display import HTML

selection_query = """
SELECT
  SeriesInstanceUID,
  SeriesDescription,
  series_aws_url,
  license_short_name,
  CONCAT('https://doi.org/',source_DOI) as source_DOI_URL
FROM
  index
WHERE
  Modality = 'MR'
  AND BodyPartExamined = 'PROSTATE'
"""
df = client.sql_query(selection_query)

# make the DOI URL clickable
def make_clickable(val):
    return '<a href="{}" target="_blank">{}</a>'.format(val,val)

df['source_DOI_URL'] = df['source_DOI_URL'].apply(make_clickable)

# Display the DataFrame with clickable URLs
HTML(df.to_html(escape=False))
```

## Visualizing individual series

You can easily visualize any of the series in IDC from the convenience of your web browser. Moreover, there are several viewers that are available. Given the information in `idc-index`, all you have to do is build the URL to point the viewers IDC team is maintaining to the specific series of interest.

IDC supports visualization using the hosted instances of the following open source viewers:
* OHIF Viewer v2 (legacy) and v3 (radiology): https://github.com/OHIF/Viewers
* VolView (hosted by Kitware Inc, radiology): https://volview.kitware.com/
* Slim (slide microscopy): https://github.com/ImagingDataCommons/slim

In the following query we build URLs for each of the series to open those in OHIF v2, OHIF v3 and VolView. We apply extra trick to make the links clickable, and limit the search results to 10 series to make the output more readable.

WARNING: Due to a [last-minute bug in `idc-index`](https://github.com/ImagingDataCommons/idc-index/issues/16), VolView URL will not work, but this will be resolved in an upcoming release of `idc-index`.


```python
from IPython.display import HTML

# remember to use the single quotes ' ' for constant strings!
# " " will cause error
selection_query = """
SELECT
  SeriesDescription,
  CONCAT('https://viewer.imaging.datacommons.cancer.gov/viewer/',
     StudyInstanceUID,
     '?SeriesInstanceUID=',
     SeriesInstanceUID) as ohif_v2_url,
  CONCAT('https://viewer.imaging.datacommons.cancer.gov/v3/viewer/?StudyInstanceUIDs=',
  StudyInstanceUID,
  '&SeriesInstanceUID=',
  SeriesInstanceUID) as ohif_v3_url,
  CONCAT('https://volview.kitware.app/?urls=[',
  series_aws_url,
  ']') as volview_url
FROM
  index
WHERE
  Modality = 'MR'
  AND BodyPartExamined = 'PROSTATE'
LIMIT
  10
"""
df = client.sql_query(selection_query)

# if you remove `target="_blank"`, the viewer will open directly
# in the notebook cell!
def make_clickable(val):
    return '<a href="{}" target="_blank">{}</a>'.format(val,val)

df['ohif_v2_url'] = df['ohif_v2_url'].apply(make_clickable)
df['ohif_v3_url'] = df['ohif_v3_url'].apply(make_clickable)
df['volview_url'] = df['volview_url'].apply(make_clickable)

# Display the DataFrame with clickable URLs
HTML(df.to_html(escape=False))
```

## Downloading the content of the cohort

Earlier we mentioned that `series_aws_url` contains the location of the series files in a AWS bucket. Download is as simple as copying the files from the bucket. To perform the download operation, we rely on the open source [`s5cmd` tool](https://github.com/peak/s5cmd), which was installed as part of the `idc-index` package installation. We first prepare `s5cmd` download manifest that contains the list of download commands for all series, and then pass that manifest to a dedicated function.

Let's build and save the manifest first.


```python
downloadDir = '/content/idc_downloads'

!rm -rf {downloadDir}
!mkdir -p {downloadDir}

selection_query = """
SELECT
  CONCAT('cp ',series_aws_url,' /content/idc_downloads') as cp_command
FROM
  index
WHERE
  Modality = 'MR'
  AND BodyPartExamined = 'PROSTATE'
LIMIT
  10
"""
df = client.sql_query(selection_query)

with open('/content/idc_downloads/download_manifest.txt', 'w') as f:
  f.write('\n'.join(df['cp_command']))
```


```python
# examine the content of the manifest
!head /content/idc_downloads/download_manifest.txt
```


```python
# efficiently download the files corresponding to the manifest
s5cmd_binary = client.s5cmdPath

!{s5cmd_binary} --no-sign-request --endpoint-url https://s3.amazonaws.com run /content/idc_downloads/download_manifest.txt
```

## Summary

After completing this tutorial, you hopefully:
* developed basic understanding of the IDC image metadata and its organization
* learned about `idc-index` as the tool for searching IDC metadata
* are motivated to start experimenting with the SQL interface to select subsets of IDC data at different levels of data model (collection, patient, study, series)
* understood how to script download of the data available in IDC

If you have any questions about this tutorial, or about searching IDC metadata, please send us an email to support@canceridc.dev or posting your question on [IDC User forum](https://discourse.cancer.dev)!

This tutorial barely scratches the surface of what you can do with BigQuery SQL. If you are interested in a comprehensive tutorial about BigQuery SQL, check out this ["Intro to SQL" course on Kaggle](https://www.kaggle.com/learn/intro-to-sql)!

If you are interested to do a deeper dive into SQL and experiment with IDC BigQuery index, check out the "original" ["Getting Started with IDC"](https://github.com/ImagingDataCommons/IDC-Tutorials/tree/master/notebooks/getting_started) series that utilizes BigQuery!

## Acknowledgments

Imaging Data Commons has been funded in whole or in part with Federal funds from the National Cancer Institute, National Institutes of Health, under Task Order No. HHSN26110071 under Contract No. HHSN261201500003l.

If you use IDC in your research, please cite the following publication:

> Fedorov, A., Longabaugh, W. J. R., Pot, D., Clunie, D. A., Pieper, S. D., Gibbs, D. L., Bridge, C., Herrmann, M. D., Homeyer, A., Lewis, R., Aerts, H. J. W., Krishnaswamy, D., Thiriveedhi, V. K., Ciausu, C., Schacherer, D. P., Bontempi, D., Pihl, T., Wagner, U., Farahani, K., Kim, E. & Kikinis, R. _National Cancer Institute Imaging Data Commons: Toward Transparency, Reproducibility, and Scalability in Imaging Artificial Intelligence_. RadioGraphics (2023). https://doi.org/10.1148/rg.230180