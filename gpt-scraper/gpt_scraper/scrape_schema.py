schema = {
    "name": {
        "type": "string",
        "description": "Name of the website or organization",
    },
    "initials": {
        "type": "string",
        "description": "initials of organization as provided by website",
    },
    "description": {"type": "string"},
    "logo_url": {"type": "string"},
    "datasets": {"type": "array", "items": {"type": "string"}},
    "metadata": {
        "type": "object",
        "properties": {
            "created_at": {"type": "number"},
            "updated_at": {"type": "number"},
            "scanned_uris": {
                "type": "array",
                "items": {"type": "string"}
            },
            "manual_verified": {"type": "boolean"}
        },
    },
    "categories": {"type": "array", "items": {"type": "string"}},
    "tags": ["string"],
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
    "documentation": [{"type": "string", "url": "string"}],
    "collections": {"type": "array", "items": {"type": "string"}},
    "data_category": {"type": "array", "items": {"type": "string"}},
    "data_type": {"type": "array", "items": {"type": "string"}},
    "file_formats": {"type": "array", "items": {"type": "string"}},
    "external_references": [{"name": "string", "base_url": "string"}],
    "access_type": {
        "type": "string",
        "description": "whether the data access is open, controlled, or both (mixed)",
    },
    "capabilities": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Capabilities the data portal service has, such as workspaces, rest api, graphl api, etc",
    },
    "data_use_limitations": {"type": "string"},
    "omics_methods": {
        "type": "array",
        "items": {"type": "string"},
        "description": "eg genomics, proteomic, etc",
    },
    "contact": {
        "type": "object",
        "properties": {"email": {"type": "string"}, "name": {"type": "string"}},
    },
}
