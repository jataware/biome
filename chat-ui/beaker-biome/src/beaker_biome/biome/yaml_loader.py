import copy
import yaml
import pathlib
import datetime
import json

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

def load(api_definition_filepath: str, documentation_root: str):
    config = None
    api_definitions = None
    parsed_apis = {}
    with open(api_definition_filepath, 'r') as f:
        try:
            contents = yaml.safe_load(f)
            config = contents['config']
            api_definitions = contents['apis']
        except Exception as e:
            print(f"failed to load API definitions file properly. check filepath and/or format: {str(e)}")
            return {}, {}, []
    
    parsed_apis['default'] = dict(api_definitions['default'])
    for api_name, definition in api_definitions.items():
        if api_name == 'default':
            continue
        
        # merge w/ overwriting defaults
        parsed_apis[api_name] = copy.deepcopy(parsed_apis['default'])

        for key, value in definition.items():
            if isinstance(value, str | int | list | bool):
                parsed_apis[api_name][key] = value
            elif isinstance(value, dict):
                parsed_apis[api_name][key] |= value
        
        if parsed_apis[api_name]['disabled']:
            del parsed_apis[api_name]
            continue 

        # fill docs body
        try:
            root_folder = pathlib.Path(__file__).resolve().parent
            filepath = '/'.join([
                str(root_folder),
                documentation_root,
                parsed_apis[api_name]["documentation_file"]
            ])
            with open(filepath, 'r') as f:
                parsed_apis[api_name]['docs'] = f.read()
        except Exception as e:
            raise ValueError(f"failed to open docs for api {api_name}: file path {parsed_apis[api_name]['documentation_file']}: {str(e)}")
        
        # formatting interpolations - don't format API docs though.
        parsed_apis[api_name] = {
            k: (v.format_map(parsed_apis[api_name]) 
                    if k not in config['deferred_formatting_fields'] 
                    else v)
                if isinstance(v, str) 
                else v
            for k, v in parsed_apis[api_name].items() 
        }

        # cache_body should be last.
        parsed_apis[api_name]['cache_body'] = parsed_apis[api_name]['cache_body'].format_map(parsed_apis[api_name])
    
    del parsed_apis['default']

    # todo - api contracts with adhoc 

    drafter_config = {'model': "models/gemini-1.5-flash-001", 'ttl_seconds': 1800}
    finalizer_config = {'model': 'gpt-4o'}
    specs = [
        {
            'name': name,
            'cache_key': api['cache']['key'],
            'description': api['description'],
            'documentation': api['cache_body'],
            'proofread_instructions': api['gpt_additional_pass']

        }
        for name, api in parsed_apis.items()
    ]

    return drafter_config, finalizer_config, specs
