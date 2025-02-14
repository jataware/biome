"""
Ensembl REST API Documentation Scraper and OpenAPI Specification Generator
"""

import requests
from bs4 import BeautifulSoup
import yaml
from urllib.parse import urljoin
from typing import Dict, List, Optional, Tuple
import json
import re
import logging

logger = logging.getLogger(__name__)
class EnsemblAPIExtractor:
    def __init__(self):
        self.method = None
        self.path = None
        self.doc = {}
        self.parameters = []
        self.openapi_spec = {
            'openapi': '3.0.0',
            'info': {
                'title': 'Ensembl REST API',
                'version': '1.0.0',
                'description': 'Ensembl REST API specification'
            },
            'servers': [
                {
                    'url': 'https://rest.ensembl.org',
                    'description': 'Ensembl REST API server'
                }
            ],
            'paths': {}
        }

    def create_openapi_spec(self) -> None:
        """Create OpenAPI specification and write to file incrementally."""
        # Write initial OpenAPI structure
        with open('ensembl_rest_openapi.yaml', 'w') as f:
            yaml.dump(self.openapi_spec, f, sort_keys=False, default_flow_style=False)
        
        # Process endpoints
        endpoints = self._get_endpoints()
        
        for endpoint in endpoints:
            print(f"\nProcessing documentation for: {endpoint['doc_url']}")
            
            # Get documentation
            doc = self.fetch_endpoint_documentation(endpoint['doc_url'])
            if not doc:
                print("Failed to get documentation, skipping...")
                continue
            
            # Set current endpoint attributes
            self.method = endpoint['method']
            self.path = endpoint['path']
            self.doc = doc
            
            if not self.method or not self.path:
                logger.error(f"Cannot create OpenAPI spec: method={self.method}, path={self.path}")
                continue
            
            logger.info(f"Creating OpenAPI spec for endpoint: {self.method} {self.path}")
            
            # Convert path parameters
            path, path_params = self._convert_path_params(endpoint['path'])
            method = endpoint['method'].lower()
            
            # Create path specification
            path_spec = {
                path: {
                    method: {
                        'tags': [endpoint['group']],  # Use the section name directly
                        'summary': doc.get('description', '').split('\n')[0],
                        'description': doc.get('description', ''),
                        'parameters': [],
                        'responses': {
                            '200': {
                                'description': 'Successful operation',
                                'content': {
                                    'application/json': {
                                        'schema': {
                                            'type': 'array' if doc.get('example_responses') and doc['example_responses'] and isinstance(doc['example_responses'][0].get('response'), list) else 'object'
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            
            # Add request body for POST endpoints with proper input example
            if method == 'post' and doc.get('response_format'):
                path_spec[path][method]['requestBody'] = {
                    'required': True,
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'object',
                                'example': json.loads(doc['response_format'].get('application/json', {}).get('example', '{}').replace("'", '"'))
                            }
                        }
                    }
                }
            
            # Add example if available
            if doc.get('example_responses') and doc['example_responses']:
                path_spec[path][method]['responses']['200']['content']['application/json']['schema']['example'] = doc['example_responses'][0].get('response', {})
            
            # Add parameters
            for param in doc.get('required_parameters', []):
                path_spec[path][method]['parameters'].append({
                    'name': param['name'],
                    'in': 'path' if param['name'] in path_params else 'query',
                    'description': param['description'],
                    'required': True,
                    'schema': {
                        'type': param['type'].lower(),
                        'example': param['example_values'][0] if param['example_values'] else None
                    }
                })
            
            for param in doc.get('optional_parameters', []):
                path_spec[path][method]['parameters'].append({
                    'name': param['name'],
                    'in': 'query',
                    'description': param['description'],
                    'required': False,
                    'schema': {
                        'type': param['type'].lower(),
                        'default': param['default'] if param['default'] != '-' else None,
                        'example': param['example_values'][0] if param['example_values'] else None
                    }
                })
            
            print(f"Writing specification for: {path}")
            
            # Read current spec
            with open('ensembl_rest_openapi.yaml', 'r') as f:
                current_spec = yaml.safe_load(f)
            
            # Update paths
            current_spec['paths'].update(path_spec)
            
            # Write updated spec
            with open('ensembl_rest_openapi.yaml', 'w') as f:
                yaml.dump(current_spec, f, sort_keys=False, default_flow_style=False)
            
            print(f"Specification updated for: {path}")

    def _convert_path_params(self, path: str) -> Tuple[str, List[str]]:
        """Convert :param style parameters to {param} style for OpenAPI spec."""
        if not path.startswith('/'):
            path = '/' + path
        
        parts = path.split('/')
        converted_parts = []
        path_params = []
        
        for part in parts:
            if part.startswith(':'):
                param_name = part[1:].rstrip(':')
                path_params.append(param_name)
                converted_parts.append(f'{{{param_name}}}')
            else:
                converted_parts.append(part)
        
        return '/'.join(converted_parts).replace('//', '/'), path_params

    def fetch_endpoint_documentation(self, doc_url: str) -> Optional[Dict]:
        """Fetch and parse endpoint documentation."""
        response = requests.get(doc_url)
        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_basic_documentation(soup)

    def _parse_basic_documentation(self, soup: BeautifulSoup) -> Dict:
        """Extract basic documentation from HTML."""
        doc = {
            'description': '',
            'required_parameters': [],
            'optional_parameters': [],
            'example_requests': [],
            'example_responses': [],
            'response_format': {},
            'resource_info': {}
        }
        
        # Get description
        desc = soup.find('p')
        if desc:
            doc['description'] = desc.text.strip()
        
        # Get Resource Information
        resource_info = soup.find('div', class_='resource-info')
        if resource_info:
            for row in resource_info.find_all('tr'):
                cells = row.find_all(['th', 'td'])
                if len(cells) == 2:
                    key = cells[0].text.strip().lower()
                    values = [v.strip() for v in cells[1].text.strip().split('\n') if v.strip()]
                    doc['resource_info'][key] = values if len(values) > 1 else values[0]
        
        # Find Parameters section
        params_section = soup.find(['h2', 'h3'], string='Parameters')
        if params_section:
            current_section = None
            current_table = params_section.find_next('table')
            
            while current_table:
                # Check for Required/Optional headers
                header = current_table.find_previous(['h3', 'h4'])
                if header and header.text.strip() in ['Required', 'Optional']:
                    current_section = header.text.strip().lower()
                    
                    for row in current_table.find_all('tr'):
                        cells = row.find_all('td')
                        if len(cells) >= 4:  # Name, Type, Description, Default, Example Values
                            param = {
                                'name': cells[0].text.strip(),
                                'type': cells[1].text.strip(),
                                'description': cells[2].text.strip(),
                                'default': cells[3].text.strip() if len(cells) > 3 else '-',
                                'example_values': [v.strip() for v in cells[-1].text.split('\n') if v.strip()]
                            }
                            
                            if current_section == 'required':
                                doc['required_parameters'].append(param)
                            elif current_section == 'optional':
                                doc['optional_parameters'].append(param)
                
                current_table = current_table.find_next('table')
        
        # Get Example Requests
        example_section = soup.find(['h2', 'h3'], string='Example Requests')
        if example_section:
            # Get the example URL
            example_url = example_section.find_next('a')
            if example_url:
                doc['example_requests'].append(example_url.text.strip())
            
            # Look for example output
            example_output = soup.find('div', class_='tab-pane hljs json active')
            if example_output:
                try:
                    # Find the code element and get its text
                    code_element = example_output.find('code', class_='json')
                    if code_element:
                        # Remove the HTML span elements and get just the text
                        response_text = ''
                        for element in code_element.children:
                            if isinstance(element, str):
                                response_text += element
                            else:
                                response_text += element.text
                        
                        # Parse the cleaned JSON
                        doc['example_responses'].append({
                            'content_type': 'application/json',
                            'response': json.loads(response_text)
                        })
                except (json.JSONDecodeError, AttributeError) as e:
                    print(f"Failed to parse example response JSON: {e}")
        
        # Get Response Format (for POST requests)
        message_section = soup.find(['h2', 'h3'], string='Message')
        if message_section:
            message_table = message_section.find_next('table')
            if message_table:
                for row in message_table.find_all('tr')[1:]:  # Skip header
                    cells = row.find_all('td')
                    if len(cells) >= 3:  # Content-type, Format, Example
                        content_type = cells[0].text.strip()
                        format_info = cells[1].text.strip()
                        example = cells[2].text.strip()
                        
                        # Clean up the example JSON string
                        example = example.replace("'", '"')  # Replace single quotes with double quotes
                        
                        doc['response_format'][content_type] = {
                            'format': format_info,
                            'example': example
                        }
        
        return doc

    def _get_endpoints(self) -> List[Dict]:
        """Get list of endpoints from main documentation."""
        print("Fetching endpoints from Ensembl REST API documentation...")
        
        response = requests.get('https://rest.ensembl.org/')
        if response.status_code != 200:
            print(f"Error fetching documentation: {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        endpoints = []
        
        # Find all section headers (Archive, Comparative Genomics, etc.)
        sections = soup.find_all(['h3'], class_=None)  # Main sections don't have classes
        
        for section in sections:
            section_name = section.text.strip()
            if not section_name:  # Skip empty headers
                continue
            
            print(f"\nProcessing section: {section_name}")
            
            # Find the next tbody after this section header
            tbody = section.find_next('tbody')
            if not tbody:
                continue
            # Process table rows
            for row in tbody.find_all('tr'):
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:  # Should have Resource and Description columns
                    resource_cell = cells[0]
                    description_cell = cells[1]
                    
                    # Extract method and path from resource cell
                    resource_link = resource_cell.find('a')
                    if resource_link:
                        text = resource_link.text.strip()
                        href = resource_link.get('href', '')
                        
                        if ' ' in text:  # Should be "METHOD /path"
                            method, path = text.split(' ', 1)
                            if method in ['GET', 'POST']:
                                endpoint = {
                                    'method': method,
                                    'path': path,
                                    'doc_url': urljoin('https://rest.ensembl.org/', href),
                                    'group': section_name,  # Use the section name as the group
                                    'description': description_cell.text.strip()
                                }
                                print(f"Found endpoint: {method} {path}")
                                endpoints.append(endpoint)
        
        print(f"Found {len(endpoints)} endpoints")
        return endpoints

def main():
    """Main function to generate and save OpenAPI specification."""
    extractor = EnsemblAPIExtractor()
    extractor.create_openapi_spec()
    print("\nOpenAPI specification generation complete!")

if __name__ == "__main__":
    main()