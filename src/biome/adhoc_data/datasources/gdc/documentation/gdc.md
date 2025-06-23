# Search and Retrieval

## Introducing Search and Retrieval Requests

The GDC API provides endpoints that search and retrieve information stored in the GDC according to the [GDC Data Model](../../Data/Data_Model/GDC_Data_Model.md). The general format of requests to search & retrieval endpoints is described below.

**Note:** Queries described in this section work for datasets that have been released to the GDC Data Portal. Unreleased data that is in the process of being submitted to GDC cannot be queried using these methods. See [Submission](Submission.md) to learn how to query unreleased data using GraphQL.

### Components of a Request

A typical search and retrieval API request specifies the following parameters:

- a `filters` parameter, that specifies the search terms for the query
- several parameters that specify the API response, such as:
	- `format` &mdash; specifies response format (JSON, TSV, XML)
	- `fields` &mdash; specifies the which data elements should be returned in the response, if available
	- `size` &mdash; specifies the the maximum number of results to include in the response
	- other parameters are described below.

Requests can be executed using HTTP GET or HTTP POST. GET requests are limited by maximum URL length, so the POST method is recommended for large queries.

**Note:** Requests for information stored in the GDC Legacy Archive must be directed to `legacy/` endpoints. See [Getting Started](Getting_Started.md#gdc-legacy-archive) for details.

### POST Example

The following is an example of an HTTP POST request to the `files` endpoint of the GDC API. It looks for Gene Expression Quantification files associated with specific TCGA cases (represented by TCGA barcodes) and retrieves the associated biospecimen metadata in TSV format.

#### Request

	curl --request POST --header "Content-Type: application/json" --data @Payload 'https://api.gdc.cancer.gov/files' > response.tsv

#### Payload

	{
	    "filters":{
	        "op":"and",
	        "content":[
	            {
	                "op":"in",
	                "content":{
	                    "field":"cases.submitter_id",
	                    "value":[
	                        "TCGA-CK-4948",
	                        "TCGA-D1-A17N",
	                        "TCGA-4V-A9QX",
	                        "TCGA-4V-A9QM"
	                    ]
	                }
	            },
	            {
	                "op":"=",
	                "content":{
	                    "field":"files.data_type",
	                    "value":"Gene Expression Quantification"
	                }
	            }
	        ]
	    },
	    "format":"tsv",
	    "fields":"file_id,file_name,cases.submitter_id,cases.case_id,data_category,data_type,cases.samples.tumor_descriptor,cases.samples.tissue_type,cases.samples.sample_type,cases.samples.submitter_id,cases.samples.sample_id,analysis.workflow_type,cases.project.project_id,cases.samples.portions.analytes.aliquots.aliquot_id,cases.samples.portions.analytes.aliquots.submitter_id",
	    "size":"1000"
	}

Each component of the request is explained below.

### GET Example

The above request can be executed as an HTTP GET:

	https://api.gdc.cancer.gov/files?filters=%7B%22op%22%3A%22and%22%2C%22content%22%3A%5B%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22cases.submitter_id%22%2C%22value%22%3A%5B%22TCGA-CK-4948%22%2C%22TCGA-D1-A17N%22%2C%22TCGA-4V-A9QX%22%2C%22TCGA-4V-A9QM%22%5D%7D%7D%2C%7B%22op%22%3A%22%3D%22%2C%22content%22%3A%7B%22field%22%3A%22files.data_type%22%2C%22value%22%3A%22Gene%20Expression%20Quantification%22%7D%7D%5D%7D&format=tsv&fields=file_id,file_name,cases.submitter_id,cases.case_id,data_category,data_type,cases.samples.tumor_descriptor,cases.samples.tissue_type,cases.samples.sample_type,cases.samples.submitter_id,cases.samples.sample_id,analysis.workflow_type,cases.project.project_id,cases.samples.portions.analytes.aliquots.aliquot_id,cases.samples.portions.analytes.aliquots.submitter_id&size=1000

Each component of the request is explained below.


## Endpoints

The following search and retrieval endpoints are available in the GDC API:

| Endpoints | Description |
| --- | --- |
| [files](/API/Users_Guide/Search_and_Retrieval/#files-endpoint) | Information about files stored in the GDC |
| [cases](/API/Users_Guide/Search_and_Retrieval/#cases-endpoint) | Information related to cases, or sample donors |
| [history](/API/Users_Guide/Search_and_Retrieval/#history-endpoint) | Information related to file version history |
| [projects](/API/Users_Guide/Search_and_Retrieval/#project-endpoint) | Information about projects |
| [annotations](/API/Users_Guide/Search_and_Retrieval/#annotations-endpoint) | Information about annotations to GDC data |
| \_mapping | Information about elements that can be used to query other endpoints |

The choice of endpoint determines what is listed in the search results. The `files` endpoint will generate a list of files, whereas the `cases` endpoint will generate a list of cases. Each of the above endpoints, other than `_mapping`, can query and return any of the related fields in the [GDC Data Model](../../Data/Data_Model/GDC_Data_Model.md). So the `cases` endpoint can be queried for file fields (e.g. to look for cases that have certain types of experimental data), and the `files` endpoint can be queried for clinical metadata associated with a case (e.g. to look for files from cases diagnosed with a specific cancer type).

### Project Endpoint
The `projects` endpoint provides access to project records, the highest level of data organization in the GDC.

#### Example
This example is a query for projects contained in the GDC. It uses the [from](#from), [size](#size), [sort](#sort), and [pretty](#pretty) parameters, and returns the first two projects sorted by project id.

```shell
curl 'https://api.gdc.cancer.gov/projects?from=0&size=2&sort=project.project_id:asc&pretty=true'
```
``` Output
{
  "data": {
    "hits": [
      {
        "dbgap_accession_number": null,
        "disease_type": [
          "Brain Lower Grade Glioma"
        ],
        "released": true,
        "state": "legacy",
        "primary_site": [
          "Brain"
        ],
        "project_id": "TCGA-LGG",
        "id": "TCGA-LGG",
        "name": "Brain Lower Grade Glioma"
      },
      {
        "dbgap_accession_number": null,
        "disease_type": [
          "Thyroid Carcinoma"
        ],
        "released": true,
        "state": "legacy",
        "primary_site": [
          "Thyroid"
        ],
        "project_id": "TCGA-THCA",
        "id": "TCGA-THCA",
        "name": "Thyroid Carcinoma"
      }
    ],
    "pagination": {
      "count": 2,
      "sort": "project.project_id:asc",
      "from": 0,
      "page": 1,
      "total": 39,
      "pages": 20,
      "size": 2
    }
  },
  "warnings": {}
}
```

#### Retrieval of project metadata using project_id

The `project` endpoint supports a simple query format that retrieves the metadata of a single project using its `project_id`:

```shell
curl 'https://api.gdc.cancer.gov/projects/TARGET-NBL?expand=summary,summary.experimental_strategies,summary.data_categories&pretty=true'
```
```Response
{
  "data": {
    "dbgap_accession_number": "phs000467",
    "disease_type": [
      "Neuroblastoma"
    ],
    "summary": {
      "data_categories": [
        {
          "case_count": 151,
          "file_count": 471,
          "data_category": "Transcriptome Profiling"
        },
        {
          "case_count": 1127,
          "file_count": 3,
          "data_category": "Biospecimen"
        },
        {
          "case_count": 216,
          "file_count": 1732,
          "data_category": "Simple Nucleotide Variation"
        },
        {
          "case_count": 7,
          "file_count": 1,
          "data_category": "Clinical"
        },
        {
          "case_count": 270,
          "file_count": 599,
          "data_category": "Raw Sequencing Data"
        }
      ],
      "case_count": 1127,
      "file_count": 2806,
      "experimental_strategies": [
        {
          "case_count": 221,
          "file_count": 2174,
          "experimental_strategy": "WXS"
        },
        {
          "case_count": 151,
          "file_count": 628,
          "experimental_strategy": "RNA-Seq"
        }
      ],
      "file_size": 8157614402888
    },
    "released": true,
    "state": "legacy",
    "primary_site": [
      "Nervous System"
    ],
    "project_id": "TARGET-NBL",
    "name": "Neuroblastoma"
  },
  "warnings": {}
}
```

### Files Endpoint

The GDC Files Endpoint `https://api.gdc.cancer.gov/files` enables search and retrieval of information relating to files stored in the GDC, including file properties such as `file_name`, `md5sum`, `data_format`, and others.

#### Example

This example is a query for files contained in the GDC. It uses the [from](#from), [size](#size), [sort](#sort), and [pretty](#pretty) parameters, and returns only the first two files, sorted by file size, from smallest to largest.

```shell
curl 'https://api.gdc.cancer.gov/files?from=0&size=2&sort=file_size:asc&pretty=true'
```
``` Output
{
  "data": {
    "hits": [
      {
        "data_release": "13.0",
        "data_type": "Raw Simple Somatic Mutation",
        "updated_datetime": "2018-07-20T22:27:55.342974+00:00",
        "file_name": "333193d5-ca9a-4262-81f5-e9f3b44358fe.vcf.gz",
        "submitter_id": "AD19_SimpleSomaticMutation",
        "file_id": "333193d5-ca9a-4262-81f5-e9f3b44358fe",
        "file_size": 866,
        "id": "333193d5-ca9a-4262-81f5-e9f3b44358fe",
        "created_datetime": "2017-09-10T19:16:02.549312-05:00",
        "md5sum": "e33e95edb778fe67643162ef0ae3297e",
        "data_format": "VCF",
        "acl": [
          "phs001179"
        ],
        "access": "controlled",
        "state": "released",
        "version": "1",
        "data_category": "Simple Nucleotide Variation",
        "type": "simple_somatic_mutation",
        "experimental_strategy": "Targeted Sequencing"
      },
      {
        "data_release": "13.0",
        "data_type": "Raw Simple Somatic Mutation",
        "updated_datetime": "2018-07-20T22:27:55.342974+00:00",
        "file_name": "d9114e23-0f62-4979-aefc-0dd4d5eb891b.vcf.gz",
        "submitter_id": "AD116_SimpleSomaticMutation",
        "file_id": "d9114e23-0f62-4979-aefc-0dd4d5eb891b",
        "file_size": 866,
        "id": "d9114e23-0f62-4979-aefc-0dd4d5eb891b",
        "created_datetime": "2017-09-10T21:53:02.376246-05:00",
        "md5sum": "95bbfd0586d3c284e9f88edf3bf26065",
        "data_format": "VCF",
        "acl": [
          "phs001179"
        ],
        "access": "controlled",
        "state": "released",
        "version": "1",
        "data_category": "Simple Nucleotide Variation",
        "type": "simple_somatic_mutation",
        "experimental_strategy": "Targeted Sequencing"
      }
    ],
    "pagination": {
      "count": 2,
      "sort": "file_size:asc",
      "from": 0,
      "page": 1,
      "total": 356381,
      "pages": 178191,
      "size": 2
    }
  },
  "warnings": {}
}
```

#### Retrieval of file metadata using individual UUIDs:

The `\files` endpoint supports a simple query format that retrieves the metadata of a single file using its UUID.  Note that the `\files` endpoint is inactive when querying for earlier file versions.  In that case, the `\history` or `/files/versions` endpoints should be used instead.

```Shell
curl 'https://api.gdc.cancer.gov/files/874e71e0-83dd-4d3e-8014-10141b49f12c?pretty=true'
```
``` Output
{
  "data": {
    "data_release": "13.0",
    "data_type": "Raw Simple Somatic Mutation",
    "updated_datetime": "2018-07-20T22:27:55.342974+00:00",
    "created_datetime": "2016-06-03T17:03:06.608739-05:00",
    "file_name": "874e71e0-83dd-4d3e-8014-10141b49f12c.vcf.gz",
    "md5sum": "acf2929b1b825bcd1377023e8b8767ec",
    "data_format": "VCF",
    "acl": [
      "phs000178"
    ],
    "access": "controlled",
    "state": "live",
    "version": "1",
    "file_id": "874e71e0-83dd-4d3e-8014-10141b49f12c",
    "data_category": "Simple Nucleotide Variation",
    "file_size": 122293,
    "submitter_id": "TCGA-V4-A9EZ-01A-11D-A39W-08_TCGA-V4-A9EZ-10A-01D-A39Z-08_mutect",
    "type": "simple_somatic_mutation",
    "experimental_strategy": "WXS"
  },
  "warnings": {}
}
```

__Note:__ The `file_size` field associated with each file is reported in bytes.  


#### Example of retrieving file version information:

The `https://api.gdc.cancer.gov/files/versions` endpoint enables search and retrieval of version information about a file.  A file may be versioned if a file is updated by the GDC (e.g. using a new alignment algorithm or fixing a file that contained an error). `Version` refers to the instance of a particular file.  Inputs can either be a list of UUIDs as shown in example 1 or a download manifest as shown in example 2.  Output includes information about the current and latest version for any given file.  While `/files` also returns information about a file version this endpoint will only work for the most recent version of a file whereas `/files/versions` will work for all previous and current versions of a file.  In both examples below the output format can be modified by adding the `format=tsv` parameter.

```Shell1
curl 'https://api.gdc.cancer.gov/files/versions/1dd28069-5777-4ff9-bd2b-d1ba68e88b06,2a03abac-f1a2-49a9-a57c-7543739dd862?pretty=true'
```

``` Output1
[
  {
    "latest_size": 332092,
    "latest_id": "1dd28069-5777-4ff9-bd2b-d1ba68e88b06",
    "latest_version": "1",
    "filename": "1dd28069-5777-4ff9-bd2b-d1ba68e88b06.vcf.gz",
    "state": "validated",
    "version": "1",
    "latest_filename": "1dd28069-5777-4ff9-bd2b-d1ba68e88b06.vcf.gz",
    "latest_release": [
      "13.0"
    ],
    "latest_state": "validated",
    "release": "13.0",
    "latest_md5": "c2f9b196e154906a70c7ec46492a859d",
    "size": 332092,
    "id": "1dd28069-5777-4ff9-bd2b-d1ba68e88b06",
    "md5": "c2f9b196e154906a70c7ec46492a859d"
  },
  {
    "latest_size": 6653119038,
    "latest_id": "2a03abac-f1a2-49a9-a57c-7543739dd862",
    "latest_version": "1",
    "filename": "a5d86cde-32ca-4ed6-b1a5-5a47575f2ac6_gdc_realn_rehead.bam",
    "state": "validated",
    "version": "1",
    "latest_filename": "a5d86cde-32ca-4ed6-b1a5-5a47575f2ac6_gdc_realn_rehead.bam",
    "latest_release": [
      "13.0"
    ],
    "latest_state": "validated",
    "release": "13.0",
    "latest_md5": "48686fcd84ac713d44261ca9e26b89fb",
    "size": 6653119038,
    "id": "2a03abac-f1a2-49a9-a57c-7543739dd862",
    "md5": "48686fcd84ac713d44261ca9e26b89fb"
  }
]
```
```Shell2
curl --request POST --header "Content-Type: text/tsv"  https://api.gdc.cancer.gov/files/versions/manifest?pretty=true --data-binary @gdc_manifest_20180809_154816.txt
```

``` Output2
[{
  "latest_size": 44857,
  "state": "validated",
  "latest_version": "1",
  "filename": "nationwidechildrens.org_clinical.TCGA-13-1500.xml",
  "latest_id": "0b20e27c-9a09-4f15-923f-d5b4f185dc22",
  "version": "1",
  "latest_filename": "nationwidechildrens.org_clinical.TCGA-13-1500.xml",
  "latest_release": [
    "12.0"
  ],
  "latest_state": "validated",
  "release": "12.0",
  "latest_md5": "597aa4df24c4d544b6c25cbd8b25a33e",
  "md5": "597aa4df24c4d544b6c25cbd8b25a33e",
  "id": "0b20e27c-9a09-4f15-923f-d5b4f185dc22",
  "size": 44857
},{
  "latest_size": 27620,
  "state": "validated",
  "latest_version": "1",
  "filename": "BUCKS_p_TCGA_272_273_N_GenomeWideSNP_6_G05_1320676.grch38.seg.v2.txt",
  "latest_id": "3edc7084-013c-4493-8507-c00b0e9962d8",
  "version": "1",
  "latest_filename": "BUCKS_p_TCGA_272_273_N_GenomeWideSNP_6_G05_1320676.grch38.seg.v2.txt",
  "latest_release": [
    "12.0"
  ],
  "latest_state": "validated",
  "release": "12.0",
  "latest_md5": "35a18d990a05eedfaf96e753bee0b96d",
  "md5": "35a18d990a05eedfaf96e753bee0b96d",
  "id": "3edc7084-013c-4493-8507-c00b0e9962d8",
  "size": 27620
},{
  "latest_size": 2346,
  "state": "validated",
  "latest_version": "1",
  "filename": "a22f5e32-b16e-458f-a412-7e438056ece6.vep.vcf.gz",
  "latest_id": "a22f5e32-b16e-458f-a412-7e438056ece6",
  "version": "1",
  "latest_filename": "a22f5e32-b16e-458f-a412-7e438056ece6.vep.vcf.gz",
  "latest_release": [
    "12.0"
  ],
  "latest_state": "validated",
  "release": "12.0",
  "latest_md5": "68b2433b31679bbbc6681919a1b81762",
  "md5": "68b2433b31679bbbc6681919a1b81762",
  "id": "a22f5e32-b16e-458f-a412-7e438056ece6",
  "size": 2346
},{
  "latest_size": 35411,
  "state": "validated",
  "latest_version": "1",
  "filename": "CYANS_p_TCGAb_422_423_424_NSP_GenomeWideSNP_6_G12_1513758.nocnv_grch38.seg.v2.txt",
  "latest_id": "ac7d2078-bd6b-446e-b30a-d889da5624b6",
  "version": "1",
  "latest_filename": "CYANS_p_TCGAb_422_423_424_NSP_GenomeWideSNP_6_G12_1513758.nocnv_grch38.seg.v2.txt",
  "latest_release": [
    "12.0"
  ],
  "latest_state": "validated",
  "release": "12.0",
  "latest_md5": "6338826b620773062232830fad51ae64",
  "md5": "6338826b620773062232830fad51ae64",
  "id": "ac7d2078-bd6b-446e-b30a-d889da5624b6",
  "size": 35411
}]
```

### Cases Endpoint

The GDC Cases Endpoint `https://api.gdc.cancer.gov/cases` enables search and retrieval of information related to a specific case.

__Note:__ The `cases` endpoint is designed to retrieve the metadata associated with one or more cases, including all nested biospecimen entities. Filters can be applied to retrieve information for entire cases, but not for lower-level biospecimen entities. For example, a sample within a case cannot be used to query for aliquots that are associated only with that sample. All aliquots associated with the case would be retrieved.


#### Example

This example is a query for files contained in GDC. It returns case where submitter id is `TCGA-BH-A0EA`, using the [pretty](#pretty) and [filters](#filters) parameters and the following [filtering operators](#filtering-operators):

	{"op":"and","content":[{"op":"in","content":{"field":"submitter_id","value":["TCGA-BH-A0EA"]}}]}

Command:

```shell
curl 'https://api.gdc.cancer.gov/cases?filters=%7B%22op%22%3A%22and%22%2C%22content%22%3A%5B%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22submitter_id%22%2C%22value%22%3A%5B%22TCGA-BH-A0EA%22%5D%7D%7D%5D%7D%0A%0A&pretty=true'
```
``` Output
{
	{
	  "data": {
	    "hits": [
	      {
	        "updated_datetime": "2017-03-04T16:39:19.244769-06:00",
	        "submitter_analyte_ids": [
	          "TCGA-BH-A0EA-01A-11R",
	          "TCGA-BH-A0EA-10A-01W",
	          "TCGA-BH-A0EA-01A-11W",
	          "TCGA-BH-A0EA-01A-11D",
	          "TCGA-BH-A0EA-10A-01D"
	        ],
	        "analyte_ids": [
	          "fe678556-acf4-4bde-a95e-860bb0150a95",
	          "66ed0f86-5ca5-4dec-ba76-7ee4dcf31831",
	          "f19f408a-815f-43d9-8032-e9482b796371",
	          "69ddc092-88a0-4839-a2bb-9f1c9e760409",
	          "30cb470f-66d4-4085-8c30-83a42e8453d4"
	        ],
	        "submitter_id": "TCGA-BH-A0EA",
	        "case_id": "1f601832-eee3-48fb-acf5-80c4a454f26e",
	        "id": "1f601832-eee3-48fb-acf5-80c4a454f26e",
	        "disease_type": "Breast Invasive Carcinoma",
	        "sample_ids": [
	          "9a6c71a6-82cd-42b1-a93f-f569370848d6",
	          "7f791228-dd77-4ab0-8227-d784a4c7fea1"
	        ],
	        "portion_ids": [
	          "cb6086d1-3416-4310-b109-e8fa6e8b72d4",
	          "8629bf5a-cdaf-4f6a-90bb-27dd4a7565c5",
	          "ae4f5816-f97a-4605-9b05-9ab820467dee"
	        ],
	        "submitter_portion_ids": [
	          "TCGA-BH-A0EA-01A-21-A13C-20",
	          "TCGA-BH-A0EA-01A-11",
	          "TCGA-BH-A0EA-10A-01"
	        ],
	        "created_datetime": null,
	        "slide_ids": [
	          "90154ea1-6b76-4445-870e-d531d6fa1239",
	          "a0826f0d-986a-491b-8c6f-b34f8929f3ee"
	        ],
	        "state": "live",
	        "aliquot_ids": [
	          "eef9dce1-6ba6-432b-bbe2-53c7dbe64fe7",
	          "cde982b7-3b0a-49eb-8710-a599cb0e44c1",
	          "b1a3739d-d554-4202-b96f-f25a444e2042",
	          "97c64d6a-7dce-4d0f-9cb3-b3e4eb4719c5",
	          "561b8777-801a-49ed-a306-e7dafeb044b6",
	          "42d050e4-e8ee-4442-b9c0-0ee14706b138",
	          "ca71ca96-cbb7-4eab-9487-251dda34e107",
	          "cfbd5476-e83a-401d-9f9a-639c73a0e35b",
	          "edad5bd3-efe0-4c5f-b05c-2c0c2951c45a",
	          "262715e1-835c-4f16-8ee7-6900e26f7cf5",
	          "2beb34c4-d493-4a73-b21e-de77d43251ff",
	          "bcb7fc6d-60a0-48b7-aa81-14c0dda72d76"
	        ],
	        "primary_site": "Breast",
	        "submitter_aliquot_ids": [
	          "TCGA-BH-A0EA-10A-01D-A113-01",
	          "TCGA-BH-A0EA-01A-11R-A115-07",
	          "TCGA-BH-A0EA-01A-11D-A10Y-09",
	          "TCGA-BH-A0EA-01A-11D-A314-09",
	          "TCGA-BH-A0EA-01A-11R-A114-13",
	          "TCGA-BH-A0EA-01A-11D-A111-01",
	          "TCGA-BH-A0EA-01A-11D-A112-05",
	          "TCGA-BH-A0EA-01A-11D-A10X-02",
	          "TCGA-BH-A0EA-10A-01D-A110-09",
	          "TCGA-BH-A0EA-10A-01W-A12U-09",
	          "TCGA-BH-A0EA-10A-01D-A10Z-02",
	          "TCGA-BH-A0EA-01A-11W-A12T-09"
	        ],
	        "submitter_sample_ids": [
	          "TCGA-BH-A0EA-10A",
	          "TCGA-BH-A0EA-01A"
	        ],
	        "submitter_slide_ids": [
	          "TCGA-BH-A0EA-01A-01-MSA",
	          "TCGA-BH-A0EA-01A-01-TSA"
	        ]
	      }
	    ],
	    "pagination": {
	      "count": 1,
	      "sort": "",
	      "from": 0,
	      "page": 1,
	      "total": 1,
	      "pages": 1,
	      "size": 10
	    }
	  },
	  "warnings": {}
	}
```

#### Retrieval of case metadata using individual UUIDs:

The `cases` endpoint supports a simple query format that retrieves the metadata of a single case using its UUID:

```shell
curl 'https://api.gdc.cancer.gov/cases/1f601832-eee3-48fb-acf5-80c4a454f26e?pretty=true&expand=diagnoses'
```
```Response
{
  "data": {
    "diagnoses": [
      {
        "classification_of_tumor": "not reported",
        "last_known_disease_status": "not reported",
        "updated_datetime": "2016-05-16T10:59:16.740358-05:00",
        "primary_diagnosis": "c50.9",
        "submitter_id": "TCGA-BH-A0EA_diagnosis",
        "tumor_stage": "stage iia",
        "age_at_diagnosis": 26548.0,
        "vital_status": "dead",
        "morphology": "8500/3",
        "days_to_death": 991.0,
        "days_to_last_known_disease_status": null,
        "days_to_last_follow_up": null,
        "state": null,
        "days_to_recurrence": null,
        "diagnosis_id": "84654ad5-2a2c-5c3b-8340-ecac6a5550fe",
        "tumor_grade": "not reported",
        "tissue_or_organ_of_origin": "c50.9",
        "days_to_birth": -26548.0,
        "progression_or_recurrence": "not reported",
        "prior_malignancy": "not reported",
        "site_of_resection_or_biopsy": "c50.9",
        "created_datetime": null
      }
    ],
    "sample_ids": [
      "7f791228-dd77-4ab0-8227-d784a4c7fea1",
      "9a6c71a6-82cd-42b1-a93f-f569370848d6"
    ],
    "portion_ids": [
      "cb6086d1-3416-4310-b109-e8fa6e8b72d4",
      "8629bf5a-cdaf-4f6a-90bb-27dd4a7565c5",
      "ae4f5816-f97a-4605-9b05-9ab820467dee"
    ],
    "submitter_portion_ids": [
      "TCGA-BH-A0EA-01A-11",
      "TCGA-BH-A0EA-01A-21-A13C-20",
      "TCGA-BH-A0EA-10A-01"
    ],
    "created_datetime": null,
    "submitter_aliquot_ids": [
      "TCGA-BH-A0EA-01A-11R-A114-13",
      "TCGA-BH-A0EA-01A-11D-A111-01",
      "TCGA-BH-A0EA-01A-11W-A12T-09",
      "TCGA-BH-A0EA-01A-11R-A114-13",
      "TCGA-BH-A0EA-01A-11R-A115-07",
      "TCGA-BH-A0EA-01A-11D-A111-01",
      "TCGA-BH-A0EA-01A-11D-A314-09",
      "TCGA-BH-A0EA-01A-11D-A112-05",
      "TCGA-BH-A0EA-01A-11D-A10Y-09",
      "TCGA-BH-A0EA-01A-11D-A10X-02",
      "TCGA-BH-A0EA-01A-11W-A12T-09",
      "TCGA-BH-A0EA-01A-11D-A10X-02",
      "TCGA-BH-A0EA-01A-11D-A10Y-09",
      "TCGA-BH-A0EA-01A-11D-A314-09",
      "TCGA-BH-A0EA-01A-11R-A115-07",
      "TCGA-BH-A0EA-01A-11D-A112-05",
      "TCGA-BH-A0EA-10A-01D-A110-09",
      "TCGA-BH-A0EA-10A-01D-A113-01",
      "TCGA-BH-A0EA-10A-01W-A12U-09",
      "TCGA-BH-A0EA-10A-01D-A10Z-02",
      "TCGA-BH-A0EA-10A-01D-A113-01",
      "TCGA-BH-A0EA-10A-01D-A110-09",
      "TCGA-BH-A0EA-10A-01W-A12U-09",
      "TCGA-BH-A0EA-10A-01D-A10Z-02"
    ],
    "updated_datetime": "2016-05-02T14:37:43.619198-05:00",
    "submitter_analyte_ids": [
      "TCGA-BH-A0EA-01A-11R",
      "TCGA-BH-A0EA-01A-11D",
      "TCGA-BH-A0EA-01A-11W",
      "TCGA-BH-A0EA-10A-01W",
      "TCGA-BH-A0EA-10A-01D"
    ],
    "analyte_ids": [
      "30cb470f-66d4-4085-8c30-83a42e8453d4",
      "66ed0f86-5ca5-4dec-ba76-7ee4dcf31831",
      "f19f408a-815f-43d9-8032-e9482b796371",
      "69ddc092-88a0-4839-a2bb-9f1c9e760409",
      "fe678556-acf4-4bde-a95e-860bb0150a95"
    ],
    "submitter_id": "TCGA-BH-A0EA",
    "case_id": "1f601832-eee3-48fb-acf5-80c4a454f26e",
    "state": null,
    "aliquot_ids": [
      "bcb7fc6d-60a0-48b7-aa81-14c0dda72d76",
      "97c64d6a-7dce-4d0f-9cb3-b3e4eb4719c5",
      "edad5bd3-efe0-4c5f-b05c-2c0c2951c45a",
      "bcb7fc6d-60a0-48b7-aa81-14c0dda72d76",
      "ca71ca96-cbb7-4eab-9487-251dda34e107",
      "97c64d6a-7dce-4d0f-9cb3-b3e4eb4719c5",
      "eef9dce1-6ba6-432b-bbe2-53c7dbe64fe7",
      "42d050e4-e8ee-4442-b9c0-0ee14706b138",
      "561b8777-801a-49ed-a306-e7dafeb044b6",
      "262715e1-835c-4f16-8ee7-6900e26f7cf5",
      "edad5bd3-efe0-4c5f-b05c-2c0c2951c45a",
      "262715e1-835c-4f16-8ee7-6900e26f7cf5",
      "561b8777-801a-49ed-a306-e7dafeb044b6",
      "eef9dce1-6ba6-432b-bbe2-53c7dbe64fe7",
      "ca71ca96-cbb7-4eab-9487-251dda34e107",
      "42d050e4-e8ee-4442-b9c0-0ee14706b138",
      "cfbd5476-e83a-401d-9f9a-639c73a0e35b",
      "2beb34c4-d493-4a73-b21e-de77d43251ff",
      "b1a3739d-d554-4202-b96f-f25a444e2042",
      "cde982b7-3b0a-49eb-8710-a599cb0e44c1",
      "2beb34c4-d493-4a73-b21e-de77d43251ff",
      "cfbd5476-e83a-401d-9f9a-639c73a0e35b",
      "b1a3739d-d554-4202-b96f-f25a444e2042",
      "cde982b7-3b0a-49eb-8710-a599cb0e44c1"
    ],
    "slide_ids": [
      "90154ea1-6b76-4445-870e-d531d6fa1239",
      "a0826f0d-986a-491b-8c6f-b34f8929f3ee"
    ],
    "submitter_sample_ids": [
      "TCGA-BH-A0EA-01A",
      "TCGA-BH-A0EA-10A"
    ]
  },
  "warnings": {}
}
```

### Annotations Endpoint

The GDC Annotation Endpoint `https://api.gdc.cancer.gov/annotations` enables search and retrieval of annotations stored in the GDC.


#### Example

This example is a query for any annotations **directly** associated with the following GDC entities:

* the case with UUID e0d36cc0-652c-4224-bb10-09d15c7bd8f1
* the sample with UUID 25ebc29a-7598-4ae4-ba7f-618d448882cc
* the aliquot with UUID fe660d7c-2746-4b50-ab93-b2ed99960553

The query uses the [filters](#filters) parameter to specify entity UUIDs. Code samples below include the bare and percent-encoded filter JSON.

```Filter-JSON
{
   "op":"in",
   "content":{
      "field":"entity_id",
      "value":[
         "e0d36cc0-652c-4224-bb10-09d15c7bd8f1",
         "25ebc29a-7598-4ae4-ba7f-618d448882cc",
         "fe660d7c-2746-4b50-ab93-b2ed99960553"
      ]
   }
}
```
```Filter-JSON-percent-encoded
%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22entity_id%22%2C%22value%22%3A%5B%22e0d36cc0-652c-4224-bb10-09d15c7bd8f1%22%2C%2225ebc29a-7598-4ae4-ba7f-618d448882cc%22%2C%22fe660d7c-2746-4b50-ab93-b2ed99960553%22%5D%7D%7D
```
```shell
curl 'https://api.gdc.cancer.gov/annotations?filters=%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22entity_id%22%2C%22value%22%3A%5B%22e0d36cc0-652c-4224-bb10-09d15c7bd8f1%22%2C%2225ebc29a-7598-4ae4-ba7f-618d448882cc%22%2C%22fe660d7c-2746-4b50-ab93-b2ed99960553%22%5D%7D%7D&pretty=true'
```
``` Output
{
  "data": {
    "hits": [
      {
        "category": "Item flagged DNU",
        "status": "Approved",
        "entity_id": "fe660d7c-2746-4b50-ab93-b2ed99960553",
        "classification": "CenterNotification",
        "entity_type": "aliquot",
        "created_datetime": "2015-09-28T00:00:00",
        "annotation_id": "5ddadefe-8b57-5ce2-b8b2-918d63d99a59",
        "notes": "The aliquot failed Broad pipeline QC and not all files are suitable for use. Consult the SDRF file to determine which files are usable.",
        "updated_datetime": "2017-03-09T13:20:38.962182-06:00",
        "submitter_id": "29087",
        "state": "submitted",
        "case_id": "41b59716-116f-4942-8b63-409870a87e26",
        "case_submitter_id": "TCGA-DK-A3IM",
        "entity_submitter_id": "TCGA-DK-A3IM-10A-01D-A20B-01",
        "id": "5ddadefe-8b57-5ce2-b8b2-918d63d99a59"
      },
      {
        "category": "Item is noncanonical",
        "status": "Approved",
        "entity_id": "25ebc29a-7598-4ae4-ba7f-618d448882cc",
        "classification": "Notification",
        "entity_type": "sample",
        "created_datetime": "2012-07-12T00:00:00",
        "annotation_id": "d6500f94-618f-5334-a810-ade76b887ec9",
        "notes": "No Matching Normal",
        "updated_datetime": "2017-03-09T13:47:18.182075-06:00",
        "submitter_id": "8009",
        "state": "submitted",
        "case_id": "bd114e05-5a97-41e2-a0d5-5d39a1e9d461",
        "case_submitter_id": "TCGA-08-0514",
        "entity_submitter_id": "TCGA-08-0514-01A",
        "id": "d6500f94-618f-5334-a810-ade76b887ec9"
      },
      {
        "category": "Prior malignancy",
        "status": "Approved",
        "entity_id": "e0d36cc0-652c-4224-bb10-09d15c7bd8f1",
        "classification": "Notification",
        "entity_type": "case",
        "created_datetime": "2013-03-12T00:00:00",
        "annotation_id": "33336cdf-2cf0-5af2-bb52-fecd3427f180",
        "notes": "Patient had a prior lymphoma. Unknown radiation or systemic chemotherapy.",
        "updated_datetime": "2017-03-09T12:11:31.786013-06:00",
        "submitter_id": "15630",
        "state": "submitted",
        "case_id": "e0d36cc0-652c-4224-bb10-09d15c7bd8f1",
        "case_submitter_id": "TCGA-FS-A1ZF",
        "entity_submitter_id": "TCGA-FS-A1ZF",
        "id": "33336cdf-2cf0-5af2-bb52-fecd3427f180"
      }
    ],
    "pagination": {
      "count": 3,
      "sort": "",
      "from": 0,
      "page": 1,
      "total": 3,
      "pages": 1,
      "size": 10
    }
  },
  "warnings": {}
}
```
### History Endpoint

The GDC History Endpoint `https://api.gdc.cancer.gov/history` enables search and retrieval of version and release information about a file.  This endpoint will return the entire provenance of all versions of a file.  A file may be versioned if a file is updated by the GDC (e.g. using a new alignment algorithm or fixing a file that contained an error). `Version` refers to the instance of a particular file. `Release` refers to which data release a file was part of.  A file may be a part of many different data releases with no change in version number or content.  

#### Example

This example is a query for versioning information associated with the follow with file `1dd28069-5777-4ff9-bd2b-d1ba68e88b06`.


```shell
curl 'https://api.gdc.cancer.gov/history/1dd28069-5777-4ff9-bd2b-d1ba68e88b06'
```
``` Output
[{"release_date": "2018-07-23", "version": "1", "uuid": "1dd28069-5777-4ff9-bd2b-d1ba68e88b06", "file_change": "released", "data_release": "13.0"}]
```


### \_mapping Endpoint

Each search and retrieval endpoint is equipped with a ```_mapping``` endpoint that provides information about available fields. For example, `files/_mapping` endpoint provides information about fields and field groups available at the `files` endpoint: `https://api.gdc.cancer.gov/files/_mapping`.

The high-level structure of a response to a `_mapping` query is as follows:

	"_mapping": {}
	, "defaults": []
	, "expand": []
	, "fields": []
	, "multi": []
	, "nested": []

[//]: # (_)

Each part of the response is described below:

| Part | Description |
|------|-------------|
| `_mapping` | All available fields and their descriptions. The endpoint-agnostic field names provided here are compatible with the `filters` parameter but are not always compatible with the `fields` parameter |
| `defaults` | The default set of fields included in the API response when the `fields` parameter is not used in the request |
| `expand` | Field group names for use with the `expand` parameter |
| `fields` | All available fields in an endpoint-specific format that is compatible with both the `filters` and `fields` parameters |
| `multi` | GDC internal use |
| `nested` | Nested fields |


#### Example

```shell
curl 'https://api.gdc.cancer.gov/projects/_mapping'
```
```output
{
	...

	  "_mapping": {
	    "projects.disease_type": {
	      "doc_type": "projects",
	      "field": "disease_type",
	      "type": "id"
	    },
	    "projects.name": {
	      "doc_type": "projects",
	      "field": "name",
	      "type": "id"
	    }
	  }

	...

}
```

Similar information can be obtained using the `fields` parameter; `fields` queries provide additional information in the response, such as the name of the Elastic Search document (`doc_type`), the field name and the type of value. A list of supported types (such as `string`, `long`, `float`, ...) can be obtained from [Elastic Search Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html).


## Request Parameters

The GDC API supports the following search & retrieval request parameters:

Parameter | Default | Description
--------- | ------- | -----------
filters| null | Specifies search parameters
format | JSON | Specifies the API response format: JSON, XML, or TSV
pretty | false | Returns response with indentations and line breaks in a human-readable format
fields | null | Specifies which fields to include in the response
expand | null | Returns multiple related fields
size | 10 | Specifies the number of results to return
from   | 0 | Specifies the first record to return from a set of search results
sort | null | Specifies sorting for the search results
facets | null | Provides all existing values for a given field and the number of records having this value.


### Filters: Specifying the Query

The `filters` parameter enables passing of complex search queries to the GDC API. The parameter carries a query in the form of a JSON object.

#### Query Format

A `filters` query consists of an operator (or a nested set of operators) with a set of `field` and `value` operands.

The following `filters` query operators are supported by the GDC API:

| Operator | Description                                      | Number of Operands | Logic example                                                |
|----------|--------------------------------------------------|--------------------|--------------------------------------------------------------|
| =        | equals (string or number)                        | one                | gender = "female"                                            |
| !=       | does not equal (string or number)                | one                | project_id != "TARGET-AML"                                   |
| <        | less than (number)                               | one                | age at diagnosis < 90y                                       |
| <=       | less than or equal (number)                      | one                | age at diagnosis <= 17                                       |
| >        | greater than (number)                            | one                | age at diagnosis > 50                                        |
| >=       | greater than or equal (number)                   | one                | age at diagnosis >= 18                                       |
| is       | is (missing)                                     | one                | gender is missing                                            |
| not      | not (missing)                                    | one                | race not missing                                             |
| in       | matches a string or number in (a list)           | multiple           | primary_site in [Brain, Lung]                                |
| exclude  | does not match any strings or values in (a list) | multiple           | experimental_strategy exclude [WXS, WGS, "Genotyping array"] |
| and      | (operation1) and (operation2)                    | multiple           | {primary_site in [Brain, Lung]} and {gender = "female"}      |
| or       | (operation1) or (operation2)                     | multiple           | {project_id != "TARGET-AML"} or {age at diagnosis < 90y}     |

The `field` operand specifies a field that corresponds to a property defined in the [GDC Data Dictionary](../../Data_Dictionary/viewer.md). A list of supported fields is provided in [Appendix A](Appendix_A_Available_Fields.md); the list can also be accessed programmatically at the [_mapping endpoint](#95mapping-endpoint).

The `value` operand specifies the search terms. Users can get a list of available values for a specific property by making a call to the appropriate API endpoint using the `facets` parameter, e.g. `https://api.gdc.cancer.gov/v0/cases?facets=demographic.gender&size=0&pretty=true`. See [Facets](#facets) for details.

A simple query with a single operator looks like this:

	{
	    "op":"=",
	    "content":{
	        "field":"cases.demographic.gender",
	        "value":[
	            "male"
	        ]
	    }
	}

A more complex query with multiple operators looks like this:

	{
	    "op":"and",
	    "content":[
	        {
	            "op":"in",
	            "content":{
	                "field":"cases.submitter_id",
	                "value":[
	                    "TCGA-CK-4948",
	                    "TCGA-D1-A17N",
	                    "TCGA-4V-A9QX",
	                    "TCGA-4V-A9QM"
	                ]
	            }
	        },
	        {
	            "op":"=",
	            "content":{
	                "field":"files.data_type",
	                "value":"Gene Expression Quantification"
	            }
	        }
	    ]
	}


#### Example: HTTP GET Request

This example requests `male` cases using HTTP GET.

The JSON object to be passed to the GDC API looks like:

	{"op": "=",
		  "content": {
			  "field": "cases.demographic.gender",
			  "value": ["male"]
		  }
	}

URL-encoding the above JSON object using [Percent-(URL)-encoding tool](https://www.beautifyconverter.com/json-escape-unescape.php) results in the following string:

	%7b%22op%22%3a+%22%3d%22%2c%0d%0a++++++%22content%22%3a+%7b%0d%0a++++++++++%22field%22%3a+%22cases.clinical.gender%22%2c%0d%0a++++++++++%22value%22%3a+%5b%22male%22%5d%0d%0a++++++%7d%0d%0a%7d

The above string can now be passed to the GDC API using the `filters` parameter:

```shell
 curl  'https://api.gdc.cancer.gov/cases?filters=%7b%22op%22%3a+%22%3d%22%2c%0d%0a++++++%22content%22%3a+%7b%0d%0a++++++++++%22field%22%3a+%22cases.demographic.gender%22%2c%0d%0a++++++++++%22value%22%3a+%5b%22male%22%5d%0d%0a++++++%7d%0d%0a%7d&pretty=true'
```
```python
import requests
import json
cases_endpt = 'https://api.gdc.cancer.gov/cases'
filt = {"op":"=",
        "content":{
            "field": "cases.demographic.gender",
            "value": ["male"]
        }
}
params = {'filters':json.dumps(filt), 'sort':'demographic.gender:asc'}
# requests URL-encodes automatically
response = requests.get(cases_endpt, params = params)
print json.dumps(response.json(), indent=2)
```
``` Output
{
  "data": {
    "hits": [
      {
        "sample_ids": [
          "1d014bf1-95ae-42e3-ae39-97ff4841d8ca",
          "6b685bfc-651b-48d1-8e68-32c8096ea205"
        ],
        "portion_ids": [
          "c061217a-266a-496d-8a96-3489191afa87",
          "0d3a6a58-0e00-4889-bc73-5ddb5a387738",
          "e858ee92-0438-48e9-a70d-80ef2c0ad539"
        ],
        "submitter_portion_ids": [
          "TCGA-66-2770-01A-21-2193-20",
          "TCGA-66-2770-01A-01",
          "TCGA-66-2770-11A-01"
        ],
        "created_datetime": null,
        "submitter_aliquot_ids": [
          "TCGA-66-2770-01A-01D-1522-08",
          "TCGA-66-2770-01A-01D-0848-05",
          "TCGA-66-2770-01A-01W-0879-09",
          "TCGA-66-2770-11A-01W-0878-08",
          "TCGA-66-2770-01A-01R-0849-01",
          "TCGA-66-2770-01A-01W-0877-08",
          "TCGA-66-2770-01A-01D-0846-06",
          "TCGA-66-2770-11A-01W-0880-09",
          "TCGA-66-2770-01A-01D-0964-09",
          "TCGA-66-2770-11A-01D-0846-06",
          "TCGA-66-2770-01A-01D-0845-04",
          "TCGA-66-2770-01A-01W-0881-10",
          "TCGA-66-2770-11A-01D-0963-08",
          "TCGA-66-2770-11A-01D-0844-01",
          "TCGA-66-2770-01A-01R-0851-07",
          "TCGA-66-2770-11A-01W-0882-10",
          "TCGA-66-2770-11A-01D-1522-08",
          "TCGA-66-2770-01A-01T-1557-13",
          "TCGA-66-2770-01A-01D-0847-02",
          "TCGA-66-2770-01A-01D-0844-01",
          "TCGA-66-2770-11A-01D-0847-02",
          "TCGA-66-2770-11A-01D-0964-09",
          "TCGA-66-2770-01A-01D-0963-08",
          "TCGA-66-2770-01A-01R-0850-03",
          "TCGA-66-2770-11A-01D-0845-04",
          "TCGA-66-2770-01A-01T-0852-07"
        ],
        "updated_datetime": "2016-05-02T15:57:03.730994-05:00",
        "submitter_analyte_ids": [
          "TCGA-66-2770-01A-01D",
          "TCGA-66-2770-11A-01W",
          "TCGA-66-2770-01A-01T",
          "TCGA-66-2770-01A-01W",
          "TCGA-66-2770-01A-01R",
          "TCGA-66-2770-11A-01D"
        ],
        "analyte_ids": [
          "385807d3-78de-4558-8d93-702d93fc835a",
          "247acc7a-b4f5-47e9-86da-5ea9b04ad444",
          "151b8cb9-6b0a-4db9-9b0e-62aa501b35d9",
          "e549aebd-4dda-4ea8-8ccf-56c03bc8b2be",
          "631ad4eb-845a-4e70-96ad-4b40157218a8",
          "9a75640e-09d4-42b7-8cb4-75d62b39e98a"
        ],
        "submitter_id": "TCGA-66-2770",
        "case_id": "f1b357e4-d67a-42c9-b0b7-12f69fa3da58",
        "state": null,
        "aliquot_ids": [
          "a2d10f8e-6b27-4df0-bd25-ac24992d0bb4",
          "8c1c733a-abed-468f-b4d0-d1ac34ba6d8b",
          "cad8d384-3b7a-4f70-89c2-5584ae75c5eb",
          "42e774cf-3c4a-4efd-9665-378cb6b4afac",
          "3755168b-f5da-422d-847a-566cb112a8d7",
          "cae4d249-ba67-4316-8761-7e71e3813182",
          "aa6e700c-ce01-4cc9-87de-8bf615a8aa1a",
          "ad5c4069-e616-4ab4-9b03-b196f9189b20",
          "07c26ea4-0584-4cb0-8e5a-d057b8fe6c14",
          "f95c2cb5-d20a-4f1f-8f2a-95a2d37fbdc4",
          "817bf327-e583-4704-b294-c3645dcc4adf",
          "2246cb75-38bd-491f-b6ee-99f4781f2564",
          "a81b9090-626d-492d-9baf-7fa3ef70111c",
          "5cd6f026-894e-45f6-bc59-d6f056e63846",
          "e417903d-ab76-44f0-aae9-3a91fa9a8d3c",
          "1d809a56-31ca-49d8-a57b-e773236b24de",
          "df60a743-ef4b-43ea-bc5a-4d75e8befb8a",
          "871350e2-958f-401c-ae86-6bc880a01942",
          "3dc4207d-5671-4c3d-b75a-d39ef69b564c",
          "69b77cc0-d00a-4ea3-9b39-3e3019d9e292",
          "3d035ee8-9523-4771-8738-c8a5a2f91403",
          "775e46bd-e56f-40fa-9891-aaedc1d49395",
          "d1c60049-922a-42d4-bd7e-8cf4ace47f05",
          "5220a53f-f3fc-476c-aa72-65a038eb2fd8",
          "b7e44e6e-ccf9-4b75-a258-159912ab51ca",
          "42750622-28d7-4d32-9262-b139fe77bc01"
        ],
        "slide_ids": [
          "a10196d2-7a81-4e1e-a9a7-62d123c30875",
          "72edc1ba-916d-42a2-9f22-6254c6e54c5c",
          "ff15eeb9-550e-4c78-90cc-a6cce8ccc3df",
          "71ccfb52-169d-4176-94d6-fff5b75f853d"
        ],
        "submitter_sample_ids": [
          "TCGA-66-2770-11A",
          "TCGA-66-2770-01A"
        ]
      },
      {
        "sample_ids": [
          "06889714-2a40-4248-98ee-f690b301e36a",
          "9f43a0c6-ea19-4021-b0ed-026f33ce1c33"
        ],
        "portion_ids": [
          "3a001d28-7cf9-4c61-b155-73938aebaa25",
          "79554cfd-e853-481e-8e37-1e296034094e"
        ],
        "submitter_portion_ids": [
          "TCGA-02-0075-01A-01",
          "TCGA-02-0075-10A-01"
        ],
        "created_datetime": null,
        "submitter_aliquot_ids": [
          "TCGA-02-0075-01A-01W-0204-02",
          "TCGA-02-0075-01A-01R-0194-03",
          "TCGA-02-0075-01A-01D-0198-02",
          "TCGA-02-0075-01A-01R-0202-01",
          "TCGA-02-0075-10A-01W-0207-09",
          "TCGA-02-0075-01A-01R-0676-04",
          "TCGA-02-0075-10A-01D-0198-02",
          "TCGA-02-0075-10A-01D-0197-06",
          "TCGA-02-0075-10A-01D-0193-01",
          "TCGA-02-0075-01A-01W-0207-09",
          "TCGA-02-0075-01A-01W-0206-08",
          "TCGA-02-0075-01A-01D-0193-01",
          "TCGA-02-0075-10A-01W-0205-10",
          "TCGA-02-0075-01A-01R-0201-02",
          "TCGA-02-0075-10A-01W-0204-02",
          "TCGA-02-0075-01A-01D-0199-05",
          "TCGA-02-0075-10A-01W-0206-08",
          "TCGA-02-0075-01A-01D-0196-04",
          "TCGA-02-0075-01A-01T-0195-07",
          "TCGA-02-0075-10A-01D-0196-04",
          "TCGA-02-0075-01A-01D-0197-06",
          "TCGA-02-0075-01A-01D-0888-01",
          "TCGA-02-0075-01A-01R-0195-07",
          "TCGA-02-0075-01A-01W-0205-10"
        ],
        "updated_datetime": "2016-05-02T15:00:01.972331-05:00",
        "submitter_analyte_ids": [
          "TCGA-02-0075-01A-01R",
          "TCGA-02-0075-10A-01D",
          "TCGA-02-0075-01A-01W",
          "TCGA-02-0075-01A-01T",
          "TCGA-02-0075-01A-01D",
          "TCGA-02-0075-10A-01W"
        ],
        "analyte_ids": [
          "fec22de0-a2b9-45df-9854-1ebe76cee84e",
          "b4d11c50-61f1-4d4a-815f-1c0413018d7f",
          "c48673d0-a38d-44e1-8cfd-e91cb23ea2d5",
          "24f1852c-999a-4ea8-917c-fcfd683e2aca",
          "aa431260-a0fc-4924-80ce-61cab8b5e83e",
          "11f21140-d761-44ca-a9b2-b24099df3b15"
        ],
        "submitter_id": "TCGA-02-0075",
        "case_id": "b196f82b-ef3f-4e05-99f7-da5df65e691e",
        "state": null,
        "aliquot_ids": [
          "75531fe0-101e-4220-bd47-98892c90ee70",
          "e5ea38d4-f47c-4c8a-8bab-13631e0a9a7b",
          "d48b7c2c-daac-4496-af8f-1f45ca43f627",
          "bbba08fc-2514-4e15-afb7-41eecc7e876f",
          "0685b37f-a47c-4222-a846-bf9f3c000de3",
          "683986da-3cee-446d-9b7a-83bef25815c9",
          "e6ffdb20-a1be-4664-bcd3-cc7a4de6f40b",
          "5d1f25c0-9e1a-41ad-9735-134f39dbf70e",
          "528b40b9-246f-4ba3-8209-777136638e62",
          "33131479-5d69-4262-a549-ba8864320f3b",
          "5c7822fc-cf4f-4f62-8482-7c0ce1b7ab9a",
          "b95e7659-e3a4-4e96-b98c-f67d26b85322",
          "30c84aca-f9db-4e07-ac34-1a92b1652ca1",
          "d5e3b5cc-06e0-4294-9d3c-8f3b63acae3d",
          "b14b3d09-3a7f-41a6-81df-2757efa67906",
          "513040e2-dc29-4e2c-86fb-57371eede17a",
          "21c3be1b-7c1e-4864-99d1-486cfe5d8f1d",
          "5e28e5dc-6dfa-44a9-8793-9134cb4cdda5",
          "b8c25892-4773-428f-a02c-f930931268e8",
          "266d5260-08e4-4cec-87f3-ca415bd98575",
          "8859a3ae-f85d-4ef2-830b-80f42f98d53e",
          "ac018a8c-a6e2-4291-a4bf-a330ae9c441e",
          "4b022f7f-7549-4d97-9d41-4e5f2e9ec74c",
          "caad3dfa-74a9-4ecc-95c1-86f6fbfd4ab5"
        ],
        "slide_ids": [
          "39f547cd-5dc3-4bf4-99ea-073bb161c23c",
          "5f096267-0cc2-4cc5-a206-7357159633d7"
        ],
        "submitter_sample_ids": [
          "TCGA-02-0075-10A",
          "TCGA-02-0075-01A"
        ]
      },
      {
        "sample_ids": [
          "ba08195b-31cf-4bb1-a470-23740225c99d",
          "929889c4-e474-4104-b69b-fac7e414a59e"
        ],
        "portion_ids": [
          "48a36eb4-79fb-45e7-8bb1-0fa1d5fcda2c",
          "1de5e67a-ac3f-4c18-92c4-27ba1868c7ac",
          "e09fc5e7-e8d2-4bf9-b12b-17b22e0387e4"
        ],
        "submitter_portion_ids": [
          "TCGA-EJ-A8FU-10A-01",
          "TCGA-EJ-A8FU-01A-21-A43L-20",
          "TCGA-EJ-A8FU-01A-11"
        ],
        "created_datetime": null,
        "submitter_aliquot_ids": [
          "TCGA-EJ-A8FU-01A-11R-A36B-13",
          "TCGA-EJ-A8FU-01A-11R-A36G-07",
          "TCGA-EJ-A8FU-01A-11D-A363-01",
          "TCGA-EJ-A8FU-10A-01D-A361-01",
          "TCGA-EJ-A8FU-10A-01D-A362-08",
          "TCGA-EJ-A8FU-01A-11W-A447-08",
          "TCGA-EJ-A8FU-01A-11D-A365-05",
          "TCGA-EJ-A8FU-01A-11D-A364-08",
          "TCGA-EJ-A8FU-10A-01W-A446-08"
        ],
        "updated_datetime": "2016-05-02T15:57:04.948573-05:00",
        "submitter_analyte_ids": [
          "TCGA-EJ-A8FU-01A-11W",
          "TCGA-EJ-A8FU-01A-11D",
          "TCGA-EJ-A8FU-01A-11R",
          "TCGA-EJ-A8FU-10A-01W",
          "TCGA-EJ-A8FU-10A-01D"
        ],
        "analyte_ids": [
          "2d4e4925-6ac8-498f-882b-4bbf319f6b7b",
          "8d09b982-1256-4674-b383-d6ca4b4bb3c8",
          "c74495d9-63bf-4ac0-b10e-04b3b06103c1",
          "b9884d98-af57-4901-8b9d-4fdbf73d2c5a",
          "2f16ac02-13bf-44fd-bbd7-658c1c384928"
        ],
        "submitter_id": "TCGA-EJ-A8FU",
        "case_id": "23e56e08-e11d-4e83-88a8-1254675b3af8",
        "state": null,
        "aliquot_ids": [
          "e77da017-5dc6-4e32-9568-755e4ee9b533",
          "c9b286d1-d500-4bb3-bb3d-5bf40b1b1265",
          "b7867d52-7987-46d4-a595-0ff5b5375a58",
          "5586ad35-94b7-459e-8982-8e7fb25697a1",
          "162a63f7-594f-4669-a06d-b4899c7fe86a",
          "b8b1ab44-ee6e-4ac5-9efd-d5bd07e67b9c",
          "7adcdf73-3ad3-4da7-ab27-2888f1d4f53a",
          "eb498e52-3eae-402f-8cac-ec930f8d938d",
          "293f781c-c2c7-479b-b1a6-5f951a2c5e5a"
        ],
        "slide_ids": [
          "454a95d5-d084-4f36-b1f1-32c6c23ab46e"
        ],
        "submitter_sample_ids": [
          "TCGA-EJ-A8FU-01A",
          "TCGA-EJ-A8FU-10A"
        ]
      },
      {
        "sample_ids": [
          "d43f0112-fe59-4842-9fda-1189e5fb7248",
          "213cbbe5-c382-47a1-b936-bf40c2c99091"
        ],
        "portion_ids": [
          "26441aae-22e5-4e69-b3f5-34ccde356c93",
          "60d7a93c-0634-438e-a72a-ce63630bb890",
          "246a8f01-7ef2-4737-a984-49aa0b41c089"
        ],
        "submitter_portion_ids": [
          "TCGA-F2-6879-10A-01",
          "TCGA-F2-6879-01A-21-A39M-20",
          "TCGA-F2-6879-01A-11"
        ],
        "created_datetime": "2016-05-02T16:23:44.347995-05:00",
        "submitter_aliquot_ids": [
          "TCGA-F2-6879-01A-11R-2155-13",
          "TCGA-F2-6879-10A-01D-2153-01",
          "TCGA-F2-6879-10A-01D-2152-26",
          "TCGA-F2-6879-01A-11D-2157-05",
          "TCGA-F2-6879-10A-01D-2154-08",
          "TCGA-F2-6879-01A-11D-A45X-08",
          "TCGA-F2-6879-01A-11D-2154-08",
          "TCGA-F2-6879-01A-11W-2179-08",
          "TCGA-F2-6879-01A-11D-2153-01",
          "TCGA-F2-6879-01A-11R-2156-07",
          "TCGA-F2-6879-01A-11D-2152-26",
          "TCGA-F2-6879-10A-01D-A45X-08",
          "TCGA-F2-6879-10A-01W-2179-08",
          "TCGA-F2-6879-01A-01D-YYYY-23"
        ],
        "updated_datetime": "2016-05-02T16:23:44.347995-05:00",
        "submitter_analyte_ids": [
          "TCGA-F2-6879-10A-01D",
          "TCGA-F2-6879-01A-11R",
          "TCGA-F2-6879-10A-01W",
          "TCGA-F2-6879-01A-11W",
          "TCGA-F2-6879-01A-11D"
        ],
        "analyte_ids": [
          "e87dde8d-3bf5-42d8-9a77-620d5c4943e0",
          "30ade77d-996b-4031-93ab-6b341d49eb0a",
          "1d94bd70-6621-4a94-8102-d673663e6665",
          "ea65d92e-1597-410d-84d8-abb2a6235b3e",
          "79697034-1cec-4d92-8195-8a35258ab477"
        ],
        "submitter_id": "TCGA-F2-6879",
        "case_id": "8d9bd437-8b4b-4da5-87ba-6b5790f05022",
        "state": null,
        "aliquot_ids": [
          "e7533585-b062-4d74-b511-05dc806a1357",
          "e107952a-cc2b-4410-b0f9-62e7115430a0",
          "61f1c8b1-986a-485a-9d96-4e4285b6425a",
          "c043e276-fece-4cb9-a848-a0b16e6099b6",
          "e5d110e1-63ad-49ce-b9b7-22bbd7ef8a88",
          "7accb08d-acdb-46bc-bf7f-b9f678193115",
          "a52cd04b-41d6-40db-b050-00ef3a143f7e",
          "207fcf5e-c422-4333-9ec2-5dab38d240c7",
          "5ddd3f83-28a8-4b7f-9aec-203a3c2efbe5",
          "ccd4dd70-c0e4-42cf-870e-33d1013b201a",
          "e12314fe-f16a-4d85-95b4-e712ede450f6",
          "695461e3-283c-4b5b-9325-6b2588b67fd8",
          "8481be1e-0993-487d-8d73-b0eb72b304ee",
          "d7200791-4f1c-418f-8744-91b793486d9f"
        ],
        "slide_ids": [
          "bcbcc947-cab1-4400-aebc-1d9e251a3ce8",
          "cae8d0b9-3605-40af-bf99-7c23df8110a9"
        ],
        "submitter_sample_ids": [
          "TCGA-F2-6879-10A",
          "TCGA-F2-6879-01A"
        ]
      },
      {
        "sample_ids": [
          "3a66b5bd-7037-463c-9f8d-2ba3de9d5571",
          "84f603d6-9f71-48fb-b2e3-190424407452"
        ],
        "portion_ids": [
          "fe90de9f-8ee3-4d55-834f-a90538958cb7",
          "7a0042fd-07f0-4894-adb0-03cebce8aa02"
        ],
        "submitter_portion_ids": [
          "TCGA-VQ-A922-01A-11",
          "TCGA-VQ-A922-10A-01"
        ],
        "created_datetime": "2016-05-02T16:26:23.121974-05:00",
        "submitter_aliquot_ids": [
          "TCGA-VQ-A922-10A-01D-A412-01",
          "TCGA-VQ-A922-01A-11D-A40Z-01",
          "TCGA-VQ-A922-10A-01D-A413-08",
          "TCGA-VQ-A922-01A-01D-YYYY-23",
          "TCGA-VQ-A922-01A-11R-A414-31",
          "TCGA-VQ-A922-01A-11D-A410-08",
          "TCGA-VQ-A922-01A-11R-A415-13",
          "TCGA-VQ-A922-01A-11D-A411-05"
        ],
        "updated_datetime": "2016-05-02T16:26:23.121974-05:00",
        "submitter_analyte_ids": [
          "TCGA-VQ-A922-01A-11R",
          "TCGA-VQ-A922-10A-01D",
          "TCGA-VQ-A922-01A-11D"
        ],
        "analyte_ids": [
          "15bec495-04c7-412b-ad69-26b1f9274ccf",
          "26a24673-04a1-4837-b888-702b0578aef2",
          "2c0ecd67-b9ff-4e60-8d2f-7744c79a13aa"
        ],
        "submitter_id": "TCGA-VQ-A922",
        "case_id": "8bd783a3-d6c9-4c87-a2a1-09f903b9c7ca",
        "state": null,
        "aliquot_ids": [
          "58a121b4-265c-44ae-b6a9-79d087ee8b34",
          "76fbba49-0123-4524-89aa-a1818c5507cb",
          "0b0805bb-edaa-400f-ae9f-effed3dbb605",
          "3370d626-d572-4d13-9cd3-1823a5df3d34",
          "60934993-a9df-4389-b64d-da6844ef22df",
          "243f24ba-bb0f-44e0-bcb1-69a97b395981",
          "6cae9f2a-1c6c-4645-98b6-20719aec1413",
          "44d020d1-c516-4a15-94e8-bcf0cb9c2683"
        ],
        "slide_ids": [
          "0ff02899-57f8-419e-8872-c6ede53f4d3c"
        ],
        "submitter_sample_ids": [
          "TCGA-VQ-A922-10A",
          "TCGA-VQ-A922-01A"
        ]
      },
      {
        "sample_ids": [
          "5bb5bd60-cf47-413b-88fa-f14977e24035",
          "82fcf670-1646-4a28-9578-f7e5b2f426e5",
          "3b87fed0-cfbd-4ee3-b71d-ab595853e836"
        ],
        "portion_ids": [
          "18bf160e-702a-464a-9920-f115024b5484",
          "10a9c093-009d-4bc0-a344-2afd3f0f9b9f",
          "8ebd06e1-5eda-47ec-8888-61965ecf005e"
        ],
        "submitter_portion_ids": [
          "TCGA-HU-8243-11A-01",
          "TCGA-HU-8243-01A-11",
          "TCGA-HU-8243-10A-01"
        ],
        "created_datetime": "2016-05-02T16:17:09.754748-05:00",
        "submitter_aliquot_ids": [
          "TCGA-HU-8243-01A-01D-YYYY-23",
          "TCGA-HU-8243-01A-11D-2340-08",
          "TCGA-HU-8243-01A-11D-2338-01",
          "TCGA-HU-8243-01A-11D-2342-05",
          "TCGA-HU-8243-11A-01D-2338-01",
          "TCGA-HU-8243-11A-01D-2340-08",
          "TCGA-HU-8243-10A-01D-2339-01",
          "TCGA-HU-8243-01A-11R-2343-13",
          "TCGA-HU-8243-10A-01D-2341-08"
        ],
        "updated_datetime": "2016-05-02T16:17:09.754748-05:00",
        "submitter_analyte_ids": [
          "TCGA-HU-8243-11A-01D",
          "TCGA-HU-8243-10A-01D",
          "TCGA-HU-8243-01A-11R",
          "TCGA-HU-8243-01A-11D"
        ],
        "analyte_ids": [
          "89c9094d-5cf6-4c7d-ad24-41b7ad9427cc",
          "2c413e60-0122-426b-afb3-ae94810e2513",
          "57d41760-0fed-49d2-8606-48231cb244ea",
          "37ed51fd-b540-408e-8bd6-4447ae4aa84a"
        ],
        "submitter_id": "TCGA-HU-8243",
        "case_id": "77a8eab6-f6a1-4739-9031-75ead40d68cb",
        "state": null,
        "aliquot_ids": [
          "ace3edd6-14a9-42cc-84f3-6127237f2913",
          "a711abd1-f1c2-4e42-8b66-79b4514ac1c4",
          "6af7ba34-58f7-4472-8c7e-89fc91ad5ac1",
          "558ff67a-a584-46f8-9089-8f4a08015294",
          "71c0a224-5953-4b59-a49c-b7aa1e959f1e",
          "a460c222-bcac-4959-961f-4dbd73e1ce13",
          "6e5789d7-4988-457a-86eb-e618c7ab06eb",
          "ff31f56b-398c-45ee-b122-f10027774527",
          "9635cfd4-3d26-4fc6-846c-fd74d5b60098"
        ],
        "slide_ids": [
          "60b7c6b8-594a-40c3-9341-a0902e4e6938",
          "e55e00a0-2048-404a-b83a-f34106468694"
        ],
        "submitter_sample_ids": [
          "TCGA-HU-8243-10A",
          "TCGA-HU-8243-01A",
          "TCGA-HU-8243-11A"
        ]
      },
      {
        "sample_ids": [
          "2f5cc9c9-31a9-5eb3-952a-b21e7cef50ca",
          "4f3f4fc8-4465-5230-83ec-c0ef6aceb2ea"
        ],
        "updated_datetime": "2016-05-25T19:12:45.610324-05:00",
        "submitter_aliquot_ids": [
          "TARGET-30-PAUXFZ-01A-01D",
          "TARGET-30-PAUXFZ-10A-01D"
        ],
        "submitter_id": "TARGET-30-PAUXFZ",
        "case_id": "a7ccef7c-14c0-5232-b647-58b4a54fb343",
        "aliquot_ids": [
          "9e1e30a8-7607-5b7e-b33c-9a6c5828d5fb",
          "c56898f9-c394-516a-bdbb-bf32a5af9d3f"
        ],
        "submitter_sample_ids": [
          "TARGET-30-PAUXFZ-01A",
          "TARGET-30-PAUXFZ-10A"
        ]
      },
      {
        "sample_ids": [
          "c1bcb8d1-e13d-4af4-93f4-02d5f7f616a2",
          "52fcf737-cdcc-43ea-b33c-4018039b42dd"
        ],
        "portion_ids": [
          "e0e97a05-656a-468e-8418-0d08c38e76ab",
          "3e2a0eab-7d89-4f3c-9c0e-8942e53d3c45"
        ],
        "submitter_portion_ids": [
          "TCGA-KK-A8I9-01A-11",
          "TCGA-KK-A8I9-11A-11"
        ],
        "created_datetime": null,
        "submitter_aliquot_ids": [
          "TCGA-KK-A8I9-11A-11D-A361-01",
          "TCGA-KK-A8I9-11A-11D-A362-08",
          "TCGA-KK-A8I9-11A-11W-A446-08",
          "TCGA-KK-A8I9-01A-11R-A36G-07",
          "TCGA-KK-A8I9-11A-11D-A40C-01",
          "TCGA-KK-A8I9-01A-11D-A363-01",
          "TCGA-KK-A8I9-01A-11W-A447-08",
          "TCGA-KK-A8I9-01A-11D-A365-05",
          "TCGA-KK-A8I9-01A-11D-A364-08",
          "TCGA-KK-A8I9-01A-11R-A36B-13"
        ],
        "updated_datetime": "2016-05-02T15:57:29.451686-05:00",
        "submitter_analyte_ids": [
          "TCGA-KK-A8I9-11A-11W",
          "TCGA-KK-A8I9-01A-11R",
          "TCGA-KK-A8I9-11A-11D",
          "TCGA-KK-A8I9-01A-11W",
          "TCGA-KK-A8I9-01A-11D"
        ],
        "analyte_ids": [
          "ddec19cb-5e4c-4151-8b6d-741044abff1e",
          "96c5b539-8eb7-4156-81d0-7b7fecd68900",
          "ced38a45-7610-49d4-8bf9-d53a1fc2d489",
          "476f5deb-1b3f-4a35-8a31-f27763ba8d8a",
          "c284f2af-1e9b-40cc-8936-b61cfd251d62"
        ],
        "submitter_id": "TCGA-KK-A8I9",
        "case_id": "261c3d74-706e-4751-bd15-8f3c1a402ff0",
        "state": null,
        "aliquot_ids": [
          "4f76de2d-e07a-402b-9818-7f04d3704a43",
          "96802a73-b1db-47d7-8f5f-4504f3ece5ad",
          "f376fc45-370a-4d96-833b-9a1322e32a42",
          "d3e88dd3-66d7-40d4-978a-4ddab868373a",
          "06f1d087-75c9-4da8-8339-80aff3bfaa12",
          "50b1e243-b45a-42a1-8692-b7ae5d51250f",
          "0f1c00d3-f3dc-4d2b-bd8a-ecc31e4f4089",
          "986a3ed6-ba56-4025-a2bd-9909648e703a",
          "bebc84b6-9179-420b-8207-858b999e8c0c",
          "239d5e7e-5fb5-4df3-ae6b-a5a06ee296ae"
        ],
        "slide_ids": [
          "1e174ca5-9298-41b6-a705-728f111a3e7b",
          "a3e31324-9e06-4799-85b4-4f6236848009"
        ],
        "submitter_sample_ids": [
          "TCGA-KK-A8I9-11A",
          "TCGA-KK-A8I9-01A"
        ]
      },
      {
        "sample_ids": [
          "d43f727a-96d6-40b8-86ae-7a3e0aa46853",
          "b8329a6d-a87b-47f4-ad00-9e979e62647b"
        ],
        "portion_ids": [
          "8960ddcc-0950-4d6e-a557-8727b652c93b",
          "e36bfd07-c911-4a98-8424-e58e5e9aaa68"
        ],
        "submitter_portion_ids": [
          "TCGA-QR-A70H-10A-01",
          "TCGA-QR-A70H-01A-12"
        ],
        "created_datetime": null,
        "submitter_aliquot_ids": [
          "TCGA-QR-A70H-01A-12R-A35K-07",
          "TCGA-QR-A70H-01A-12R-A35M-13",
          "TCGA-QR-A70H-01A-12D-A35E-05",
          "TCGA-QR-A70H-10A-01D-A35A-01",
          "TCGA-QR-A70H-01A-12D-A35C-01",
          "TCGA-QR-A70H-01A-12W-A43Z-08",
          "TCGA-QR-A70H-10A-01D-A35B-08",
          "TCGA-QR-A70H-10A-01W-A441-08",
          "TCGA-QR-A70H-01A-12D-A35D-08"
        ],
        "updated_datetime": "2016-05-02T15:37:31.996088-05:00",
        "submitter_analyte_ids": [
          "TCGA-QR-A70H-10A-01D",
          "TCGA-QR-A70H-10A-01W",
          "TCGA-QR-A70H-01A-12D",
          "TCGA-QR-A70H-01A-12W",
          "TCGA-QR-A70H-01A-12R"
        ],
        "analyte_ids": [
          "c4a41555-dd45-4e10-a3be-50d49a1121a3",
          "957e01f6-eb3f-446e-9f45-b50c66337e2d",
          "1acde950-2e0c-4586-852b-b4ac4e1ea4a4",
          "67c033c0-9fe8-4004-967e-c605e1890f4d",
          "b0873010-5d60-4691-b700-e172950f1d7c"
        ],
        "submitter_id": "TCGA-QR-A70H",
        "case_id": "13b41b15-a785-4ab7-b864-ffff6d35dd45",
        "state": null,
        "aliquot_ids": [
          "d9120f00-7f10-49d5-ae84-6177e9424c7c",
          "31c6fa50-200a-46c1-a546-61b52592fd8f",
          "ab50f38c-2e7d-4d75-a216-27aeaa4d9305",
          "382d5e31-6c66-4df3-a695-6b8c29cfc681",
          "51d1fb14-c918-4439-b816-ef6cd3253c64",
          "f586d8d5-d0c6-4979-aaa7-10217a88fa4c",
          "2f9a60eb-602e-44bb-bc57-87e20d946f76",
          "fbafc85e-deff-46cd-a40f-479b9dc92a60",
          "cacbc8a6-0eb0-4277-931f-d0075c9b1de9"
        ],
        "slide_ids": [
          "2310e34c-0ea5-4876-9f87-bad0b7a44513"
        ],
        "submitter_sample_ids": [
          "TCGA-QR-A70H-01A",
          "TCGA-QR-A70H-10A"
        ]
      },
      {
        "sample_ids": [
          "19dee039-9c98-4d4a-8baf-eea1b6dda8eb",
          "fdf1e501-f34f-450c-9a5c-611157079a86"
        ],
        "portion_ids": [
          "10b6ccb4-3637-4769-8988-417c0306eaef",
          "92f8cd48-451d-4ed6-8e60-b15aa93d2c09",
          "d0d55efa-c91d-45de-92bf-cf6f0d263b21"
        ],
        "submitter_portion_ids": [
          "TCGA-BJ-A18Z-01A-21",
          "TCGA-BJ-A18Z-01A-11-A21L-20",
          "TCGA-BJ-A18Z-10A-01"
        ],
        "created_datetime": null,
        "submitter_aliquot_ids": [
          "TCGA-BJ-A18Z-01A-21D-A13U-02",
          "TCGA-BJ-A18Z-10A-01D-A13V-01",
          "TCGA-BJ-A18Z-01A-21R-A13Y-07",
          "TCGA-BJ-A18Z-01A-21W-A14T-08",
          "TCGA-BJ-A18Z-01A-21D-A13Z-05",
          "TCGA-BJ-A18Z-01A-21D-A37T-08",
          "TCGA-BJ-A18Z-10A-01D-A13W-08",
          "TCGA-BJ-A18Z-01A-21R-A13X-13",
          "TCGA-BJ-A18Z-01A-21D-A13W-08",
          "TCGA-BJ-A18Z-10A-01D-A13U-02",
          "TCGA-BJ-A18Z-10A-01W-A14T-08",
          "TCGA-BJ-A18Z-01A-21D-A13V-01"
        ],
        "updated_datetime": "2016-05-02T16:18:19.199189-05:00",
        "submitter_analyte_ids": [
          "TCGA-BJ-A18Z-01A-21W",
          "TCGA-BJ-A18Z-01A-21D",
          "TCGA-BJ-A18Z-01A-21R",
          "TCGA-BJ-A18Z-10A-01D",
          "TCGA-BJ-A18Z-10A-01W"
        ],
        "analyte_ids": [
          "119ebfa1-75b2-4f24-816a-4e9a5061f6b5",
          "f86759fd-ecc5-4f42-b5fe-b9f079d23968",
          "39691042-bd28-40ed-b66b-26414ecf1ba0",
          "76ea5056-d7fa-49fb-94bf-11171ca7c100",
          "71a822c9-b510-4a4c-8c30-18b8083acc2d"
        ],
        "submitter_id": "TCGA-BJ-A18Z",
        "case_id": "0d497faf-2c1c-4173-a5fe-770cca73323c",
        "state": null,
        "aliquot_ids": [
          "fa580596-e70f-4ed0-85a2-6fb594ca679a",
          "776cb4b1-8efd-4ea2-b53f-9dff7dd94b10",
          "85a7922f-0327-437c-bdf5-1bb67a1e932f",
          "6d532180-0175-4610-8bfa-cca3a7c3697a",
          "b5977e73-49d8-4e99-9e97-993cc44dad17",
          "918793fa-b35e-4745-ac75-4d1c868089f8",
          "ba9479a1-929f-4e4e-8bf5-e23cb280dfcf",
          "e9776ff5-69b9-4669-ab33-e4bb030461ec",
          "8ba98907-ab03-4c9e-a900-e31aa16ff810",
          "35e18649-183e-4223-b2f6-d812bdd9becd",
          "4aa17671-4420-4989-a6dd-379250f4aeda",
          "815c53c3-8add-4612-b93c-3ed4bfa530aa"
        ],
        "slide_ids": [
          "7c5b5c77-9fbc-4b48-81f5-48b5ede7c436"
        ],
        "submitter_sample_ids": [
          "TCGA-BJ-A18Z-01A",
          "TCGA-BJ-A18Z-10A"
        ]
      }
    ],
    "pagination": {
      "count": 10,
      "sort": "",
      "from": 0,
      "page": 1,
      "total": 6340,
      "pages": 634,
      "size": 10
    }
  },
  "warnings": {}
}
```



#### Example: HTTP POST Request

This example demonstrates how to obtain metadata in TSV format for a set of files using their UUIDs (e.g. UUIDs obtained from a [download manifest file generated by the GDC Data Portal](/Data_Portal/Users_Guide/Cart/#gdc-data-transfer-tool)).

The first step is to construct a JSON query object, including `filters`, `fields`, `format`, and `size` parameters. The object is then submitted as HTTP POST payload to the GDC API using curl, in order to retrieve a TSV file with the requested metadata.

```Payload_txt
{
    "filters":{
        "op":"in",
        "content":{
            "field":"files.file_id",
            "value":[
                "0001801b-54b0-4551-8d7a-d66fb59429bf",
                "002c67f2-ff52-4246-9d65-a3f69df6789e",
                "003143c8-bbbf-46b9-a96f-f58530f4bb82",
                "0043d981-3c6b-463f-b512-ab1d076d3e62",
                "004e2a2c-1acc-4873-9379-ef1aa12283b6",
                "005239a8-2e63-4ff1-9cd4-714f81837a61",
                "006b8839-31e5-4697-b912-8e3f4124dd15",
                "006ce9a8-cf38-462e-bb99-7f08499244ab",
                "007ce9b5-3268-441e-9ffd-b40d1127a319",
                "0084a614-780b-42ec-b85f-7a1b83128cd3",
                "00a5e471-a79f-4d56-8a4c-4847ac037400",
                "00ab2b5a-b59e-4ec9-b297-76f74ff1d3fb",
                "00c5f14e-a398-4076-95d1-25f320ee3a37",
                "00c74a8b-10aa-40cc-991e-3365ea1f3fce",
                "00df5a50-bce3-4edf-a078-641e54800dcb"
            ]
        }
    },
    "format":"TSV",
    "fields":"file_id,file_name,cases.submitter_id,cases.case_id,data_category,data_type,cases.samples.tumor_descriptor,cases.samples.tissue_type,cases.samples.sample_type,cases.samples.submitter_id,cases.samples.sample_id,cases.samples.portions.analytes.aliquots.aliquot_id,cases.samples.portions.analytes.aliquots.submitter_id",
    "size":"100"
}
```
```Shell
curl --request POST --header "Content-Type: application/json" --data @Payload.txt 'https://api.gdc.cancer.gov/files' > File_metadata.txt
```
```File_metadata_txt
cases_0_submitter_id	cases_0_case_id	data_type	cases_0_samples_0_sample_type	cases_0_samples_0_tissue_type	file_name	cases_0_samples_0_submitter_id	cases_0_samples_0_portions_0_analytes_0_aliquots_0_aliquot_id	cases_0_samples_0_sample_id	file_id	data_category	cases_0_samples_0_tumor_descriptor	cases_0_samples_0_portions_0_analytes_0_aliquots_0_submitter_id
TCGA-B0-5094	8aaa4e25-5c12-4ace-96dc-91aaa0c4457c	Aligned Reads	Solid Tissue Normal		C345.TCGA-B0-5094-11A-01D-1421-08.5_gdc_realn.bam	TCGA-B0-5094-11A	b4e4630a-b38c-4b62-b0e8-d73f0e3b4e47	7519d7a8-c3ee-417b-9cfc-111bc5ad0637	0001801b-54b0-4551-8d7a-d66fb59429bf	Raw Sequencing Data		TCGA-B0-5094-11A-01D-1421-08
TCGA-B0-5117	ae55b2d3-62a1-419e-9f9a-5ddfac356db4	Aligned Reads	Solid Tissue Normal		C345.TCGA-B0-5117-11A-01D-1421-08.5_gdc_realn.bam	TCGA-B0-5117-11A	45c68b6b-0bed-424d-9a77-4f87bbaa3649	b1116541-bece-4df3-b3dd-cec50aeb277b	003143c8-bbbf-46b9-a96f-f58530f4bb82	Raw Sequencing Data		TCGA-B0-5117-11A-01D-1421-08
TCGA-G7-6790	e7a1cbe2-793c-4747-8412-8be794f2382b	Aligned Reads	Blood Derived Normal		C489.TCGA-G7-6790-10A-01D-1962-08.2_gdc_realn.bam	TCGA-G7-6790-10A	66cbb40f-14b3-40c0-a332-e8a8e21bca11	4be83d0f-8b09-4e9e-8318-358371d34332	004e2a2c-1acc-4873-9379-ef1aa12283b6	Raw Sequencing Data		TCGA-G7-6790-10A-01D-1962-08
TCGA-B9-A69E	a4225cb2-7b4b-4122-b6b9-629c26e3ea56	Aligned Reads	Blood Derived Normal		TCGA-B9-A69E-10A-01D-A31X-10_Illumina_gdc_realn.bam	TCGA-B9-A69E-10A	f4799bdc-b207-4053-9a4b-5a26ebf8ab91	5d6d6cd4-6a7b-499d-936a-1be9bf74b07f	0084a614-780b-42ec-b85f-7a1b83128cd3	Raw Sequencing Data		TCGA-B9-A69E-10A-01D-A31X-10
TCGA-EE-A2GU	24faa36a-268d-4a13-b3ae-eacd431a2bcc	Aligned Reads	Blood Derived Normal		C828.TCGA-EE-A2GU-10A-01D-A198-08.2_gdc_realn.bam	TCGA-EE-A2GU-10A	c3feacc2-5a26-4bb2-a312-8b2ee53ccad1	cc4a5ed8-376a-4842-a25d-ffb07d8e1ca0	00c74a8b-10aa-40cc-991e-3365ea1f3fce	Raw Sequencing Data		TCGA-EE-A2GU-10A-01D-A198-08
TCGA-CE-A484	e62a728d-390f-428a-bea1-fc8c9814fb11	Aligned Reads	Blood Derived Normal		C499.TCGA-CE-A484-10A-01D-A23U-08.3_gdc_realn.bam	TCGA-CE-A484-10A	641a0220-6eec-434a-b606-e256113b65da	27a8008e-044a-4966-b518-cc6905e292ca	00df5a50-bce3-4edf-a078-641e54800dcb	Raw Sequencing Data		TCGA-CE-A484-10A-01D-A23U-08
TCGA-DA-A1IB	8fc9cc74-f388-49f0-b957-debb62638634	Aligned Reads	Blood Derived Normal		C828.TCGA-DA-A1IB-10A-01D-A198-08.2_gdc_realn.bam	TCGA-DA-A1IB-10A	30919a1a-df9f-4604-835e-f66ac7bcacdf	432952c5-6505-4220-a581-f65270a45281	00ab2b5a-b59e-4ec9-b297-76f74ff1d3fb	Raw Sequencing Data		TCGA-DA-A1IB-10A-01D-A198-08
TCGA-AX-A2HG	7a2cf5ce-8317-4fff-946e-b9937afab815	Aligned Reads	Blood Derived Normal		6c2a8ea343da8d6cc0fd2043492f16df_gdc_realn.bam	TCGA-AX-A2HG-10A	8c34ffe2-9012-4b4a-b610-a42a9c6a9780	ef4b80ec-b453-48ec-8ad8-ccac83e1e4db	00c5f14e-a398-4076-95d1-25f320ee3a37	Raw Sequencing Data		TCGA-AX-A2HG-10A-01D-A17D-09
TCGA-EC-A24G	b5c1e511-baf2-45b3-9919-110e8941e3c2	Aligned Reads	Blood Derived Normal		671333b193812fc2bd2744053b383459_gdc_realn.bam	TCGA-EC-A24G-10A	2a8cb8fe-b64f-453e-8139-7ede12f3fc51	61cf2e54-1b8d-40a0-9c73-a7449cbd570a	00a5e471-a79f-4d56-8a4c-4847ac037400	Raw Sequencing Data		TCGA-EC-A24G-10A-01D-A16D-09
TCGA-B5-A0K0	29c8f468-5ac1-4d6c-8376-e36e6d246926	Aligned Reads	Blood Derived Normal		TCGA-B5-A0K0-10A-01W-A062-09_IlluminaGA-DNASeq_exome_gdc_realn.bam	TCGA-B5-A0K0-10A	02e65074-ffda-4795-b8f5-1bfd20bd1019	1df69e2e-f392-465f-8e61-4671ba2fcd35	007ce9b5-3268-441e-9ffd-b40d1127a319	Raw Sequencing Data		TCGA-B5-A0K0-10A-01W-A062-09
TCGA-C8-A27B	f0d8a1fe-e313-44f1-99cc-b965cbeeff0e	Aligned Reads	Blood Derived Normal		3c99d98ea8eb6acbf819e67fc77623d9_gdc_realn.bam	TCGA-C8-A27B-10A	922226ba-6244-4953-ad42-f4daa474c288	31139082-7978-45aa-9d8f-ac4789ac5cec	006b8839-31e5-4697-b912-8e3f4124dd15	Raw Sequencing Data		TCGA-C8-A27B-10A-01D-A167-09
TCGA-E9-A295	fec0da58-1047-44d2-b6d1-c18cceed43dc	Aligned Reads	Blood Derived Normal		fd4421a6bbf3efd4e3d5c17fdd610314_gdc_realn.bam	TCGA-E9-A295-10A	cd761feb-9a20-4495-8943-c6243532a5cf	e74183e1-f0b4-412a-8dac-a62d404add78	002c67f2-ff52-4246-9d65-a3f69df6789e	Raw Sequencing Data		TCGA-E9-A295-10A-01D-A16D-09
TCGA-EB-A44O	c787c4da-c564-44f1-89eb-dd9da107acb1	Aligned Reads	Blood Derived Normal		C828.TCGA-EB-A44O-10A-01D-A25O-08.3_gdc_realn.bam	TCGA-EB-A44O-10A	c723584a-c404-4c88-bfea-e40f5dbba542	5b738547-1825-4684-81bd-864bf2eb43ef	006ce9a8-cf38-462e-bb99-7f08499244ab	Raw Sequencing Data		TCGA-EB-A44O-10A-01D-A25O-08
TCGA-A2-A3XX	53886143-c1c6-40e9-88e6-e4e5e0271fc8	Aligned Reads	Blood Derived Normal		b40998d4778f18ed80d6dd8bff0eb761_gdc_realn.bam	TCGA-A2-A3XX-10A	e96d5811-4736-40dd-966d-e0e172aeb0af	c6eb6218-ad71-40a6-88b7-a4f1a015b816	0043d981-3c6b-463f-b512-ab1d076d3e62	Raw Sequencing Data		TCGA-A2-A3XX-10A-01D-A23C-09
TCGA-EB-A3XB	a9255dcb-b236-4777-ac43-555e3a5386c3	Aligned Reads	Blood Derived Normal		C828.TCGA-EB-A3XB-10B-01D-A23B-08.1_gdc_realn.bam	TCGA-EB-A3XB-10B	9f4ffc2f-d006-4d86-b3b1-b25020481893	0e1d4c7c-204d-4765-b090-68ed4cd83835	005239a8-2e63-4ff1-9cd4-714f81837a61	Raw Sequencing Data		TCGA-EB-A3XB-10B-01D-A23B-08
```


### Format

Specifies the format of the API response: JSON (default), `TSV` or `XML`.

#### Examples

```shell1
curl  'https://api.gdc.cancer.gov/cases?fields=submitter_id&size=5&format=TSV'
```
```python1
import requests

cases_endpt = 'https://api.gdc.cancer.gov/cases'
params = {'fields':'submitter_id',
          'format':'TSV'}
response = requests.get(cases_endpt, params = params)
print response.content
```
```response1
submitter_id
TCGA-RC-A6M6
TCGA-B6-A0RV
TCGA-MB-A5Y8
TCGA-BQ-5876
TCGA-Z6-A9VB
```
```shell2
curl  'https://api.gdc.cancer.gov/cases?fields=submitter_id&size=5&format=XML&pretty=true'
```
```python2
import requests

cases_endpt = 'https://api.gdc.cancer.gov/cases'
params = {'fields':'submitter_id',
          'format':'XML',
          'pretty':'true'}
response = requests.get(cases_endpt, params = params)
print response.content
```
```Output2
<?xml version="1.0" ?>
<response>
	<data>
		<hits>
			<item>
				<submitter_id>TCGA-MQ-A4LV</submitter_id>
			</item>
			<item>
				<submitter_id>TCGA-N9-A4Q1</submitter_id>
			</item>
			<item>
				<submitter_id>TCGA-78-7154</submitter_id>
			</item>
			<item>
				<submitter_id>TCGA-S7-A7WX</submitter_id>
			</item>
			<item>
				<submitter_id>TCGA-XF-AAML</submitter_id>
			</item>
		</hits>
		<pagination>
			<count>5</count>
			<sort/>
			<from>0</from>
			<pages>2811</pages>
			<total>14052</total>
			<page>1</page>
			<size>5</size>
		</pagination>
	</data>
	<warnings/>
</response>
```

### Pretty

Returns when the `pretty` parameter is set to `true`, the API response is formatted with additional whitespace to improve legibility.

#### Example

```Request1
curl  'https://api.gdc.cancer.gov/cases?fields=submitter_id&sort=submitter_id:asc&size=5'
```
```Response1
{"data": {"hits": [{"id": "f7af65fc-97e3-52ce-aa2c-b707650e747b", "submitter_id": "TARGET-00-NAAEMA"}, {"id": "513d0a2a-3c94-5a36-97a4-24c3656fc66e", "submitter_id": "TARGET-00-NAAEMB"}, {"id": "b5f20676-727b-50b0-9b5a-582cd8572d6d", "submitter_id": "TARGET-00-NAAEMC"}, {"id": "0c0b183f-0d4a-5a9d-9888-0617cebcc462", "submitter_id": "TARGET-20-PABGKN"}, {"id": "0f5ed7a7-226d-57bc-a4ce-8a6b18560c55", "submitter_id": "TARGET-20-PABHET"}], "pagination": {"count": 5, "sort": "submitter_id:asc", "from": 0, "page": 1, "total": 14551, "pages": 2911, "size": 5}}, "warnings": {}}
```
```Request2
curl  'https://api.gdc.cancer.gov/cases?fields=submitter_id&sort=submitter_id:asc&size=5&pretty=true'
```
```Response2
{
  "data": {
    "hits": [
      {
        "id": "f7af65fc-97e3-52ce-aa2c-b707650e747b",
        "submitter_id": "TARGET-00-NAAEMA"
      },
      {
        "id": "513d0a2a-3c94-5a36-97a4-24c3656fc66e",
        "submitter_id": "TARGET-00-NAAEMB"
      },
      {
        "id": "b5f20676-727b-50b0-9b5a-582cd8572d6d",
        "submitter_id": "TARGET-00-NAAEMC"
      },
      {
        "id": "0c0b183f-0d4a-5a9d-9888-0617cebcc462",
        "submitter_id": "TARGET-20-PABGKN"
      },
      {
        "id": "0f5ed7a7-226d-57bc-a4ce-8a6b18560c55",
        "submitter_id": "TARGET-20-PABHET"
      }
    ],
    "pagination": {
      "count": 5,
      "sort": "submitter_id:asc",
      "from": 0,
      "page": 1,
      "total": 14551,
      "pages": 2911,
      "size": 5
    }
  },
  "warnings": {}
}
```

### Fields

This query parameter specifies which fields are to be included in the API response. The fields in the API response will be unordered. A listing of available fields for each endpoint is provided in [Appendix A](Appendix_A_Available_Fields.md).

#### Example

The following example requests case submitter ID, file UUID, file name and file size from the `files` endpoint.

```shell
curl 'https://api.gdc.cancer.gov/files?fields=cases.submitter_id,file_id,file_name,file_size&pretty=true'
```
```python
import requests
import json

files_endpt = 'https://api.gdc.cancer.gov/files'
params = {'fields':'cases.submitter_id,file_id,file_name,file_size'}
response = requests.get(files_endpt, params = params)
print json.dumps(response.json(), indent=2)
```
```Response
{
  "data": {
    "hits": [
      {
        "file_name": "NARKY_p_TCGAb69_SNP_N_GenomeWideSNP_6_H03_697832.grch38.seg.txt",
        "cases": [
          {
            "submitter_id": "TCGA-BP-4989"
          }
        ],
        "file_id": "3bd4d5dc-563a-481c-87a6-ec0017d0d58a",
        "file_size": 54200
      },
      {
        "file_name": "652ecf99-1af9-41fc-b0a5-d3e5c07a7b5d.FPKM.txt.gz",
        "cases": [
          {
            "submitter_id": "TCGA-60-2709"
          }
        ],
        "file_id": "b3286166-01f9-4149-81b5-a2ea5f27c50e",
        "file_size": 530665
      },
      {
        "file_name": "CUSKS_p_TCGAb47_SNP_1N_GenomeWideSNP_6_D05_628212.nocnv_grch38.seg.txt",
        "cases": [
          {
            "submitter_id": "TCGA-A8-A07Z"
          }
        ],
        "file_id": "282cc9d1-c5e9-49ff-b27b-e00c1e5529c6",
        "file_size": 15806
      },
      {
        "file_name": "REEDY_p_TCGAb65_SNP_N_GenomeWideSNP_6_F01_697686.nocnv_grch38.seg.txt",
        "cases": [
          {
            "submitter_id": "TCGA-CJ-4871"
          }
        ],
        "file_id": "fe44a644-eefc-42c5-aac7-a216bc1e88e1",
        "file_size": 6179
      },
      {
        "file_name": "84df7a8fee9fedb5e8e22849ec66d294_gdc_realn.bam",
        "cases": [
          {
            "submitter_id": "TCGA-A2-A0CO"
          }
        ],
        "file_id": "acd0ec73-c1fe-463e-912c-84e8416510e5",
        "file_size": 15545555724
      },
      {
        "file_name": "ed8c4bb6-891a-4cf2-80ba-42c5594760d0.vcf",
        "cases": [
          {
            "submitter_id": "TCGA-BQ-7059"
          }
        ],
        "file_id": "ed8c4bb6-891a-4cf2-80ba-42c5594760d0",
        "file_size": 264694
      },
      {
        "file_name": "nationwidechildrens.org_clinical.TCGA-IG-A6QS.xml",
        "cases": [
          {
            "submitter_id": "TCGA-IG-A6QS"
          }
        ],
        "file_id": "fe8cf009-f033-4536-95c7-836adcba5bf3",
        "file_size": 36996
      },
      {
        "file_name": "05f6f9f7-6fb7-4c95-b79c-fdfaba16539d.vep.reheader.vcf.gz",
        "cases": [
          {
            "submitter_id": "TCGA-DK-A3IV"
          }
        ],
        "file_id": "05f6f9f7-6fb7-4c95-b79c-fdfaba16539d",
        "file_size": 415044
      },
      {
        "file_name": "C484.TCGA-12-5301-01A-01D-1486-08.7_gdc_realn.bam",
        "cases": [
          {
            "submitter_id": "TCGA-12-5301"
          }
        ],
        "file_id": "3b0293c2-4a26-428c-b097-9489f23a2a2d",
        "file_size": 23661175335
      },
      {
        "file_name": "75a36e71-400d-46a5-93b0-7813cf0595ea.FPKM.txt.gz",
        "cases": [
          {
            "submitter_id": "TCGA-BF-A5EO"
          }
        ],
        "file_id": "28f763c7-8064-4151-ae0e-31e70cd9bfe8",
        "file_size": 488422
      }
    ],
    "pagination": {
      "count": 10,
      "sort": "",
      "from": 0,
      "page": 1,
      "total": 216435,
      "pages": 21644,
      "size": 10
    }
  },
  "warnings": {}
}
```

### Expand

The `expand` parameter provides a shortcut to request multiple related fields (field groups) in the response. Instead of specifying each field using the `fields` parameter, users can specify a field group name using the `expand` parameter to request all fields in the group. Available field groups are listed in [Appendix A](Appendix_A_Available_Fields.md#field-group-listing-by-endpoint); the list can also be accessed programmatically at the [_mapping endpoint](#95mapping-endpoint). The `fields` and `expand` parameters can be used together to request custom combinations of field groups and individual fields.

#### Example

```Shell
curl 'https://api.gdc.cancer.gov/files/ac2ddebd-5e5e-4aea-a430-5a87c6d9c878?expand=cases.samples&pretty=true'
```
```
{
  "data": {
    "data_type": "Aligned Reads",
    "updated_datetime": "2016-09-18T04:25:13.163601-05:00",
    "created_datetime": "2016-05-26T18:55:53.506549-05:00",
    "file_name": "000aa811c15656604161e8f0e3a0aae4_gdc_realn.bam",
    "md5sum": "200475f5f6e42520204e5f6aadfe954f",
    "data_format": "BAM",
    "acl": [
      "phs000178"
    ],
    "access": "controlled",
    "platform": "Illumina",
    "state": "submitted",
    "file_id": "ac2ddebd-5e5e-4aea-a430-5a87c6d9c878",
    "data_category": "Raw Sequencing Data",
    "file_size": 12667634731,
    "cases": [
      {
        "samples": [
          {
            "sample_type_id": "11",
            "updated_datetime": "2016-09-08T11:00:45.021005-05:00",
            "time_between_excision_and_freezing": null,
            "oct_embedded": "false",
            "tumor_code_id": null,
            "submitter_id": "TCGA-QQ-A5VA-11A",
            "intermediate_dimension": null,
            "sample_id": "b4e7558d-898e-4d68-a897-381edde0bbcc",
            "is_ffpe": false,
            "pathology_report_uuid": null,
            "created_datetime": null,
            "tumor_descriptor": null,
            "sample_type": "Solid Tissue Normal",
            "state": null,
            "current_weight": null,
            "composition": null,
            "time_between_clamping_and_freezing": null,
            "shortest_dimension": null,
            "tumor_code": null,
            "tissue_type": null,
            "days_to_sample_procurement": null,
            "freezing_method": null,
            "preservation_method": null,
            "days_to_collection": 5980,
            "initial_weight": 810.0,
            "longest_dimension": null
          }
        ]
      }
    ],
    "submitter_id": "32872121-d38a-4128-b96a-698a6f18f29d",
    "type": "aligned_reads",
    "file_state": "processed",
    "experimental_strategy": "WXS"
  },
  "warnings": {}
}
```

### Size and From

GDC API provides a pagination feature that limits the number of results returned by the API. It is implemented using `size` and `from` query parameters.

The `size` query parameter specifies the maximum number of results to return. Default `size` is 10. If the number of query results is greater than `size`, only some of the results will be returned.

The `from` query parameter specifies the first record to return out of the set of results. For example, if there are 20 cases returned from the `cases` endpoint, then setting `from` to `11` will return results 12 to 20. The `from` parameter can be used in conjunction with the `size` parameter to return a specific subset of results.


#### Example


``` Shell1
curl 'https://api.gdc.cancer.gov/files?fields=file_name&from=0&size=2&pretty=true'
```
``` Python1
import requests
import json

files_endpt = 'https://api.gdc.cancer.gov/files'
params = {'fields':'file_name',
          'from':0, 'size':2}
response = requests.get(files_endpt, params = params)
print json.dumps(response.json(), indent=2)

```
```Response1
{
  "data": {
    "hits": [
      {
        "file_name": "unc.edu.276a1e00-cf3a-4463-a97b-d544381219ea.2363081.rsem.isoforms.normalized_results"
      },
      {
        "file_name": "nationwidechildrens.org_clinical.TCGA-EY-A5W2.xml"
      }
    ],
    "pagination": {
      "count": 2,
      "sort": "",
      "from": 0,
      "pages": 300936,
      "total": 601872,
      "page": 1,
      "size": 2
    }
  },
  "warnings": {}
}
```
``` Shell2
curl 'https://api.gdc.cancer.gov/files?fields=file_name&from=101&size=5&pretty=true'
```
``` Python2
import requests
import json

files_endpt = 'https://api.gdc.cancer.gov/files'
params = {'fields':'file_name',
          'from':101, 'size':5}
response = requests.get(files_endpt, params = params)
print json.dumps(response.json(), indent=2)
```
``` Output2
{
  "data": {
    "hits": [
      {
        "file_name": "OCULI_p_TCGA_159_160_SNP_N_GenomeWideSNP_6_E09_831242.grch38.seg.txt",
        "id": "1d959137-d8e6-4336-b357-8ab9c88eeca8"
      },
      {
        "file_name": "jhu-usc.edu_SKCM.HumanMethylation450.3.lvl-3.TCGA-EE-A3JI-06A-11D-A21B-05.gdc_hg38.txt",
        "id": "9c02ec95-4aa3-4112-8823-c0fa87f71773"
      },
      {
        "file_name": "jhu-usc.edu_LAML.HumanMethylation450.2.lvl-3.TCGA-AB-3002-03A-01D-0742-05.gdc_hg38.txt",
        "id": "731c3560-bcef-4ebf-bfbc-7320399a5bcb"
      },
      {
        "file_name": "CUSKS_p_TCGAb47_SNP_1N_GenomeWideSNP_6_B03_628222.grch38.seg.txt",
        "id": "a6f73a3e-faf8-49d9-9b68-77781bd302df"
      },
      {
        "file_name": "5496e9f1-a383-4874-95bb-f4d1b33f4594.vcf",
        "id": "5496e9f1-a383-4874-95bb-f4d1b33f4594"
      }
    ],
    "pagination": {
      "count": 5,
      "sort": "",
      "from": 101,
      "page": 21,
      "total": 274724,
      "pages": 54945,
      "size": 5
    }
  },
  "warnings": {}
}
```

### Sort

The `sort` query parameter sorts the results by a specific field, and with the sort direction specified using the `:asc` (ascending) or `:desc` (descending) prefix, e.g. `sort=field:desc`. A list of all valid _field_ names is available in [Appendix A](Appendix_A_Available_Fields.md); the list can also be accessed programmatically at the [_mapping endpoint](#95mapping-endpoint).

#### Example

Sort cases by `submitter_id` in ascending order:

``` shell
curl  'https://api.gdc.cancer.gov/cases?fields=submitter_id&sort=submitter_id:asc&pretty=true'
```
``` python
import requests
import json

cases_endpt = 'https://api.gdc.cancer.gov/cases'
params = {'fields':'submitter_id',
          'sort':'submitter_id:asc'}
response = requests.get(cases_endpt, params = params)
print json.dumps(response.json(), indent=2)

```
``` Output
{
  "data": {
    "hits": [
      {
        "id": "f7af65fc-97e3-52ce-aa2c-b707650e747b",
        "submitter_id": "TARGET-00-NAAEMA"
      },
      {
        "id": "513d0a2a-3c94-5a36-97a4-24c3656fc66e",
        "submitter_id": "TARGET-00-NAAEMB"
      },
      {
        "id": "b5f20676-727b-50b0-9b5a-582cd8572d6d",
        "submitter_id": "TARGET-00-NAAEMC"
      },
      {
        "id": "0c0b183f-0d4a-5a9d-9888-0617cebcc462",
        "submitter_id": "TARGET-20-PABGKN"
      },
      {
        "id": "0f5ed7a7-226d-57bc-a4ce-8a6b18560c55",
        "submitter_id": "TARGET-20-PABHET"
      },
      {
        "id": "b2a560a4-5e52-5d78-90ef-d680fbaf44d0",
        "submitter_id": "TARGET-20-PABHKY"
      },
      {
        "id": "1e5c8323-383d-51a0-9199-1b9504b29c7e",
        "submitter_id": "TARGET-20-PABLDZ"
      },
      {
        "id": "c550a267-30bd-5bf3-9699-61341559e0d5",
        "submitter_id": "TARGET-20-PACDZR"
      },
      {
        "id": "0fe29a81-74fc-5158-ae13-0437bc272805",
        "submitter_id": "TARGET-20-PACEGD"
      },
      {
        "id": "dd2b23ec-46f4-56b2-9429-6015c6dc730f",
        "submitter_id": "TARGET-20-PADDXZ"
      }
    ],
    "pagination": {
      "count": 10,
      "sort": "submitter_id:asc",
      "from": 0,
      "page": 1,
      "total": 14551,
      "pages": 1456,
      "size": 10
    }
  },
  "warnings": {}
}
```

### Facets
The `facets` parameter provides aggregate information for a specified field. It provides all values that exist for that field, and the number of entities (cases, projects, files, or annotations) that this value. The primary intended use of this parameter is for displaying aggregate information in the GDC Data Portal.

The `facets` parameter can be used in conjunction with the `filters` parameter to get aggregate information for a set of search results. The following limitations apply when using `facets` and `filters` together:

1. The `filters` object's top level operator must be `and`, and the internal filters must be limited to: `=`, `!=`, `in`, `exclude`, `is`, and `not`.
2. The information provided by `facets` for a given field will disregard any filters applied to that same field.

#### Example

This is an example of a request for a count of projects in each program.

```shell
curl  'https://api.gdc.cancer.gov/projects?facets=program.name&from=0&size=0&sort=program.name:asc&pretty=true'
```
```python
import requests
import json

projects_endpt = 'https://api.gdc.cancer.gov/projects'
params = {'facets':'program.name',
          'from':0, 'size':0,
          'sort':'program.name:asc'}
response = requests.get(projects_endpt, params = params)
print json.dumps(response.json(), indent=2)
```
```Response
{
  "data": {
    "pagination": {
      "count": 0,
      "sort": "program.name:asc",
      "from": 0,
      "page": 1,
      "total": 39,
      "pages": 39,
      "size": 0
    },
    "hits": [],
    "aggregations": {
      "program.name": {
        "buckets": [
          {
            "key": "TCGA",
            "doc_count": 33
          },
          {
            "key": "TARGET",
            "doc_count": 6
          }
        ]
      }
    }
  },
  "warnings": {}
}
```

#### Example

In this sample POST request, both `filters` and `facets` parameters are used. Note that `facets` ignores the `primary_site` filter.

```Payload
{
    "filters":{
        "op":"and",
        "content":[
            {
                "op":"=",
                "content":{
                    "field":"cases.project.primary_site",
                    "value":"Kidney"
                }
            },
            {
                "op":"=",
                "content":{
                    "field":"project.program.name",
                    "value":"TCGA"
                }
            }
        ]
    },
    "size":"0",
    "facets":"project.primary_site",
    "pretty":"true"
}
```
```Shell
curl --request POST --header "Content-Type: application/json" --data @Payload 'https://api.gdc.cancer.gov/v0/cases'
```
``` Response
{
  "data": {
    "pagination": {
      "count": 0,
      "sort": "",
      "from": 0,
      "page": 1,
      "total": 941,
      "pages": 941,
      "size": 0
    },
    "hits": [],
    "aggregations": {
      "project.primary_site": {
        "buckets": [
          {
            "key": "Brain",
            "doc_count": 1133
          },
          {
            "key": "Breast",
            "doc_count": 1098
          },
          {
            "key": "Lung",
            "doc_count": 1089
          },
          {
            "key": "Kidney",
            "doc_count": 941
          },
          {
            "key": "Colorectal",
            "doc_count": 635
          },
          {
            "key": "Uterus",
            "doc_count": 617
          },
          {
            "key": "Ovary",
            "doc_count": 608
          },
          {
            "key": "Head and Neck",
            "doc_count": 528
          },
          {
            "key": "Thyroid",
            "doc_count": 507
          },
          {
            "key": "Prostate",
            "doc_count": 500
          },
          {
            "key": "Stomach",
            "doc_count": 478
          },
          {
            "key": "Skin",
            "doc_count": 470
          },
          {
            "key": "Bladder",
            "doc_count": 412
          },
          {
            "key": "Liver",
            "doc_count": 377
          },
          {
            "key": "Cervix",
            "doc_count": 308
          },
          {
            "key": "Adrenal Gland",
            "doc_count": 271
          },
          {
            "key": "Soft Tissue",
            "doc_count": 261
          },
          {
            "key": "Bone Marrow",
            "doc_count": 200
          },
          {
            "key": "Esophagus",
            "doc_count": 185
          },
          {
            "key": "Pancreas",
            "doc_count": 185
          },
          {
            "key": "Testis",
            "doc_count": 150
          },
          {
            "key": "Thymus",
            "doc_count": 124
          },
          {
            "key": "Pleura",
            "doc_count": 87
          },
          {
            "key": "Eye",
            "doc_count": 80
          },
          {
            "key": "Lymph Nodes",
            "doc_count": 58
          },
          {
            "key": "Bile Duct",
            "doc_count": 51
          }
        ]
      }
    }
  },
  "warnings": {}
}
```


## Alternative Request Format

The GDC API also supports POST requests with `Content-Type: application/x-www-form-urlencoded` (curl default), which require payloads in the following format:
```
	filters=%7B%0A%20%20%20%20%22op%22%3A%22in%22%2C%0A%20%20%20%20%22content%22%3A%7B%0A%20%20%20%20%20%20%20%20%22field%22%3A%22files.file_id%22%2C%0A%20%20%20%20%20%20%20%20%22value%22%3A%5B%0A%20%20%20%20%20%20%20%20%20%20%20%20%220001801b-54b0-4551-8d7a-d66fb59429bf%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%22002c67f2-ff52-4246-9d65-a3f69df6789e%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%22003143c8-bbbf-46b9-a96f-f58530f4bb82%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%220043d981-3c6b-463f-b512-ab1d076d3e62%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%22004e2a2c-1acc-4873-9379-ef1aa12283b6%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%22005239a8-2e63-4ff1-9cd4-714f81837a61%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%22006b8839-31e5-4697-b912-8e3f4124dd15%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%22006ce9a8-cf38-462e-bb99-7f08499244ab%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%22007ce9b5-3268-441e-9ffd-b40d1127a319%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%220084a614-780b-42ec-b85f-7a1b83128cd3%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%2200a5e471-a79f-4d56-8a4c-4847ac037400%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%2200ab2b5a-b59e-4ec9-b297-76f74ff1d3fb%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%2200c5f14e-a398-4076-95d1-25f320ee3a37%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%2200c74a8b-10aa-40cc-991e-3365ea1f3fce%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%2200df5a50-bce3-4edf-a078-641e54800dcb%22%0A%20%20%20%20%20%20%20%20%5D%0A%20%20%20%20%7D%0A%7D&fields=file_id,file_name,cases.submitter_id,cases.case_id,data_category,data_type,cases.samples.tumor_descriptor,cases.samples.tissue_type,cases.samples.sample_type,cases.samples.submitter_id,cases.samples.sample_id&format=tsv&size=100
```
## Using Wildcards

The GDC API supports the use of the wildcard character, an asterisk (\*), in the `value` fields of a JSON query.  For example, if a user wanted to retrieve information about projects with a disease type that ended in "Adenocarcinoma" a query for `"disease_type": "*Adenocarcinoma"` would be appropriate. See below:

```
{  
   "size":"20000",
   "pretty":"TRUE",
   "fields":"submitter_id,disease_type",
   "format":"TSV",
   "filters":{  
      "op":"=",
      "content":{  
         "field":"disease_type",
         "value":"*Adenocarcinoma"
      }
   }
}
```

## Quicksearch Endpoint

The GDC Portal has a quicksearch functionality that allows for a project, case, or file to be queried from a search box. This function calls the `/v0/all` endpoint, which retrieves the top cases, files, and projects that match to the query. The quicksearch can also be used programmatically through the API.  For example, a search term of 'TCGA' would produce the following query:  

```Shell
curl "https://api.gdc.cancer.gov/v0/all?query=TCGA&size=5"
```
```Response
{
  "data": {
    "query": {
      "hits": [
        {
          "disease_type": [
            "Esophageal Carcinoma"
          ],
          "id": "UHJvamVjdDpUQ0dBLUVTQ0E=",
          "name": "Esophageal Carcinoma",
          "primary_site": [
            "Esophagus"
          ],
          "project_id": "TCGA-ESCA"
        },
        {
          "disease_type": [
            "Head and Neck Squamous Cell Carcinoma"
          ],
          "id": "UHJvamVjdDpUQ0dBLUhOU0M=",
          "name": "Head and Neck Squamous Cell Carcinoma",
          "primary_site": [
            "Head and Neck"
          ],
          "project_id": "TCGA-HNSC"
        },
        {
          "disease_type": [
            "Liver Hepatocellular Carcinoma"
          ],
          "id": "UHJvamVjdDpUQ0dBLUxJSEM=",
          "name": "Liver Hepatocellular Carcinoma",
          "primary_site": [
            "Liver"
          ],
          "project_id": "TCGA-LIHC"
        },
        {
          "disease_type": [
            "Colon Adenocarcinoma"
          ],
          "id": "UHJvamVjdDpUQ0dBLUNPQUQ=",
          "name": "Colon Adenocarcinoma",
          "primary_site": [
            "Colorectal"
          ],
          "project_id": "TCGA-COAD"
        },
        {
          "disease_type": [
            "Adrenocortical Carcinoma"
          ],
          "id": "UHJvamVjdDpUQ0dBLUFDQw==",
          "name": "Adrenocortical Carcinoma",
          "primary_site": [
            "Adrenal Gland"
          ],
          "project_id": "TCGA-ACC"
        }
      ]
    }
  }
}
```

This endpoint can be used to quickly retrieve information about a file.  For example, if a user wanted to know the UUID for `nationwidechildrens.org_biospecimen.TCGA-EL-A4K1.xml`, the following query could be used to quickly retrieve it programmatically:

```Shell
curl "https://api.gdc.cancer.gov/v0/all?query=nationwidechildrens.org_biospecimen.TCGA-EL-A4K1.xml&size=5"
```
```Response
{
  "data": {
    "query": {
      "hits": [
        {
          "file_id": "2a7a354b-e497-4ae6-8a85-a170951596c1",
          "file_name": "nationwidechildrens.org_biospecimen.TCGA-EL-A4K1.xml",
          "id": "RmlsZToyYTdhMzU0Yi1lNDk3LTRhZTYtOGE4NS1hMTcwOTUxNTk2YzE=",
          "submitter_id": null
        }
      ]
    }
  }
}
```

# Data Analysis

The GDC DAVE tools use the same API as the rest of the Data Portal and takes advantage of several new endpoints. Similar to the [GDC Data Portal Exploration](http://docs.gdc.cancer.gov/Data_Portal/Users_Guide/Exploration/) feature, the GDC data analysis endpoints allow API users to programmatically explore data in the GDC using advanced filters at a gene and mutation level. Survival analysis data is also available.  

## Endpoints

The following data analysis endpoints are available from the GDC API:

| __Endpoint__ | __Description__ |
|---|---|
| __/genes__ | Allows users to access summary information about each gene using its Ensembl ID. |
| __/ssms__ | Allows users to access information about each somatic mutation. For example, a `ssm` would represent the transition of C to T at position 52000 of chromosome 1. |
| __/ssm_occurrences__ | A `ssm` entity as applied to a single instance (case). An example of a `ssm occurrence` would be that the transition of C to T at position 52000 of chromosome 1 occurred in patient TCGA-XX-XXXX. |
|__/analysis/top_cases_counts_by_genes__| Returns the number of cases with a mutation in each gene listed in the gene_ids parameter for each project. Note that this endpoint cannot be used with the `format` or `fields` parameters.|
|__/analysis/top_mutated_genes_by_project__| Returns a list of genes that have the most mutations within a given project. |
|__/analysis/top_mutated_cases_by_gene__| Generates information about the cases that are most affected by mutations in a given number of genes |
|__/analysis/mutated_cases_count_by_project__| Returns counts for the number of cases that have associated `ssm` data in each project. The number of affected cases can be found under "case_with_ssm": {"doc_count": $case_count}.|
|__/analysis/survival__| Survival plots can be generated in the Data Portal for different subsets of data, based upon many query factors such as variants, disease type and projects. This endpoint can be used to programmatically retrieve the raw data to generate these plots and apply different filters to the data. (see Survival Example)|

The methods for retrieving information from these endpoints are very similar to those used for the `cases` and `files` endpoints. These methods are explored in depth in the [API Search and Retrieval](https://docs.gdc.cancer.gov/API/Users_Guide/Search_and_Retrieval/) documentation. The `_mapping` parameter can also be used with each of these endpoints to generate a list of potential fields.  For example:

`https://api.gdc.cancer.gov/ssms/_mapping`

Note: While it is not an endpoint, the `observation` entity is featured in the visualization section of the API. The `observation` entity provides information from the MAF file, such as read depth and normal genotype, that supports the validity of the associated `ssm`. An example is demonstrated below:

```Shell
curl "https://api.gdc.cancer.gov/ssms/57bb3f2e-ec05-52c2-ab02-7065b7d24849?expand=occurrence.case.observation.read_depth&pretty=true"
```
```Response
{
  "data": {
    "ncbi_build": "GRCh38",
    "occurrence": [
      {
        "case": {
          "observation": [
            {
              "read_depth": {
                "t_ref_count": 321,
                "t_alt_count": 14,
                "t_depth": 335,
                "n_depth": 115
              }
            }
          ]
        }
      }
    ],
    "tumor_allele": "G",
    "mutation_type": "Simple Somatic Mutation",
    "end_position": 14304578,
    "reference_allele": "C",
    "ssm_id": "57bb3f2e-ec05-52c2-ab02-7065b7d24849",
    "start_position": 14304578,
    "mutation_subtype": "Single base substitution",
    "cosmic_id": null,
    "genomic_dna_change": "chr5:g.14304578C>G",
    "gene_aa_change": [
      "TRIO L229V",
      "TRIO L437V",
      "TRIO L447V",
      "TRIO L496V"
    ],
    "chromosome": "chr5"
  },
  "warnings": {}
}
```

## Genes Endpoint Examples

__Example 1:__ A user would like to access information about the gene `ZMPSTE24`, which has an Ensembl gene ID of `ENSG00000084073`.  This would be accomplished by appending `ENSG00000084073` (`gene_id`) to the `genes` endpoint.

```Shell
curl "https://api.gdc.cancer.gov/genes/ENSG00000084073?pretty=true"
```
```Response
{
  "data": {
    "canonical_transcript_length": 3108,
    "description": "This gene encodes a member of the peptidase M48A family. The encoded protein is a zinc metalloproteinase involved in the two step post-translational proteolytic cleavage of carboxy terminal residues of farnesylated prelamin A to form mature lamin A. Mutations in this gene have been associated with mandibuloacral dysplasia and restrictive dermopathy. [provided by RefSeq, Jul 2008]",
    "cytoband": [
      "1p34.2"
    ],
    "gene_start": 40258107,
    "canonical_transcript_length_genomic": 36078,
    "gene_id": "ENSG00000084073",
    "gene_strand": 1,
    "canonical_transcript_length_cds": 1425,
    "gene_chromosome": "1",
    "synonyms": [
      "FACE-1",
      "HGPS",
      "PRO1",
      "STE24",
      "Ste24p"
    ],
    "is_cancer_gene_census": null,
    "biotype": "protein_coding",
    "gene_end": 40294184,
    "canonical_transcript_id": "ENST00000372759",
    "symbol": "ZMPSTE24",
    "name": "zinc metallopeptidase STE24"
  },
  "warnings": {}
}
```

__Example 2:__ A user wants a subset of elements such as a list of coordinates for all genes on chromosome 7. The query can be filtered for only results from chromosome 7 using a JSON-formatted query that is URL-encoded.

```Shell
curl "https://api.gdc.cancer.gov/genes?pretty=true&fields=gene_id,symbol,gene_start,gene_end&format=tsv&size=2000&filters=%7B%0D%0A%22op%22%3A%22in%22%2C%0D%0A%22content%22%3A%7B%0D%0A%22field%22%3A%22gene_chromosome%22%2C%0D%0A%22value%22%3A%5B%0D%0A%227%22%0D%0A%5D%0D%0A%7D%0D%0A%7D"
```
```Response
gene_start      gene_end        symbol  id
28995231        29195451        CPVL    ENSG00000106066
33014114        33062797        NT5C3A  ENSG00000122643
143052320       143053347       OR6V1   ENSG00000225781
100400826       100428992       ZCWPW1  ENSG00000078487
73861159        73865893        WBSCR28 ENSG00000175877
64862999        64864370        EEF1DP4 ENSG00000213640
159231435       159233377       PIP5K1P2        ENSG00000229435
141972631       141973773       TAS2R38 ENSG00000257138
16646131        16706523        BZW2    ENSG00000136261
149239651       149255609       ZNF212  ENSG00000170260
57405025        57405090        MIR3147 ENSG00000266168
130393771       130442433       CEP41   ENSG00000106477
150800403       150805120       TMEM176A        ENSG00000002933
93591573        93911265        GNGT1   ENSG00000127928
117465784       117715971       CFTR    ENSG00000001626
5879827 5886362 OCM     ENSG00000122543
144118461       144119360       OR2A15P ENSG00000239981
30424527        30478784        NOD1    ENSG00000106100
137227341       137343865       PTN     ENSG00000105894
84876554        84876956        HMGN2P11        ENSG00000232605
107470018       107475659       GPR22   ENSG00000172209
31330711        31330896        RP11-463M14.1   ENSG00000271027
78017057        79453574        MAGI2   ENSG00000187391
55736779        55739605        CICP11  ENSG00000237799
142111749       142222324       RP11-1220K2.2   ENSG00000257743
(truncated)
```

## Simple Somatic Mutation Endpoint Examples

__Example 1__: Similar to the `/genes` endpoint, a user would like to retrieve information about the mutation based on its COSMIC ID. This would be accomplished by creating a JSON filter such as:

```Query
 {
   "op":"in",
   "content":{
      "field":"cosmic_id",
      "value":[
         "COSM4860838"
      ]
   }
}
```

```Shell
curl 'https://api.gdc.cancer.gov/ssms?pretty=true&filters=%7B%0A%22op%22%3A%22in%22%2C%0A%22content%22%3A%7B%0A%22field%22%3A%22cosmic_id%22%2C%0A%22value%22%3A%5B%0A%22COSM4860838%22%0A%5D%0A%7D%0A%7D%0A'
```

```Response
{
  "data": {
    "hits": [
      {
        "ncbi_build": "GRCh38",
        "mutation_type": "Simple Somatic Mutation",
        "mutation_subtype": "Single base substitution",
        "end_position": 62438203,
        "reference_allele": "C",
        "ssm_id": "8b3c1a7a-e4e0-5200-9d46-5767c2982145",
        "start_position": 62438203,
        "cosmic_id": [
          "COSM4860838",
          "COSM731764",
          "COSM731765"
        ],
        "id": "8b3c1a7a-e4e0-5200-9d46-5767c2982145",
        "tumor_allele": "T",
        "gene_aa_change": [
          "CADPS G1147G",
          "CADPS G1187G",
          "CADPS G1217G",
          "CADPS G1226G",
          "CADPS G127G",
          "CADPS G218G",
          "CADPS G95G"
        ],
        "chromosome": "chr3",
        "genomic_dna_change": "chr3:g.62438203C>T"
      }
    ],
    "pagination": {
      "count": 1,
      "sort": "",
      "from": 0,
      "page": 1,
      "total": 1,
      "pages": 1,
      "size": 10
    }
  },
  "warnings": {}
}
```

## Simple Somatic Mutation Occurrence Endpoint Examples

__Example 1:__ A user wants to determine the chromosome in case `TCGA-DU-6407` that contains the greatest number of `ssms`. As this relates to mutations that are observed in a case, the `ssm_occurrences` endpoint is used.

```
{  
   "op":"in",
   "content":{  
      "field":"case.submitter_id",
      "value":["TCGA-DU-6407"]
   }
}
```
```Shell
curl "https://api.gdc.cancer.gov/ssm_occurrences?format=tsv&fields=ssm.chromosome&size=5000&filters=%7B%0D%0A%22op%22%3A%22in%22%2C%0D%0A%22content%22%3A%7B%0D%0A%22field%22%3A%22case.submitter_id%22%2C%0D%0A%22value%22%3A%5B%0D%0A%22TCGA-DU-6407%22%0D%0A%5D%0D%0A%7D%0D%0A%7D"
```
```Response
ssm.chromosome	id
chr3	552c09d1-69b1-5c04-b543-524a6feae3eb
chr10	391011ff-c1fd-5e2a-a128-652bc660f64c
chr10	1378cbc4-af88-55bb-b2e5-185bb4246d7a
chr10	3a2b3870-a395-5bc3-8c8f-0d40b0f2202c
chr1	4a93d7a5-988d-5055-80da-999dc3b45d80
chrX	22a07c7c-16ba-51df-a9a9-1e41e2a45225
chr12	dbc5eafa-ea26-5f1c-946c-b6974a345b69
chr11	02ae553d-1f27-565d-96c5-2c3cfca7264a
chr2	faee73a9-4804-58ea-a91f-18c3d901774f
chr6	97c5b38b-fc96-57f5-8517-cc702b3aa70a
chr17	0010a89d-9434-5d97-8672-36ee394767d0
chr19	f08dcc53-eadc-5ceb-bf31-f6b38629e4cb
chrX	19ca262d-b354-54a0-b582-c4719e37e91d
chr19	c44a93a1-5c73-5cff-b40e-98ce7e5fe57b
chr3	b67f31b5-0341-518e-8fcc-811cd2e36af1
chr1	94abd5fd-d539-5a4a-8719-9615cf7cec5d
chr17	1476a543-2951-5ec4-b165-67551b47d810
chr2	b4822fc9-f0cc-56fd-9d97-f916234e309d
chr2	3548ecfe-5186-51e7-8f40-37f4654cd260
chr16	105e7811-4601-5ccb-ae93-e7107923599e
chr2	99b3aad4-d368-506d-99d6-047cbe5dff0f
chr13	9dc3f7cd-9efa-530a-8524-30d067e49d54
chr21	1267330b-ae6d-5e25-b19e-34e98523679e
chr16	c77f7ce5-fbe6-5da4-9a7b-b528f8e530cb
chr10	2cb06277-993e-5502-b2c5-263037c45d18
chr17	d25129ad-3ad7-584f-bdeb-fba5c3881d32
chr17	a76469cb-973c-5d4d-bf82-7cf4e8f6c129
chr10	727c9d57-7b74-556f-aa5b-e1ca1f76d119
chr15	b4a86ffd-e60c-5c9c-aaa1-9e9f02d86116
chr5	3a023e72-da92-54f7-aa18-502c1076b2b0
```

## Analysis Endpoints

In addition to the `ssms`, `ssm_occurrences`, and `genes` endpoints mentioned previously, several `/analysis` endpoints were designed to quickly retrieve specific datasets used for visualization display.  

__Example 1:__ The `/analysis/top_cases_counts_by_genes` endpoint gives the number of cases with a mutation in each gene listed in the `gene_ids` parameter for each project. Note that this endpoint cannot be used with the `format` or `fields` parameters. In this instance, the query will produce the number of cases in each projects with mutations in the gene `ENSG00000155657`.

```Shell
curl "https://api.gdc.cancer.gov/analysis/top_cases_counts_by_genes?gene_ids=ENSG00000155657&pretty=true"
```


This JSON-formatted output is broken up by project. For an example, see the following text:

```json
          "genes": {
            "my_genes": {
              "gene_id": {
                "buckets": [
                  {
                    "key": "ENSG00000155657",
                    "doc_count": 45
                  }
                ],
                "sum_other_doc_count": 0,
                "doc_count_error_upper_bound": 0
              },
              "doc_count": 45
            },
            "doc_count": 12305
          },
          "key": "TCGA-GBM",
          "doc_count": 45
        }
```

This portion of the output shows TCGA-GBM including 45 cases that have `ssms` in the gene `ENSG00000155657`.

__Example 2:__ The following demonstrates a use of the `/analysis/top_mutated_genes_by_project` endpoint.  This will output the genes that are mutated in the most cases in "TCGA-DLBC" and will count the mutations that have a `HIGH` or `MODERATE` impact on gene function. Note that the `score` field does not represent the number of mutations in a given gene, but a calculation that is used to determine which genes have the greatest number of unique mutations.  

```json
{  
   "op":"AND",
   "content":[  
      {  
         "op":"in",
         "content":{  
            "field":"case.project.project_id",
            "value":[  
               "TCGA-DLBC"
            ]
         }
      },
      {  
         "op":"in",
         "content":{  
            "field":"case.ssm.consequence.transcript.annotation.impact",
            "value":[  
               "HIGH",
               "MODERATE"
            ]
         }
      }
   ]
}
```
```Shell
curl "https://api.gdc.cancer.gov/analysis/top_mutated_genes_by_project?fields=gene_id,symbol&filters=%7B%22op%22%3A%22AND%22%2C%22content%22%3A%5B%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22case.project.project_id%22%2C%22value%22%3A%5B%22TCGA-DLBC%22%5D%7D%7D%2C%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22case.ssm.consequence.transcript.annotation.impact%22%2C%22value%22%3A%5B%22HIGH%22%2C%22MODERATE%22%5D%7D%7D%5D%7D&pretty=true"
```
```Response
{
  "data": {
    "hits": [
      {
        "_score": 14.0,
        "symbol": "IGHV2-70",
        "gene_id": "ENSG00000274576"
      },
      {
        "_score": 14.0,
        "symbol": "IGLV3-1",
        "gene_id": "ENSG00000211673"
      },
      {
        "_score": 14.0,
        "symbol": "IGHM",
        "gene_id": "ENSG00000211899"
      },
      {
        "_score": 11.0,
        "symbol": "KMT2D",
        "gene_id": "ENSG00000167548"
      },
      {
        "_score": 11.0,
        "symbol": "IGLL5",
        "gene_id": "ENSG00000254709"
      },
      {
        "_score": 11.0,
        "symbol": "BTG2",
        "gene_id": "ENSG00000159388"
      },
      {
        "_score": 9.0,
        "symbol": "CARD11",
        "gene_id": "ENSG00000198286"
      },
      {
        "_score": 9.0,
        "symbol": "IGHG1",
        "gene_id": "ENSG00000211896"
      },
      {
        "_score": 9.0,
        "symbol": "IGLC2",
        "gene_id": "ENSG00000211677"
      },
      {
        "_score": 9.0,
        "symbol": "LRP1B",
        "gene_id": "ENSG00000168702"
      }
    ],
    "pagination": {
      "count": 10,
      "sort": "None",
      "from": 0,
      "page": 1,
      "total": 3214,
      "pages": 322,
      "size": 10
    }
  },
  "warnings": {}
}
```

__Example 3:__ The `/analysis/top_mutated_cases_by_gene` endpoint will generate information about the cases that are most affected by mutations in a given number of genes. Below, the file count for each category is given for the cases most affected by mutations in these 50 genes.  The size of the output is limited to two cases with the `size=2` parameter, but a higher value can be set by the user.

```Shell
curl "https://api.gdc.cancer.gov/analysis/top_mutated_cases_by_gene?fields=diagnoses.days_to_death,diagnoses.age_at_diagnosis,diagnoses.vital_status,diagnoses.primary_diagnosis,demographic.gender,demographic.race,demographic.ethnicity,case_id,summary.data_categories.file_count,summary.data_categories.data_category&filters=%7B%22op%22%3A%22and%22%2C%22content%22%3A%5B%7B%22op%22%3A%22%3D%22%2C%22content%22%3A%7B%22field%22%3A%22cases.project.project_id%22%2C%22value%22%3A%22TCGA-DLBC%22%7D%7D%2C%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22genes.gene_id%22%2C%22value%22%3A%5B%22ENSG00000166710%22%2C%22ENSG00000005339%22%2C%22ENSG00000083857%22%2C%22ENSG00000168769%22%2C%22ENSG00000100906%22%2C%22ENSG00000184677%22%2C%22ENSG00000101680%22%2C%22ENSG00000101266%22%2C%22ENSG00000028277%22%2C%22ENSG00000140968%22%2C%22ENSG00000181827%22%2C%22ENSG00000116815%22%2C%22ENSG00000275221%22%2C%22ENSG00000139083%22%2C%22ENSG00000112851%22%2C%22ENSG00000112697%22%2C%22ENSG00000164134%22%2C%22ENSG00000009413%22%2C%22ENSG00000071626%22%2C%22ENSG00000135407%22%2C%22ENSG00000101825%22%2C%22ENSG00000104814%22%2C%22ENSG00000166415%22%2C%22ENSG00000142867%22%2C%22ENSG00000254585%22%2C%22ENSG00000139718%22%2C%22ENSG00000077721%22%2C%22ENSG00000130294%22%2C%22ENSG00000117245%22%2C%22ENSG00000117318%22%2C%22ENSG00000270550%22%2C%22ENSG00000163637%22%2C%22ENSG00000166575%22%2C%22ENSG00000065526%22%2C%22ENSG00000156453%22%2C%22ENSG00000128191%22%2C%22ENSG00000055609%22%2C%22ENSG00000204469%22%2C%22ENSG00000187605%22%2C%22ENSG00000185875%22%2C%22ENSG00000110888%22%2C%22ENSG00000007341%22%2C%22ENSG00000173198%22%2C%22ENSG00000115568%22%2C%22ENSG00000163714%22%2C%22ENSG00000125772%22%2C%22ENSG00000080815%22%2C%22ENSG00000189079%22%2C%22ENSG00000120837%22%2C%22ENSG00000143951%22%5D%7D%7D%2C%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22ssms.consequence.transcript.annotation.impact%22%2C%22value%22%3A%5B%22HIGH%22%5D%7D%7D%5D%7D&pretty=true&size=2"
```
```Response
{
  "data": {
    "hits": [
      {
        "_score": 7.0,
        "diagnoses": [
          {
            "days_to_death": null,
            "vital_status": "alive",
            "age_at_diagnosis": 18691,
            "primary_diagnosis": "c83.3"
          }
        ],
        "case_id": "eda9496e-be80-4a13-bf06-89f0cc9e937f",
        "demographic": {
          "gender": "male",
          "race": "white",
          "ethnicity": "hispanic or latino"
        },
        "summary": {
          "data_categories": [
            {
              "file_count": 1,
              "data_category": "DNA Methylation"
            },
            {
              "file_count": 5,
              "data_category": "Transcriptome Profiling"
            },
            {
              "file_count": 1,
              "data_category": "Biospecimen"
            },
            {
              "file_count": 16,
              "data_category": "Simple Nucleotide Variation"
            },
            {
              "file_count": 1,
              "data_category": "Clinical"
            },
            {
              "file_count": 4,
              "data_category": "Copy Number Variation"
            },
            {
              "file_count": 4,
              "data_category": "Raw Sequencing Data"
            }
          ]
        }
      },
      {
        "_score": 4.0,
        "diagnoses": [
          {
            "days_to_death": null,
            "vital_status": "alive",
            "age_at_diagnosis": 27468,
            "primary_diagnosis": "c83.3"
          }
        ],
        "case_id": "a43e5f0e-a21f-48d8-97e0-084d413680b7",
        "demographic": {
          "gender": "male",
          "race": "white",
          "ethnicity": "not hispanic or latino"
        },
        "summary": {
          "data_categories": [
            {
              "file_count": 1,
              "data_category": "DNA Methylation"
            },
            {
              "file_count": 5,
              "data_category": "Transcriptome Profiling"
            },
            {
              "file_count": 1,
              "data_category": "Biospecimen"
            },
            {
              "file_count": 16,
              "data_category": "Simple Nucleotide Variation"
            },
            {
              "file_count": 1,
              "data_category": "Clinical"
            },
            {
              "file_count": 4,
              "data_category": "Copy Number Variation"
            },
            {
              "file_count": 4,
              "data_category": "Raw Sequencing Data"
            }
          ]
        }
      }
    ],
    "pagination": {
      "count": 2,
      "sort": "None",
      "from": 0,
      "page": 1,
      "total": 27,
      "pages": 14,
      "size": 2
    }
  },
  "warnings": {}
}
```

__Example 4:__  The `/analysis/mutated_cases_count_by_project` endpoint produces counts for the number of cases that have associated `ssm` data in each project. The number of affected cases can be found under `"case_with_ssm": {"doc_count": $case_count}`.  

```Shell
curl "https://api.gdc.cancer.gov/analysis/mutated_cases_count_by_project?size=0&pretty=true"
```
```Response
{
  "hits": {
    "hits": [],
    "total": 14551,
    "max_score": 0.0
  },
  "_shards": {
    "successful": 9,
    "failed": 0,
    "total": 9
  },
  "took": 4,
  "aggregations": {
    "projects": {
      "buckets": [
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 216
            },
            "doc_count": 637
          },
          "key": "TARGET-NBL",
          "doc_count": 1127
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 1044
            },
            "doc_count": 7625
          },
          "key": "TCGA-BRCA",
          "doc_count": 1098
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 8
            },
            "doc_count": 579
          },
          "key": "TARGET-AML",
          "doc_count": 988
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 34
            },
            "doc_count": 290
          },
          "key": "TARGET-WT",
          "doc_count": 652
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 396
            },
            "doc_count": 3197
          },
          "key": "TCGA-GBM",
          "doc_count": 617
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 443
            },
            "doc_count": 3880
          },
          "key": "TCGA-OV",
          "doc_count": 608
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 569
            },
            "doc_count": 3874
          },
          "key": "TCGA-LUAD",
          "doc_count": 585
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 542
            },
            "doc_count": 3874
          },
          "key": "TCGA-UCEC",
          "doc_count": 560
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 339
            },
            "doc_count": 3547
          },
          "key": "TCGA-KIRC",
          "doc_count": 537
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 510
            },
            "doc_count": 3671
          },
          "key": "TCGA-HNSC",
          "doc_count": 528
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 513
            },
            "doc_count": 3606
          },
          "key": "TCGA-LGG",
          "doc_count": 516
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 496
            },
            "doc_count": 3536
          },
          "key": "TCGA-THCA",
          "doc_count": 507
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 497
            },
            "doc_count": 3520
          },
          "key": "TCGA-LUSC",
          "doc_count": 504
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 498
            },
            "doc_count": 3490
          },
          "key": "TCGA-PRAD",
          "doc_count": 500
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 470
            },
            "doc_count": 3289
          },
          "key": "TCGA-SKCM",
          "doc_count": 470
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 433
            },
            "doc_count": 3188
          },
          "key": "TCGA-COAD",
          "doc_count": 461
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 441
            },
            "doc_count": 3095
          },
          "key": "TCGA-STAD",
          "doc_count": 443
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 412
            },
            "doc_count": 2884
          },
          "key": "TCGA-BLCA",
          "doc_count": 412
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 0
            },
            "doc_count": 0
          },
          "key": "TARGET-OS",
          "doc_count": 381
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 375
            },
            "doc_count": 2635
          },
          "key": "TCGA-LIHC",
          "doc_count": 377
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 305
            },
            "doc_count": 2142
          },
          "key": "TCGA-CESC",
          "doc_count": 307
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 288
            },
            "doc_count": 2033
          },
          "key": "TCGA-KIRP",
          "doc_count": 291
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 255
            },
            "doc_count": 1821
          },
          "key": "TCGA-SARC",
          "doc_count": 261
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 149
            },
            "doc_count": 1192
          },
          "key": "TCGA-LAML",
          "doc_count": 200
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 184
            },
            "doc_count": 1293
          },
          "key": "TCGA-ESCA",
          "doc_count": 185
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 183
            },
            "doc_count": 1285
          },
          "key": "TCGA-PAAD",
          "doc_count": 185
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 179
            },
            "doc_count": 1253
          },
          "key": "TCGA-PCPG",
          "doc_count": 179
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 158
            },
            "doc_count": 1169
          },
          "key": "TCGA-READ",
          "doc_count": 172
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 150
            },
            "doc_count": 1018
          },
          "key": "TCGA-TGCT",
          "doc_count": 150
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 123
            },
            "doc_count": 867
          },
          "key": "TCGA-THYM",
          "doc_count": 124
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 66
            },
            "doc_count": 556
          },
          "key": "TCGA-KICH",
          "doc_count": 113
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 92
            },
            "doc_count": 620
          },
          "key": "TCGA-ACC",
          "doc_count": 92
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 83
            },
            "doc_count": 605
          },
          "key": "TCGA-MESO",
          "doc_count": 87
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 80
            },
            "doc_count": 560
          },
          "key": "TCGA-UVM",
          "doc_count": 80
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 0
            },
            "doc_count": 163
          },
          "key": "TARGET-RT",
          "doc_count": 75
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 48
            },
            "doc_count": 346
          },
          "key": "TCGA-DLBC",
          "doc_count": 58
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 57
            },
            "doc_count": 399
          },
          "key": "TCGA-UCS",
          "doc_count": 57
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 51
            },
            "doc_count": 306
          },
          "key": "TCGA-CHOL",
          "doc_count": 51
        },
        {
          "case_summary": {
            "case_with_ssm": {
              "doc_count": 0
            },
            "doc_count": 13
          },
          "key": "TARGET-CCSK",
          "doc_count": 13
        }
      ],
      "sum_other_doc_count": 0,
      "doc_count_error_upper_bound": 0
    }
  },
  "timed_out": false
}
```
### Survival Analysis Endpoint

[Survival plots](/Data_Portal/Projects/#Survival-Analysis) are generated for different subsets of data, based on variants or projects, in the GDC Data Portal. The `/analysis/survival` endpoint can be used to programmatically retrieve the raw data used to generate these plots and apply different filters. Note that the `fields` and `format` parameters cannot be modified.

 __Example 1:__ A user wants to download data to generate a survival plot for cases from the project TCGA-DLBC.

```Shell
curl "https://api.gdc.cancer.gov/analysis/survival?filters=%5B%7B%22op%22%3A%22%3D%22%2C%22content%22%3A%7B%22field%22%3A%22cases.project.project_id%22%2C%22value%22%3A%22TCGA-DLBC%22%7D%7D%5D&pretty=true"
```
```Response
{
  "overallStats": {},
  "results": [
    {
      "donors": [
        {
          "survivalEstimate": 1,
          "id": "dc87a809-95de-4eb7-a1c2-2650475f2d7e",
          "censored": true,
          "time": 1
        },
        {
          "survivalEstimate": 1,
          "id": "4dd86ebd-ef16-4b2b-9ea0-5d1d7afef257",
          "censored": true,
          "time": 17
        },
        {
          "survivalEstimate": 1,
          "id": "0bf573ac-cd1e-42d8-90cf-b30d7b08679c",
          "censored": false,
          "time": 58
        },
        {
          "survivalEstimate": 0.9777777777777777,
          "id": "f978cb0f-d319-4c01-b4c5-23ae1403a106",
          "censored": true,
          "time": 126
        },
        {
          "survivalEstimate": 0.9777777777777777,
          "id": "a43e5f0e-a21f-48d8-97e0-084d413680b7",
          "censored": true,
          "time": 132
        },
        {
          "survivalEstimate": 0.9777777777777777,
          "id": "1843c82e-7a35-474f-9f79-c0a9af9aa09c",
          "censored": true,
          "time": 132
        },
        {
          "survivalEstimate": 0.9777777777777777,
          "id": "0030a28c-81aa-44b0-8be0-b35e1dcbf98c",
          "censored": false,
          "time": 248
        },
        {
          "survivalEstimate": 0.9539295392953929,
          "id": "f553f1a9-ecf2-4783-a609-6adca7c4c597",
          "censored": true,
          "time": 298
        },
        {
          "survivalEstimate": 0.9539295392953929,
          "id": "f784bc3a-751b-4025-aab2-0af2f6f24266",
          "censored": false,
          "time": 313
        },
        {
          "survivalEstimate": 0.929469807518588,
          "id": "29e3d122-15a1-4235-a356-b1a9f94ceb39",
          "censored": true,
          "time": 385
        },
        {
          "survivalEstimate": 0.929469807518588,
          "id": "0e251c03-bf86-4ed8-b45d-3cbc97160502",
          "censored": false,
          "time": 391
        },
        {
          "survivalEstimate": 0.9043490019099776,
          "id": "e6365b38-bc44-400c-b4aa-18ce8ff5bfce",
          "censored": true,
          "time": 427
        },
        {
          "survivalEstimate": 0.9043490019099776,
          "id": "b56bdbdb-43af-4a03-a072-54dd22d7550c",
          "censored": true,
          "time": 553
        },
        {
          "survivalEstimate": 0.9043490019099776,
          "id": "31bbad4e-3789-42ec-9faa-1cb86970f723",
          "censored": false,
          "time": 595
        },
        {
          "survivalEstimate": 0.8777505018538018,
          "id": "0e9fcccc-0630-408d-a121-2c6413824cb7",
          "censored": true,
          "time": 679
        },
        {
          "survivalEstimate": 0.8777505018538018,
          "id": "a5b188f0-a6d3-4d4a-b04f-36d47ec05338",
          "censored": false,
          "time": 708
        },
        {
          "survivalEstimate": 0.8503207986708705,
          "id": "ed746cb9-0f2f-48ce-923a-3a9f9f00b331",
          "censored": true,
          "time": 719
        },
        {
          "survivalEstimate": 0.8503207986708705,
          "id": "c85f340e-584b-4f3b-b6a5-540491fc8ad2",
          "censored": true,
          "time": 730
        },
        {
          "survivalEstimate": 0.8503207986708705,
          "id": "69f23725-adca-48ac-9b33-80a7aae24cfe",
          "censored": true,
          "time": 749
        },
        {
          "survivalEstimate": 0.8503207986708705,
          "id": "67325322-483f-443f-9ffa-2a20d108a2fb",
          "censored": true,
          "time": 751
        },
        {
          "survivalEstimate": 0.8503207986708705,
          "id": "eda9496e-be80-4a13-bf06-89f0cc9e937f",
          "censored": true,
          "time": 765
        },
        {
          "survivalEstimate": 0.8503207986708705,
          "id": "25ff86af-beb4-480c-b706-f3fe0306f7cf",
          "censored": true,
          "time": 788
        },
        {
          "survivalEstimate": 0.8503207986708705,
          "id": "1d0db5d7-39ca-466d-96b3-0d278c5ea768",
          "censored": true,
          "time": 791
        },
        {
          "survivalEstimate": 0.8503207986708705,
          "id": "c8cde9ea-89e9-4ee8-8a46-417a48f6d3ab",
          "censored": true,
          "time": 832
        },
        {
          "survivalEstimate": 0.8503207986708705,
          "id": "f0a326d2-1f3e-4a5d-bca8-32aaccc52338",
          "censored": true,
          "time": 946
        },
        {
          "survivalEstimate": 0.8503207986708705,
          "id": "a8e2df1e-4042-42af-9231-3a00e83489f0",
          "censored": true,
          "time": 965
        },
        {
          "survivalEstimate": 0.8503207986708705,
          "id": "e56e4d9c-052e-4ec6-a81b-dbd53e9c8ffe",
          "censored": true,
          "time": 972
        },
        {
          "survivalEstimate": 0.8503207986708705,
          "id": "45b0cf9f-a879-417f-8f39-7770552252c0",
          "censored": true,
          "time": 982
        },
        {
          "survivalEstimate": 0.8503207986708705,
          "id": "1f971af1-6772-4fe6-8d35-bbe527a037fe",
          "censored": true,
          "time": 1081
        },
        {
          "survivalEstimate": 0.8503207986708705,
          "id": "33365d22-cb83-4d8e-a2d1-06b675f75f6e",
          "censored": true,
          "time": 1163
        },
        {
          "survivalEstimate": 0.8503207986708705,
          "id": "6a21c948-cd85-4150-8c01-83017d7dc1ed",
          "censored": false,
          "time": 1252
        },
        {
          "survivalEstimate": 0.8003019281608192,
          "id": "f855dad1-6ffc-493e-ba6c-970874bc9210",
          "censored": true,
          "time": 1299
        },
        {
          "survivalEstimate": 0.8003019281608192,
          "id": "c1c06604-5ae2-4a53-b9c0-eb210d38e3f0",
          "censored": true,
          "time": 1334
        },
        {
          "survivalEstimate": 0.8003019281608192,
          "id": "58e66976-4507-4552-ac53-83a49a142dde",
          "censored": true,
          "time": 1373
        },
        {
          "survivalEstimate": 0.8003019281608192,
          "id": "ea54dbad-1b23-41cc-9378-d4002a8fca51",
          "censored": true,
          "time": 1581
        },
        {
          "survivalEstimate": 0.8003019281608192,
          "id": "d7df78b5-24f1-4ff4-bd9b-f0e6bec8289a",
          "censored": true,
          "time": 1581
        },
        {
          "survivalEstimate": 0.8003019281608192,
          "id": "29aff186-c321-4ff9-b81b-105e27e620ff",
          "censored": true,
          "time": 1617
        },
        {
          "survivalEstimate": 0.8003019281608192,
          "id": "5eff68ff-f6c3-40c9-9fc8-00e684a7b712",
          "censored": true,
          "time": 1739
        },
        {
          "survivalEstimate": 0.8003019281608192,
          "id": "f8cf647b-1447-4ac3-8c43-bef07765cabf",
          "censored": true,
          "time": 2131
        },
        {
          "survivalEstimate": 0.8003019281608192,
          "id": "c3d662ee-48d0-454a-bb0c-77d3338d3747",
          "censored": true,
          "time": 2983
        },
        {
          "survivalEstimate": 0.8003019281608192,
          "id": "6e9437f0-a4ed-475c-ab0e-bf1431c70a90",
          "censored": true,
          "time": 3333
        },
        {
          "survivalEstimate": 0.8003019281608192,
          "id": "fdecb74f-ac4e-46b1-b23a-5f7fde96ef9f",
          "censored": true,
          "time": 3394
        },
        {
          "survivalEstimate": 0.8003019281608192,
          "id": "a468e725-ad4b-411d-ac5c-2eacc68ec580",
          "censored": false,
          "time": 3553
        },
        {
          "survivalEstimate": 0.6402415425286554,
          "id": "1ea575f1-f731-408b-a629-f5f4abab569e",
          "censored": true,
          "time": 3897
        },
        {
          "survivalEstimate": 0.6402415425286554,
          "id": "7a589441-11ef-4158-87e7-3951d86bc2aa",
          "censored": true,
          "time": 4578
        },
        {
          "survivalEstimate": 0.6402415425286554,
          "id": "3622cf29-600f-4410-84d4-a9afeb41c475",
          "censored": true,
          "time": 5980
        },
        {
          "survivalEstimate": 0.6402415425286554,
          "id": "3f5a897d-1eaa-4d4c-8324-27ac07c90927",
          "censored": false,
          "time": 6425
        }
      ],
      "meta": {
        "id": 140429063094496
      }
    }
  ]
}
```

__Example 2:__ Here the survival endpoint is used to compare two survival plots for TCGA-BRCA cases.  One plot will display survival information about cases with a particular mutation (in this instance: `chr3:g.179234297A>G`) and the other plot will display information about cases without that mutation. This type of query will also print the results of a chi-squared analysis between the two subsets of cases.  

```json
[  
  {  
    "op":"and",
    "content":[  
      {  
        "op":"=",
        "content":{  
          "field":"cases.project.project_id",
          "value":"TCGA-BRCA"
        }
      },
      {  
        "op":"=",
        "content":{  
          "field":"gene.ssm.ssm_id",
          "value":"edd1ae2c-3ca9-52bd-a124-b09ed304fcc2"
        }
      }
    ]
  },
  {  
    "op":"and",
    "content":[  
      {  
        "op":"=",
        "content":{  
          "field":"cases.project.project_id",
          "value":"TCGA-BRCA"
        }
      },
      {  
        "op":"excludeifany",
        "content":{  
          "field":"gene.ssm.ssm_id",
          "value":"edd1ae2c-3ca9-52bd-a124-b09ed304fcc2"
        }
      }
    ]
  }
]
```
```Shell
curl "https://api.gdc.cancer.gov/analysis/survival?filters=%5B%7B%22op%22%3A%22and%22%2C%22content%22%3A%5B%7B%22op%22%3A%22%3D%22%2C%22content%22%3A%7B%22field%22%3A%22cases.project.project_id%22%2C%22value%22%3A%22TCGA-BRCA%22%7D%7D%2C%7B%22op%22%3A%22%3D%22%2C%22content%22%3A%7B%22field%22%3A%22gene.ssm.ssm_id%22%2C%22value%22%3A%22edd1ae2c-3ca9-52bd-a124-b09ed304fcc2%22%7D%7D%5D%7D%2C%7B%22op%22%3A%22and%22%2C%22content%22%3A%5B%7B%22op%22%3A%22%3D%22%2C%22content%22%3A%7B%22field%22%3A%22cases.project.project_id%22%2C%22value%22%3A%22TCGA-BRCA%22%7D%7D%2C%7B%22op%22%3A%22excludeifany%22%2C%22content%22%3A%7B%22field%22%3A%22gene.ssm.ssm_id%22%2C%22value%22%3A%22edd1ae2c-3ca9-52bd-a124-b09ed304fcc2%22%7D%7D%5D%7D%5D&pretty=true"
```
```json2
{
  "overallStats": {
    "degreesFreedom": 1,
    "chiSquared": 0.8577589072612264,
    "pValue": 0.35436660628146011
  },
  "results": [
    {
      "donors": [
        {
          "survivalEstimate": 1,
          "id": "a991644b-3ee6-4cda-acf0-e37de48a49fc",
          "censored": true,
          "time": 10
        },
        {
          "survivalEstimate": 1,
          "id": "2e1e3bf0-1708-4b65-936c-48b89eb8966a",
          "censored": true,
          "time": 19
        },
(truncated)
],
"meta": {
  "id": 140055251282040
}
},
{
"donors": [
  {
    "survivalEstimate": 1,
    "id": "5e4187c9-98f8-4bdb-a8da-6a914e96f47a",
    "censored": true,
    "time": -31
  },
(truncated)
```

The output represents two sets of coordinates delimited as objects with the `donors` tag. One set of coordinates will generate a survival plot representing TCGA-BRCA cases that have the mutation of interest and the other will generate a survival plot for the remaining cases in TCGA-BRCA.

__Example 3:__ Custom survival plots can be generated using the GDC API.  For example, a user could generate survival plot data comparing patients with a mutation in genes associated with a biological pathway with patients without mutations in that pathway. The following example compares a patient with at least one mutation in either gene `ENSG00000141510` or `ENSG00000155657` with patients that do not have mutations in these genes.

``` Query
[  
   {  
      "op":"and",
      "content":[  
         {  
            "op":"=",
            "content":{  
               "field":"cases.project.project_id",
               "value":"TCGA-BRCA"
            }
         },
         {  
            "op":"=",
            "content":{  
               "field":"gene.gene_id",
               "value":["ENSG00000141510","ENSG00000155657"]
            }
         }
      ]
   },
   {  
      "op":"and",
      "content":[  
         {  
            "op":"=",
            "content":{  
               "field":"cases.project.project_id",
               "value":"TCGA-BRCA"
            }
         },
         {  
            "op":"excludeifany",
            "content":{  
               "field":"gene.gene_id",
               "value":["ENSG00000141510","ENSG00000155657"]
            }
         }
      ]
   }
]
```
```Shell
curl "https://api.gdc.cancer.gov/analysis/survival?filters=%5B%0D%0A%7B%0D%0A%22op%22%3A%22and%22%2C%0D%0A%22content%22%3A%5B%0D%0A%7B%0D%0A%22op%22%3A%22%3D%22%2C%0D%0A%22content%22%3A%7B%0D%0A%22field%22%3A%22cases.project.project_id%22%2C%0D%0A%22value%22%3A%22TCGA-BRCA%22%0D%0A%7D%0D%0A%7D%2C%0D%0A%7B%0D%0A%22op%22%3A%22%3D%22%2C%0D%0A%22content%22%3A%7B%0D%0A%22field%22%3A%22gene.gene_id%22%2C%0D%0A%22value%22%3A%5B%22ENSG00000141510%22%2C%22ENSG00000155657%22%5D%0D%0A%7D%0D%0A%7D%0D%0A%5D%0D%0A%7D%2C%0D%0A%7B%0D%0A%22op%22%3A%22and%22%2C%0D%0A%22content%22%3A%5B%0D%0A%7B%0D%0A%22op%22%3A%22%3D%22%2C%0D%0A%22content%22%3A%7B%0D%0A%22field%22%3A%22cases.project.project_id%22%2C%0D%0A%22value%22%3A%22TCGA-BRCA%22%0D%0A%7D%0D%0A%7D%2C%0D%0A%7B%0D%0A%22op%22%3A%22excludeifany%22%2C%0D%0A%22content%22%3A%7B%0D%0A%22field%22%3A%22gene.gene_id%22%2C%0D%0A%22value%22%3A%5B%22ENSG00000141510%22%2C%22ENSG00000155657%22%5D%0D%0A%7D%0D%0A%7D%0D%0A%5D%0D%0A%7D%0D%0A%5D&pretty=true"
```

__Example 4:__ Survival plots can be even more customizable when sets of case IDs are used. Two sets of case IDs (or barcodes) can be retrieved in a separate step based on custom criteria and compared in a survival plot. See below for an example query.

```Json
[{  
   "op":"=",
   "content":{  
      "field":"cases.submitter_id",
      "value":["TCGA-HT-A74J","TCGA-43-A56U","TCGA-GM-A3XL","TCGA-A1-A0SQ","TCGA-K1-A6RV","TCGA-J2-A4AD","TCGA-XR-A8TE"]
   }
},
{  
   "op":"=",
   "content":{  
      "field":"cases.submitter_id",
      "value":["TCGA-55-5899","TCGA-55-6642","TCGA-55-7907","TCGA-67-6216","TCGA-75-5146","TCGA-49-4510","TCGA-78-7159"]
   }
}]
```
```Shell
curl "https://api.gdc.cancer.gov/analysis/survival?filters=%5B%7B%22op%22%3A%22%3D%22%2C%22content%22%3A%7B%22field%22%3A%22cases.submitter_id%22%2C%22value%22%3A%5B%22TCGA-HT-A74J%22%2C%22TCGA-43-A56U%22%2C%22TCGA-GM-A3XL%22%2C%22TCGA-A1-A0SQ%22%2C%22TCGA-K1-A6RV%22%2C%22TCGA-J2-A4AD%22%2C%22TCGA-XR-A8TE%22%5D%7D%7D%2C%7B%22op%22%3A%22%3D%22%2C%22content%22%3A%7B%22field%22%3A%22cases.submitter_id%22%2C%22value%22%3A%5B%22TCGA-55-5899%22%2C%22TCGA-55-6642%22%2C%22TCGA-55-7907%22%2C%22TCGA-67-6216%22%2C%22TCGA-75-5146%22%2C%22TCGA-49-4510%22%2C%22TCGA-78-7159%22%5D%7D%7D%5D"
```

# Additional Examples

## Data Search and Retrieval

### Endpoint Examples

This section contains additional examples for using endpoints.

#### Project Endpoint Example

This example is a query for Projects contained in GDC. It returns only the first five projects sorted by project name.

```Query
curl 'https://api.gdc.cancer.gov/projects?from=0&size=5&sort=project.name:asc&pretty=true'
```
```Response
{
  "data": {
    "hits": [
      {
        "state": "legacy",
        "project_id": "TARGET-AML",
        "primary_site": "Blood",
        "disease_type": "Acute Myeloid Leukemia",
        "name": "Acute Myeloid Leukemia"
      },
      {
        "state": "legacy",
        "project_id": "TCGA-LAML",
        "primary_site": "Blood",
        "disease_type": "Acute Myeloid Leukemia",
        "name": "Acute Myeloid Leukemia"
      },
      {
        "state": "legacy",
        "project_id": "TARGET-AML-IF",
        "primary_site": "Blood",
        "disease_type": "Acute Myeloid Leukemia Induction Failure",
        "name": "Acute Myeloid Leukemia Induction Failure"
      },
      {
        "state": "legacy",
        "project_id": "TARGET-ALL-P2",
        "primary_site": "Blood",
        "disease_type": "Acute Lymphoblastic Leukemia",
        "name": "Acute Lymphoblastic Leukemia - Phase II"
      },
      {
        "state": "legacy",
        "project_id": "TARGET-ALL-P1",
        "primary_site": "Blood",
        "disease_type": "Acute Lymphoblastic Leukemia",
        "name": "Acute Lymphoblastic Leukemia - Phase I"
      }
    ],
    "pagination": {
      "count": 5,
      "sort": "project.name:asc",
      "from": 0,
      "pages": 10,
      "total": 46,
      "page": 1,
      "size": 5
    }
  },
  "warnings": {}
}
```
#### Files Endpoint Example

This example is a query for files contained in GDC. It returns only the first two files, sorted by file size, from smallest to largest.

``` Query
curl 'https://api.gdc.cancer.gov/files?from=0&size=2&sort=file_size:asc&pretty=true'
```
```Response
{
  "data": {
    "hits": [
      {
        "data_type": "Raw Simple Somatic Mutation",
        "updated_datetime": "2017-03-04T16:45:40.925270-06:00",
        "file_name": "9f78a291-2d50-472c-8f56-5f8fbd09ab2a.snp.Somatic.hc.vcf.gz",
        "submitter_id": "TCGA-13-0757-01A-01W-0371-08_TCGA-13-0757-10A-01W-0371-08_varscan",
        "file_id": "9f78a291-2d50-472c-8f56-5f8fbd09ab2a",
        "file_size": 1120,
        "id": "9f78a291-2d50-472c-8f56-5f8fbd09ab2a",
        "created_datetime": "2016-05-04T14:50:54.560567-05:00",
        "md5sum": "13c1ceb3519615e2c67128b350365fbf",
        "data_format": "VCF",
        "acl": [
          "phs000178"
        ],
        "access": "controlled",
        "state": "live",
        "data_category": "Simple Nucleotide Variation",
        "type": "simple_somatic_mutation",
        "file_state": "submitted",
        "experimental_strategy": "WXS"
      },
      {
        "data_type": "Raw Simple Somatic Mutation",
        "updated_datetime": "2017-03-04T16:45:40.925270-06:00",
        "file_name": "7780009b-abb6-460b-903d-accdac626c2e.snp.Somatic.hc.vcf.gz",
        "submitter_id": "TCGA-HC-8261-01A-11D-2260-08_TCGA-HC-8261-10A-01D-2260-08_varscan",
        "file_id": "7780009b-abb6-460b-903d-accdac626c2e",
        "file_size": 1237,
        "id": "7780009b-abb6-460b-903d-accdac626c2e",
        "created_datetime": "2016-05-08T13:54:38.369393-05:00",
        "md5sum": "fd9bb46c8022b96af730c48dc00e2c41",
        "data_format": "VCF",
        "acl": [
          "phs000178"
        ],
        "access": "controlled",
        "state": "live",
        "data_category": "Simple Nucleotide Variation",
        "type": "simple_somatic_mutation",
        "file_state": "submitted",
        "experimental_strategy": "WXS"
      }
    ],
    "pagination": {
      "count": 2,
      "sort": "file_size:asc",
      "from": 0,
      "page": 1,
      "total": 274724,
      "pages": 137362,
      "size": 2
    }
  },
  "warnings": {}
}
```

#### Cases Endpoint Example

This example is a query for cases contained in GDC. It returns only the first five files.

```Query
curl 'https://api.gdc.cancer.gov/cases?from=0&size=5&pretty=true'
```
```Response
{
  "data": {
    "hits": [
      {
        "updated_datetime": "2017-03-09T10:01:14.834935-06:00",
        "submitter_analyte_ids": [
          "TCGA-ER-A193-06A-12D",
          "TCGA-ER-A193-06A-12R",
          "TCGA-ER-A193-06A-12W",
          "TCGA-ER-A193-10A-01W",
          "TCGA-ER-A193-10A-01D"
        ],
        "analyte_ids": [
          "62e14ca4-95f5-4af3-848f-83f7273c3b70",
          "6178b8aa-6afb-4951-bc92-bf9bfc57b9c7",
          "e16b701c-7809-4fb5-a9e0-4ff71e5d1d84",
          "5bfa8c9f-6797-4b2b-9122-854f8ab3bbba",
          "9b73d64e-c973-45b6-be31-a486fb8d1708"
        ],
        "submitter_id": "TCGA-ER-A193",
        "case_id": "8ab09143-daf6-40a9-85d3-0fe9de7b3e06",
        "id": "8ab09143-daf6-40a9-85d3-0fe9de7b3e06",
        "disease_type": "Skin Cutaneous Melanoma",
        "sample_ids": [
          "378b3d8a-adbb-4912-a0bf-6b74a282113e",
          "7a384d44-8b05-4197-9921-7d020ada2437"
        ],
        "portion_ids": [
          "6680bbf2-9cf1-4f93-9ec3-04318cffb5ba",
          "690d3b12-a61d-42fd-af2a-5a7a9a3e5de8",
          "824d724e-6836-423e-a751-fee3260ef4d2"
        ],
        "submitter_portion_ids": [
          "TCGA-ER-A193-06A-21-A20N-20",
          "TCGA-ER-A193-10A-01",
          "TCGA-ER-A193-06A-12"
        ],
        "created_datetime": null,
        "slide_ids": [
          "d2751354-a8b7-4f7a-a4f1-d062de5ceb14"
        ],
        "state": "live",
        "aliquot_ids": [
          "dc9f9544-6c76-4b45-b5c3-dd2fecd5acfe",
          "390b3574-ba23-4ecb-acf8-f5ad8a958bd2",
          "33f43961-b32d-46fc-ba11-264f1101e78d",
          "cd17367c-3270-42ae-8ac5-941a3453ea33",
          "b17269a2-79aa-459e-9c3d-589b7efe6fd9",
          "28a7d729-7555-4545-924b-3dec49b54230",
          "13256e77-0b0b-49e3-9959-3b6730d68732",
          "87ca642a-dd4c-47ea-b81f-2d3402f2157a",
          "8a1bfe0e-c97a-41c4-815f-cf5bb5cfc69f",
          "5e1e9c82-99fd-49de-9dfb-a349d4d8ac94",
          "67f00459-e423-4900-be23-9283b0478620",
          "d939c477-a01f-4d54-bcfb-c9fdd957f2ec"
        ],
        "primary_site": "Skin",
        "submitter_aliquot_ids": [
          "TCGA-ER-A193-06A-12D-A18Y-02",
          "TCGA-ER-A193-10A-01D-A193-01",
          "TCGA-ER-A193-10A-01D-A190-02",
          "TCGA-ER-A193-06A-12D-A197-08",
          "TCGA-ER-A193-06A-12R-A18S-07",
          "TCGA-ER-A193-06A-12W-A20H-08",
          "TCGA-ER-A193-10A-01D-A199-08",
          "TCGA-ER-A193-10A-01D-A38R-08",
          "TCGA-ER-A193-10A-01W-A20J-08",
          "TCGA-ER-A193-06A-12R-A18V-13",
          "TCGA-ER-A193-06A-12D-A19C-05",
          "TCGA-ER-A193-06A-12D-A191-01"
        ],
        "submitter_sample_ids": [
          "TCGA-ER-A193-10A",
          "TCGA-ER-A193-06A"
        ],
        "submitter_slide_ids": [
          "TCGA-ER-A193-06A-01-TSA"
        ]
      },
      {
        "updated_datetime": "2017-03-04T16:39:19.244769-06:00",
        "submitter_analyte_ids": [
          "TCGA-VR-AA4G-10A-01W",
          "TCGA-VR-AA4G-01A-11R",
          "TCGA-VR-AA4G-10A-01D",
          "TCGA-VR-AA4G-01A-11D",
          "TCGA-VR-AA4G-01A-11W"
        ],
        "analyte_ids": [
          "152d7d7a-c746-4b58-8c3f-4252454c7b7c",
          "9090d556-bd2e-4851-8a0c-46e22cc61408",
          "7118f4c3-b635-4428-8240-8db85281f2d9",
          "1d8223ff-685a-4427-a3d1-f53887f2a19d",
          "60dfb30a-bea0-426d-b11d-d5813ba39cfc"
        ],
        "submitter_id": "TCGA-VR-AA4G",
        "case_id": "df5bd25c-d70b-4126-89cb-6c838044ae3b",
        "id": "df5bd25c-d70b-4126-89cb-6c838044ae3b",
        "disease_type": "Esophageal Carcinoma",
        "sample_ids": [
          "21456849-38a9-4190-9ece-ed69b3c24fda",
          "6ee6d239-2af6-41cd-bc32-c5cdaf7742b0"
        ],
        "portion_ids": [
          "484b40d5-d77c-4e6f-9e80-1ef27ffbc8a5",
          "fdc56e67-52ab-44fd-823a-5a3124876ff7"
        ],
        "submitter_portion_ids": [
          "TCGA-VR-AA4G-10A-01",
          "TCGA-VR-AA4G-01A-11"
        ],
        "created_datetime": null,
        "slide_ids": [
          "e950eba2-7d6e-4ffd-a2d5-e0eb6486848a"
        ],
        "state": "live",
        "aliquot_ids": [
          "db6beed3-a5a2-469f-8dc8-00d838c1f37f",
          "f5db4d36-034b-429b-a7be-26a872b702ee",
          "16421a96-b843-4f7e-9f7c-64d2fb5b2a25",
          "5d938cb5-7064-40bc-877d-57faa94c3333",
          "d231404d-ece5-43c0-a8a3-e9f294ceb777",
          "8c77dc3e-2ea3-4626-88f5-e74f242bedf3",
          "993624d4-1c28-41a5-a0b6-094a0e442c36",
          "105a18c9-df7e-4573-b1a2-6a987e57d553",
          "af81c3bb-3b9e-41cb-b85a-b55c6437d05b",
          "38938066-5fd9-415c-b00e-65efff14085e",
          "20139afe-ad04-4571-b779-0c4a51e74ada"
        ],
        "primary_site": "Esophagus",
        "submitter_aliquot_ids": [
          "TCGA-VR-AA4G-10A-01W-A44M-09",
          "TCGA-VR-AA4G-01A-11D-A37B-01",
          "TCGA-VR-AA4G-01A-11D-A37D-05",
          "TCGA-VR-AA4G-10A-01D-A37F-09",
          "TCGA-VR-AA4G-01A-11D-A37R-26",
          "TCGA-VR-AA4G-01A-11R-A37J-13",
          "TCGA-VR-AA4G-01A-11R-A37I-31",
          "TCGA-VR-AA4G-01A-11D-A37C-09",
          "TCGA-VR-AA4G-10A-01D-A37R-26",
          "TCGA-VR-AA4G-10A-01D-A37E-01",
          "TCGA-VR-AA4G-01A-11W-A44L-09"
        ],
        "submitter_sample_ids": [
          "TCGA-VR-AA4G-01A",
          "TCGA-VR-AA4G-10A"
        ],
        "submitter_slide_ids": [
          "TCGA-VR-AA4G-01A-01-TS1"
        ]
      },
      {
        "updated_datetime": "2017-03-04T16:39:19.244769-06:00",
        "submitter_analyte_ids": [
          "TCGA-D1-A174-01A-11D",
          "TCGA-D1-A174-01A-11W",
          "TCGA-D1-A174-10A-01D",
          "TCGA-D1-A174-10A-01W",
          "TCGA-D1-A174-01A-11R"
        ],
        "analyte_ids": [
          "96203028-f824-4a90-9758-22340285062c",
          "f4878e33-b773-43b5-83a5-9fd8e539e668",
          "8627ccd0-0575-4d03-b589-ca45642d523d",
          "1183f7c6-992d-4084-946e-adce7c52f9cc",
          "5343f6a8-8ac2-4446-ace5-a27d21e76844"
        ],
        "submitter_id": "TCGA-D1-A174",
        "case_id": "fc7315b0-9f48-4206-b197-2268c0518eb4",
        "id": "fc7315b0-9f48-4206-b197-2268c0518eb4",
        "disease_type": "Uterine Corpus Endometrial Carcinoma",
        "sample_ids": [
          "df9a1f44-9b3f-48b2-96af-54aaabdfd243",
          "ad5a9cb6-b3f9-4651-b6d1-13c78010bd88"
        ],
        "portion_ids": [
          "79dd516c-bae3-4f6e-b4cb-901de030acb7",
          "6e55e6d9-902f-439b-b6f1-ca296c123fd3"
        ],
        "submitter_portion_ids": [
          "TCGA-D1-A174-01A-11",
          "TCGA-D1-A174-10A-01"
        ],
        "created_datetime": null,
        "slide_ids": [
          "7602727e-b46d-40fc-bd03-5ccf631041f8"
        ],
        "state": "live",
        "aliquot_ids": [
          "5c15542b-cd63-44b5-b278-e211410fb0aa",
          "d661cfb9-248a-49e6-b0db-865ca257e8dc",
          "83bd3bdb-9bd3-46fa-888c-f6f5efec530f",
          "c46551c9-c0d0-4140-8d0a-946b53e504e2",
          "96b511df-3a69-4168-908c-662060b4f976",
          "0182d4e1-f835-46b5-a8f0-53decf5868de",
          "e9563a06-0b86-4986-976e-43d4040f1d61",
          "6bb2de6e-5b85-4e97-a930-1f2c6bf663a1",
          "f6ee5558-a1b6-4b11-8f48-c17186fff39a",
          "67f6f0d9-6581-4946-a9c7-a6629da86888",
          "39e9a948-054a-4b50-b108-7d7aee686363",
          "ddb4ca26-655d-4bdc-a00d-7caf26cadafe"
        ],
        "primary_site": "Uterus",
        "submitter_aliquot_ids": [
          "TCGA-D1-A174-01A-11D-A12F-02",
          "TCGA-D1-A174-01A-01D-YYYY-23",
          "TCGA-D1-A174-01A-11W-A139-09",
          "TCGA-D1-A174-10A-01W-A139-09",
          "TCGA-D1-A174-01A-11D-A12K-05",
          "TCGA-D1-A174-10A-01D-A12F-02",
          "TCGA-D1-A174-10A-01D-A12G-01",
          "TCGA-D1-A174-01A-11R-A12I-07",
          "TCGA-D1-A174-01A-11D-A12J-09",
          "TCGA-D1-A174-10A-01D-A12J-09",
          "TCGA-D1-A174-01A-11R-A12H-13",
          "TCGA-D1-A174-01A-11D-A12G-01"
        ],
        "submitter_sample_ids": [
          "TCGA-D1-A174-01A",
          "TCGA-D1-A174-10A"
        ],
        "submitter_slide_ids": [
          "TCGA-D1-A174-01A-01-TS1"
        ]
      },
      {
        "updated_datetime": "2017-03-04T16:39:19.244769-06:00",
        "submitter_analyte_ids": [
          "TCGA-XM-A8RL-10A-01D",
          "TCGA-XM-A8RL-01A-11R",
          "TCGA-XM-A8RL-01A-11D"
        ],
        "analyte_ids": [
          "2c483e72-92b0-425d-ac1b-b75a169cf531",
          "57f88d4f-8b3a-4349-88b0-3d2e58a95ed9",
          "499bfbe1-639c-479c-abaa-42cbb11c0568"
        ],
        "submitter_id": "TCGA-XM-A8RL",
        "case_id": "dd240b82-b1d6-4c0f-aa3e-6fcfe1364ec1",
        "id": "dd240b82-b1d6-4c0f-aa3e-6fcfe1364ec1",
        "disease_type": "Thymoma",
        "sample_ids": [
          "cb091cc1-7bbe-43a4-8460-01215af3aa21",
          "cabc9729-c1e1-4f08-9959-985dcb7a00d5"
        ],
        "portion_ids": [
          "e8ea57c9-729e-46ea-b1da-2db7a00b02bc",
          "8e2edb92-753f-4cb0-a5b8-8c45dbefaf36",
          "650fa4f2-9fa2-4d3a-8b63-ff4a9bd8c33e"
        ],
        "submitter_portion_ids": [
          "TCGA-XM-A8RL-01A-21-A45R-20",
          "TCGA-XM-A8RL-10A-01",
          "TCGA-XM-A8RL-01A-11"
        ],
        "created_datetime": null,
        "slide_ids": [
          "08cedd34-aafd-4b47-891f-cf66ee1f627b"
        ],
        "state": "live",
        "aliquot_ids": [
          "df9d8553-8d5b-4c65-8b28-74030a8f8e76",
          "47b7f634-b36f-49e9-a4dc-d8f5508fdc0a",
          "e692ebed-9721-40db-8986-fcaba07d68f1",
          "189ee080-95d1-4ccb-8618-955605c7bd55",
          "83af7ff3-45be-4378-a8b5-5dff3584e95d",
          "42ebb1f0-e236-48ae-847f-69a153969903",
          "e8a4938f-6b93-4ad1-9324-31c97dd1d477"
        ],
        "primary_site": "Thymus",
        "submitter_aliquot_ids": [
          "TCGA-XM-A8RL-10A-01D-A426-09",
          "TCGA-XM-A8RL-01A-11D-A423-09",
          "TCGA-XM-A8RL-01A-11D-A422-01",
          "TCGA-XM-A8RL-01A-11R-A42C-07",
          "TCGA-XM-A8RL-10A-01D-A425-01",
          "TCGA-XM-A8RL-01A-11R-A42W-13",
          "TCGA-XM-A8RL-01A-11D-A424-05"
        ],
        "submitter_sample_ids": [
          "TCGA-XM-A8RL-10A",
          "TCGA-XM-A8RL-01A"
        ],
        "submitter_slide_ids": [
          "TCGA-XM-A8RL-01A-01-TSA"
        ]
      },
      {
        "updated_datetime": "2017-03-04T16:39:19.244769-06:00",
        "submitter_analyte_ids": [
          "TCGA-B0-5120-01A-01W",
          "TCGA-B0-5120-01A-01D",
          "TCGA-B0-5120-01A-01R",
          "TCGA-B0-5120-11A-01W",
          "TCGA-B0-5120-11A-01D"
        ],
        "analyte_ids": [
          "996336e6-fad7-4100-96ae-60adb5c276f1",
          "0eb7da02-0b90-4f6d-abd2-b048a9cb2995",
          "fa2861b9-67c1-486a-a1e0-95d8f8adf65b",
          "7e9f5639-a462-493e-98f8-1b7aeee383c7",
          "d51e9fd4-0c99-49ec-9de5-db3946b0bf43"
        ],
        "submitter_id": "TCGA-B0-5120",
        "case_id": "c5bf474c-6919-47b4-ba59-34ab20c087d5",
        "id": "c5bf474c-6919-47b4-ba59-34ab20c087d5",
        "disease_type": "Kidney Renal Clear Cell Carcinoma",
        "sample_ids": [
          "b50d3c6f-fdec-488b-ab26-a9b690fad34f",
          "f3148210-ecae-4314-b5f8-9bee2315a093"
        ],
        "portion_ids": [
          "b8fcbf00-4c5a-42c3-95e9-fb6e169a8da9",
          "34443e91-0210-4477-9511-53026ae62b38",
          "e466f011-79a1-4158-b796-f8e9dda32d68"
        ],
        "submitter_portion_ids": [
          "TCGA-B0-5120-01A-01",
          "TCGA-B0-5120-11A-01",
          "TCGA-B0-5120-01A-21-1740-20"
        ],
        "created_datetime": null,
        "slide_ids": [
          "e5a29e92-4125-4acb-a797-86822b4961a2",
          "78d873e0-037f-4aef-8725-7c651598b1f8",
          "43d8cec7-f5a0-45d5-a5f8-cc77d6b7b539"
        ],
        "state": "live",
        "aliquot_ids": [
          "b35280fe-dbfa-4e45-8f49-3d0489e68743",
          "a2e3a2f2-c32b-44a1-9b29-911145d700b8",
          "a064d108-e8b2-46fa-b277-0a7a89904a3a",
          "59be71a1-50e3-4565-852a-173afc8a6851",
          "136dff0e-b181-49c9-8305-b3289625ea2e",
          "8fbb983b-53ad-44a9-976a-7945628eaa51",
          "cecf40f8-7301-4db9-b276-a14317d4dd59",
          "fac8b066-bf2c-4f08-b42b-251035596a28",
          "fa55c92f-54e8-436b-b8c4-04cb68a24e93",
          "007e3098-aaf9-4ee7-9ae1-f94b131a5ae0",
          "6ce58fbc-6742-4ade-84b0-cd025266e030",
          "9668e15e-a3fa-4ead-ad42-322c5700e0db",
          "c1167003-0730-41d5-bdd5-1cbf501c1463",
          "73aab074-cbd1-45f2-8266-9ef6f7c559bc"
        ],
        "primary_site": "Kidney",
        "submitter_aliquot_ids": [
          "TCGA-B0-5120-11A-01D-1416-02",
          "TCGA-B0-5120-11A-01D-2099-10",
          "TCGA-B0-5120-11A-01D-1418-05",
          "TCGA-B0-5120-01A-01W-1475-10",
          "TCGA-B0-5120-01A-01D-1421-08",
          "TCGA-B0-5120-01A-01D-1416-02",
          "TCGA-B0-5120-01A-01R-1419-13",
          "TCGA-B0-5120-01A-01R-1420-07",
          "TCGA-B0-5120-11A-01D-1421-08",
          "TCGA-B0-5120-01A-01D-1417-01",
          "TCGA-B0-5120-01A-01D-1418-05",
          "TCGA-B0-5120-11A-01W-1475-10",
          "TCGA-B0-5120-01A-01D-2099-10",
          "TCGA-B0-5120-11A-01D-1417-01"
        ],
        "submitter_sample_ids": [
          "TCGA-B0-5120-11A",
          "TCGA-B0-5120-01A"
        ],
        "submitter_slide_ids": [
          "TCGA-B0-5120-11A-01-TS1",
          "TCGA-B0-5120-01A-01-BS1",
          "TCGA-B0-5120-01A-01-TS1"
        ]
      }
    ],
    "pagination": {
      "count": 5,
      "sort": "",
      "from": 0,
      "page": 1,
      "total": 14551,
      "pages": 2911,
      "size": 5
    }
  },
  "warnings": {}
}
```

#### Annotations Endpoint Example

This example is a query for annotations contained in the GDC. It returns only the first two annotations.

```Query
curl 'https://api.gdc.cancer.gov/annotations?from=0&size=2&pretty=true'
```
```Response
{
  "data": {
    "hits": [
      {
        "category": "History of unacceptable prior treatment related to a prior/other malignancy",
        "status": "Approved",
        "entity_id": "51c37449-6a2e-4c3d-a7cc-06f901e1224f",
        "classification": "Notification",
        "entity_type": "case",
        "created_datetime": "2014-06-16T00:00:00",
        "annotation_id": "3d086829-de62-5d08-b848-ce0724188ff0",
        "notes": "unknown treatment history",
        "updated_datetime": "2017-03-09T12:32:36.305475-06:00",
        "submitter_id": "20743",
        "state": "submitted",
        "case_id": "51c37449-6a2e-4c3d-a7cc-06f901e1224f",
        "case_submitter_id": "TCGA-AG-A014",
        "entity_submitter_id": "TCGA-AG-A014",
        "id": "3d086829-de62-5d08-b848-ce0724188ff0"
      },
      {
        "category": "Center QC failed",
        "status": "Approved",
        "entity_id": "733f0607-6c6b-4385-9868-fa6f155a9a2e",
        "classification": "CenterNotification",
        "entity_type": "aliquot",
        "created_datetime": "2012-07-20T00:00:00",
        "annotation_id": "5cf05f41-ce70-58a3-8ecb-6bfaf6264437",
        "notes": "RNA-seq:INSUFFICIENT INPUT MATERIAL,LOW SEQUENCE YIELD/DIVERSITY;LOW 5/3 COVERAGE RATIO",
        "updated_datetime": "2017-03-09T13:51:45.396638-06:00",
        "submitter_id": "8764",
        "state": "submitted",
        "case_id": "3e8a51bf-7e1f-4eab-af83-3c60d04db1bf",
        "case_submitter_id": "TCGA-13-0913",
        "entity_submitter_id": "TCGA-13-0913-02A-01R-1564-13",
        "id": "5cf05f41-ce70-58a3-8ecb-6bfaf6264437"
      }
    ],
    "pagination": {
      "count": 2,
      "sort": "",
      "from": 0,
      "page": 1,
      "total": 2361,
      "pages": 1181,
      "size": 2
    }
  },
  "warnings": {}
}
```

### Filters Examples

This section contains additional examples for using the `filters` parameter.

#### Example: Basic syntax

The following is an example of `filters` syntax, including the JSON object passed to the `filters` parameter, the corresponding API query, and the JSON object returned by the API. The example finds projects where the primary site is Blood.

```Filter
{
  "op": "and",
  "content": [
    {
      "op": "in",
      "content": {
        "field": "primary_site",
        "value": [
          "Blood"
        ]
      }
    }
  ]
}
```
```Query
curl 'https://api.gdc.cancer.gov/projects?filters=%7b%0d%0a++%22op%22%3a+%22and%22%2c%0d%0a++%22content%22%3a+%5b%0d%0a++++%7b%0d%0a++++++%22op%22%3a+%22in%22%2c%0d%0a++++++%22content%22%3a+%7b%0d%0a++++++++%22field%22%3a+%22primary_site%22%2c%0d%0a++++++++%22value%22%3a+%5b%0d%0a++++++++++%22Blood%22%0d%0a++++++++%5d%0d%0a++++++%7d%0d%0a++++%7d%0d%0a++%5d%0d%0a%7d&pretty=true'
```
```Response
{
  "data": {
    "hits": [
      {
        "dbgap_accession_number": "phs000465",
        "disease_type": [
          "Acute Myeloid Leukemia"
        ],
        "released": true,
        "state": "legacy",
        "primary_site": [
          "Blood"
        ],
        "project_id": "TARGET-AML",
        "id": "TARGET-AML",
        "name": "Acute Myeloid Leukemia"
      }
    ],
    "pagination": {
      "count": 1,
      "sort": "",
      "from": 0,
      "page": 1,
      "total": 1,
      "pages": 1,
      "size": 10
    }
  },
  "warnings": {}
}
```

#### Example: Filter cases keeping only 'male'

This is an example of a value-based filter:


```Filter
{
   "op" : "=" ,
   "content" : {
       "field" : "cases.demographic.gender" ,
       "value" : [ "male" ]
   }
}
```
```Query
curl 'https://api.gdc.cancer.gov/cases?filters=%7b%0d%0a+++%22op%22+%3a+%22%3d%22+%2c%0d%0a+++%22content%22+%3a+%7b%0d%0a+++++++%22field%22+%3a+%22cases.demographic.gender%22+%2c%0d%0a+++++++%22value%22+%3a+%5b+%22male%22+%5d%0d%0a+++%7d%0d%0a%7d%0d%0a&fields=demographic.gender,case_id&pretty=true'
```

#### Example: Filter using a range

This is an example of filtering for age at diagnosis. The request is for cases where the age at diagnosis is between 40 and 70 years. *Note:* `age_at_diagnosis` is expressed in days.

```Filter
{
    "op": "and",
    "content": [
        {
            "op": ">=",
            "content": {
                "field": "cases.diagnoses.age_at_diagnosis",
                "value": [
                    14600
                ]
            }
        },
        {
            "op": "<=",
            "content": {
                "field": "cases.diagnoses.age_at_diagnosis",
                "value": [
                    25550
                ]
            }
        }
    ]
}
```
```Query
curl 'https://api.gdc.cancer.gov/cases?filters=%7B%22op%22:%22and%22,%22content%22:%5B%7B%22op%22:%22%3E%3D%22,%22content%22:%7B%22field%22:%22cases.diagnoses.age_at_diagnosis%22,%22value%22:%5B14600%5D%7D%7D,%7B%22op%22:%22%3C%3D%22,%22content%22:%7B%22field%22:%22cases.diagnoses.age_at_diagnosis%22,%22value%22:%5B25550%5D%7D%7D%5D%7D&fields=diagnoses.age_at_diagnosis,case_id&pretty=true'
```


#### Example: Multiple fields

Filter projects for primary_site being Kidney or Brain and program.name being TCGA

```Filter
{
     "op" : "and" ,
     "content" : [{
             "op" : "in" ,
             "content" : {
                 "field" : "primary_site" ,
                 "value" : [
                     "Kidney" ,
                     "Brain"
                 ]
             }
         }, {
             "op" : "in" ,
             "content" : {
                 "field" : "program.name" ,
                 "value" : [
                     "TCGA"
                 ]
             }
         }]
}
```
```Query
curl 'https://api.gdc.cancer.gov/projects?filters=%7B%22op%22%3A%22and%22%2C%22content%22%3A%5B%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22primary_site%22%2C%22value%22%3A%5B%22Kidney%22%2C%22Brain%22%5D%7D%7D%2C%7B%22op%22%3A%22in%22%2C%22content%22%3A%7B%22field%22%3A%22program.name%22%2C%22value%22%3A%5B%22TCGA%22%5D%7D%7D%5D%7D&pretty=true'
```

# Downloading Files

The GDC API implements file download functionality using `data` and `manifest` endpoints. The `data` endpoint allows users to download files stored in the GDC by specifying file UUID(s). The `manifest` endpoint generates a download manifest file that can be used with the GDC Data Transfer Tool to transfer large volumes of data.

**Note:** Downloading controlled access data requires the use of an authentication token. See [Getting Started: Authentication](Getting_Started.md#authentication) for details.

**Note:** Requests to download data from the GDC Legacy Archive may be directed to `legacy/data` or `data`. See [Getting Started: Legacy Archive](Getting_Started.md#gdc-legacy-archive) for details.

## Data endpoint

To download a file, users can pass UUID(s) to the `data` endpoint.  If a single UUID is provided, the API will return the associated file. If a comma-separated list of UUIDs is provided, the API will return an archive file containing the requested files.

The `data` endpoint supports GET and POST requests as demonstrated in the following examples.


### Downloading a Single File using GET

This example demonstrates downloading a single file from the GDC. Here we pass the file's UUID to the `data` endpoint with a GET request.

```shell
curl --remote-name --remote-header-name 'https://api.gdc.cancer.gov/data/5b2974ad-f932-499b-90a3-93577a9f0573'
```
```Output
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 6111k  100 6111k    0     0   414k      0  0:00:14  0:00:14 --:--:--  412k
curl: Saved to filename '14-3-3_beta-R-V_GBL1112940.tif'
```
### Related Files

If the `related_files=true` parameter is specified, the following related files, if available, will be included in the download package by the GDC API:

* BAM index files (BAI files)
* Metadata files (such as SRA XML or MAGE-TAB files)

For example, this request will download a legacy copy number segmentation file and its associated MAGE-TAB metadata file:

```shell
curl --remote-name --remote-header-name 'https://api.gdc.cancer.gov/data/7efc039a-fde3-4bc1-9433-2fc6b5e3ffa5?related_files=true'
```
```Output
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
															 Dload  Upload   Total   Spent    Left  Speed
100 65353    0 65353    0     0  65353      0 --:--:-- --:--:-- --:--:--  102k
curl: Saved to filename 'gdc_download_20180830_131817.826097.tar.gz'
```


### Downloading Multiple Files using GET

This example demonstrates downloading multiple files from the GDC using a GET request. The GDC API returns a `.tar.gz` archive containing the downloaded files.

```shell
curl --remote-name --remote-header-name 'https://api.gdc.cancer.gov/data/e3228020-1c54-4521-9182-1ea14c5dc0f7,18e1e38e-0f0a-4a0e-918f-08e6201ea140'
```
```Output
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                               Dload  Upload   Total   Spent    Left  Speed
100  287k    0  287k    0     0  30131      0 --:--:--  0:00:09 --:--:-- 42759
curl: Saved to filename 'gdc_download_064d1aa8cc8cbab33e93979bebbf7d6af2d6a802.tar.gz'
```

**Note:** This method supports downloading a limited number of files at one time. To download a large number of files, please use [POST](#downloading-multiple-files-using-post).

#### Downloading an Uncompressed Group of Files

If the `?tarfile` parameter is specified to a data endpoint download query all files requested in the download string will be bundled in a single tar file rather than a tar.gz file which is the default behavior.  
```shell
curl --remote-name --remote-header-name 'https://api.gdc.cancer.gov/data/1da7105a-f0ff-479d-9f82-6c1d94456c91,77e73cc4-ff31-449e-8e3c-7ae5ce57838c?tarfile'
```      

### Downloading Multiple Files using POST

The following two examples demonstrate downloading multiple files from the GDC using a POST request that contains a payload in one of two formats: percent-encoded form data or JSON. The GDC API returns a `.tar.gz` archive containing the downloaded files.

#### POST request with form data payload

POST requests that carry a payload of percent-encoded form data must include the HTTP header `Content-Type: application/x-www-form-urlencoded`.

The payload is a string in the following format:

	ids=UUID1&ids=UUID2&ids=UUID3...

where UUID# corresponds to the UUIDs of the files to be downloaded.

In this example we use `curl` to download a set of files from the GDC Legacy Archive. The payload is stored in a plain text file named `Payload`; `curl` includes the `Content-Type: application/x-www-form-urlencoded` header by default.

```Payload
ids=556e5e3f-0ab9-4b6c-aa62-c42f6a6cf20c&ids=e0de63e2-02f3-4309-9b24-69f4c24e85fc&ids=f1a06178-2ec2-4b06-83f3-3aedac332cfe&ids=11a8aca0-c8e6-4ff8-8ab6-fe18a1b8ba82&ids=69a69c84-00de-45ff-b397-fd2b6713ed4f&ids=9ec48233-395d-401e-b205-951c971f8dd4&ids=93129547-378c-4b69-b858-532abfff678e&ids=8d4277e9-a472-4590-886d-24dc2538ea65&ids=6733b412-56da-4f1c-a12b-ff804cb656d7&ids=a72eec98-c5e0-4866-8953-765780acb6c1&ids=e77b2294-1bdd-4fba-928a-d81d2622312f&ids=965e01fc-318e-4c02-a801-d6fad60bfae4&ids=21ad5409-fe0b-4728-97e4-15520b9fc287&ids=1a777521-277c-4aeb-baf1-66871a7c2d2a&ids=c13a3449-9e0d-45a9-bcc0-518f55e45c8a&ids=5f2d329b-d59d-4112-b490-5114b830e34d&ids=bb966617-6c1f-4bb0-a1ed-ceb37ecade67&ids=05d11519-2b33-4742-aa87-3934632f2f2b&ids=39bfafe2-9628-434e-bd72-148051a47477&ids=481bea69-3cd5-45f3-8a52-2d4cc8fc8df7&ids=f95e407b-de69-416c-920c-6be8c9414862&ids=75940293-8fa6-47f9-ad5d-155b61933fdc&ids=e8e84ccf-f8a8-4551-9257-ef731d02116f&ids=e4991159-f088-4a2a-88b7-38d6ac47c6bc
```
```Shell
curl --remote-name --remote-header-name --request POST 'https://api.gdc.cancer.gov/data' --data @Payload
```
```Output
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
															 Dload  Upload   Total   Spent    Left  Speed
100 2563k    0 2562k  100   983   854k    327  0:00:03  0:00:03 --:--:--  776k
curl: Saved to filename 'gdc_download_20180830_132402.379282.tar.gz'
```

#### POST request with JSON payload

POST requests that carry a JSON payload must include the HTTP header `Content-Type: application/json`.

The payload is a string in the following format:

	{
	    "ids":[
	        "UUID1",
	        "UUID2",
					...
	        "UUID3"
	    ]
	}


where UUID# corresponds to the UUIDs of the files to be downloaded.

In this example we use `curl` to download a set of files from the GDC Legacy Archive; the payload is stored in a plain text file named `Payload`.


```Payload
{
    "ids":[
        "556e5e3f-0ab9-4b6c-aa62-c42f6a6cf20c",
        "e0de63e2-02f3-4309-9b24-69f4c24e85fc",
        "f1a06178-2ec2-4b06-83f3-3aedac332cfe",
        "11a8aca0-c8e6-4ff8-8ab6-fe18a1b8ba82",
        "69a69c84-00de-45ff-b397-fd2b6713ed4f",
        "9ec48233-395d-401e-b205-951c971f8dd4",
        "93129547-378c-4b69-b858-532abfff678e",
        "8d4277e9-a472-4590-886d-24dc2538ea65",
        "6733b412-56da-4f1c-a12b-ff804cb656d7",
        "a72eec98-c5e0-4866-8953-765780acb6c1",
        "e77b2294-1bdd-4fba-928a-d81d2622312f",
        "965e01fc-318e-4c02-a801-d6fad60bfae4",
        "21ad5409-fe0b-4728-97e4-15520b9fc287",
        "1a777521-277c-4aeb-baf1-66871a7c2d2a",
        "c13a3449-9e0d-45a9-bcc0-518f55e45c8a",
        "5f2d329b-d59d-4112-b490-5114b830e34d",
        "bb966617-6c1f-4bb0-a1ed-ceb37ecade67",
        "05d11519-2b33-4742-aa87-3934632f2f2b",
        "39bfafe2-9628-434e-bd72-148051a47477",
        "481bea69-3cd5-45f3-8a52-2d4cc8fc8df7",
        "f95e407b-de69-416c-920c-6be8c9414862",
        "75940293-8fa6-47f9-ad5d-155b61933fdc",
        "e8e84ccf-f8a8-4551-9257-ef731d02116f",
        "e4991159-f088-4a2a-88b7-38d6ac47c6bc"
    ]
}
```
```Shell
curl --remote-name --remote-header-name --request POST --header 'Content-Type: application/json' --data @request.txt 'https://api.gdc.cancer.gov/data'
```
```Output
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 2562k    0 2561k  100  1145   788k    352  0:00:03  0:00:03 --:--:--  788k
curl: Saved to filename 'gdc_download_20160701_011007.tar.gz'
```

### Downloading Controlled-access Files

To download controlled-access files, a valid authentication token must be passed to the GDC API using the `X-Auth-Token` HTTP header:

```shell
token=$(<gdc-token-text-file.txt)

curl --remote-name --remote-header-name --header "X-Auth-Token: $token" 'https://api.gdc.cancer.gov/data/0eccf79d-1f1e-4205-910f-8e126b08276e'
```
```Output
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 31.4M  100 31.4M    0     0   290k      0  0:01:50  0:01:50 --:--:--  172k
curl: Saved to filename 'ACOLD_p_TCGA_Batch17_SNP_N_GenomeWideSNP_6_A03_466078.tangent.copynumber.data.txt'
```

## Manifest endpoint

The `manifest` endpoint generates a download manifest file that can be used with the GDC Data Transfer Tool. The Data Transfer Tool is recommended for transferring large volumes of data. The GDC API can also generate a download manifest from a list of results that match a [Search and Retrieval](Search_and_Retrieval.md) query. To do this, append `&return_type=manifest` to the end of the query.

### Using the manifest endpoint

The `manifest` endpoint allows users to create a download manifest, which can be used with the GDC Data Transfer Tool to download a large volume of data. The `manifest` endpoint generates a manifest file from a comma-separated list of UUIDs.

```shell
curl --remote-name --remote-header-name 'https://api.gdc.cancer.gov/v0/manifest/ae9db773-78ab-48d0-972d-debe1bedd37d,3d815e6e-db97-419d-ad7f-dba4e4023b3e'
```
```Output
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   274  100   274    0     0   1042      0 --:--:-- --:--:-- --:--:--  1041
curl: Saved to filename 'gdc_manifest_20160428_234614.txt'
```

The `manifest` endpoint also supports HTTP POST requests in the same format as the `data` endpoint; see [above](#post-request-with-json-payload) for details.


### Using return_type=manifest

Alternatively, users can create a manifest by appending `&return_type=manifest` to a [Search and Retrieval](Search_and_Retrieval.md) query. In this example, we generate a download manifest for RNA-seq data files from solid tissue normal samples, that are part of the TCGA-KIRC project:

```Shell
curl --remote-name --remote-header-name 'https://api.gdc.cancer.gov/files?filters=%7B%22op%22%3A%22and%22%2C%22content%22%3A%5B%7B%22op%22%3A%22%3D%22%2C%22content%22%3A%7B%22field%22%3A%22experimental_strategy%22%2C%22value%22%3A%5B%22RNA-Seq%22%5D%7D%7D%2C%7B%22op%22%3A%22%3D%22%2C%22content%22%3A%7B%22field%22%3A%22cases.project.project_id%22%2C%22value%22%3A%5B%22TCGA-KIRC%22%5D%7D%7D%2C%7B%22op%22%3A%22%3D%22%2C%22content%22%3A%7B%22field%22%3A%22cases.samples.sample_type%22%2C%22value%22%3A%5B%22Solid+Tissue+Normal%22%5D%7D%7D%5D%7D&size=30000&return_type=manifest'
```
```Output
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 40663    0 40663    0     0  77109      0 --:--:-- --:--:-- --:--:-- 77306
curl: Saved to filename 'gdc_manifest.2016-06-28T13:26:33.850459.tsv'
```