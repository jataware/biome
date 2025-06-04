# Data Commons Python API V2

The Data Commons Python API is a Python client library that enables developers to programmatically access nodes in the Data Commons knowledge graph. This package allows you to explore the structure of the graph, integrate statistics from the graph into data analysis workflows and much more.

Source code


## What’s new in V2

The latest version of Python client libraries implements the REST V2 APIs and adds many convenience methods. The package name is datacommons_client.

Here are just some of the changes from the previous version of the libraries:

You can use this new version to query custom Data Commons instances in addition to base datacommons.org.

The Data Commons Pandas module is included as an option in the install package; there is no need to install each library separately. Pandas APIs have also been migrated to use the REST V2 Observation API.

Requests to base datacommons.org require an API key.

The primary interface is a set of classes representing the REST V2 API endpoints.

Each class provides a fetch method that takes an API relation expression as an argument as well as several convenience methods for commonly used operations.

## Create a client

You access all Data Commons Python endpoints and methods through the DataCommonsClient class.

To create a client and connect to the base Data Commons, namely datacommons.org:

```
from datacommons_client.client import DataCommonsClient
client = DataCommonsClient(api_key="YOUR_API_KEY")
```

See below about API keys.

To create a client and connect to a custom Data Commons by a publicly resolvable DNS hostname:

```
from datacommons_client.client import DataCommonsClient
client = DataCommonsClient(dc_instance="DNS_HOSTNAME")
```

For example:

```
client = DataCommonsClient(dc_instance="datacommons.one.org")
```

To create a client and connect to a custom Data Commons by a private/non-resolvable address, specify the full API path, including the protocol and API version:

```
from datacommons_client.client import DataCommonsClient
client = DataCommonsClient(url="http://YOUR_ADDRESS/core/api/v2/")
```

For example, to connect to a locally running DataCommons instance:

```
from datacommons_client.client import DataCommonsClient
client = DataCommonsClient(url="http://localhost:8080/core/api/v2/")
```

## Authentication

All access to the base Data Commons (datacommons.org) the V2 APIs must be authenticated and authorized with an API key. The DataCommonsClient object manages propagating the API key to all requests, so you don’t need to specify it as part of data requests.

For custom DC instances, you do not need to provide any API key.
Request endpoints and responses

The Python client library sends HTTP POST requests to the Data Commons REST API endpoints and receives JSON responses. Each endpoint has a corresponding response type. The classes are below:

API 	Endpoint 	Description 	Response type
Observation 	observation 	Fetches statistical observations (time series) 	ObservationResponse
Observations Pandas DataFrame 	Similar to the fetch_observatons_by_entity_dcids and fetch_observations_by_entity_type methods of the Observation endpoint, except that the functionality is provided by a single method of the DataCommonsClient class directly, instead of an intermediate endpoint. Requires the optional Pandas module. 	pd.DataFrame
Node 	node 	Fetches information about edges and neighboring nodes 	NodeResponse and Python dictionary
Resolve entities 	resolve 	Returns Data Commons IDs (DCID) for entities in the knowledge graph 	ResolveResponse

To send a request, you use one of the endpoints available as methods of the client object. For example:

Request:

```
client.resolve.fetch_dcids_by_name(names="Georgia")
```

Response:

```
ResolveResponse(entities=[Entity(node='Georgia', candidates=[Candidate(dcid='geoId/13', dominantType=None), Candidate(dcid='country/GEO', dominantType=None), Candidate(dcid='geoId/5027700', dominantType=None)])])
```

See the linked pages for descriptions of the methods available for each endpoint, its methods and responses.
Find available entities, variables, and their DCIDs

Many requests require the DCID of the entity or variable you wish to query. For tips on how to find relevant DCIDs, entities and variables, please see the Key concepts document, specifically the following sections:

* Find a DCID for an entity or variable
* Find places available for a statistical variable

## Relation expressions

Each endpoint has a fetch() method that takes a relation expression. For complete information on the syntax and usage of relation expressions, please see the REST V2 API relation expressions documentation.

For common requests, each endpoint also provides convenience methods that build the expressions for you. See the endpoint pages for details.
Response formatting

By default, responses are returned as Python dataclass objects with the full structure. For example:

```
response = client.resolve.fetch_dcids_by_name(names="Georgia")
print(response)
ResolveResponse(entities=[Entity(node='Georgia', candidates=[Candidate(dcid='geoId/13', dominantType=None), Candidate(dcid='country/GEO', dominantType=None), Candidate(dcid='geoId/5027700', dominantType=None)])])
```

Each response class provides some property methods that are useful for formatting the output.
Method 	Description
to_dict 	Converts the dataclass to a Python dictionary.
to_json 	Serializes the dataclass to a JSON string (using json.dumps()).

Both methods take the following input parameter:
Parameter 	Description
exclude_none
Optional 	Compact response with nulls and empty lists removed. Defaults to True. To preserve the original structure and return all properties including null values and empty lists, set this to False.

Some endpoints include additional response formatting methods; see the individual endpoint pages for details.

### Examples

Example 1: Return dictionary in compact format

This example removes all properties that have null values or empty lists.

Request:

```
client.resolve.fetch_dcids_by_name(names="Georgia").to_dict()
```

Response:

```
{'entities': [{'node': 'Georgia', 'candidates': [{'dcid': 'geoId/13'}, {'dcid': 'country/GEO'}, {'dcid': 'geoId/5027700'}]}]}
```

Example 2: Return dictionary with original structure

This example sets exclude_none to False to preserve all properties from the original response, including all nulls and empty lists.

Request:

```
client.resolve.fetch_dcids_by_name(names="Georgia").to_dict(exclude_none=False)
```

Response:

```
{'entities': [{'node': 'Georgia', 'candidates': [{'dcid': 'geoId/13', 'dominantType': None}, {'dcid': 'country/GEO', 'dominantType': None}, {'dcid': 'geoId/5027700', 'dominantType': None}]}]}
```

Example 3: Return compact JSON string

This example converts the response to a formatted JSON string, in compact form, and prints the response for better readability.

Request:

```
client.resolve.fetch_dcids_by_name(names="Georgia").to_json()
```

Response:

```
{
  "entities": [
    {
      "node": "Georgia",
      "candidates": [
        {
          "dcid": "geoId/13"
        },
        {
          "dcid": "country/GEO"
        },
        {
          "dcid": "geoId/5027700"
        }
      ]
    }
  ]
}
```

Note: On the endpoint reference pages we will show all responses using this format, but will leave out the response methods for succinctness.

- - -

