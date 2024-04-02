schema = {
    "name": {
        "type": "string",
        "description": "Name of the website organization",
    },
    "initials": {
        "type": "string",
        "description": "Initials of organization as provided by website",
    },
    "description": {
        "type": "string",
        "description": "Description of the cancer data web portal",
    },
    "logo_url": {
        "type": "string",
        "description": "Full absolute path of logo of image url including protocol and domain (http(s)://domain.../image.extension)",
    },
    "datasets": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Some portals mention including varius datasets by name, using a 'Datasets' (or 'Datasets include') headig to describe the various datasets the portal includes.",
    },
    # "metadata": {
    #     "type": "object",
    #     "properties": {
    #         "created_at": {"type": "number"},
    #         "updated_at": {"type": "number"},
    #         "scanned_uris": {"type": "array", "items": {"type": "string"}},
    #     },
    # },
    "categories": {
        "type": "array",
        "items": {
            "type": "string",
            "enum": ["genomics", "clinical", "imaging"],
        },
    },
    "tags": {
        "type": "array",
        "items": {
            "type": "string",
            "description": "Tags that we can group these sources with. Enum describes some examples but may use other common attributes",
            "enum": ["human", "canine", "cancer"],
        },
    },
    "urls": {
        "type": "object",
        "properties": {
            "home_page": {"type": "string"},
            "site_map": {
                "type": "string",
                "description": "Full path to sitemap if found, linked from site.",
            },
            "data_landing": {
                "type": "string",
                "description": "Full http path to data portal page, which is usually different from home page url",
            },
            "git_repository": {
                "type": "string",
                "description": "Some portals have links or document their tools github (or other code repository) url. Should include full http path to it here if found.",
            },
            "git_org": {"type": "string"},
            "submission_portal": {
                "type": "string",
                "description": "Most portals include a link to a data submit or submission page. Include should http path to it here.",
            },
            "openapi_spec": {
                "type": "string",
                "description": "If a swagger or openapi spec url is found, add full http path to it here. If no direct openapi spec url is found, but a page mentions they do have an openapi or swagger page, include the uri to it here instead.",
            },
        },
    },
    "use_cases": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Some portals include an explicit use case section with various use cases listed. If found, include those here.",
    },
    "documentation": {
        "type": "array",
        "description": "urls linked from document which contain documentation (for api, data access, data model, etc)",
        "items": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "url": {"type": "string"},
            },
        },
    },
    "collections": {
        "type": "array",
        "items": {
            "type": "string",
            "description": "Describes ways the portal offers to group data or save data for use for later.",
            "enum": ["case sets", "cohorts", "projects"],
        },
    },
    "data_categories": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Some data portals pages include an explicit section on data categories. If found, list the items here. If none found, but some controls are found to filter/search through data (checkboxes), group those here.",
    },
    "data_types": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Some portals mention data types explicitly. List these here.",
    },
    "file_formats": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Available data formats to explore and/or export, such as json, tsv, bam, tif, png, bedpe, excel, idat, txt, etc ...",
    },
    "external_references": {
        "type": "array",
        "description": "Any http references linked from the document. Of interest are explicitly mentioned as references or additional linked references for data or imaging from other data source portals.",
        "items": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "base_url": {"type": "string"},
            },
        },
    },
    "access_type": {
        "type": "string",
        "enum": ["open", "controlled", "mixed"],
        "description": "Whether the data access is open, controlled, or both (mixed)",
    },
    "capabilities": {
        "type": "array",
        "items": {
            "type": "string",
            "enum": [
                "workspaces",
                "cohorts",
                "graphql",
                "sql",
                "http_api",
                "ui_case_search",
                "ui_organ_search",
            ],
        },
        "description": "Capabilities the data portal service has, such as being able to create, save and manage workspaces,  or include access to an http rest api, graphl data api, etc",
    },
    "data_use_limitations": {
        "type": "string",
        "description": "Sentence describing data use restrictions of available (eg. for research only, or other limitations)",
    },
    "omics_methods": {
        "type": "array",
        "items": {"type": "string"},
        "description": "'omics (genomics, proteomic, etc) methods listed on html data and/or available on data portal",
    },
    "contact": {
        "type": "object",
        "description": "Contact information of team that manages the data, the portal, or the documentation.",
        "properties": {"email": {"type": "string"}, "name": {"type": "string"}},
    },
}

#  In case we want to specify a sipler schema to use outside
# the function tools chatCompletion API, or to start from there
# and generate the more complex spec above?
simple_schema = {}

# def simple_to_completion_schema(simple):
