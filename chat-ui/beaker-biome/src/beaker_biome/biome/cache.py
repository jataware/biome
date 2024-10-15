import copy
import yaml
import google.generativeai as genai
from google.generativeai import caching
import pathlib
import datetime
import json
# requires gemini API key initialization done beforehand

class APICache:
    cache: dict
    chats: dict 
    models: dict
    config: dict
    def __init__(self, api_definition_filepath: str):
        self.cache = {}
        self.chats = {}
        self.models = {}
        self.config = {}
        with open(api_definition_filepath, 'r') as f:
            try:
                contents = yaml.safe_load(f)
                self.config = contents['config']
                api_definitions = contents['apis']
            except Exception as e:
                print(f"failed to load API definitions file properly. check filepath and/or format: {str(e)}")
                return
        self.cache['default'] = dict(api_definitions['default'])
        for api_name, definition in api_definitions.items():
            if api_name == 'default':
                continue
            
            # merge w/ overwriting defaults
            self.cache[api_name] = copy.deepcopy(self.cache['default'])

            for key, value in definition.items():
                if isinstance(value, str | int | list | bool):
                    self.cache[api_name][key] = value
                elif isinstance(value, dict):
                    self.cache[api_name][key] |= value
            
            if self.cache[api_name]['disabled']:
                del self.cache[api_name]
                continue 

            # fill docs body
            try:
                root_folder = pathlib.Path(__file__).resolve().parent
                filepath = '/'.join([
                    str(root_folder),
                    self.config["documentation_root"],
                    self.cache[api_name]["documentation_file"]
                ])
                with open(filepath, 'r') as f:
                    self.cache[api_name]['docs'] = f.read()
            except Exception as e:
                raise ValueError(f"failed to open docs for api {api_name}: file path {self.cache[api_name]['documentation_file']}: {str(e)}")
            
            # formatting interpolations - don't format API docs though.
            self.cache[api_name] = {
                k: (v.format_map(self.cache[api_name]) 
                        if k not in self.config['deferred_formatting_fields'] 
                        else v)
                    if isinstance(v, str) 
                    else v
                for k, v in self.cache[api_name].items() 
            }
            # cache_body should be last.
            self.cache[api_name]['cache_body'] = self.cache[api_name]['cache_body'].format_map(self.cache[api_name])
        with open('cachedump.json', 'w') as f:
            json.dump(self.cache, f)
        del self.cache['default']

    def available_apis(self) -> dict[str, str]:
        """Returns a mapping of available APIs to their descriptions and full, human readable names."""
        return {key: f"{self.cache[key]['name']}: {self.cache[key]['description']}" for key in self.cache.keys()}

    def available_api_context(self) -> str:
        """Nicer formatting for a system prompt of APIs and their descriptions."""
        return "\n".join([f'    - {k}: {v}' for k, v in self.available_apis().items()])

    def loaded_apis(self):
        """Returns a list of loaded APIs."""
        return self.chats.keys()

    def load_api(self, api_name: str):
        if api_name not in self.available_apis():
            raise ValueError("requested API is not in available APIs - check definitions file and API name")
        content = caching.CachedContent.list()
        is_cached = False
        for cache_object in content: 
            if cache_object.display_name == self.cache[api_name]['cache']['key']:
                is_cached = True 
                break
        if not is_cached:
            cache_object = self.build_cache(api_name)
        self.models[api_name] = genai.GenerativeModel.from_cached_content(cached_content=cache_object)
        self.chats[api_name] = self.models[api_name].start_chat()

    def build_cache(self, api_name):
        if api_name not in self.available_apis():
            raise ValueError("requested API is not in available APIs - check definitions file and API name")
        api = self.cache[api_name]
        cache = caching.CachedContent.create(
            model=api['cache']['model'],
            display_name=api['cache']['key'],
            contents=[api['cache_body']],
            ttl=datetime.timedelta(minutes=api['cache']['ttl']),
            system_instruction=api['system_prompt']
        )
        return cache
