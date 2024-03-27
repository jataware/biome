schema = {
    "name": {
        "type": "string",
        "description": "Name of the website or organization",
    },
    "initials": {
        "type": "string",
        "description": "Initials of organization as provided by website",
    },
    "description": {
        "type": "string",
        "description": "Description of the cancer data web portal",
    },
    "logo_url": {"type": "string"},
    "datasets": {"type": "array", "items": {"type": "string"}},
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
            "enum": ["human", "canine", "animal", "genetics", "cancer"],
        },
    },
    "urls": {
        "type": "object",
        "properties": {
            "homepage": {"type": "string"},
            "sitemap": {"type": "string"},
            "data_landing": {"type": "string"},
            "git_repository": {"type": "string"},
            "git_org": {"type": "string"},
            "submission_portal": {"type": "string"},
            "openapi_spec": {"type": "string"},
        },
    },
    "use_cases": {"type": "array", "items": {"type": "string"}},
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
            "enum": ["case sets", "cohorts", "projects"],
        },
    },
    "data_categories": {"type": "array", "items": {"type": "string"}},
    "data_types": {"type": "array", "items": {"type": "string"}},
    "file_formats": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Available data formats to explore and/or export, such as json, tsv, bam, tif, png, bedpe, excel, idat, txt ...",
    },
    "external_references": {
        "type": "array",
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
        "description": "whether the data access is open, controlled, or both (mixed)",
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
        "description": "Capabilities the data portal service has, such as workspaces, rest_api, graphl, etc",
    },
    "data_use_limitations": {
        "type": "string",
        "description": "sentence describing data use restrictions of available (eg. for research only)",
    },
    "omics_methods": {
        "type": "array",
        "items": {"type": "string"},
        "description": "'omics (genomics, proteomic, etc) methods listed on html data and/or available on data portal",
    },
    "contact": {
        "type": "object",
        "properties": {"email": {"type": "string"}, "name": {"type": "string"}},
    },
}

#  In case we want to specify a sipler schema to use outside
# the function tools chatCompletion API, or to start from there
# and generate the more complex spec above?
simple_schema = {}

# def simple_to_completion_schema(simple):
