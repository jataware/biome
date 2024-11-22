import copy
from typing import TypedDict
import yaml
import pathlib
import datetime
import json
import os

from adhoc_api.tool import DrafterConfig, FinalizerConfig, APISpec

class MessageLogger():
    def __init__(self, context):
        self.context = context 
    def info(self, message):
        self.context.send_response("iopub",
            "gemini_info", {
                "body": message
            },
        ) 
    def error(self, message):
        self.context.send_response("iopub",
            "gemini_error", {
                "body": message
            },
        ) 

class APILoaderOutput(TypedDict):
    drafter_config: dict
    finalizer_config: dict 
    api_specs: list 

def load(agent_config_filepath: str) -> APILoaderOutput:    
    # the folder where this file lives.
    root_folder = pathlib.Path(__file__).resolve().parent
    
    with open(agent_config_filepath, 'r') as f:
        try: 
            config = yaml.safe_load(f)
        except Exception as e:
            msg = f"ERROR: api loader: failed to load API agent config file properly. check filepath and/or format: {str(e)}"
            raise ValueError(msg)

    # pull all {subfolder}/api.yaml definitions and ensure they have 'name' set
    # additional validation happens below.
    api_location = os.path.join(root_folder, config['definitions_root'])
    api_definitions = []
    for filename in os.listdir(api_location):
        api_folder = os.path.join(api_location, filename)
        if os.path.isdir(api_folder):
            definition_file = os.path.join(api_folder, "api.yaml")
            with open('dump', 'a') as f:
                f.write(json.dumps({
                    'f': api_folder,
                    'df': definition_file
                }))

            # api definition is missing, ignore
            if not os.path.isfile(definition_file):
                continue
            with open(definition_file, 'r') as f:
                definition = yaml.safe_load(f)
            if 'name' not in definition:
                msg = f"ERROR: api loader: {definition_file} has no 'name' key."
                raise ValueError(msg)
            api_definitions.append({
                'folder': api_folder,
                'definition': definition
            })
    
    # steps:
    # * load all keys - if they are file definitions instead, load them as the file's contents 
    # * copy cache_body from config default if needed 
    # * format cache_body with them
    for definition_info in api_definitions:
        definition = definition_info['definition']
        root_folder = definition_info['folder']
        additional_files_path = os.path.join(root_folder, 'documentation')

        # validation pass
        required_keys = [
            'name',
            'cache_key',
            'description',
            'instructions'
        ]
        missing_key = None
        for key in required_keys:
            if key not in definition:
                missing_key = key 
        if missing_key:
            msg = f'ERROR: api loader: api {definition["name"]} is missing required key {key}'
            raise ValueError(msg)
        
        # omitted cache_body || cache_body.default = true -- if either, use config default.
        # this ignores cache_body.file = path, handled below
        if (
            ('cache_body' not in definition) or 
            (isinstance(definition['cache_body'], dict) and definition['cache_body'].get('default', False))
        ):
            definition['cache_body'] = config['default_cache_body']

        # replace `file:` directives with string contents of filepath
        for key, value in definition.items():
            if isinstance(value, dict) and 'file' in value:
                filepath = os.path.join(additional_files_path, value['file'])
                if not os.path.isfile(filepath):
                    msg = f'ERROR: api loader: api `{definition["name"]}` (in {root_folder}/{definition["name"]}) references file `{filepath}` which does not exist or is a directory.'
                    raise ValueError(msg)
                with open(filepath, 'r') as f:
                    definition[key] = f.read()
        
        # finally interpolate instructions, then cache_body - this allows loading file contents into the definitions
        definition['instructions'] = definition['instructions'].format_map(definition)
        definition['cache_body'] = definition['cache_body'].format_map(definition)

    drafter_config = {'model': "models/gemini-1.5-flash-001", 'ttl_seconds': 1800}
    if 'drafter' in config:
        for key, value in config['drafter'].items():
            drafter_config[key] = value

    finalizer_config = {'model': 'gpt-4o'}
    if 'finalizer' in config:
        for key, value in config['finalizer'].items():
            finalizer_config[key] = value

    api_specs = [
        {
            'name': api['definition']['name'],
            'cache_key': api['definition']['cache_key'],
            'description': api['definition']['description'],
            'documentation': api['definition']['cache_body'],
            'proofread_instructions': api['definition']['instructions']

        }
        for api in api_definitions
    ]

    lr = {
        'api_specs': api_specs,
        'finalizer_config': finalizer_config,
        'drafter_config': drafter_config
    }

    with open('dump', 'w') as f:
        f.write(json.dumps(lr))

    return {
        'api_specs': api_specs,
        'finalizer_config': finalizer_config,
        'drafter_config': drafter_config
    }
