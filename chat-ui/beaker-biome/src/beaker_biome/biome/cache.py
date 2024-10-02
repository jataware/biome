import copy
import yaml
import google.generativeai as genai
from google.generativeai import caching
import pathlib
import datetime

# requires gemini API key initialization done beforehand

class APICache:
    cache: dict
    chats: dict 
    models: dict
    def __init__(self, api_definition_filepath: str):
        self.cache = {}
        self.chats = {}
        self.models = {}
        with open(api_definition_filepath, 'r') as f:
            try:
                api_definitions = yaml.safe_load(f)['apis']
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
                filepath = f'{root_folder}/docs/{self.cache[api_name]["docs"]}'
                with open(filepath, 'r') as f:
                    self.cache[api_name]['docs'] = f.read()
            except Exception as e:
                print(f"failed to open docs for api {api_name}: file path {self.cache[api_name]['docs']}: {str(e)}")
            
            # formatting interpolations - don't format API docs though.
            self.cache[api_name] = {
                k: v.format_map(self.cache[api_name]) 
                    if isinstance(v, str) else v
                for k, v in self.cache[api_name].items() 
                    if k != 'docs'
            }
        del self.cache['default']

    def available_apis(self):
        return self.cache.keys()

    def loaded_apis(self):
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
