# this file is a beaker procedure and is a jinja template.
# this template is executed by beaker, not by the model extractor.
# there is a matching tool in tool.py_template

import requests as _requests

try:
    _url = '{{url}}'.format_map({{path_params}})
except:
    _url = '{{url}}'

try: 
    _query=dict({{query_params}})
except:
    _query={}

try: 
    import json as _json
    _body=dict(_json.loads({{request_body}}))
except:
    _body={}

if len(_body.keys()) > 0:
    _response = _requests.{{operation}}(_url, params=_query, data=_body)
else: 
    _response = _requests.{{operation}}(_url, params=_query)

_result = ''
if _response.status_code == 200:
    try:
        _result = _response.json()
    except:
        pass
else:
    print(f'Failed to run API call. HTTP Status code: {_response.status_code}')

{{target_var}} = _result

_api_input = {
    'url': _url,
    'operation': '{{operation}}',
    'query': _query,
    'body': _body,
    'response': _response
}

try:
    _api_history.append(_api_input)
except: 
    _api_history = [_api_input]
del _api_input

try:
    _json = _response.json()
except:
    _json = {}

{
    'json':_json, 
    'status_code':_response.status_code
}
