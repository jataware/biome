import json

starting_sources = [
    {
        "name": "Genomic Data Commons",
        "initials": "GDC",
        "description": "The GDC Data Portal is a cohort-centric cancer genomics data platform supporting the data analysis workflow. It provides tools and data for cancer research.",
        "logo_url": "https://docs.gdc.cancer.gov/img/nih-header-logo-color.png",
        "datasets": [],
        "categories": ["genomics", "clinical"],
        "tags": ["human", "cancer"],
        "urls": {
            "home_page": "https://docs.gdc.cancer.gov/",
            "site_map": "",
            "data_landing": "https://portal.gdc.cancer.gov/",
            "git_repository": "",
            "git_org": "",
            "submission_portal": "https://portal.gdc.cancer.gov/submission/",
            "openapi_spec": "https://gdc.cancer.gov/developers/gdc-application-programming-interface-api",
        },
        "use_cases": [],
        "documentation": [
            {"name": "GDC Docs", "url": "https://docs.gdc.cancer.gov/"},
            {
                "name": "GDC API",
                "url": "https://gdc.cancer.gov/developers/gdc-application-programming-interface-api",
            },
            {
                "name": "GDC Data Transfer Tool",
                "url": "https://gdc.cancer.gov/access-data/gdc-data-transfer-tool",
            },
        ],
        "collections": [],
        "data_categories": [
            "projects",
            "cases",
            "mutations",
            "files",
            "genes",
            "annotations",
        ],
        "data_types": ["clinical", "biospecimen", "molecular"],
        "file_formats": ["JSON", "TSV"],
        "external_references": [],
        "access_type": "controlled",
        "capabilities": ["ui_case_search"],
        "data_use_limitations": "Authentication required for access to controlled access datasets.",
        "omics_methods": [],
        "contact": {"email": "", "name": ""},
        "metadata": {
            "scanned_uris": [
                "https://docs.gdc.cancer.gov/Data_Portal/Users_Guide/getting_started/"
            ]
        },
    },
    {
        "name": "Imaging Data Commons",
        "initials": "IDC",
        "description": "NCI Imaging Data Commons (IDC) is a cloud-based environment containing publicly available cancer imaging data co-located with analysis and exploration tools and resources. IDC is a node within the broader NCI Cancer Research Data Commons (CRDC) infrastructure that provides secure access to a large, comprehensive, and expanding collection of cancer research data.",
        "logo_url": "https://storage.googleapis.com/idc-prod-web-static-files/static/img/NIH_IDC_title.svg",
        "datasets": [],
        "categories": ["imaging"],
        "tags": ["human", "cancer"],
        "urls": {
            "home_page": "https://portal.imaging.datacommons.cancer.gov/",
            "site_map": "",
            "data_landing": "https://portal.imaging.datacommons.cancer.gov/explore/",
            "git_repository": "https://github.com/ImagingDataCommons/IDC-Tutorials",
            "git_org": "https://github.com/ImagingDataCommons",
            "submission_portal": "",
            "openapi_spec": "https://api.imaging.datacommons.cancer.gov/v1/swagger",
        },
        "use_cases": [
            "Explore metadata, visualize images and annotations, build cohorts from the data included in public TCIA collections",
            "Analyze TCIA public collections data on the cloud",
            "Use existing tools such as Google Colab, BigQuery, and DataStudio with the TCIA public collections data",
            "Perform complex queries against any of the DICOM attributes in the TCIA public collections",
            "Utilize other resources available in CRDC, such as CRDC Cloud Resources, for data analysis",
            "Quickly visualize specific images from TCIA public collections",
        ],
        "documentation": [
            {"name": "Downloading data", "url": "/data/downloading-data"},
            {
                "name": "Getting Started with IDC",
                "url": "/getting-started-with-idc",
            },
            {
                "name": "Google Colab",
                "url": "https://colab.research.google.com",
            },
            {
                "name": "Cancer Imaging Archive (TCIA)",
                "url": "https://www.cancerimagingarchive.net",
            },
            {
                "name": "Clinical Data Tutorial",
                "url": "https://github.com/ImagingDataCommons/IDC-Examples/blob/master/notebooks/clinical_data_intro.ipynb",
            },
            {
                "name": "Getting Started Tutorial Series",
                "url": "https://github.com/ImagingDataCommons/IDC-Tutorials/tree/master/notebooks/getting_started",
            },
            {
                "name": "DataStudio Dashboard",
                "url": "https://datastudio.google.com/reporting/ab96379c-e134-414f-8996-188e678f1b70/page/KHtxB",
            },
        ],
        "collections": ["case sets", "cohorts"],
        "data_categories": [
            "Cancer Imaging Archive (TCIA) collections",
            "HTAN and other pathology images",
        ],
        "data_types": ["Clinical data", "Imaging metadata"],
        "file_formats": ["DICOM"],
        "external_references": [
            {
                "name": "CRDC Cloud Resources",
                "base_url": "https://datacommons.cancer.gov",
            }
        ],
        "access_type": "open",
        "capabilities": ["ui_case_search"],
        "data_use_limitations": "IDC only hosts public datasets. It does not support access limitations, such as data embargoes or sequestration.",
        "omics_methods": [],
        "contact": {
            "email": "support+submissions@canceridc.dev",
            "name": "Cancer Imaging Data Commons",
        },
    },
    {
        "name": "Proteomic Data Commons",
        "initials": "PDC",
        "description": "The objectives of the National Cancer Institute’s Proteomic Data Commons (PDC) are to make cancer-related proteomic datasets easily accessible to the public, and facilitate direct multiomics integration in support of precision medicine through interoperability with accompanying data resources (genomic and medical image datasets). The PDC was developed to advance our understanding of how proteins help to shape the risk, diagnosis, development, progression, and treatment of cancer. In-depth analysis of proteomic data allows us to study both how and why cancer develops and to devise ways of personalizing treatment for patients using precision medicine. The PDC is one of several repositories within the NCI Cancer Research Data Commons (CRDC), a secure cloud-based infrastructure featuring diverse data sets and innovative analytic tools – all designed to advance data-driven scientific discovery. The CRDC enables researchers to link proteomic data with other data sets (e.g., genomic and imaging data) and to submit, collect, analyze, store, and share data throughout the cancer data ecosystem.",
        "logo_url": "https://pdc.cancer.gov/pdc/assets/css/images/PDC-NIH-Logo.png",
        "categories": ["genomics", "clinical", "imaging"],
        "tags": ["human", "cancer"],
        "urls": {
            "home_page": "https://pdc.cancer.gov",
            "submission_portal": "https://pdc.cancer.gov/submission/",
            "site_map": "https://pdc.cancer.gov/sitemap/",
            "data_landing": "https://pdc.cancer.gov/pdc/",
        },
        "use_cases": [],
        "documentation": [],
        "collections": ["cohorts", "projects"],
        "data_categories": [
            "biospecimen",
            "clinical",
            "proteomic",
            "genomic",
            "medical image datasets",
        ],
        "data_types": [],
        "file_formats": [],
        "external_references": [
            {
                "name": "NCI Cancer Research Data Commons (CRDC)",
                "base_url": "https://datacommons.cancer.gov",
            }
        ],
        "access_type": "controlled",
        "capabilities": ["workspaces", "cohorts", "http_api"],
        "data_use_limitations": "",
        "omics_methods": ["proteomics"],
        "contact": {"email": "PDCHelpDesk@mail.nih.gov"},
        "metadata": {"scanned_uris": ["https://pdc.cancer.gov/pdc/about"]},
    },
    {
    "name":"CDC Open Data",
    "initials": None,
    "description":"Centers for Disease Control and Prevention's open data portal providing various datasets, including COVID-19 datasets, disability status and types data, and state-based motor vehicle data.",
    "logo_url":"https://data.cdc.gov/api/assets/471B2483-2373-4083-B711-051170D91D8B",
    "datasets":[
        "COVID-19 Public Data Sets",
        "Disability Status and Types Data",
        "State-based Motor Vehicle Data"
    ],
    "categories":[
        "clinical"
    ],
    "tags":[
        "human"
    ],
    "urls":{
        "home_page":"https://data.cdc.gov/",
        "git_repository":"https://github.com/CDCgov"
    },
    "use_cases":[
        
    ],
    "documentation":[
        {
            "name":"BACTFACTS Interactive Dashboard",
            "url":"https://www.cdc.gov/abcs/bact-facts-interactive-dashboard.html"
        },
        {
            "name":"HAICViz",
            "url":"https://www.cdc.gov/hai/eip/haicviz.html"
        },
        {
            "name":"NCHHSTP AtlasPlus",
            "url":"https://www.cdc.gov/nchhstp/atlas/index.htm"
        },
        {
            "name":"CDC COVID-19 Data Tracker Vaccination Data",
            "url":"https://data.cdc.gov/browse?q=izdl&sortBy=relevance"
        }
    ],
    "collections":[
        
    ],
    "data_categories":[
        
    ],
    "data_types":[
        "data sets"
    ],
    "file_formats":[
        
    ],
    "external_references":[
        
    ],
    "access_type":"open",
    "capabilities":[
        "ui_case_search"
    ],
    "oms_methods":[
        
    ],
    "contact":{
        "email": None
    },
    "source_url":"https://data.cdc.gov/"
    },
]


def seed(es_client, target_index):
    print(f"Checking if {target_index} should be seeded.")
    all_query = {"query": {"match_all": {}}}

    results = es_client.search(index=target_index, body=all_query)
    count = results["hits"]["total"]["value"]

    if count == 0:
        print("Need to seed index as it is empty.")
        if target_index == "datasources":
            print("Seeding datasources")
            for source in starting_sources:
                body = json.dumps(source)
                es_client.index(index=target_index, body=body)
    else:
        print("No need to seed as it is not empty.")
