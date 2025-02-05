import requests
import json

endpoints = ['files','cases','projects','annotations','genes',
             'ssms','ssm_occurrences','cnvs','cnv_occurrences']

def get_endpoint_mapping(endpoint):
    print(f'Getting mapping for {endpoint}')
    mapping = requests.get(f'https://api.gdc.cancer.gov/{endpoint}/_mapping').json()
    print(f'Mapping for {endpoint} retrieved with keys: {mapping.keys()}')
    return mapping['fields']

def collect_mappings(endpoints):
    mappings = {}
    for endpoint in endpoints:
        mapping = get_endpoint_mapping(endpoint)
        mappings[endpoint] = mapping
    return mappings


if __name__ == '__main__':
    mappings = collect_mappings(endpoints)

    with open('../biome/api_definitions/gdc/documentation/gdc_mappings.json', 'w') as f:
        json.dump(mappings, f, indent=4)
