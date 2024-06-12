import json

starting_sources = [
  {
      "content": {
          "Web Page Descriptions": {
              "name": "NIH National Cancer Institute GDC Documentation",
              "initials": "NIH",
              "purpose": "The purpose of this page is to provide detailed information on GDC processes and tools for researchers, data submitters, and developers.",
              "actions": [
                  "Navigate to the NIH National Cancer Institute GDC Documentation homepage",
                  "Access the GDC Apps menu",
                  "Navigate to the API documentation",
                  "Navigate to the Data Portal",
                  "Navigate to Data Portal v1.0",
                  "Navigate to Data Submission guidelines",
                  "Navigate to the Data Transfer Tool",
                  "Navigate to the Data Dictionary",
                  "Navigate to the Encyclopedia",
                  "Perform a quick search",
                  "Understand the data in the GDC",
                  "Access controlled data in the GDC",
                  "Explore data in the GDC",
                  "Download files in the GDC",
                  "Analyze data in the GDC",
                  "View the GDC Data Dictionary",
                  "Search the GDC Data Dictionary",
                  "Understand GDC Harmonized Data",
                  "Submit data",
                  "Review submitted data",
                  "Understand the GDC Data Model",
                  "Use the GDC API",
                  "Access the GDC Codebase",
                  "Visit the GDC Website",
                  "Contact the GDC",
                  "Navigate to the Site Home",
                  "View policies",
                  "View accessibility information",
                  "View FOIA information",
                  "View HHS Vulnerability Disclosure",
                  "Visit the U.S. Department of Health and Human Services website",
                  "Visit the National Institutes of Health website",
                  "Visit the National Cancer Institute website",
                  "Visit the USA.gov website"
              ],
              "sections": [
                  "Header with navigation links",
                  "Search bar",
                  "Sections for Researchers, Data Submitters, and Developers with relevant links",
                  "Footer with additional links to policies, accessibility, FOIA, HHS Vulnerability Disclosure, and other related websites"
              ]
          },
          "Information on Links on Web Page": {
              "https://docs.gdc.cancer.gov/": "Link to the NIH National Cancer Institute GDC Documentation, providing detailed information on GDC processes and tools.",
              "https://docs.gdc.cancer.gov/#": "Link to the GDC Apps Menu, API, Data Portal, Data Portal v1.0, Data Submission, Data Transfer Tool, Data Dictionary, and Data sections of the GDC Documentation.",
              "https://docs.gdc.cancer.gov/Encyclopedia/": "Link to the GDC Encyclopedia, a resource for understanding various terms and concepts related to GDC.",
              "https://docs.gdc.cancer.gov/Data/Introduction/": "Link to the 'Understand the Data in the GDC' section, providing an introduction to the data available in the GDC.",
              "https://docs.gdc.cancer.gov/Data/Data_Security/Data_Security/": "Link to the 'Access Controlled Data in the GDC' section, detailing how to access controlled data.",
              "https://docs.gdc.cancer.gov/Data_Portal_V1/Users_Guide/Exploration/": "Link to the 'Explore Data in the GDC' section, guiding users on how to explore data in the GDC Data Portal.",
              "https://docs.gdc.cancer.gov/Data_Transfer_Tool/Users_Guide/Preparing_for_Data_Download_and_Upload/": "Link to the 'Download Files in the GDC' section, providing instructions on downloading files using the GDC Data Transfer Tool.",
              "https://docs.gdc.cancer.gov/Data_Portal_V1/Users_Guide/Custom_Set_Analysis/": "Link to the 'Analyze Data in the GDC' section, explaining how to analyze data using the GDC Data Portal.",
              "https://docs.gdc.cancer.gov/Data_Dictionary/viewer/": "Link to the 'View the GDC Data Dictionary' section, allowing users to view the GDC Data Dictionary.",
              "https://docs.gdc.cancer.gov/Data_Dictionary/gdcmvs/": "Link to the 'Search the GDC Data Dictionary' section, enabling users to search the GDC Data Dictionary.",
              "https://gdc.cancer.gov/about-data/data-harmonization-and-generation/genomic-data-harmonization-0": "Link to the 'Understand GDC Harmonized Data' section, providing information on GDC data harmonization.",
              "https://docs.gdc.cancer.gov/Data_Submission_Portal/Users_Guide/Data_Submission_Overview/": "Link to the 'Submit Data' section, offering guidance on submitting data to the GDC.",
              "https://docs.gdc.cancer.gov/Data_Submission_Portal/Users_Guide/Data_Submission_Process/#review": "Link to the 'Review Submitted Data' section, explaining how to review data submitted to the GDC.",
              "https://docs.gdc.cancer.gov/Data/Data_Model/GDC_Data_Model/": "Link to the 'Understand the GDC Data Model' section, detailing the GDC data model.",
              "https://docs.gdc.cancer.gov/API/Users_Guide/Getting_Started/": "Link to the 'Use the GDC API' section, providing a guide on using the GDC API.",
              "https://github.com/NCI-GDC": "Link to the GDC Codebase on GitHub, where users can access the GDC codebase.",
              "https://gdc.cancer.gov/": "Link to the GDC Website, the main website for the Genomic Data Commons.",
              "https://gdc.cancer.gov/contact-us": "Link to the 'Contact Us' page for the GDC, providing contact information.",
              "https://portal.gdc.cancer.gov/": "Link to the GDC Portal Home, the main portal for accessing GDC data.",
              "http://www.cancer.gov/global/web/policies": "Link to the Policies page on the National Cancer Institute website, detailing various policies.",
              "http://www.cancer.gov/global/web/policies/accessibility": "Link to the Accessibility page on the National Cancer Institute website, providing information on accessibility policies.",
              "http://www.cancer.gov/global/web/policies/foia": "Link to the FOIA page on the National Cancer Institute website, providing information on the Freedom of Information Act.",
              "https://www.hhs.gov/vulnerability-disclosure-policy": "Link to the HHS Vulnerability Disclosure page, detailing the vulnerability disclosure policy of the U.S. Department of Health and Human Services.",
              "http://www.hhs.gov/": "Link to the U.S. Department of Health and Human Services website, the main website for HHS.",
              "http://www.nih.gov/": "Link to the National Institutes of Health website, the main website for NIH.",
              "http://www.cancer.gov/": "Link to the National Cancer Institute website, the main website for NCI.",
              "http://www.usa.gov/": "Link to USA.gov, the U.S. government's official web portal."
          },
          "Information on options on web page": {
              "Data Portal Sections": {
                  "type": "links",
                  "options": {
                      "23": "Getting Started",
                      "24": "Quick Start",
                      "25": "Tutorial Videos",
                      "26": "Cohort Builder",
                      "27": "Analysis Center",
                      "28": "Repository",
                      "29": "Projects",
                      "30": "BAM Slicing",
                      "31": "Clinical Data Analysis",
                      "32": "Cohort Comparison",
                      "33": "Cohort Level MAF",
                      "34": "Gene Expression Clustering",
                      "35": "Mutation Frequency",
                      "36": "OncoMatrix",
                      "37": "ProteinPaint",
                      "38": "Sequence Reads",
                      "39": "Set Operations",
                      "40": "For Developers",
                      "41": "Release Notes",
                      "42": "Download PDF"
                  },
                  "selected": None
              },
              "Data Portal v1.0 Sections": {
                  "type": "links",
                  "options": {
                      "43": "Getting Started",
                      "44": "Projects",
                      "45": "Exploration",
                      "46": "Analysis",
                      "47": "Repository",
                      "48": "Advanced Search",
                      "49": "Cart and File Download",
                      "50": "Release Notes",
                      "51": "Download PDF"
                  },
                  "selected": None
              },
              "Data Dictionary Sections": {
                  "type": "links",
                  "options": {
                      "68": "About",
                      "69": "Viewer",
                      "70": "Search",
                      "71": "Release Notes"
                  },
                  "selected": None
              },
              "Data Sections": {
                  "type": "links",
                  "options": {
                      "72": "Introduction",
                      "73": "GDC Data Model",
                      "74": "Data Security",
                      "75": "File Format: MAF",
                      "76": "File Format: VCF",
                      "77": "Bioinformatics Pipeline: DNA-Seq Analysis",
                      "78": "Bioinformatics Pipeline: mRNA Analysis",
                      "79": "Bioinformatics Pipeline: miRNA Analysis",
                      "80": "Bioinformatics Pipeline: Copy Number Variation Analysis",
                      "81": "Bioinformatics Pipeline: Methylation Analysis Pipeline",
                      "82": "Bioinformatics Pipeline: Protein Expression",
                      "83": "Aligned Reads Summary Metrics",
                      "84": "GDC Reference Files",
                      "85": "Release Notes",
                      "86": "Download PDF"
                  },
                  "selected": None
              }
          },
          "documentation": "https://docs.gdc.cancer.gov/Encyclopedia/:\n\n        Skip to main content\n\nGDC Document Keyword Search Modal\n\nSearch\n\nNIH National Cancer Institute GDC Documentation\n\nToggle navigation\n\nGDC Apps\n\nData Portal\n\nAPI\n\nDocumentation\n\nWebsite\n\nData Transfer Tool\n\nData Submission Portal\n\nHome\n\nAPI \n                    \n                    \n                        \n  \n    \n    Getting Started\n    \n  \n  \n\n                    \n                        \n  \n    \n    Search and Retrieval\n    \n  \n  \n\n                    \n                        \n  \n    \n    Downloading Files\n    \n  \n  \n\n                    \n                        \n  \n    \n    Data Analysis\n    \n  \n  \n\nBAM Slicing\n    \n  \n  \n\n                    \n                        \n  \n    \n    Submission\n    \n  \n  \n\n                    \n                        \n  \n    \n    Python Examples\n    \n  \n  \n\n                    \n                        \n  \n    \n    GraphQL Examples\n    \n  \n  \n\n                    \n                        \n  \n    \n    System Information\n    \n  \n  \n\n                    \n                        \n  \n    \n    Additional Examples\n    \n  \n  \n\n                    \n                        \n  \n    \n    Appendix A: Available Fields\n    \n  \n\n\n                    \n                        \n  \n    \n    Appendix B: Key Terms\n    \n  \n  \n\n                    \n                        \n  \n    \n    Appendix C: Format of Submission Queries and Responses\n    \n  \n  \n\n                    \n                        \n  \n    \n    Release Notes\n    \n  \n  \n\n                    \n                        \n  \n    \n    Download PDF\n\nData Portal \n                    \n                    \n                        \n  \n    \n    Getting Started\n    \n  \n  \n\n                    \n                        \n  \n    \n    Quick Start\n    \n  \n  \n\n                    \n                        \n  \n    \n    Tutorial Videos\n    \n  \n  \n\n                    \n                        \n  \n    \n    Cohort Builder\n    \n  \n \n\n                    \n                        \n  \n    \n    Analysis Center\n    \n  \n  \n\n                    \n                        \n  \n    \n    Repository\n    \n  \n  \n\n      \n                        \n  \n    \n    Projects\n    \n  \n  \n\n                    \n                        \n  \n    \n    BAM Slicing\n    \n  \n  \n\n                    \n       \n  \n    \n    Clinical Data Analysis\n    \n  \n  \n\n                    \n                        \n  \n    \n    Cohort Comparison\n    \n  \n  \n\n                    \n  \n  \n    \n    Cohort Level MAF\n    \n  \n  \n\n                    \n                        \n  \n    \n    Gene Expression Clustering\n    \n  \n  \n\n                    \n\n  \n    \n    Mutation Frequency\n    \n  \n  \n\n                    \n                        \n  \n    \n    OncoMatrix\n    \n  \n  \n\n                    \n                        \n  \n    \nProteinPaint\n    \n  \n  \n\n                    \n                        \n  \n    \n    Sequence Reads\n    \n  \n  \n\n                    \n                        \n  \n    \n    Set Operations\n  \n  \n  \n\n                    \n                        \n  \n    \n    For Developers\n    \n  \n  \n\n                    \n                        \n  \n    \n    Release Notes\n    \n  \n  \n\n                 \n                        \n  \n    \n    Download PDF\n\nData Portal v1.0 \n                    \n                    \n                        \n  \n    \n    Getting Started\n    \n  \n  \n\n                    \n                        \n  \n    \n    Projects\n    \n  \n  \n\n                    \n                        \n  \n    \n    Exploration\n    \n  \n  \n\n  \n                        \n  \n    \n    Analysis\n    \n  \n  \n\n                    \n                        \n  \n    \n    Repository\n    \n  \n  \n\n                    \n  \n  \n    \n    Advanced Search\n    \n  \n  \n\n                    \n                        \n  \n    \n    Cart and File Download\n    \n  \n  \n\n                    \n                        \n  \n    \n    Release Notes\n    \n  \n  \n\n                    \n                        \n  \n    \n    Download PDF\n\nData Submission \n                    \n                    \n  \n  \n    \n    Before Submitting Data to the GDC Portal\n    \n  \n  \n\n                    \n                        \n  \n    \n    Data Submission Overview\n    \n  \n  \n\n                    \n                      \n  \n    \n    Data Submission Portal\n    \n  \n  \n\n                    \n                        \n  \n    \n    Data Upload Walkthrough\n    \n  \n  \n\n                    \n                       \n  \n    \n    Pre-Release Data Portal\n    \n  \n  \n\n                    \n                        \n  \n    \n    Submission Best Practices\n    \n  \n  \n\n \n                        \n  \n    \n    Release Notes\n    \n  \n  \n\n                    \n                        \n  \n    \n    Download PDF\n\nData Transfer Tool \n                    \n           \n                        \n  \n    \n    Getting Started\n    \n  \n  \n\n                    \n                        \n  \n    \n    Preparing for Data Download and Upload\n    \n  \n  \n\n                    \n                        \n  \n    \n    Data Transfer Tool Command Line Documentation\n    \n  \n  \n\n                    \n                        \n  \n    \n    Release Notes - Command Line\n    \n  \n  \n\n                    \n                        \n  \n    \n    Data Transfer Tool UI Documentation\n    \n  \n  \n\n                    \n                        \n  \n    \n  Release Notes - UI\n    \n  \n  \n\n                    \n                        \n  \n    \n    Troubleshooting Guide\n    \n  \n  \n\n                    \n                        \n  \n    \n    Download PDF\n\nData Dictionary \n                    \n                    \n                        \n  \n    \n    About\n    \n  \n  \n\n                    \n                        \n  \n    \n    Viewer\n    \n  \n  \n\n                    \n                        \n  \n    \n    Search\n    \n  \n  \n\n                    \n                        \n  \n    \n    Release Notes\n\nData \n        \n                    \n                        \n  \n    \n    Introduction\n    \n  \n  \n\n                    \n                        \n  \n    \n    GDC Data Model\n    \n  \n  \n\n            \n                        \n  \n    \n    Data Security\n    \n  \n  \n\n                    \n                        \n  \n    \n    File Format: MAF\n    \n  \n  \n\n                    \n                       \n  \n    \n    File Format: VCF\n    \n  \n  \n\n                    \n                        \n  \n    \n    Bioinformatics Pipeline: DNA-Seq Analysis\n    \n  \n  \n\n          \n                        \n  \n    \n    Bioinformatics Pipeline: mRNA Analysis\n    \n  \n  \n\n                    \n                        \n  \n    \n    Bioinformatics Pipeline: miRNA Analysis\n    \n  \n  \n\n                    \n                        \n  \n    \n    Bioinformatics Pipeline: Copy Number Variation Analysis\n    \n  \n  \n\n                    \n\n  \n    \n    Bioinformatics Pipeline: Methylation Analysis Pipeline\n    \n  \n  \n\n                    \n                        \n  \n    \n    Bioinformatics Pipeline: Protein Expression\n    \n  \n  \n\n                    \n                        \n  \n    \n    Aligned Reads Summary Metrics\n    \n  \n  \n  \n     GDC Reference Files\n  \n  \n\n                    \n                        \n\n    \n    Release Notes\n    \n  \n  \n\n                    \n                        \n  \n    \n    Download PDF\n\nEncyclopedia\n\n\n\nQuick Search\n\nEncyclopedia\n\nBrowse the terms\n\nView All\n\nSuggest a Topic\n\nOur goal is to maintain this resource as an important tool for understanding cancer biology. If there is\n            a topic you are unsure about, please suggest it below.\n\nContactus\n\nThe GDC Encyclopedia is an informational tool that makes GDC applications easier to use. It helps researchers, data submitters, developers and clinicians quickly find specific information without needing to browse for it.\n\nCommon Topics for Researchers\n\nControlled access\n\ndbGaP\n\nGDC Data Portal\n\nGDC Data Transfer Tool (DTT)\n\nHarmonized Data\n\nManifest File\n\nMutation Annotation Format(MAF)\n\nVariant Type\n\nVariant Call Format (VCF)\n\nCommon Topics for Data Submitters\n\nBiospecimen Data\n\nCase\n\nClinical Data\n\nClinical Supplement\n\nData Submitter\n\ndbGaP\n\nGDC Data Submission Portal\n\nGDC Data Transfer Tool (DTT)\n\nRedaction\n\nCommon Topics for Data Developers\n\nEntity\n\nGDC API\n\nLatest Data\n\nManifest File\n\nMutation Annotation Format (MAF)\n\nRelease Number\n\nREST API\n\nUniversally Unique Identifier (UUID)\n\nVariant Call Format (VCF)\n\nAffymetrix SNP 6.0\n\nAggregated Somatic Mutation\n\nAligned Reads\n\nAliquot\n\nAnalyte\n\nAnnotations\n\nAnnotations TCGA\n\nBiospecimen Data\n\nCancer Genomics Hub\n\nCase\n\nCenter for Cancer Genomics\n\nClinical Data\n\nClinical Supplement\n\nControlled Access\n\nData Access Policy\n\nData Submitter\n\ndbGaP\n\nEntity\n\nFPKM\n\nFPKM-UQ\n\nGDC API\n\nGDC Data Portal\n\nGDC Data Submission Portal\n\nGDC Data Transfer Tool\n\nGDC Documentation Site\n\nGDC Web Site\n\nGenomic Data Analysis Network\n\nGenomic Data Commons\n\nHarmonized Data\n\nLatest Data\n\nManifest File\n\nMD5 Checksum\n\nMutation Annotation Format\n\nMutation Annotation Format TCGAv2\n\nRedaction\n\nRelease Number\n\nREST API\n\nRNA-Seq\n\nSNP Array-Based Data\n\nTCGA Barcode\n\nTCGA VCF 1.1v2\n\nTCIA\n\nUUID\n\nVariant Call Format\n\nVariant Type\n\nSite Home\n                            |\n\nPolicies\n                            |\n\nAccessibility\n                     |\n\nFOIA\n                            |\n\nHHS Vulnerability Disclosure\n\nU.S. Department of Health and Human Services\n                            |\n\nNational Institutes of Health\n                            |\n\nNational Cancer Institute\n                            |\n\nUSA.gov\n\nNIH... Turning Discovery Into Health \u00ae\n\nGDC Docs Version 1.0\n\nScroll to the top of thispage."
      },
      "summary": "{\n  \"reasoning\": \"To create a comprehensive summary of the NIH National Cancer Institute GDC Documentation website, it is essential to include detailed information about the purpose of the site, the specific types of data and tools available, and the various sections and functionalities provided. This will help users determine if this data source is appropriate for their specificdata needs.\",\n  \"summary\": \"The NIH National Cancer Institute GDC Documentation website serves as a comprehensive resource for researchers, data submitters, and developers involved in cancer research. The primary purpose of this site is to provide detailed information on the Genomic Data Commons (GDC) processes and tools. It offers extensive documentation on how to navigate and utilize the GDC's various applications, APIs, data portals, and submission tools. The site is structured to cater to different user groups, including researchers, data submitters, and developers, each with tailored sections and relevant links to facilitate their specific needs. The website includes a header with navigation links, a search bar, and a footer with additional links to policies, accessibility, FOIA, HHS Vulnerability Disclosure, and other related websites. Key sections of the site include the GDC Apps menu, API documentation, Data Portal, Data Submission guidelines, Data Transfer Tool, Data Dictionary, and the GDCEncyclopedia. Each section provides in-depth guides and user manuals to help users understand and interact with the GDC's data and tools. For instance, the Data Portal section includes links to getting started guides, tutorial videos, cohort builders, analysis centers, and various data exploration and analysis tools. The Data Submission section offers comprehensive guidelines on how to submit data to theGDC, including best practices and walkthroughs. The Data Transfer Tool section provides instructions on preparing for data download and upload, along with troubleshooting guides. The Data Dictionary section allows users to view and search the GDC Data Dictionary, which is essential for understanding the data model and the specific data elements used in the GDC. The GDC Encyclopedia is an informational tool designed to help users quickly find specific information related to GDC applications, making it easier to understand cancer biology and the various terms and concepts used in the GDC. Overall, the NIH National Cancer Institute GDC Documentation website is a vital resource for anyone involved in cancer research, providing the necessary tools and information to effectively use the GDC's vast data resources.\"\n}"
  },
  {
    "content": {
      "Web Page Descriptions": {
        "name": "Imaging Data Commons",
        "initials": "IDC",
        "purpose": "The purpose of this page is to provide access to and information about the Imaging Data Commons (IDC), a platform for exploring, collecting, and analyzing medical imaging data related to cancer research.",
        "actions": [
          "Navigate to the home page",
          "Explore image data",
          "View IDC collections",
          "Access getting started notebooks",
          "Visit the user forum",
          "View news items",
          "Learn about IDC",
          "Access help documentation",
          "Sign in to the portal",
          "Join community office hours via Google Meet",
          "Close pop-up or modal windows",
          "View example images in the IDC Viewer",
          "Navigate through image carousels"
        ],
        "sections": [
          "Header with navigation links (Home, Explore Images, Collections, Getting Started, User Forum, News, About, Help, Sign In)",
          "Main content area with image exploration and data visualization",
          "Data portal summary with statistics on collections, cases, data volume, and image series",
          "Footer with additional links (Site Home, Contact Us, Privacy Policy, Accessibility, FOIA, HHS Vulnerability Disclosure, U.S. Department of Health and Human Services, National Institutes of Health, National Cancer Institute, USA.gov)"
        ]
      },
      "Information on Links on Web Page": {
        "https://portal.imaging.datacommons.cancer.gov/": "Link to the home page of the Imaging Data Commons (IDC) portal.",
        "https://portal.imaging.datacommons.cancer.gov/explore/": "Link to explore image data available on the IDC portal.",
        "https://portal.imaging.datacommons.cancer.gov/collections/": "Link to view various collections of imaging data on the IDC portal.",
        "https://portal.imaging.datacommons.cancer.gov/news/": "Link to view news items related to the IDC portal.",
        "https://portal.imaging.datacommons.cancer.gov/about/": "Link to information aboutthe Imaging Data Commons (IDC).",
        "https://portal.imaging.datacommons.cancer.gov/accounts/login/": "Link to sign in to the IDC portal.",
        "https://meet.google.com/xyt-vody-tvb": "Link to a Google Meet session for IDC Community Office Hours.",
        "https://viewer.imaging.datacommons.cancer.gov/viewer/1.3.6.1.4.1.14519.5.2.1.5168.1900.259520120774497994844579066293?seriesInstanceUID=1.3.6.1.4.1.14519.5.2.1.5168.1900.379274847602196071565482395253,1.3.6.1.4.1.14519.5.2.1.5168.1900.924189791316990444955278117416,1.3.6.1.4.1.14519.5.2.1.5168.1900.308784784152451259100701859682,1.3.6.1.4.1.14519.5.2.1.5168.1900.924189791316990444955278117416,1.3.6.1.4.1.14519.5.2.1.5168.1900.379274847602196071565482395253,1.3.6.1.4.1.14519.5.2.1.5168.1900.308784784152451259100701859682": "Link to view a PET example image in the IDCViewer.",
        "https://viewer.imaging.datacommons.cancer.gov/slim/studies/2.25.211094631316408413440371843585977094852/series/1.3.6.1.4.1.5962.99.1.208792987.352384958.1640886332827.2.0": "Link to view a Slide Microscopy (Brightfield) example image in the IDC SliM Viewer.",
        "mailto:support@canceridc.dev": "Link to contact support for the IDC portal via email.",
        "https://portal.imaging.datacommons.cancer.gov/privacy/": "Link to the privacy policy of the IDC portal.",
        "https://www.cancer.gov/policies/accessibility": "Link to the accessibility policy of the National Cancer Institute.",
        "https://www.cancer.gov/policies/foia": "Link to the Freedom of Information Act (FOIA) policy of the National Cancer Institute.",
        "https://www.hhs.gov/vulnerability-disclosure-policy/index.html": "Link to the vulnerability disclosure policy of the U.S. Department of Health and Human Services.",
        "https://www.hhs.gov/": "Link to the U.S. Department of Health and Human Services website.",
        "https://www.nih.gov/": "Link to the National Institutes of Health (NIH) website.",
        "https://www.cancer.gov/": "Link to the National Cancer Institute (NCI) website.",
        "https://www.usa.gov/": "Link to the USA.gov website."
      },
      "Information on options on web page": {
        "Imaging Modalities": {
          "type": "links",
          "options": {
            "1": "Computed Tomography (CT)",
            "2": "Magnetic Resonance (MR)",
            "3": "Positron Emission Tomography (PET)",
            "4": "Slide Microscopy (SM) -Brightfield",
            "5": "Slide Microscopy (SM) - Fluorescence"
          },
          "selected": None
        },
        "Cases by Major Primary Site": {
          "type": "text",
          "options": {
            "6": "Colorectal"
          },
          "selected": None
        }
      }
    },
    "summary": "{\n    \"reasoning\": \"To create a comprehensive summary of the Imaging Data Commons (IDC) website, it is essential to include details about its purpose, the types of data available, the functionalities provided, and the specific sections and links that users can navigate. This information will help determine if the IDC is the appropriate data source for a user's query, especially if the query is related to medicalimaging data for cancer research.\",\n    \"summary\": \"The Imaging Data Commons (IDC) is a specialized platform designed to facilitate the exploration, collection, and analysis of medical imaging data specifically related to cancer research. The primary purpose of the IDC is to provide researchers, clinicians, and other stakeholders with access to a vast repository of imaging data that can be used for various research and clinical applications. The IDC offers a range of functionalities and resources to support users in their work with medical imaging data. Users can navigate to the home page, explore image data, view IDC collections, access getting started notebooks, visit the user forum, view news items, learn about the IDC, access help documentation, sign in to the portal, and join community office hours via Google Meet. Additionally, users can view example images in the IDC Viewer and navigate through image carousels. The website is structured with a header containing navigation links to key sections such as Home, Explore Images, Collections, Getting Started, User Forum, News, About, Help, and Sign In. The main content area focuses on image exploration and data visualization, providing users with tools to interact with and analyze the imaging data. The data portal summary offers statistics on collections, cases, data volume, and image series, giving users an overview of the available data. The footer includes additional links to the site home, contact information, privacy policy, accessibility policy, FOIA policy, HHS vulnerability disclosure, and links to related organizations such as the U.S. Department of Health and Human Services, National Institutes of Health, National Cancer Institute, and USA.gov. The IDC provides access to various imaging modalities, including Computed Tomography (CT), Magnetic Resonance (MR), Positron Emission Tomography (PET), and Slide Microscopy (SM) in both Brightfield and Fluorescence formats. Users can also explore cases by major primary site, such as colorectal cancer. The website includes specific links to explore image data, view collections, read news items, learn about the IDC, sign in to the portal, join community office hours, and view example images in the IDCViewer. Contact support is available via email, and policies related to privacy, accessibility, FOIA, and vulnerability disclosure are accessible through dedicated links. Overall, the IDC is a comprehensive resource for accessing and analyzing medical imaging data related to cancer research, making it a valuable tool for researchers and clinicians in the field.\"\n}"
  },
  {
    "content": {
      "Web Page Descriptions": {
        "name": "Proteomic Data Commons",
        "initials": "NCI",
        "purpose": "The purpose of the Proteomic Data Commons (PDC) page is to provide access to proteomic data and resources for cancer research. It offers tools for exploring, analyzing, and submitting data, as well as information on recent releases, publications, and various types of cancer studies.",
        "actions": [
          "Navigate to the home page",
          "Login to the platform",
          "Search for gene symbols or case IDs",
          "Access guidelines for citing PDC",
          "Explore data",
          "Analyze data",
          "View publications",
          "Submit data",
          "Learn aboutthe PDC",
          "Access more options"
        ],
        "sections": [
          "Header with navigation links",
          "Login button",
          "Search bar",
          "Links to various sections such as Home, Explore, Analysis, Publications, Submit Data, About, and More",
          "Cases by Major Primary Site chart",
          "Cases by Disease Type list",
          "Recent Releases section",
          "News section",
          "Technology Advancement Studies section",
          "CPTAC Pan-Cancer Data section",
          "Footer with additional links such as Site Home, Contact Us, Privacy Policy, Policies, Accessibility, Disclaimer Policy, FOIA, HHS Vulnerability Disclosure, U.S. Department of Health and Human Services, National Institutes of Health, National Cancer Institute, and USA.gov"
        ]
      },
      "Information on Links on Web Page": {
        "https://pdc.cancer.gov/": "Link to the NCI Proteomics Data Commons homepage, providing access to proteomics data and resources.",
        "https://pdc.cancer.gov/pdc/data-use-guidelines#Cite_PDC": "Link to guidelines for citing the Proteomics Data Commons in research publications.",
        "https://pdc.cancer.gov/pdc/browse": "Link to explore the data available in the Proteomics Data Commons.",
        "https://pdc.cancer.gov/pdc/publications": "Link to publications related to the Proteomics Data Commons.",
        "https://pdc.cancer.gov/pdc/browse/filters/disease_type:Acute%20Myeloid%20Leukemia": "Link to data related to Acute Myeloid Leukemia in the Proteomics Data Commons.",
        "https://pdc.cancer.gov/pdc/browse/filters/disease_type:Breast%20Invasive%20Carcinoma": "Link to data related to Breast Invasive Carcinoma in the Proteomics Data Commons.",
        "https://pdc.cancer.gov/pdc/browse/filters/disease_type:Cholangiocarcinoma": "Link to data related to Cholangiocarcinoma in the Proteomics Data Commons.",
        "https://pdc.cancer.gov/pdc/browse/filters/disease_type:Chromophobe%20Renal%20Cell%20Carcinoma": "Link to data related to Chromophobe Renal Cell Carcinoma in the Proteomics Data Commons.",
        "https://pdc.cancer.gov/pdc/browse/filters/disease_type:Clear%20Cell%20Renal%20Cell%20Carcinoma": "Link to data related to Clear Cell Renal Cell Carcinoma in the Proteomics Data Commons.",
        "https://pdc.cancer.gov/pdc/browse/filters/disease_type:Colon%20Adenocarcinoma": "Link to data related to Colon Adenocarcinoma in the Proteomics Data Commons.",
        "https://pdc.cancer.gov/pdc/browse/filters/disease_type:Early%20Onset%20Gastric%20Cancer": "Link to data related to Early Onset Gastric Cancer in the Proteomics Data Commons.",
        "https://pdc.cancer.gov/pdc/browse/filters/disease_type:Glioblastoma": "Link to data related to Glioblastoma in the Proteomics Data Commons.",
        "https://pdc.cancer.gov/pdc/browse/filters/disease_type:Head%20and%20Neck%20Squamous%20Cell%20Carcinoma": "Link to data related to Head and Neck Squamous Cell Carcinoma in the Proteomics Data Commons.",
        "https://pdc.cancer.gov/pdc/browse/filters/disease_type:Hepatocellular%20Carcinoma": "Link to data related to Hepatocellular Carcinoma in the Proteomics Data Commons.",
        "https://pdc.cancer.gov/pdc/browse/filters/disease_type:Lung%20Adenocarcinoma": "Link to data related to Lung Adenocarcinoma in the Proteomics Data Commons.",
        "https://pdc.cancer.gov/pdc/browse/filters/disease_type:Lung%20Squamous%20Cell%20Carcinoma": "Link to data related to Lung Squamous Cell Carcinoma in the Proteomics Data Commons.",
        "https://pdc.cancer.gov/pdc/browse/filters/disease_type:Myelodysplastic%20Syndromes": "Link to data related to Myelodysplastic Syndromes in the Proteomics Data Commons.",
        "https://pdc.cancer.gov/pdc/browse/filters/disease_type:Non-Clear%20Cell%20Renal%20Cell%20Carcinoma": "Link to data related to Non-Clear Cell Renal Cell Carcinoma in the Proteomics Data Commons.",
        "https://pdc.cancer.gov/pdc/browse/filters/disease_type:Not%20Applicable": "Link to data categorized as Not Applicable in the Proteomics Data Commons.",
        "https://pdc.cancer.gov/pdc/browse/filters/disease_type:Oral%20Squamous%20Cell%20Carcinoma": "Link to data related to Oral Squamous Cell Carcinoma in the Proteomics Data Commons.",
        "https://pdc.cancer.gov/pdc/browse/filters/disease_type:Other%20Leukemias": "Link to data related to Other Leukemias in the Proteomics Data Commons.",
        "https://pdc.cancer.gov/pdc/browse/filters/disease_type:Ovarian%20Serous%20Cystadenocarcinoma": "Link to data related to Ovarian Serous Cystadenocarcinoma in the Proteomics Data Commons.",
        "https://pdc.cancer.gov/pdc/browse/filters/disease_type:Pancreatic%20Ductal%20Adenocarcinoma": "Link to data related to Pancreatic Ductal Adenocarcinoma in the Proteomics DataCommons.",
        "https://pdc.cancer.gov/pdc/browse/filters/disease_type:Papillary%20Renal%20Cell%20Carcinoma": "Link to data related to Papillary Renal Cell Carcinoma in the Proteomics Data Commons.",
        "https://pdc.cancer.gov/pdc/browse/filters/disease_type:Pediatric_slashAYA%20Brain%20Tumors": "Link to data related to Pediatric/AYA Brain Tumors in the Proteomics Data Commons.",
        "https://pdc.cancer.gov/pdc/browse/filters/disease_type:Rectum%20Adenocarcinoma": "Link to data related to Rectum Adenocarcinoma in the Proteomics Data Commons.",
        "https://pdc.cancer.gov/pdc/browse/filters/disease_type:Uterine%20Corpus%20Endometrial%20Carcinoma": "Link to data related to Uterine Corpus Endometrial Carcinoma in the Proteomics Data Commons.",
        "https://pdc.cancer.gov/pdc/browse/filters/disease_type:Other": "Link to data categorized as Other in the Proteomics Data Commons.",
        "https://pdc-release-notes.s3.amazonaws.com/PDC_Data_Release_Notes.htm": "Link to the release notes for the Proteomics Data Commons, detailing recent updates and data releases.",
        "https://pdc.cancer.gov/pdc/cptac-pancancer": "Link to the CPTAC Pan-Cancer Analysis Page, providing information and access to data generated by the Clinical Proteomic Tumor Analysis Consortium.",
        "https://proquest.iad1.qualtrics.com/jfe/form/SV_bP1hth2gAEHwn5k?Q_CHL=qr": "Link to a survey by the NCI inviting feedback on the Clinical Proteomic Tumor Analysis Consortium.",
        "https://datacommons.cancer.gov/publications/aacr-cancer-research": "Link to a manuscript series in AACR Cancer Research, detailing the resources of the Cancer Research Data Commons.",
        "https://nci.rev.vbrick.com/sharevideo/ecc3ebe1-31ba-4117-816e-4b896883f205": "Link to a video of the NCI CBIIT Data Science Webinar on the Proteomic Data Commons in Cancer Research.",
        "https://datascience.cancer.gov/news-events/events/proteomic-data-commons-cancer-research": "Link to the Data Science Webinar event page for learning how to effectively use the Proteomic Data Commons.",
        "https://pdc.cancer.gov/pdc/TechnologyAdvancementStudies": "Link to the Technology Advancement Studies page, detailing various studies related to proteomics.",
        "mailto:PDCHelpDesk@mail.nih.gov?Subject=PDC%20Help": "Link to contact the PDC Help Desk via email for assistance.",
        "https://www.cancer.gov/policies": "Link to the policies page of the National Cancer Institute.",
        "https://www.cancer.gov/policies/accessibility": "Link to the accessibility policy page of the National Cancer Institute.",
        "https://www.cancer.gov/policies/disclaimer": "Link to the disclaimer policy page of the National Cancer Institute.",
        "https://www.cancer.gov/policies/foia": "Link to the FOIA (Freedom of Information Act) page of the National Cancer Institute.",
        "https://www.hhs.gov/vulnerability-disclosure-policy": "Link to the HHS Vulnerability Disclosure Policy page.",
        "https://www.hhs.gov/": "Link to the U.S. Department of Health and Human Services homepage.",
        "https://www.nih.gov/": "Link to the National Institutes of Health homepage.",
        "https://www.cancer.gov/": "Link to the National Cancer Institute homepage.",
        "https://www.usa.gov/": "Link to the USA.gov homepage, the U.S. government's official web portal."
      },
      "Information on options on web page": {
        "Cancer Types": {
          "type": "list",
          "options": {
            "1": "Acute Myeloid Leukemia",
            "2": "Breast Invasive Carcinoma",
            "3": "Cholangiocarcinoma",
            "4": "Chromophobe Renal Cell Carcinoma",
            "5": "Clear Cell Renal Cell Carcinoma",
            "6": "Colon Adenocarcinoma",
            "7": "Early Onset Gastric Cancer",
            "8": "Glioblastoma",
            "9": "Head and Neck Squamous Cell Carcinoma",
            "10": "Hepatocellular Carcinoma",
            "11": "Lung Adenocarcinoma",
            "12": "Lung Squamous Cell Carcinoma",
            "13": "Myelodysplastic Syndromes",
            "14": "Non-Clear Cell Renal Cell Carcinoma",
            "15": "Not Applicable",
            "16": "Oral Squamous Cell Carcinoma",
            "17": "Other Leukemias",
            "18": "OvarianSerous Cystadenocarcinoma",
            "19": "Pancreatic Ductal Adenocarcinoma",
            "20": "Papillary Renal Cell Carcinoma",
            "21": "Pediatric/AYA Brain Tumors",
            "22": "Rectum Adenocarcinoma",
            "23": "Uterine Corpus Endometrial Carcinoma",
            "24": "Other"
          },
          "selected": None
        }
      }
    },
    "summary": "{\n    \"reasoning\": \"To create a comprehensive summary of the Proteomic Data Commons (PDC) website, it is essential to include details about its purpose, the specific types of data it offers, the tools and resources available for data exploration and analysis, and the various sections and functionalities of the website. This information will help users determine if the PDC is the appropriate data source for their research needs, particularly in the context of cancer proteomics.\",\n    \"summary\": \"The Proteomic Data Commons (PDC) is a specialized platform designed to provide access to proteomic data and resources specifically for cancer research. The primary purpose of the PDC is to facilitate the exploration, analysis, and submission of proteomic data, thereby supporting advancements in cancer research. The website offers a variety of tools and resources that cater to researchers' needs, including data exploration, analysis tools,and submission guidelines. Users can navigate to the home page, log in to the platform, search for specific gene symbols or case IDs, and access guidelines for citing the PDC in their research publications. The PDC also features sections dedicated to recent releases, news, technology advancement studies, and the CPTAC Pan-Cancer Data, which provides comprehensive data generated by the Clinical Proteomic Tumor Analysis Consortium (CPTAC). The website is structured with a header containing navigation links, a search bar, and various sections such as Home, Explore, Analysis, Publications, Submit Data, About, and More. Additionally, it includes visual aids like the 'Cases by Major Primary Site' chart and the 'Cases by Disease Type' list to help users quickly identify relevant data. The footer provides additional links to important resources such as the Site Home, Contact Us, Privacy Policy, and various policies related to accessibility, disclaimer, and FOIA. The PDC offers detailed data on a wide range of cancer types, including Acute Myeloid Leukemia, Breast Invasive Carcinoma, Cholangiocarcinoma, Chromophobe Renal Cell Carcinoma, Clear Cell Renal Cell Carcinoma, Colon Adenocarcinoma, Early Onset Gastric Cancer, Glioblastoma, Head and Neck Squamous Cell Carcinoma, Hepatocellular Carcinoma, Lung Adenocarcinoma, Lung Squamous Cell Carcinoma, Myelodysplastic Syndromes, Non-Clear Cell Renal Cell Carcinoma, OralSquamous Cell Carcinoma, Other Leukemias, Ovarian Serous Cystadenocarcinoma, Pancreatic Ductal Adenocarcinoma, Papillary Renal Cell Carcinoma, Pediatric/AYA Brain Tumors, Rectum Adenocarcinoma, Uterine Corpus Endometrial Carcinoma, and other categories. Each cancer type has a dedicated link that directs users to specific data related to that disease. The PDC also provides access to release notes, detailing recent updates and data releases, and offers a survey for user feedback. For those seeking further information or assistance, the PDC Help Desk can be contacted via email. Overall, the PDC is a comprehensive resource for researchers looking to access and analyze proteomic data related to various types of cancer, making it a valuable tool for advancing cancer research.\"\n}"
  },
  {
    "content": {
      "Web Page Descriptions": {
        "name": "Centers for Disease Control and Prevention",
        "initials": "CDC",
        "purpose": "The purpose of this page is to provide access to various datasets, tools, and resources related to public health data managed by the CDC. It serves as a portal for users to explore, search, and utilize data for research, analysis, and public health initiatives.",
        "actions": [
          "Navigate to the CDC homepage",
          "Search for specific datasets or information",
          "Access the data catalog",
          "Explore resources for developers",
          "Watch video guides",
          "Follow CDC on social media platforms (Facebook, Github, X, YouTube, Instagram)",
          "Sign in to access personalized features",
          "Pause the carousel of featured data",
          "Access specific datasets and tools such as Disability Status and Types Data, BACTFACTS Interactive, HAICViz, NCHHSTP AtlasPlus, and CDC COVID-19 Data Tracker",
          "Browse data by categories such as National Center for Health Statistics, Injury & Violence, National Notifiable Diseases Surveillance System, Vaccination, Smoking & Tobacco Use, Pregnancy & Vaccination, Disability & Health, Chronic Diseases",
          "Learn more about the CDC, job opportunities, funding, policies, privacy, FOIA, No Fear Act, OIG, and vulnerability disclosure policy",
          "Access podcasts/RSS feeds",
          "Contact the CDC"
        ],
        "sections": [
          "Header with CDC logo and navigation links (Home, Data Catalog, Developers, Video Guides)",
          "Search bar",
          "Social media links (Facebook, Github, X, YouTube, Instagram)",
          "Sign In button",
          "Carousel of featured data",
          "Links to specific datasets and tools (Disability Status and Types Data, BACTFACTS Interactive, HAICViz, NCHHSTP AtlasPlus, CDC COVID-19 Data Tracker)",
          "Categories of data (National Center for Health Statistics, Injury & Violence, National Notifiable Diseases Surveillance System, Vaccination, Smoking & Tobacco Use, Pregnancy & Vaccination, Disability & Health, Chronic Diseases, Browse All)",
          "Footer with additional links (About CDC, Jobs, Funding, Policies, Privacy, FOIA, No Fear Act, OIG, Vulnerability Disclosure Policy, Podcasts/RSS, Contact Us)"
        ]
      },
      "Information on Links on Web Page": {
        "http://www.cdc.gov/": "Link to the CDC's main website, providing information on various health topics and resources.",
        "https://data.cdc.gov/": "Link to the CDC's data portal homepage, offering access to a wide range of public health data.",
        "https://data.cdc.gov/browse": "Link to the CDC's data catalog, where users can browse various datasets.",
        "http://dev.socrata.com/": "Link to the Socrata developer portal, providing resources for developers working with open data.",
        "https://data.cdc.gov/videos": "Link to the CDC's video guides, offering instructional videos on using CDC data.",
        "http://www.facebook.com/CDC": "Link to the CDC's Facebook profile, where users can follow and interact with the CDC on Facebook.",
        "https://github.com/CDCgov": "Link to the CDC's GitHub profile, providing access to the CDC's open-source projects and code repositories.",
        "http://twitter.com/CDCgov": "Link to the CDC's X (formerly Twitter) profile, where users can follow and interact with the CDC on X.",
        "http://www.youtube.com/CDCstreamingHealth": "Link to the CDC's YouTube profile, offering videos on various health topics.",
        "https://instagram.com/CDCgov/": "Link to the CDC's Instagram profile, where users can follow and interact with the CDC on Instagram.",
        "https://data.cdc.gov/login": "Link to the CDC's data portal login page, allowing users to sign in to their accounts.",
        "https://data.cdc.gov/browse?tags=covid-19": "Link to the CDC's COVID-19 public data sets, featuring various datasets related to COVID-19.",
        "https://data.cdc.gov/browse?category=NCHS&sortBy=last_modified": "Link to the National Center for Health Statistics data, offering datasets on health statistics.",
        "https://data.cdc.gov/browse?category=Injury+%26+Violence": "Link to the CDC's injury and violence data, providing datasets on related topics.",
        "https://data.cdc.gov/browse?category=NNDSS&sortBy=last_modified": "Link to the National Notifiable Diseases Surveillance System data, offering datasets on notifiable diseases.",
        "https://data.cdc.gov/browse?category=Vaccinations": "Link to the CDC's vaccination data, providing datasets on vaccination statistics.",
        "https://data.cdc.gov/browse?category=Smoking+%26+Tobacco+Use": "Link to the CDC's smoking and tobacco use data, offering datasets on related topics.",
        "https://data.cdc.gov/browse?category=Pregnancy+%26+Vaccination": "Link to the CDC's pregnancy and vaccination data, providing datasets on related topics.",
        "https://data.cdc.gov/browse?category=Disability+%26+Health": "Link to the CDC's disability and health data, offering datasets on related topics.",
        "https://data.cdc.gov/browse?category=Chronic+Diseases": "Link to the CDC's chronic diseases data, providing datasets on related topics.",
        "https://www.cdc.gov/abcs/bact-facts-interactive-dashboard.html": "Link to the BACTFACTS Interactive tool, visualizing trends in invasive bacterial pathogens.",
        "https://www.cdc.gov/hai/eip/haicviz.html": "Link to HAICViz, a tool for analyzing and visualizing healthcare-associated infections data.",
        "https://www.cdc.gov/nchhstp/atlas/index.htm": "Link to NCHHSTP AtlasPlus, an interactive tool for creating customized tables, maps, and charts using CDC surveillance data.",
        "https://data.cdc.gov/browse?q=izdl&sortBy=relevance": "Link to the CDC COVID-19 Data Tracker Vaccination Data, providing data on COVID-19 vaccine delivery and administration.",
        "http://www.cdc.gov/about/default.htm": "Link to the 'About CDC' page, providing information about the CDC's mission and activities.",
        "http://jobs.cdc.gov/": "Link to the CDC's jobs page, offering information on employment opportunities at the CDC.",
        "http://www.cdc.gov/funding/": "Link to the CDC's funding page, providing information on funding opportunities and grants.",
        "http://www.cdc.gov/Other/policies.html": "Link to the CDC's policies page, offering information on various policies.",
        "http://www.cdc.gov/Other/privacy.html": "Link to the CDC's privacy page, providing information on privacy policies.",
        "http://www.cdc.gov/od/foia/": "Link to the CDC's FOIA page, offering information on the Freedom of Information Act.",
        "http://www.cdc.gov/eeo/nofearact/index.htm": "Link to the CDC's No Fear Act page, providing information on the No Fear Act.",
        "https://oig.hhs.gov/": "Link to the Office of Inspector General (OIG) website, providing information on oversight and investigations.",
        "https://www.hhs.gov/vulnerability-disclosure-policy/index.html": "Link to the HHS Vulnerability Disclosure Policy page, providing information on reporting vulnerabilities.",
        "http://www2c.cdc.gov/podcasts/": "Link to the CDC's Podcasts/RSS page, offering access to CDC podcasts and RSS feeds.",
        "https://www.cdc.gov/cdc-info/index.html": "Link to the CDC's 'Contact Us' page, providing contact information for the CDC."
      },
      "Information on options on web page": {
        "Data Categories": {
          "type": "buttons",
          "options": {
            "9": "COVID-19 Public Data Sets",
            "10": "Disability Status and Types Data",
            "11": "Motor Vehicle Data"
          },
          "selected": None
        }
      },
      "documentation": "https://dev.socrata.com/docs/endpoints:\n\n        Toggle navigation\n\nSODA Developers\n\nApp Developers \n  \n    \n  App Developers\n  Getting Started\n  Finding Open Data\n\n  Examples\n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Data Visualization with Plotly and Pandas\n      \n    \n  \n    \n      \n        Data Analysis with Python and pandas using Jupyter Notebook\n      \n    \n  \n    \n  \n    \n  \n    \n      \n        Using R and Shiny to Find Outliers with Scatter and Box Plots\n      \n    \n  \n    \n  \n    \n      \n        Analyzing Open Data with SAS\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Building SMS Applications with Twilio\n      \n    \n  \n    \n      \n        Forecasting with RSocrata\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Making a heatmap with R\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Create a column chart with Highcharts\n      \n    \n  \n    \n  \n    \n      \n        Generating a within_box() query with Leaflet.js\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Using a jQueryUI date slider to build a SODA Query\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Data Analysis with Python, Pandas, and Bokeh\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Animated Heatmap with Heatmap.js\n      \n    \n  \n    \n      \n        Build a physical \"Traffic Light\"\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Google Maps Mashup\n      \n    \n  \n    \n      \n        Google Maps with KML\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Simple column chart with D3\n      \n    \n  \n\n  SDKs & Libraries\n  \n    \n  \n    \n  \n    \n  \n    \n      \n        PhpSoda\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Google Android\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        .NET\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        DataSync SDK (Java)\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Elixr\n      \n    \n  \n    \n  \n    \n  \n    \n      \n        ember-socrata\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        go-soda\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Apple iOS\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Java\n      \n    \n  \n    \n      \n        javascript\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Julia\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        PHP\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        PowerShell\n      \n    \n  \n    \n  \n    \n  \n    \n      \n        Python (Dataset Management API)\n      \n    \n  \n    \n      \n        Python\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        R\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Ruby\n      \n    \n  \n    \n  \n    \n  \n    \n      \n        Scala\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Swift\n\nData Publishers \n  \n    \n  Data Publishers\n  Publisher Guide\n\n  APIs for Publishing Data\n  SODA Producer API\n  Dataset Management API\n  Import API\n\n  Tools & Connectors\n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Connectors & ETL Templates\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Pentaho Kettle\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        RSocrata\n      \n    \n  \n    \n  \n    \n  \n    \n      \n        Safe FME\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Socrata Datasync\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n\n  SDKs & Libraries\n  \n    \n  \n    \n  \n    \n  \n    \n      \n        PhpSoda\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        .NET\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        DataSync SDK (Java)\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        ember-socrata\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        go-soda\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Java\n      \n    \n  \n    \n      \n        javascript\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        PHP\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        PowerShell\n      \n    \n  \n    \n  \n    \n  \n    \n      \n        Python (Dataset Management API)\n      \n    \n  \n    \n      \n        Python\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        R\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Ruby\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n\n  Examples\n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Visualizing data using the Google Calendar Chart\n      \n    \n  \n    \n      \n        Scrubbing data with Python\n      \n    \n  \n    \n      \n        Gauge Visualizations using the Google Charts library\n      \n    \n  \n    \n  \n    \n      \n        Pulling data from Hadoop and Publishing to Socrata\n      \n    \n  \n    \n      \n        Using Pentaho to Read data from Salesforce and Publish to Socrata\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Using a SSIS to write to a Socrata Dataset\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Pentaho Kettle ETL Toolkit\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Using a Wufoo form to write to a Socrata Dataset\n      \n    \n  \n    \n  \n    \n      \n        Pushing Sensor Data to Socrata\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Using the FME Socrata Writer\n      \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      \n        Upsert via soda-ruby\n\nAPI Docs \n  \n    \n  Overview\n  API Endpoints\n  Row Identifiers\n  RESTful Verbs\n  Application Tokens\n  Authentication\n  Response Codes & Headers\n  System Fields\n  CORS & JSONP\n  \n\n  Filtering & Querying\n  Simple Filters\n  SoQL Queries\n  Paging Through Data\n  SoQL Function and Keyword Listing\n  Data Transform Functions\n\n  Data Formats\n  JSON\n  GeoJSON\n  CSV\n  RDF-XML\n\n  Datatypes\n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      Checkbox\n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      Fixed Timestamp\n    \n  \n    \n      Floating Timestamp\n    \n  \n    \n  \n    \n  \n    \n  \n \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n   \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      Line\n    \n  \n    \n  \n    \n  \n    \n      Location\n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      MultiLine\n    \n  \n    \n  \n    \n      MultiPoint\n    \n  \n    \n      MultiPolygon\n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      Number\n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n\n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      Point\n    \n  \n    \n  \n    \n  \n    \n      Polygon\n    \n  \n    \n\n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n  \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      Text\n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n      URL\n    \n  \n \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n   \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n    \n  \n  \n\n  Other APIs\n\nLibraries & SDKs\n\nSocrata was acquired by Tyler Technologies in 2018 and is now the Data and Insights division of Tyler. The platform is still powered by the same software formerly known as Socrata but you will see references to Data & Insights going forward.\n\nLearn more...\n\nstatus.socrata.com.\n\nAPI Endpoints\n\nOverview\n\nAPI Endpoints\n\nRow Identifiers\n\nRESTful Verbs\n\nApplication Tokens\n\nAuthentication\n\nResponse Codes & Headers\n\nSystem Fields\n\nCORS & JSONP\n\nFiltering & Querying\n\nSimple Filters\n\nSoQL Queries\n\nPaging Through Data\n\nSoQL Function and Keyword Listing\n\nData Transform Functions\n\nData Formats\n\nJSON\n\nGeoJSON\n\nCSV\n\nRDF-XML\n\nDatatypes\n\nCheckbox\n\nFixed Timestamp\n\nFloating Timestamp\n\nLine\n\nLocation\n\nMultiLine\n\nMultiPoint\n\nMultiPolygon\n\nNumber\n\nPoint\n\nPolygon\n\nText\n\nURL\n\nOther APIs\n\nWhat is an API Endpoint?\n\nThe “endpoint” of a SODA API is simply a unique URL that represents an object or collection of objects. Every Socrata dataset, and even every individual data record, has its own endpoint. The endpoint is what you’ll point your HTTP client at to interact with data resources.\n\nAll resources are accessed through a common base path of /resource/ along with their dataset identifier. This paradigm holds true for every dataset in every SODA API. All datasets have a unique identifier - eight alphanumeric characters split into two four-character phrases by a dash. For example, ydr8-5enu is the identifier for the Building Permits. This identifier can then be appended to the /resource/ endpoint to construct the API endpoint.\n\ntry it\n\ndocs\n\ncopy\n\njson\n\ncsv\n\ngeojson\n\njson\n\nhttps://data.cityofchicago.org/resource/ydr8-5enu.json\n\nOnce you’ve got your API endpoint, you can add on filtering and SoQL parameters to filter and manipulate your dataset.\n\nLocating the API endpoint for a dataset\n\nYou can also find API endpoints, and links to detailed developer documentation for each dataset, in a number of different places, depending on where you are:\n\nIf you’re viewing a dataset listing within the Open Data Network, there will be a prominent “API” button that will takeyou directly to the API documentation for that dataset. \n See this\n\nIf you’re viewing a dataset directly, there will be an “API Documentation” button under “Export” and then “SODA API”. \n See this\n\nIf you’re viewing a dataset in Data Lens, there will be an API button you can click to get the API endpoint and a link to API documentation. \n See this\n\nEndpoint Versioning\n\nSODA and SoQL are very flexible and allow us to add functionality over time without needing to completely deprecate and replace our APIs. We can do so in several different ways:\n\nBy introducing new SoQL functions that provide new functionality. We could, for example, add a new function that allows you to filter or aggregate a dataset in a new way.\n\nBy adding new datatypes to represent new data, like a new datatype for a new class of geospatial data.\n\nThis allows us to introduce additional capabilities while still allowing you to issue the same kinds of queries in a backwards-compatible manner. We can extend SODA APIs without needing all developers to migrate their code to a new version.\n\nHowever, some functionalities are not available on all of our API endpoints, which is why we differentiate between versions of a dataset’s API. Functions made available on a newer version might not be available on an API endpoint of an older version. In the sidebar of our automatic API documentation, we list the version that that endpoint complies with, as well as other useful information. \n   See this\n\nThroughout the documentation on this developer portal you’ll notice version togglesand info boxes that will help you understand the difference between SODA endpoint versions.\n\nVersion 2.1 (Latest)\n\nThe first SODA 2.1 APIs (previously referred to as our “high-performance Socrata Open Data APIs”) were released in April of 2015, and in November of 2015 they received the “2.1” version designation for clarity. SODA 2.1 introduces a number of new datatypes as well as numerous new SoQL functions:\n\nTons of new advanced SoQL functions to introduce powerful filtering and analysis into your queries\n\nNew geospatial datatypes like Point\n, Line\n, and Polygon\n replace the Location\n datatype\n\nSupport for the standardized GeoJSON output format, for direct use within geospatial tools like Leaflet\n\nCloser compliance with SQL semantics, such as Text\n comparisons becoming case-sensitive\n\nCurrently only the JSON, CSV, and GeoJSON output formats are supported\n\nNew functionality will be added to this version over time.\n\nFor more information:\n\nSoQL functions that work with version 2.1\n\nDatatypes that are available in version 2.1\n\nVersion 2.0\n\nSODA 2.0 was originally released in 2011. Although 2.1 is backwards-compatible with 2.0, there are a number of differences between the two APIs:\n\n2.0 supports fewer SoQL functions than 2.1.\n\nThe only geospatial datatype supported is the Location\n datatype\n\nText\n comparisons are case-insensitive\n\nFor more information:\n\nSoQL functions that work with version 2.0\n\nDatatypes that are available in version 2.0\n\nVersioning HTTP headers\n\nThe simplest way to tell the difference between a 2.0 API and a 2.1 API is via the X-SODA2-Legacy-Types header, which will be true if you’re accessing a legacy 2.0 API.\n\nWhen we will increment endpoint versions\n\nFrom time to time, we’ll introduce new SoQL functions and datatypes to the latest version of the SODA API. Those changes will be non-breaking, and old queries and applications will continue to function unchanged. The SODA API is designed to make it easy to introduce new functionality over time without making breaking changes.\n\nLicensed by\n\nTyler Technologies\n        under\n\nCC BY-NC-SA 3.0. Learn how\n\nyou can contribute!\n\nbye bye!"
    },
    "summary": "{\"reasoning\":\"To create a comprehensive summary of the CDC website, I included information about the website's purpose, the types of data available, the tools and resources provided, and the various sections and links that users can navigate to. This information is crucial for understanding the breadth and depth of the data available on the CDC website, which will help in determining if this is the correct data source for a user's query.\",\n \"summary\":\"The Centers for Disease Control and Prevention (CDC) website serves as a comprehensive portal for accessing a wide range of public health data, tools,and resources. The primary purpose of the site is to provide users with the ability to explore, search, and utilize data for research, analysis, and public health initiatives. The website offers a variety of actions such as navigating to the CDC homepage, searching for specific datasets, accessing the data catalog, exploring resources for developers, watching video guides, and following the CDC on multiple social media platforms including Facebook, GitHub, X (formerly Twitter), YouTube, and Instagram. Users can also sign in to access personalized features and pause the carousel of featured data. Specificdatasets and tools available on the site include Disability Status and Types Data, BACTFACTS Interactive, HAICViz, NCHHSTP AtlasPlus, and the CDC COVID-19 Data Tracker. The data is categorized into several sections such as National Center for Health Statistics, Injury & Violence, National Notifiable Diseases Surveillance System, Vaccination, Smoking & Tobacco Use, Pregnancy & Vaccination, Disability & Health, and Chronic Diseases. The website also provides information about the CDC, job opportunities, funding, policies, privacy, FOIA, No Fear Act, OIG, and vulnerability disclosure policy. Additionally, users can access podcasts and RSS feeds, and contact the CDC for more information. The website includes a header with the CDC logo and navigation links, a search bar, social media links, a sign-in button, a carousel of featured data, and links to specific datasets and tools. The footer contains additional links to various CDC-related pages. The CDC website is a valuable resource for accessing public healthdata and tools, making it a crucial data source for users seeking information on health statistics, disease surveillance, vaccination data, and more. The site also provides extensive resources for developers, including links to the Socrata developer portal, video guides, and various SDKs and libraries for different programming languages. The CDC's data portal offers access to a wide range of public health data, including COVID-19 datasets, health statistics, injury and violence data, notifiable diseases data, vaccination data, smoking and tobacco use data, pregnancy and vaccination data, disability and health data, and chronic diseases data. The site also features interactive tools like BACTFACTS Interactive, HAICViz, and NCHHSTP AtlasPlus, which allow users to visualize and analyze data. The CDC websiteis an essential resource for researchers, public health professionals, and developers seeking comprehensive public health data and tools.\"}"
  }
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
