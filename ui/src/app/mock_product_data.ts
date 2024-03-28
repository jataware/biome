
export const ProductService = {
  getProductsData() {
    return [
      {
        id: '1000',
        name: 'NCI Genomic Data Commons',
        initials: "GDC",
        description: 'NCI\'s Genomic Data Commons (GDC) provides the cancer research community with a unified repository and cancer knowledge base that enables data sharing across cancer genomic studies in support of precision medicine. GDC enables access to data from various projects, genes, and mutations.',
        // TODO -> icon
        logo_url: "https://gdc.cancer.gov/sites/all/themes/gdc_bootstrap/logo.png",
        "datasets": [
          "Standardized data from cancer studies"
        ],
        "categories": [
          "genomics"
        ],
        "tags": [
          "human",
          "genetics",
          "cancer"
        ],
        "urls": {
          "homepage": "https://gdc.cancer.gov",
          "sitemap": "",
          "data_landing": "https://portal.gdc.cancer.gov",
          "git_repository": "https://github.com/NCI-GDC",
          "git_org": "https://github.com/NCIP",
          "submission_portal": "https://portal.gdc.cancer.gov/submission",
          "openapi_spec": "https://docs.gdc.cancer.gov/API/Users_Guide/Getting_Started"
        },
        "use_cases": [
          "Standardized data access",
          "Data analysis and visualization",
          "Gene and variant level data analysis"
        ],
        "documentation": [
          {
            "name": "GDC Data Portal User\u2019s Guide",
            "url": "https://docs.gdc.cancer.gov/Data_Portal/Users_Guide/getting_started"
          },
          {
            "name": "GDC Data Transfer Tool User's Guide",
            "url": "http://docs.gdc.cancer.gov/Data_Transfer_Tool/Users_Guide/Getting_Started"
          },
          {
            "name": "GDC Application Programming Interface (API) User's Guide",
            "url": "https://docs.gdc.cancer.gov/API/Users_Guide/Getting_Started"
          }
        ],
        "collections": [
          "case sets",
          "projects"
        ],
        "data_categories": [
          "Clinical",
          "Biospecimen",
          "Analytical Data"
        ],
        "data_types": [
          "Genomic Data",
          "Bioinformatic Pipelines"
        ],
        "file_formats": [
          "json",
          "tsv",
          "bam",
          "vcf",
          "xlsx"
        ],
        "external_references": [
          {
            "name": "GDC Documentation",
            "base_url": "https://docs.gdc.cancer.gov/"
          },
          {
            "name": "GDC API",
            "base_url": "https://docs.gdc.cancer.gov/API/Users_Guide/Getting_Started"
          }
        ],
        "access_type": "mixed",
        "capabilities": [
          "workspaces",
          "http_api",
          "ui_case_search",
          "ui_organ_search"
        ],
        "data_use_limitations": "Access to some datasets may be restricted due to patient confidentiality.",
        "omics_methods": [
          "Genomics",
          "Bioinformatics"
        ],
        "contact": {
          "email": "support@nci-gdc.datacommons.io",
          "name": "GDC Help Desk"
        },

        scraped: true,

        price: 65,
        category: 'liver',
        quantity: 24,
        inventoryStatus: 'Verified',
        rating: 3,

        icon: 'bolt'
      },
      {
        id: '1001',
        // code: 'nvklal433',
        name: 'Cancer Research Data Commons',

        // "name": "National Cancer Institute Center for Biomedical Informatics and Information Technology",
        "initials": "CBIIT",
        "description": "The CBIIT supports data sharing and science informatics related to cancer research. It offers guidance on data management and sharing policy through its Office of Data Sharing (ODS).",
        "logo_url": "https://datacommons.cancer.gov/themes/custom/crdc_foundation/images/logos/CRDC-logo.svg",
        "datasets": [
          "NCI-funded research datasets",
          "International Cancer Proteogenome Consortium (ICPC) datasets"
        ],
        "categories": [
          "clinical",
          "genomics",
          "imaging"
        ],
        "tags": [
          "human",
          "genetics",
          "cancer"
        ],
        "urls": {
          "homepage": "https://datacommons.cancer.gov/",
          "data_landing": "https://datacommons.cancer.gov/explore",
          "submission_portal": "https://datacommons.cancer.gov/submit",
        },
        "use_cases": [
          "Data Management and Sharing Plan guidance",
          "Data submissions to CRDC data commons",
          "Access and analysis of data within CRDC",
          "Comparative analysis of cancer-related datasets",
          "Secure cloud workspace for bringing and analyzing own data"
        ],
        "documentation": [
          {
            "name": "Data Management and Sharing Policy Guidelines",
            "url": "https://datascience.cancer.gov/data-sharing/policies"
          },
          {
            "name": "NIH Scientific Data Sharing Repository Options",
            "url": "https://sharing.nih.gov/data-management-and-sharing-policy/sharing-scientific-data/repositories-for-sharing-scientific-data"
          },
          {
            "name": "NIH Allowable DMS Costs",
            "url": "https://sharing.nih.gov/data-management-and-sharing-policy/planning-and-budgeting-for-data-management-and-sharing/budgeting-for-data-management-sharing#allowable-costs"
          },
          {
            "name": "Submitting data to CRDC Data Commons",
            "url": "https://datacommons.cancer.gov/data"
          }
        ],
        "collections": [
          "case sets",
          "cohorts",
          "projects"
        ],
        "data_categories": [
          "genomic",
          "proteomic",
          "imaging",
          "canine",
          "Biological",
          "Biospecimen",
          "Clinical",
          "Data File",
          "Metadata",
          "Processed"
        ],
        "data_types": [
          "Proteogenomics",
          "Genomic analysis",
          "Molecular data",
          "Clinical data"
        ],
        "file_formats": [
          "json",
          "tsv",
          "bam",
          "tif",
          "png"
        ],
        "external_references": [],
        "access_type": "mixed",
        "capabilities": [
          "workspaces",
          "http_api",
          "ui_case_search",
          "ui_organ_search"
        ],
        "omics_methods": [
          "Genomics",
          "Proteomics",
          "Imaging"
        ],

        "data_use_limitations": "Data use limitations are subject to the policies outlined by NCI's Office of Data Sharing (ODS).",
        "contact": {
          "email": "NCIinfo@nih.gov",
          "name": "National Cancer Institute"
        },

        image: 'black-watch.jpg',
        price: 72,
        category: 'kidney',
        quantity: 61,
        inventoryStatus: 'Verified',
        rating: 2,
        icon: 'apple'
      },
      {
        id: '1002',
        // code: 'zz21cz3c1',


        "name": "NCI Proteomics Data Commons",
        "initials": "PDC",
        "description": "PDC is a fully open-access cancer proteomic dataportal that provides access to highly curated human cancer multi'omics data.",
        "logo_url": "assets/css/images/PDC-NIH-Logo.png",
        "datasets": [],
        "categories": [
          "clinical",
          "genomics"
        ],
        "tags": [
          "human",
          "cancer",
          "genetics"
        ],
        "urls": {
          "homepage": "/",
          "sitemap": "",
          "data_landing": "",
          "git_repository": "",
          "git_org": "",
          "submission_portal": "/submitDataNavBar"
        },
        "use_cases": [],
        "documentation": [
          {
            "name": "Data Dictionary",
            "url": "/pdc/data-dictionary/data-dictionary-graph"
          }
        ],
        "collections": [
          "case sets",
          "cohorts",
          "projects"
        ],
        "data_types": [
          "Case",
          "Program",
          "Project",
          "Study",
          "Gene",
          "Aliquot",
          "Analyte",
          "Portion",
          "Sample",
          "Demographic",
          "Diagnosis",
          "Family History",
          "Follow-Up",
          "Exposure",
          "Treatment",
          "File",
          "Aliquot Run Metadata",
          "Protocol",
          "Study Run Metadata",
          "Workflow Metadata",
          "Publication",
          "Gene Abundance"
        ],
        "file_formats": [],
        "external_references": [
          {
            "name": "NCI Thesaurus",
            "base_url": "https://ncit.nci.nih.gov/ncitbrowser/pages/concept_details.jsf?dictionary=NCI%20Thesaurus&code="
          }
        ],
        "access_type": "open",
        "capabilities": [],
        "data_use_limitations": "",
        "omics_methods": [],
        "contact": {
          "email": "PDCHelpDesk@mail.nih.gov",
          "name": "PDC Help Desk"
        },

        scraped: true,
        image: 'blue-band.jpg',
        price: 79,
        category: 'lung',
        quantity: 2,
        inventoryStatus: 'LOW',
        rating: 1,
        icon: 'bitcoin'
      },
      {
        id: '1003',
        // code: '244wgerg2',

        "name": "Clinical and Translational Data Commons",
        "initials": "CTDC",
        "description": "The Clinical and Translational Data Commons (CTDC) is being developed to accelerate scientific discoveries that make an impact on cancer outcomes to help people live longer, healthier lives. The CTDC supports cancer research by sharing NCI-funded clinical studies, with features including a Data Exploration dashboard, multiple data types including clinical (PDF, CSV) and molecular/sequencing data (bam/bai, vcf, tsv), data harmonization, data visualization and analysis on the cloud via Seven Bridges Cancer Genomics Cloud, developer resources including a Graphical user interface (GUI) and an Application Programming Interface (API), and a federated identity management system.",
        "logo_url": "https://datacommons.cancer.gov/themes/custom/crdc_foundation/images/logos/CRDC-logo-mobile.svg",

        // "logo_url": "/assets/images/biobank-logo.svg",

        "datasets": [
          "Cancer Moonshot Biobank (first release Fall 2023)"
        ],
        "categories": [
          "clinical",
          "genomics"
        ],
        "tags": [
          "human",
          "cancer"
        ],
        "urls": {
          "homepage": "https://datacommons.cancer.gov/",
          "data_landing": "/explore/data-commons"
        },
        "use_cases": [],
        "documentation": [
          {
            "name": "Seven Bridges Cancer Genomics Cloud",
            "url": "https://sevenbridges.com/cancer-genomics-cloud/"
          }
        ],
        "data_categories": [
          "Clinical data and reports",
          "Molecular findings and sequence annotation"
        ],
        "data_types": [
          "txt",
          "pdf",
          "vcf",
          "bam"
        ],
        "file_formats": [
          "txt",
          "pdf",
          "vcf",
          "bam",
          "bai",
          "tsv"
        ],

        "external_references": [
          {
            "name": "Biorepositories and Biospecimen Research Branch",
            "base_url": "https://biospecimens.cancer.gov"
          },
          {
            "name": "National Cancer Institute",
            "base_url": "https://www.cancer.gov"
          },
          {
            "name": "National Institutes of Health",
            "base_url": "https://www.nih.gov"
          },
          {
            "name": "U.S. Department of Health and Human Services",
            "base_url": "https://www.hhs.gov"
          },
          {
            "name": "USA.gov",
            "base_url": "https://www.usa.gov"
          }
        ],

        "access_type": "mixed",
        "capabilities": [
          "http_api",
          "ui_case_search"
        ],
        "data_use_limitations": "The data use limitations are not provided in the provided HTML snippet. This information would typically be detailed in a terms of service or use conditions document.",
        "omics_methods": [
          "genomics"
        ],
        "contact": {
          "email": "1-800-4-CANCER",
          "name": "Cancer Information Service"
        },

        image: 'blue-t-shirt.jpg',
        price: 29,
        category: 'bone',
        quantity: 25,
        inventoryStatus: 'INSTOCK',
        rating: 1,
        icon: 'compass'
      },
      {
        id: '1004',
        // code: 'h456wer53',
        name: 'Imaging Data Commons (IDC)',

        "initials": "IDC",
        "description": "A guide providing information on how to interact with the Imaging Data Commons portal and utilize its various features. It includes guidance on downloading data, submitting data to IDC, and understanding the costs of using cloud resources. It also explains IDC's purpose, status, the data available, how to acknowledge IDC, and the differences between IDC and TCIA.",
        "logo_url": "https://storage.googleapis.com/idc-prod-web-static-files/static/img/NIH_IDC_title.svg",
        "datasets": [],
        "categories": [
          "imaging"
        ],
        "tags": [
          "human",
          "cancer"
        ],
        "urls": {
          "homepage": "https://portal.imaging.datacommons.cancer.gov/",
          "sitemap": "",
          "data_landing": "",
          "git_repository": "https://github.com/ImagingDataCommons/IDC-Examples",
          "git_org": "",
          "submission_portal": "",
          "openapi_spec": "https://api.imaging.datacommons.cancer.gov/v1/swagger"
        },
        "use_cases": [
          "Explore metadata, visualize images and annotations, build cohorts from the data included in public TCIA collections",
          "Analyze TCIA public collections data on the cloud",
          "Use existing tools such as Google Colab, BigQuery, and DataStudio with the TCIA public collections data",
          "Perform complex queries against any of the DICOM attributes in the TCIA public collections",
          "Utilize other resources available in CRDC, such as CRDC Cloud Resources, for data analysis",
          "Quickly visualize specific images from TCIA public collections"
        ],
        "documentation": [
          {
            "name": "Downloading data",
            "url": "https://learn.canceridc.dev/data/downloading-data"
          },
          {
            "name": "Getting Started with IDC",
            "url": "https://learn.canceridc.dev/getting-started-with-idc"
          },
          {
            "name": "Google Colab",
            "url": "https://colab.research.google.com"
          },
          {
            "name": "Cancer Imaging Archive (TCIA)",
            "url": "https://www.cancerimagingarchive.net"
          },
          {
            "name": "Clinical Data Tutorial",
            "url": "https://github.com/ImagingDataCommons/IDC-Examples/blob/master/notebooks/clinical_data_intro.ipynb"
          },
          {
            "name": "Getting Started Tutorial Series",
            "url": "https://github.com/ImagingDataCommons/IDC-Tutorials/tree/master/notebooks/getting_started"
          },
          {
            "name": "DataStudio Dashboard",
            "url": "https://datastudio.google.com/reporting/ab96379c-e134-414f-8996-188e678f1b70/page/KHtxB"
          }
        ],
        "collections": [
          "case sets",
          "cohorts"
        ],
        "data_categories": [
          "Cancer Imaging Archive (TCIA) collections",
          "HTAN and other pathology images"
        ],
        "data_types": [
          "Clinical data",
          "Imaging metadata"
        ],
        "file_formats": [
          "DICOM"
        ],
        "external_references": [
          {
            "name": "CRDC Cloud Resources",
            "base_url": "https://datacommons.cancer.gov"
          }
        ],
        "access_type": "open",
        "capabilities": [
          "ui_case_search"
        ],
        "data_use_limitations": "IDC only hosts public datasets. It does not support access limitations, such as data embargoes or sequestration.",
        "omics_methods": [],
        "contact": {
          "email": "support+submissions@canceridc.dev",
          "name": ""
        },

        image: 'bracelet.jpg',
        price: 15,
        category: 'skin',
        quantity: 73,
        inventoryStatus: 'INSTOCK',
        rating: 3,
        icon: 'eject'
      },

      {
        id: '1005',
        // code: 'av2231fwg',

        "name": "Cancer Data Service",
        "initials": "CDS",
        "description": "The Cancer Data Service (CDS) is one of several data commons within the Cancer Research Data Commons (CRDC). CDS provides data storage and sharing capabilities for NCI-funded studies. It currently hosts a variety of data types from NCI projects such as the Human Tumor Atlas Network (HTAN), Division of Cancer Control and Population Sciences (DCCPS), Childhood Cancer Data Initiative (CCDI), and data from independent research projects. The CDS is home to both open and controlled access data, but the CDS Portal is accessible for users to search and browse with no login. Users can see if the CDS has data of interest before requesting access.",
        "logo_url": "/themes/custom/crdc_foundation/images/logos/CRDC-logo-mobile.svg",
        "datasets": [
          "Childhood Cancer Data Initiative (CCDI): Genomic Analysis in Pediatric Malignancies - phs002430.v1.p1",
          "DCCPS CIDR: The Role of Rare Coding Variation in Prostate Cancer in Men of African Ancestry - RESPOND Project 2 \u2013 phs002637.v1.p1",
          "CCDI: MCI - Molecular Characterization Initiative \u2013 phs002790.v5.p1",
          "TCGA WGS Variants Across 18 Cancer Types - phs003155.v1.p1"
        ],
        "categories": [
          "genomics",
          "imaging"
        ],
        "tags": [
          "human",
          "genetics",
          "cancer"
        ],
        "urls": {
          "homepage": "https://dataservice.datacommons.cancer.gov/#/home",
          "data_landing": "https://dataservice.datacommons.cancer.gov/#/submit",
          "submission_portal": "https://dataservice.datacommons.cancer.gov/#/submit"
        },
        "use_cases": [
          "Data storage and sharing for NCI-funded studies",
          "Search and browse data of interest before requesting access"
        ],
        "documentation": [
          {
            "name": "CDS User Guide",
            "url": "https://docs.cancergenomicscloud.org/v1.0/page/cds-data"
          },
          {
            "name": "CDS portal's Data Submission page",
            "url": "https://dataservice.datacommons.cancer.gov/#/submit"
          },
          {
            "name": "CDS Access and Analysis page",
            "url": "https://dataservice.datacommons.cancer.gov/#/analysis"
          }
        ],
        "collections": [
          "cohorts"
        ],
        "data_categories": [
          "open access",
          "controlled access"
        ],
        "file_formats": [
          "not specified"
        ],
        "external_references": [
          {
            "name": "dbGaP",
            "base_url": "https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin"
          }
        ],
        "access_type": "mixed",
        "capabilities": [
          "http_api",
          "ui_case_search"
        ],
        "data_use_limitations": "The CDS is home to both open and controlled access data. Open-access data are publicly accessible; no approval is required. For controlled-access data, users must request access and obtain approval.",
        "omics_methods": [
          "genomic",
          "imaging"
        ],
        "contact": {
          "email": "CDSHelpDesk@mail.nih.gov"
        },

        image: 'brown-purse.jpg',
        price: 120,
        category: 'bone',
        quantity: 0,
        inventoryStatus: 'OUT',
        rating: 2,
        icon: 'moon'
      },

      // {
      //   id: '1006',
      //   code: 'bib36pfvm',
      //   name: 'Human Tumor Atlas Network (HTAN)',
      //   description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      //   image: 'chakra-bracelet.jpg',
      //   price: 32,
      //   category: 'thyroid',
      //   quantity: 5,
      //   inventoryStatus: 'LOWSTOCK',
      //   rating: 3,
      //   icon: 'slack'
      // },
      // {
      //   id: '1007',
      //   code: 'mbvjkgip5',
      //   name: 'ACA',
      //   description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      //   image: 'galaxy-earrings.jpg',
      //   price: 34,
      //   category: 'pancreas',
      //   quantity: 23,
      //   inventoryStatus: 'INSTOCK',
      //   rating: 2,
      //   icon: 'shield'
      // },
      {
        id: '1008',
        code: 'vbb124btr',
        name: 'The Cancer Imaging Archive (TCIA)',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'game-controller.jpg',
        price: 99,
        category: 'Electronics',
        quantity: 2,
        inventoryStatus: 'LOWSTOCK',
        rating: 1,
        icon: 'telegram'
      },
      {
        id: '1009',
        code: 'cm230f032',
        name: 'The Cancer Genome Atlas (TCGA)',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'gaming-set.jpg',
        price: 299,
        category: 'Electronics',
        quantity: 63,
        inventoryStatus: 'INSTOCK',
        rating: 3,
        icon: 'wifi'
      },
      {
        id: '1010',
        code: 'plb34234v',
        name: 'Human Cancer Model Initiative (HCMI)',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'gold-phone-case.jpg',
        price: 24,
        category: 'Accessories',
        quantity: 0,
        inventoryStatus: 'OUTOFSTOCK',
        rating: 2,
        icon: 'youtube'
      },
      {
        id: '1011',
        code: '4920nnc2d',
        name: 'Foundation Medicine (FM)',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'green-earbuds.jpg',
        price: 89,
        category: 'Electronics',
        quantity: 23,
        inventoryStatus: 'INSTOCK',
        rating: 3,
        icon: 'truck'
      },
      {
        id: '1012',
        code: '250vm23cc',
        name: 'Multiple Myeloma Research Foundation (MMRF)',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'green-t-shirt.jpg',
        price: 49,
        category: 'Clothing',
        quantity: 74,
        inventoryStatus: 'INSTOCK',
        rating: 2,
        icon: 'video'
      },
      // {
      //   id: '1013',
      //   code: 'fldsmn31b',
      //   name: 'Grey T-Shirt',
      //   description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      //   image: 'grey-t-shirt.jpg',
      //   price: 48,
      //   category: 'Clothing',
      //   quantity: 0,
      //   inventoryStatus: 'OUTOFSTOCK',
      //   rating: 3
      // },
      // {
      //   id: '1014',
      //   code: 'waas1x2as',
      //   name: 'Headphones',
      //   description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      //   image: 'headphones.jpg',
      //   price: 175,
      //   category: 'Electronics',
      //   quantity: 8,
      //   inventoryStatus: 'LOWSTOCK',
      //   rating: 5
      // },
      // {
      //   id: '1015',
      //   code: 'vb34btbg5',
      //   name: 'Light Green T-Shirt',
      //   description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      //   image: 'light-green-t-shirt.jpg',
      //   price: 49,
      //   category: 'Clothing',
      //   quantity: 34,
      //   inventoryStatus: 'INSTOCK',
      //   rating: 4
      // },
      // {
      //   id: '1016',
      //   code: 'k8l6j58jl',
      //   name: 'Lime Band',
      //   description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      //   image: 'lime-band.jpg',
      //   price: 79,
      //   category: 'Lung',
      //   quantity: 12,
      //   inventoryStatus: 'INSTOCK',
      //   rating: 3
      // },
      // {
      //   id: '1017',
      //   code: 'v435nn85n',
      //   name: 'Mini Speakers',
      //   description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      //   image: 'mini-speakers.jpg',
      //   price: 85,
      //   category: 'Clothing',
      //   quantity: 42,
      //   inventoryStatus: 'INSTOCK',
      //   rating: 4
      // },
      // {
      //   id: '1018',
      //   code: '09zx9c0zc',
      //   name: 'Painted Phone Case',
      //   description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      //   image: 'painted-phone-case.jpg',
      //   price: 56,
      //   category: 'Accessories',
      //   quantity: 41,
      //   inventoryStatus: 'INSTOCK',
      //   rating: 5
      // },
      // {
      //   id: '1019',
      //   code: 'mnb5mb2m5',
      //   name: 'Pink Band',
      //   description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      //   image: 'pink-band.jpg',
      //   price: 79,
      //   category: 'Lung',
      //   quantity: 63,
      //   inventoryStatus: 'INSTOCK',
      //   rating: 4
      // },
      // {
      //   id: '1020',
      //   code: 'r23fwf2w3',
      //   name: 'Pink Purse',
      //   description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      //   image: 'pink-purse.jpg',
      //   price: 110,
      //   category: 'Accessories',
      //   quantity: 0,
      //   inventoryStatus: 'OUTOFSTOCK',
      //   rating: 4
      // },
      // {
      //   id: '1021',
      //   code: 'pxpzczo23',
      //   name: 'Purple Band',
      //   description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      //   image: 'purple-band.jpg',
      //   price: 79,
      //   category: 'Lung',
      //   quantity: 6,
      //   inventoryStatus: 'LOWSTOCK',
      //   rating: 3
      // },
      // {
      //   id: '1022',
      //   code: '2c42cb5cb',
      //   name: 'Purple Gemstone Necklace',
      //   description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      //   image: 'purple-gemstone-necklace.jpg',
      //   price: 45,
      //   category: 'Accessories',
      //   quantity: 62,
      //   inventoryStatus: 'INSTOCK',
      //   rating: 4
      // },
      // {
      //   id: '1023',
      //   code: '5k43kkk23',
      //   name: 'Purple T-Shirt',
      //   description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      //   image: 'purple-t-shirt.jpg',
      //   price: 49,
      //   category: 'Clothing',
      //   quantity: 2,
      //   inventoryStatus: 'LOWSTOCK',
      //   rating: 5
      // },
      // {
      //   id: '1024',
      //   code: 'lm2tny2k4',
      //   name: 'Shoes',
      //   description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      //   image: 'shoes.jpg',
      //   price: 64,
      //   category: 'Clothing',
      //   quantity: 0,
      //   inventoryStatus: 'INSTOCK',
      //   rating: 4
      // },
      // {
      //   id: '1025',
      //   code: 'nbm5mv45n',
      //   name: 'Sneakers',
      //   description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      //   image: 'sneakers.jpg',
      //   price: 78,
      //   category: 'Clothing',
      //   quantity: 52,
      //   inventoryStatus: 'INSTOCK',
      //   rating: 4
      // },
      // {
      //   id: '1026',
      //   code: 'zx23zc42c',
      //   name: 'Teal T-Shirt',
      //   description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      //   image: 'teal-t-shirt.jpg',
      //   price: 49,
      //   category: 'Clothing',
      //   quantity: 3,
      //   inventoryStatus: 'LOWSTOCK',
      //   rating: 3
      // },
      // {
      //   id: '1027',
      //   code: 'acvx872gc',
      //   name: 'Yellow Earbuds',
      //   description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      //   image: 'yellow-earbuds.jpg',
      //   price: 89,
      //   category: 'Electronics',
      //   quantity: 35,
      //   inventoryStatus: 'INSTOCK',
      //   rating: 3
      // },
      // {
      //   id: '1028',
      //   code: 'tx125ck42',
      //   name: 'Yoga Mat',
      //   description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      //   image: 'yoga-mat.jpg',
      //   price: 20,
      //   category: 'Lung',
      //   quantity: 15,
      //   inventoryStatus: 'INSTOCK',
      //   rating: 5
      // },
      // {
      //   id: '1029',
      //   code: 'gwuby345v',
      //   name: 'Yoga Set',
      //   description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
      //   image: 'yoga-set.jpg',
      //   price: 20,
      //   category: 'Lung',
      //   quantity: 25,
      //   inventoryStatus: 'INSTOCK',
      //   rating: 8
      // }
    ];
  },

  getProductsWithOrdersData() {
    return [
      {
        id: '1000',
        code: 'f230fh0g3',
        name: 'Bamboo Watch',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'bamboo-watch.jpg',
        price: 65,
        category: 'Accessories',
        quantity: 24,
        inventoryStatus: 'INSTOCK',
        rating: 5,
        orders: [
          {
            id: '1000-0',
            productCode: 'f230fh0g3',
            date: '2020-09-13',
            amount: 65,
            quantity: 1,
            customer: 'David James',
            status: 'PENDING'
          },
          {
            id: '1000-1',
            productCode: 'f230fh0g3',
            date: '2020-05-14',
            amount: 130,
            quantity: 2,
            customer: 'Leon Rodrigues',
            status: 'DELIVERED'
          },
          {
            id: '1000-2',
            productCode: 'f230fh0g3',
            date: '2019-01-04',
            amount: 65,
            quantity: 1,
            customer: 'Juan Alejandro',
            status: 'RETURNED'
          },
          {
            id: '1000-3',
            productCode: 'f230fh0g3',
            date: '2020-09-13',
            amount: 195,
            quantity: 3,
            customer: 'Claire Morrow',
            status: 'CANCELLED'
          }
        ]
      },
      {
        id: '1001',
        code: 'nvklal433',
        name: 'Black Watch',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'black-watch.jpg',
        price: 72,
        category: 'Accessories',
        quantity: 61,
        inventoryStatus: 'INSTOCK',
        rating: 4,
        orders: [
          {
            id: '1001-0',
            productCode: 'nvklal433',
            date: '2020-05-14',
            amount: 72,
            quantity: 1,
            customer: 'Maisha Jefferson',
            status: 'DELIVERED'
          },
          {
            id: '1001-1',
            productCode: 'nvklal433',
            date: '2020-02-28',
            amount: 144,
            quantity: 2,
            customer: 'Octavia Murillo',
            status: 'PENDING'
          }
        ]
      },
      {
        id: '1002',
        code: 'zz21cz3c1',
        name: 'Blue Band',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'blue-band.jpg',
        price: 79,
        category: 'Lung',
        quantity: 2,
        inventoryStatus: 'LOWSTOCK',
        rating: 3,
        orders: [
          {
            id: '1002-0',
            productCode: 'zz21cz3c1',
            date: '2020-07-05',
            amount: 79,
            quantity: 1,
            customer: 'Stacey Leja',
            status: 'DELIVERED'
          },
          {
            id: '1002-1',
            productCode: 'zz21cz3c1',
            date: '2020-02-06',
            amount: 79,
            quantity: 1,
            customer: 'Ashley Wickens',
            status: 'DELIVERED'
          }
        ]
      },
      {
        id: '1003',
        code: '244wgerg2',
        name: 'Blue T-Shirt',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'blue-t-shirt.jpg',
        price: 29,
        category: 'Clothing',
        quantity: 25,
        inventoryStatus: 'INSTOCK',
        rating: 5,
        orders: []
      },
      {
        id: '1004',
        code: 'h456wer53',
        name: 'Bracelet',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'bracelet.jpg',
        price: 15,
        category: 'Accessories',
        quantity: 73,
        inventoryStatus: 'INSTOCK',
        rating: 4,
        orders: [
          {
            id: '1004-0',
            productCode: 'h456wer53',
            date: '2020-09-05',
            amount: 60,
            quantity: 4,
            customer: 'Mayumi Misaki',
            status: 'PENDING'
          },
          {
            id: '1004-1',
            productCode: 'h456wer53',
            date: '2019-04-16',
            amount: 2,
            quantity: 30,
            customer: 'Francesco Salvatore',
            status: 'DELIVERED'
          }
        ]
      },
      {
        id: '1005',
        code: 'av2231fwg',
        name: 'Brown Purse',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'brown-purse.jpg',
        price: 120,
        category: 'Accessories',
        quantity: 0,
        inventoryStatus: 'OUTOFSTOCK',
        rating: 4,
        orders: [
          {
            id: '1005-0',
            productCode: 'av2231fwg',
            date: '2020-01-25',
            amount: 120,
            quantity: 1,
            customer: 'Isabel Sinclair',
            status: 'RETURNED'
          },
          {
            id: '1005-1',
            productCode: 'av2231fwg',
            date: '2019-03-12',
            amount: 240,
            quantity: 2,
            customer: 'Lionel Clifford',
            status: 'DELIVERED'
          },
          {
            id: '1005-2',
            productCode: 'av2231fwg',
            date: '2019-05-05',
            amount: 120,
            quantity: 1,
            customer: 'Cody Chavez',
            status: 'DELIVERED'
          }
        ]
      },
      {
        id: '1006',
        code: 'bib36pfvm',
        name: 'Chakra Bracelet',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'chakra-bracelet.jpg',
        price: 32,
        category: 'Accessories',
        quantity: 5,
        inventoryStatus: 'LOWSTOCK',
        rating: 3,
        orders: [
          {
            id: '1006-0',
            productCode: 'bib36pfvm',
            date: '2020-02-24',
            amount: 32,
            quantity: 1,
            customer: 'Arvin Darci',
            status: 'DELIVERED'
          },
          {
            id: '1006-1',
            productCode: 'bib36pfvm',
            date: '2020-01-14',
            amount: 64,
            quantity: 2,
            customer: 'Izzy Jones',
            status: 'PENDING'
          }
        ]
      },
      {
        id: '1007',
        code: 'mbvjkgip5',
        name: 'Galaxy Earrings',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'galaxy-earrings.jpg',
        price: 34,
        category: 'Accessories',
        quantity: 23,
        inventoryStatus: 'INSTOCK',
        rating: 5,
        orders: [
          {
            id: '1007-0',
            productCode: 'mbvjkgip5',
            date: '2020-06-19',
            amount: 34,
            quantity: 1,
            customer: 'Jennifer Smith',
            status: 'DELIVERED'
          }
        ]
      },
      {
        id: '1008',
        code: 'vbb124btr',
        name: 'Game Controller',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'game-controller.jpg',
        price: 99,
        category: 'Electronics',
        quantity: 2,
        inventoryStatus: 'LOWSTOCK',
        rating: 4,
        orders: [
          {
            id: '1008-0',
            productCode: 'vbb124btr',
            date: '2020-01-05',
            amount: 99,
            quantity: 1,
            customer: 'Jeanfrancois David',
            status: 'DELIVERED'
          },
          {
            id: '1008-1',
            productCode: 'vbb124btr',
            date: '2020-01-19',
            amount: 198,
            quantity: 2,
            customer: 'Ivar Greenwood',
            status: 'RETURNED'
          }
        ]
      },
      {
        id: '1009',
        code: 'cm230f032',
        name: 'Gaming Set',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'gaming-set.jpg',
        price: 299,
        category: 'Electronics',
        quantity: 63,
        inventoryStatus: 'INSTOCK',
        rating: 3,
        orders: [
          {
            id: '1009-0',
            productCode: 'cm230f032',
            date: '2020-06-24',
            amount: 299,
            quantity: 1,
            customer: 'Kadeem Mujtaba',
            status: 'PENDING'
          },
          {
            id: '1009-1',
            productCode: 'cm230f032',
            date: '2020-05-11',
            amount: 299,
            quantity: 1,
            customer: 'Ashley Wickens',
            status: 'DELIVERED'
          },
          {
            id: '1009-2',
            productCode: 'cm230f032',
            date: '2019-02-07',
            amount: 299,
            quantity: 1,
            customer: 'Julie Johnson',
            status: 'DELIVERED'
          },
          {
            id: '1009-3',
            productCode: 'cm230f032',
            date: '2020-04-26',
            amount: 299,
            quantity: 1,
            customer: 'Tony Costa',
            status: 'CANCELLED'
          }
        ]
      },
      {
        id: '1010',
        code: 'plb34234v',
        name: 'Gold Phone Case',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'gold-phone-case.jpg',
        price: 24,
        category: 'Accessories',
        quantity: 0,
        inventoryStatus: 'OUTOFSTOCK',
        rating: 4,
        orders: [
          {
            id: '1010-0',
            productCode: 'plb34234v',
            date: '2020-02-04',
            amount: 24,
            quantity: 1,
            customer: 'James Butt',
            status: 'DELIVERED'
          },
          {
            id: '1010-1',
            productCode: 'plb34234v',
            date: '2020-05-05',
            amount: 48,
            quantity: 2,
            customer: 'Josephine Darakjy',
            status: 'DELIVERED'
          }
        ]
      },
      {
        id: '1011',
        code: '4920nnc2d',
        name: 'Green Earbuds',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'green-earbuds.jpg',
        price: 89,
        category: 'Electronics',
        quantity: 23,
        inventoryStatus: 'INSTOCK',
        rating: 4,
        orders: [
          {
            id: '1011-0',
            productCode: '4920nnc2d',
            date: '2020-06-01',
            amount: 89,
            quantity: 1,
            customer: 'Art Venere',
            status: 'DELIVERED'
          }
        ]
      },
      {
        id: '1012',
        code: '250vm23cc',
        name: 'Green T-Shirt',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'green-t-shirt.jpg',
        price: 49,
        category: 'Clothing',
        quantity: 74,
        inventoryStatus: 'INSTOCK',
        rating: 5,
        orders: [
          {
            id: '1012-0',
            productCode: '250vm23cc',
            date: '2020-02-05',
            amount: 49,
            quantity: 1,
            customer: 'Lenna Paprocki',
            status: 'DELIVERED'
          },
          {
            id: '1012-1',
            productCode: '250vm23cc',
            date: '2020-02-15',
            amount: 49,
            quantity: 1,
            customer: 'Donette Foller',
            status: 'PENDING'
          }
        ]
      },
      {
        id: '1013',
        code: 'fldsmn31b',
        name: 'Grey T-Shirt',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'grey-t-shirt.jpg',
        price: 48,
        category: 'Clothing',
        quantity: 0,
        inventoryStatus: 'OUTOFSTOCK',
        rating: 3,
        orders: [
          {
            id: '1013-0',
            productCode: 'fldsmn31b',
            date: '2020-04-01',
            amount: 48,
            quantity: 1,
            customer: 'Simona Morasca',
            status: 'DELIVERED'
          }
        ]
      },
      {
        id: '1014',
        code: 'waas1x2as',
        name: 'Headphones',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'headphones.jpg',
        price: 175,
        category: 'Electronics',
        quantity: 8,
        inventoryStatus: 'LOWSTOCK',
        rating: 5,
        orders: [
          {
            id: '1014-0',
            productCode: 'waas1x2as',
            date: '2020-05-15',
            amount: 175,
            quantity: 1,
            customer: 'Lenna Paprocki',
            status: 'DELIVERED'
          },
          {
            id: '1014-1',
            productCode: 'waas1x2as',
            date: '2020-01-02',
            amount: 175,
            quantity: 1,
            customer: 'Donette Foller',
            status: 'CANCELLED'
          }
        ]
      },
      {
        id: '1015',
        code: 'vb34btbg5',
        name: 'Light Green T-Shirt',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'light-green-t-shirt.jpg',
        price: 49,
        category: 'Clothing',
        quantity: 34,
        inventoryStatus: 'INSTOCK',
        rating: 4,
        orders: [
          {
            id: '1015-0',
            productCode: 'vb34btbg5',
            date: '2020-07-02',
            amount: 98,
            quantity: 2,
            customer: 'Mitsue Tollner',
            status: 'DELIVERED'
          }
        ]
      },
      {
        id: '1016',
        code: 'k8l6j58jl',
        name: 'Lime Band',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'lime-band.jpg',
        price: 79,
        category: 'Lung',
        quantity: 12,
        inventoryStatus: 'INSTOCK',
        rating: 3,
        orders: []
      },
      {
        id: '1017',
        code: 'v435nn85n',
        name: 'Mini Speakers',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'mini-speakers.jpg',
        price: 85,
        category: 'Clothing',
        quantity: 42,
        inventoryStatus: 'INSTOCK',
        rating: 4,
        orders: [
          {
            id: '1017-0',
            productCode: 'v435nn85n',
            date: '2020-07-12',
            amount: 85,
            quantity: 1,
            customer: 'Minna Amigon',
            status: 'DELIVERED'
          }
        ]
      },
      {
        id: '1018',
        code: '09zx9c0zc',
        name: 'Painted Phone Case',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'painted-phone-case.jpg',
        price: 56,
        category: 'Accessories',
        quantity: 41,
        inventoryStatus: 'INSTOCK',
        rating: 5,
        orders: [
          {
            id: '1018-0',
            productCode: '09zx9c0zc',
            date: '2020-07-01',
            amount: 56,
            quantity: 1,
            customer: 'Abel Maclead',
            status: 'DELIVERED'
          },
          {
            id: '1018-1',
            productCode: '09zx9c0zc',
            date: '2020-05-02',
            amount: 56,
            quantity: 1,
            customer: 'Minna Amigon',
            status: 'RETURNED'
          }
        ]
      },
      {
        id: '1019',
        code: 'mnb5mb2m5',
        name: 'Pink Band',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'pink-band.jpg',
        price: 79,
        category: 'Lung',
        quantity: 63,
        inventoryStatus: 'INSTOCK',
        rating: 4,
        orders: []
      },
      {
        id: '1020',
        code: 'r23fwf2w3',
        name: 'Pink Purse',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'pink-purse.jpg',
        price: 110,
        category: 'Accessories',
        quantity: 0,
        inventoryStatus: 'OUTOFSTOCK',
        rating: 4,
        orders: [
          {
            id: '1020-0',
            productCode: 'r23fwf2w3',
            date: '2020-05-29',
            amount: 110,
            quantity: 1,
            customer: 'Kiley Caldarera',
            status: 'DELIVERED'
          },
          {
            id: '1020-1',
            productCode: 'r23fwf2w3',
            date: '2020-02-11',
            amount: 220,
            quantity: 2,
            customer: 'Graciela Ruta',
            status: 'DELIVERED'
          }
        ]
      },
      {
        id: '1021',
        code: 'pxpzczo23',
        name: 'Purple Band',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'purple-band.jpg',
        price: 79,
        category: 'Lung',
        quantity: 6,
        inventoryStatus: 'LOWSTOCK',
        rating: 3,
        orders: [
          {
            id: '1021-0',
            productCode: 'pxpzczo23',
            date: '2020-02-02',
            amount: 79,
            quantity: 1,
            customer: 'Cammy Albares',
            status: 'DELIVERED'
          }
        ]
      },
      {
        id: '1022',
        code: '2c42cb5cb',
        name: 'Purple Gemstone Necklace',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'purple-gemstone-necklace.jpg',
        price: 45,
        category: 'Accessories',
        quantity: 62,
        inventoryStatus: 'INSTOCK',
        rating: 4,
        orders: [
          {
            id: '1022-0',
            productCode: '2c42cb5cb',
            date: '2020-06-29',
            amount: 45,
            quantity: 1,
            customer: 'Mattie Poquette',
            status: 'DELIVERED'
          },
          {
            id: '1022-1',
            productCode: '2c42cb5cb',
            date: '2020-02-11',
            amount: 135,
            quantity: 3,
            customer: 'Meaghan Garufi',
            status: 'DELIVERED'
          }
        ]
      },
      {
        id: '1023',
        code: '5k43kkk23',
        name: 'Purple T-Shirt',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'purple-t-shirt.jpg',
        price: 49,
        category: 'Clothing',
        quantity: 2,
        inventoryStatus: 'LOWSTOCK',
        rating: 5,
        orders: [
          {
            id: '1023-0',
            productCode: '5k43kkk23',
            date: '2020-04-15',
            amount: 49,
            quantity: 1,
            customer: 'Gladys Rim',
            status: 'RETURNED'
          }
        ]
      },
      {
        id: '1024',
        code: 'lm2tny2k4',
        name: 'Shoes',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'shoes.jpg',
        price: 64,
        category: 'Clothing',
        quantity: 0,
        inventoryStatus: 'INSTOCK',
        rating: 4,
        orders: []
      },
      {
        id: '1025',
        code: 'nbm5mv45n',
        name: 'Sneakers',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'sneakers.jpg',
        price: 78,
        category: 'Clothing',
        quantity: 52,
        inventoryStatus: 'INSTOCK',
        rating: 4,
        orders: [
          {
            id: '1025-0',
            productCode: 'nbm5mv45n',
            date: '2020-02-19',
            amount: 78,
            quantity: 1,
            customer: 'Yuki Whobrey',
            status: 'DELIVERED'
          },
          {
            id: '1025-1',
            productCode: 'nbm5mv45n',
            date: '2020-05-21',
            amount: 78,
            quantity: 1,
            customer: 'Fletcher Flosi',
            status: 'PENDING'
          }
        ]
      },
      {
        id: '1026',
        code: 'zx23zc42c',
        name: 'Teal T-Shirt',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'teal-t-shirt.jpg',
        price: 49,
        category: 'Clothing',
        quantity: 3,
        inventoryStatus: 'LOWSTOCK',
        rating: 3,
        orders: [
          {
            id: '1026-0',
            productCode: 'zx23zc42c',
            date: '2020-04-24',
            amount: 98,
            quantity: 2,
            customer: 'Bette Nicka',
            status: 'DELIVERED'
          }
        ]
      },
      {
        id: '1027',
        code: 'acvx872gc',
        name: 'Yellow Earbuds',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'yellow-earbuds.jpg',
        price: 89,
        category: 'Electronics',
        quantity: 35,
        inventoryStatus: 'INSTOCK',
        rating: 3,
        orders: [
          {
            id: '1027-0',
            productCode: 'acvx872gc',
            date: '2020-01-29',
            amount: 89,
            quantity: 1,
            customer: 'Veronika Inouye',
            status: 'DELIVERED'
          },
          {
            id: '1027-1',
            productCode: 'acvx872gc',
            date: '2020-06-11',
            amount: 89,
            quantity: 1,
            customer: 'Willard Kolmetz',
            status: 'DELIVERED'
          }
        ]
      },
      {
        id: '1028',
        code: 'tx125ck42',
        name: 'Yoga Mat',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'yoga-mat.jpg',
        price: 20,
        category: 'Lung',
        quantity: 15,
        inventoryStatus: 'INSTOCK',
        rating: 5,
        orders: []
      },
      {
        id: '1029',
        code: 'gwuby345v',
        name: 'Yoga Set',
        description: 'Lorem ipsum dolor sit amet, consec adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        image: 'yoga-set.jpg',
        price: 20,
        category: 'Lung',
        quantity: 25,
        inventoryStatus: 'INSTOCK',
        rating: 8,
        orders: [
          {
            id: '1029-0',
            productCode: 'gwuby345v',
            date: '2020-02-14',
            amount: 4,
            quantity: 80,
            customer: 'Maryann Royster',
            status: 'DELIVERED'
          }
        ]
      }
    ];
  },

  getProductsMini() {
    return Promise.resolve(this.getProductsData().slice(0, 5));
  },

  getProductsSmall() {
    return Promise.resolve(this.getProductsData().slice(0, 10));
  },

  getProducts() {
    return Promise.resolve(this.getProductsData());
  },

  getProductsWithOrdersSmall() {
    return Promise.resolve(this.getProductsWithOrdersData().slice(0, 10));
  },

  getProductsWithOrders() {
    return Promise.resolve(this.getProductsWithOrdersData());
  }
};
