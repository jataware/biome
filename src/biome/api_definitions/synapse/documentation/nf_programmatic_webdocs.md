## Downloading Data Programmatically From a Portal

Portals are websites created to promote data sharing within a specific research community. These websites aggregate relevant data from Synapse, and they allow users to explore data, projects, people, and organizations within their research community.

Sage Bionetworks hosts a variety of web portals for different research communities. The AD Knowledge Portal, the NF Data Portal, and the PsychENCODE Knowledge Portal are a few examples. The following guide describes how to programmatically download data discovered on a portal.

## Find Files Using Explore
All entities in Synapse are automatically assigned a globally unique identifier used for reference with the format syn12345678. Often abbreviated to “synID”, the ID of an object never changes, even if the name does. You will use a synID to locate the files you wish to download.

Regular human users/researchers will use a web portal, but we will have to use the API to find the synID.

## Python
The synapseclient package provides an interface to Synapse, a collaborative, open-source research platform that allows teams to share data, track analyses, and collaborate, providing support for:

integrated presentation of data, code and text
fine grained access control
provenance tracking
The synapseclient package lets you communicate with the cloud-hosted Synapse service to access data and create shared data analysis projects from within Python scripts or at the interactive Python console. Other Synapse clients exist for R, Java, and the web. The Python client can also be used from the command line.

Installing this package will install synapseclient, synapseutils and the command line client. synapseutils contains beta features and the behavior of these features are subject to change.

In order to download data programmatically, you need a list of synIDs that correspond to the files.

```
import synapseclient, pandas, os
from pathlib import Path

downloads_dir = Path(__file__).parent.parent / "downloads" / "synapse"

print(f"downloads_dir: {{downloads_dir.resolve()}}")

# cache_root_dir specifies the download location for Synapse files
syn = synapseclient.Synapse(cache_root_dir=downloads_dir) 
syn.login(authToken=os.environ.get("API_SYNAPSE")) 

# sample using SQL query knowing the table/view ID:
results = syn.tableQuery('select * from syn7511263')

# Example when already have a file ID handle and wish to download the file:
syn4988822 = syn.get(entity='syn4988822')
# Get the path to the local copy of the data file 
filepath = syn4988822.path 
```

### Python Client API Reference

#### class synapseclient.Synapse
Bases: object

Constructs a Python client object for the Synapse repository service

ATTRIBUTE	DESCRIPTION
repoEndpoint	Location of Synapse repository

authEndpoint	Location of authentication service

fileHandleEndpoint	Location of file service

portalEndpoint	Location of the website

serviceTimeoutSeconds	Wait time before timeout (currently unused)

debug	Print debugging messages if True

skip_checks	Skip version and endpoint checks

configPath	Path to config File with setting for Synapse. Defaults to ~/.synapseConfig

requests_session	A custom requests.Session object that this Synapse instance will use when making http requests.

cache_root_dir	Root directory for storing cache data

silent	Defaults to False.

##### Functions (for synapseclient.Synapse)
method `get`

get(entity, **kwargs)
Gets a Synapse entity from the repository service.

PARAMETER	DESCRIPTION
entity	A Synapse ID (e.g. syn123 or syn123.1, with .1 denoting version), a Synapse Entity object, a plain dictionary in which 'id' maps to a Synapse ID or a local file that is stored in Synapse (found by the file MD5)

version	The specific version to get. Defaults to the most recent version. If not denoted in the entity input.

downloadFile	Whether associated files(s) should be downloaded. Defaults to True.

downloadLocation	Directory where to download the Synapse File Entity. Defaults to the local cache.

followLink	Whether the link returns the target Entity. Defaults to False.

ifcollision	Determines how to handle file collisions. May be "overwrite.local", "keep.local", or "keep.both". Defaults to "keep.both".

limitSearch	A Synanpse ID used to limit the search in Synapse if entity is specified as a local file. That is, if the file is stored in multiple locations in Synapse only the ones in the specified folder/project will be returned.

md5	The MD5 checksum for the file, if known. Otherwise if the file is a local file, it will be calculated automatically.

RETURNS	DESCRIPTION
A new Synapse Entity object of the appropriate type.

Using this function
Download file into cache

entity = syn.get('syn1906479')
print(entity.name)
print(entity.path)
Download file into current working directory


entity = syn.get('syn1906479', downloadLocation='.')
print(entity.name)
print(entity.path)
Determine the provenance of a locally stored file as indicated in Synapse

entity = syn.get('/path/to/file.txt', limitSearch='syn12312')
print(syn.getProvenance(entity))


method `get_annotations`

get_annotations(entity: Union[str, Entity], version: Union[str, int] = None) -> Annotations
Retrieve annotations for an Entity from the Synapse Repository as a Python dict.

Note that collapsing annotations from the native Synapse format to a Python dict may involve some loss of information. See _getRawAnnotations to get annotations in the native format.

PARAMETER	DESCRIPTION
entity	An Entity or Synapse ID to lookup
TYPE: Union[str, Entity]

version	The version of the Entity to retrieve.
TYPE: Union[str, int]DEFAULT: None

RETURNS	DESCRIPTION
Annotations	A synapseclient.annotations.Annotations object, a dict that also has id and etag attributes

tableQuery ¶

tableQuery(query: str, resultsAs: str = 'csv', **kwargs)
Query a Synapse Table.

You can receive query results either as a generator over rows or as a CSV file. For smallish tables, either method will work equally well. Use of a "rowset" generator allows rows to be processed one at a time and processing may be stopped before downloading the entire table.

Optional keyword arguments differ for the two return types of rowset or csv

PARAMETER	DESCRIPTION
query	Query string in a SQL-like syntax, for example: "SELECT * from syn12345"
TYPE: str

resultsAs	select whether results are returned as a CSV file ("csv") or incrementally downloaded as sets of rows ("rowset")
TYPE: strDEFAULT: 'csv'

limit	(rowset only) Specify the maximum number of rows to be returned, defaults to None

offset	(rowset only) Don't return the first n rows, defaults to None

quoteCharacter	(csv only) default double quote

escapeCharacter	(csv only) default backslash

lineEnd	(csv only) defaults to os.linesep

separator	(csv only) defaults to comma

header	(csv only) True by default

includeRowIdAndRowVersion	(csv only) True by default

downloadLocation	(csv only) directory path to download the CSV file to

RETURNS	DESCRIPTION
A TableQueryResult or CsvFileTable object
NOTE
When performing queries on frequently updated tables, the table can be inaccessible for a period leading to a timeout of the query. Since the results are guaranteed to eventually be returned you can change the max timeout by setting the table_query_timeout variable of the Synapse object:

```
  # Sets the max timeout to 5 minutes.
  syn.table_query_timeout = 300

  getColumn
```

getColumn(id)
Gets a Column object from Synapse by ID.

See: synapseclient.table.Column

PARAMETER	DESCRIPTION
id	The ID of the column to retrieve

RETURNS	DESCRIPTION
An object of type synapseclient.table.Column
Using this function
Getting a column

column = syn.getColumn(123)

getColumns

getColumns(x, limit=100, offset=0)
Get the columns defined in Synapse either (1) corresponding to a set of column headers, (2) those for a given schema, or (3) those whose names start with a given prefix.

PARAMETER	DESCRIPTION
x	A list of column headers, a Table Entity object (Schema/EntityViewSchema), a Table's Synapse ID, or a string prefix

limit	maximum number of columns to return (pagination parameter)
DEFAULT: 100

offset	the index of the first column to return (pagination parameter)
DEFAULT: 0

YIELDS	DESCRIPTION
A generator over synapseclient.table.Column objects

 getTableColumns

getTableColumns(table)
Retrieve the column models used in the given table schema.

PARAMETER	DESCRIPTION
table	The schema of the Table whose columns are to be retrieved

YIELDS	DESCRIPTION
A Generator over the Table's columns

downloadTableColumns

downloadTableColumns(table, columns, downloadLocation=None, **kwargs)
Bulk download of table-associated files.

PARAMETER	DESCRIPTION
table	Table query result

columns	A list of column names as strings

downloadLocation	Directory into which to download the files
DEFAULT: None

RETURNS	DESCRIPTION
A dictionary from file handle ID to path in the local file system.
For example, consider a Synapse table whose ID is "syn12345" with two columns of type FILEHANDLEID named 'foo' and 'bar'. The associated files are JSON encoded, so we might retrieve the files from Synapse and load for the second 100 of those rows as shown here:

```
import json

results = syn.tableQuery('SELECT * FROM syn12345 LIMIT 100 OFFSET 100')
file_map = syn.downloadTableColumns(results, ['foo', 'bar'])

for file_handle_id, path in file_map.items():
    with open(path) as f:
        data[file_handle_id] = f.read()
```


get_acl

get_acl(entity: Union[Entity, Evaluation, str, Mapping], principal_id: str = None) -> List[str]
Get the ACL that a user or group has on an Entity.

PARAMETER	DESCRIPTION
entity	An Entity or Synapse ID to lookup
TYPE: Union[Entity, Evaluation, str, Mapping]

principal_id	Identifier of a user or group (defaults to PUBLIC users)
TYPE: strDEFAULT: None

RETURNS	DESCRIPTION
List[str]	An array containing some combination of ['READ', 'UPDATE', 'CREATE', 'DELETE', 'DOWNLOAD', 'MODERATE', 'CHANGE_PERMISSIONS', 'CHANGE_SETTINGS'] or an empty array

get_permissions

get_permissions(entity: Union[Entity, Evaluation, str, Mapping]) -> Permissions
Get the permissions that the caller has on an Entity.

PARAMETER	DESCRIPTION
entity	An Entity or Synapse ID to lookup
TYPE: Union[Entity, Evaluation, str, Mapping]

RETURNS	DESCRIPTION
Permissions	An Permissions object
Using this function:
Getting permissions for a Synapse Entity


permissions = syn.get_permissions(Entity)
Getting permissions for a Synapse ID


permissions = syn.get_permissions("syn12345")
Getting access types list from the Permissions object


permissions.access_types

 getProvenance ¶

getProvenance(entity: Union[str, Mapping, Number], version: int = None) -> Activity
Retrieve provenance information for a Synapse Entity.

PARAMETER	DESCRIPTION
entity	An Entity or Synapse ID to lookup
TYPE: Union[str, Mapping, Number]

version	The version of the Entity to retrieve. Gets the most recent version if omitted
TYPE: intDEFAULT: None

RETURNS	DESCRIPTION
Activity	An Activity object or raises exception if no provenance record exists
RAISES	DESCRIPTION
SynapseHTTPError	if no provenance record exists


findEntityId ¶

findEntityId(name, parent=None)
Find an Entity given its name and parent.

PARAMETER	DESCRIPTION
name	Name of the entity to find

parent	An Entity object or the Id of an entity as a string. Omit if searching for a Project by name
DEFAULT: None

RETURNS	DESCRIPTION
The Entity ID or None if not found


getChildren(parent, includeTypes=['folder', 'file', 'table', 'link', 'entityview', 'dockerrepo', 'submissionview', 'dataset', 'materializedview'], sortBy='NAME', sortDirection='ASC')
Retrieves all of the entities stored within a parent such as folder or project.

PARAMETER	DESCRIPTION
parent	An id or an object of a Synapse container or None to retrieve all projects

includeTypes	Must be a list of entity types (ie. ["folder","file"]) which can be found here
DEFAULT: ['folder', 'file', 'table', 'link', 'entityview', 'dockerrepo', 'submissionview', 'dataset', 'materializedview']

sortBy	How results should be sorted. Can be NAME, or CREATED_ON
DEFAULT: 'NAME'

sortDirection	The direction of the result sort. Can be ASC, or DESC
DEFAULT: 'ASC'

YIELDS	DESCRIPTION
An iterator that shows all the children of the container.
Also see:

synapseutils.walk

getTeam ¶

getTeam(id: Union[int, str]) -> Team
Finds a team with a given ID or name.

PARAMETER	DESCRIPTION
id	The ID or name of the team or a Team object to retrieve.
TYPE: Union[int, str]

RETURNS	DESCRIPTION
Team	An object of type synapseclient.team.Team

getConfigFile cached

getConfigFile(configPath: str) -> RawConfigParser
Retrieves the client configuration information.

PARAMETER	DESCRIPTION
configPath	Path to configuration file on local file system
TYPE: str

RETURNS	DESCRIPTION
RawConfigParser	A RawConfigParser populated with properties from the user's configuration file.

get_available_services

get_available_services() -> List[str]
Get available Synapse services This is a beta feature and is subject to change

RETURNS	DESCRIPTION
List[str]	List of available services
Source code in synapseclient/client.py
 service ¶

service(service_name: str)
Get available Synapse services This is a beta feature and is subject to change

PARAMETER	DESCRIPTION
service_name	name of the service
TYPE: str

clear_download_list

clear_download_list()
Clear all files from download list

getWiki

getWiki(owner, subpageId=None, version=None)
Get a synapseclient.wiki.Wiki object from Synapse. Uses wiki2 API which supports versioning.

PARAMETER	DESCRIPTION
owner	The entity to which the Wiki is attached

subpageId	The id of the specific sub-page or None to get the root Wiki page
DEFAULT: None

version	The version of the page to retrieve or None to retrieve the latest
DEFAULT: None

RETURNS	DESCRIPTION
A synapseclient.wiki.Wiki object

 getWikiAttachments

getWikiAttachments(wiki)
Retrieve the attachments to a wiki page.

PARAMETER	DESCRIPTION
wiki	The Wiki object for which the attachments are to be returned.

RETURNS	DESCRIPTION
A list of file handles for the files attached to the Wiki.

get_download_list 
get_download_list(downloadLocation: str = None) -> str
Download all files from your Synapse download list

PARAMETER	DESCRIPTION
downloadLocation	Directory to download files to.
TYPE: strDEFAULT: None

RETURNS	DESCRIPTION
str	Manifest file with file paths

md5Query

md5Query(md5)
Find the Entities which have attached file(s) which have the given MD5 hash.

PARAMETER	DESCRIPTION
md5	The MD5 to query for (hexadecimal string)

RETURNS	DESCRIPTION
A list of Entity headers

restGET

restGET(uri, endpoint=None, headers=None, retryPolicy={{}}, requests_session=None, **kwargs)
Sends an HTTP GET request to the Synapse server.

PARAMETER	DESCRIPTION
uri	URI on which get is performed

endpoint	Server endpoint, defaults to self.repoEndpoint
DEFAULT: None

headers	Dictionary of headers to use rather than the API-key-signed default set of headers
DEFAULT: None

requests_session	An external requests.Session object to use when making this specific call
DEFAULT: None

kwargs	Any other arguments taken by a request method
DEFAULT: {{}}

RETURNS	DESCRIPTION
JSON encoding of response

rest_get_async async ¶

rest_get_async(uri: str, endpoint: str = None, headers: Headers = None, retry_policy: Dict[str, Any] = {{}}, requests_session_async_synapse: AsyncClient = None, **kwargs) -> Union[Dict[str, Any], str, None]
Sends an HTTP GET request to the Synapse server.

PARAMETER	DESCRIPTION
uri	URI on which get is performed
TYPE: str

endpoint	Server endpoint, defaults to self.repoEndpoint
TYPE: strDEFAULT: None

headers	Dictionary of headers to use.
TYPE: HeadersDEFAULT: None

retry_policy	A retry policy that matches the arguments of synapseclient.core.retry.with_retry_time_based_async.
TYPE: Dict[str, Any]DEFAULT: {{}}

requests_session_async_synapse	The async client to use when making this specific call.
TYPE: AsyncClientDEFAULT: None

kwargs	Any other arguments taken by a request method
DEFAULT: {{}}

RETURNS	DESCRIPTION
Union[Dict[str, Any], str, None]	JSON encoding of response

#### class Entity
The Entity class is the base class for all entities, including Project, Folder, File, and Link.
Entities are dictionary-like objects in which both object and dictionary notation (entity.foo or entity['foo']) can be used interchangeably.

#### class synapseclient.entity.Entity

Bases: MutableMapping

A Synapse entity is an object that has metadata, access control, and potentially a file. It can represent data, source code, or a folder that contains other entities.

Entities should typically be created using the constructors for specific subclasses such as synapseclient.Project, synapseclient.Folder or synapseclient.File.

ATTRIBUTE	DESCRIPTION
id	The unique immutable ID for this entity. A new ID will be generated for new Entities. Once issued, this ID is guaranteed to never change or be re-issued

name	The name of this entity. Must be 256 characters or less. Names may only contain: letters, numbers, spaces, underscores, hyphens, periods, plus signs, apostrophes, and parentheses

description	The description of this entity. Must be 1000 characters or less.

parentId	The ID of the Entity that is the parent of this Entity.

entityType	The type of this entity.

concreteType	Indicates which implementation of Entity this object represents. The value is the fully qualified class name, e.g. org.sagebionetworks.repo.model.FileEntity.

etag	Synapse employs an Optimistic Concurrency Control (OCC) scheme to handle concurrent updates. Since the E-Tag changes every time an entity is updated it is used to detect when a client's current representation of an entity is out-of-date.

annotations	The dict of annotations for this entity.

accessControlList	The access control list for this entity.

createdOn	The date this entity was created.

createdBy	The ID of the user that created this entity.

modifiedOn	The date this entity was last modified.

modifiedBy	The ID of the user that last modified this entity.

##### Functions (for synapseclient.entity.Entity)

 local_state

local_state(state: dict = None) -> dict
Set or get the object's internal state, excluding properties, or annotations.

PARAMETER	DESCRIPTION
state	A dictionary containing the object's internal state.
TYPE: dictDEFAULT: None

RETURNS	DESCRIPTION
result	The object's internal state, excluding properties, or annotations.
TYPE: dict

Source code in synapseclient/entity.py
 keys

keys()
RETURNS	DESCRIPTION
A set of property and annotation keys
Source code in synapseclient/entity.py
 has_key

has_key(key)
Is the given key a property or annotation?

#### class synapseclient.entity.Project
Bases: Entity

Represents a project in Synapse.

Projects in Synapse must be uniquely named. Trying to create a project with a name that's already taken, say 'My project', will result in an error

ATTRIBUTE	DESCRIPTION
name	The name of the project

alias	The project alias for use in friendly project urls.

properties	A map of Synapse properties

annotations	A map of user defined annotations

local_state	Internal use only
TYPE: dict

Using this class
Creating an instance and storing the project


project = Project('Foobarbat project')
project = syn.store(project)

#### Folder  synapseclient.entity.Folder
Bases: Entity

Represents a folder in Synapse.

Folders must have a name and a parent and can optionally have annotations.

ATTRIBUTE	DESCRIPTION
name	The name of the folder

parent	The parent project or folder

properties	A map of Synapse properties

annotations	A map of user defined annotations

local_state	Internal use only
TYPE: dict

Using this class
Creating an instance and storing the folder


folder = Folder(name='my data', parent=project)
folder = syn.store(folder)

#### File synapseclient.entity.File ¶
Bases: Entity, Versionable

Represents a file in Synapse.

When a File object is stored, the associated local file or its URL will be stored in Synapse. A File must have a path (or URL) and a parent. By default, the name of the file in Synapse matches the filename, but by specifying the name attribute, the File Entity name can be different.

##### Changing File Names
A Synapse File Entity has a name separate from the name of the actual file it represents. When a file is uploaded to Synapse, its filename is fixed, even though the name of the entity can be changed at any time. Synapse provides a way to change this filename and the content-type of the file for future downloads by creating a new version of the file with a modified copy of itself. This can be done with the synapseutils.copy_functions.changeFileMetaData function.

```
import synapseutils
e = syn.get(synid)
print(os.path.basename(e.path))  ## prints, e.g., "my_file.txt"
e = synapseutils.changeFileMetaData(syn, e, "my_newname_file.txt")
```
Setting fileNameOverride will not change the name of a copy of the file that's already downloaded into your local cache. Either rename the local copy manually or remove it from the cache and re-download.:

```
syn.cache.remove(e.dataFileHandleId)
e = syn.get(e)
print(os.path.basename(e.path))  ## prints "my_newname_file.txt"
```

PARAMETER	DESCRIPTION
path	Location to be represented by this File
DEFAULT: None

name	Name of the file in Synapse, not to be confused with the name within the path

parent	Project or Folder where this File is stored
DEFAULT: None

synapseStore	Whether the File should be uploaded or if only the path should be stored when synapseclient.Synapse.store is called on the File object.
DEFAULT: True

contentType	Manually specify Content-type header, for example "application/png" or "application/json; charset=UTF-8"

dataFileHandleId	Defining an existing dataFileHandleId will use the existing dataFileHandleId The creator of the file must also be the owner of the dataFileHandleId to have permission to store the file.

properties	A map of Synapse properties
DEFAULT: None

annotations	A map of user defined annotations
DEFAULT: None

local_state	Internal use only





#### Annotations  class synapseclient.annotations

Annotations are arbitrary metadata attached to Synapse entities. They can be accessed like ordinary object properties or like dictionary keys:

```
entity.my_annotation = 'This is one way to do it'
entity['other_annotation'] = 'This is another'
```

Annotations can be given in the constructor for Synapse Entities:

```
entity = File('data.xyz', parent=my_project, rating=9.1234)
```

Annotate the entity with location data:
```
entity.lat_long = [47.627477, -122.332154]
```
Record when we collected the data. This will use the current timezone of the machine running the code.
```
from datetime import datetime as Datetime
entity.collection_date = Datetime.now()
```
Record when we collected the data in UTC:
```
from datetime import datetime as Datetime
entity.collection_date = Datetime.utcnow()
```
You may also use a Timezone aware datetime object like the following example. Using the pytz library is recommended for this purpose.:
```
from datetime import datetime as Datetime, timezone as Timezone, timedelta as Timedelta

date = Datetime(2023, 12, 20, 8, 10, 0, tzinfo=Timezone(Timedelta(hours=-5)))
```
See:

> synapseclient.Synapse.get_annotations
> synapseclient.Synapse.set_annotations

##### Annotating data sources
Data sources are best recorded using Synapse's Activity/Provenance tools.

Implementation details
In Synapse, entities have both properties and annotations. Properties are used by the system, whereas annotations are completely user defined. In the Python client, we try to present this situation as a normal object, with one set of properties.


Represent Synapse Entity annotations as a flat dictionary with the system assigned properties id, etag as object attributes.

ATTRIBUTE	DESCRIPTION
id	Synapse ID of the Entity

etag	Synapse etag of the Entity

values	(Optional) dictionary of values to be copied into annotations

**kwargs	additional key-value pairs to be added as annotations

Creating a few instances
Creating and setting annotations

```
from synapseclient import Annotations

example1 = Annotations('syn123','40256475-6fb3-11ea-bb0a-9cb6d0d8d984', {{'foo':'bar'}})
example2 = Annotations('syn123','40256475-6fb3-11ea-bb0a-9cb6d0d8d984', foo='bar')
example3 = Annotations('syn123','40256475-6fb3-11ea-bb0a-9cb6d0d8d984')
example3['foo'] = 'bar'
```

##### Functions
 is_synapse_annotations

is_synapse_annotations(annotations: Mapping) -> bool
Tests if the given object is a Synapse-style Annotations object.

PARAMETER	DESCRIPTION
annotations	A key-value mapping that may or may not be a Synapse-style
TYPE: Mapping

RETURNS	DESCRIPTION
bool	True if the given object is a Synapse-style Annotations object, False
bool	otherwise.

from_synapse_annotations ¶

from_synapse_annotations(raw_annotations: Dict[str, Any]) -> Annotations
Transforms a Synapse-style Annotation object to a simple flat dictionary.

PARAMETER	DESCRIPTION
raw_annotations	A Synapse-style Annotation dict.
TYPE: Dict[str, Any]

RETURNS	DESCRIPTION
Annotations	A simple flat dictionary of annotations.

 convert_old_annotation_json ¶

convert_old_annotation_json(annotations)
Transforms a parsed JSON dictionary of old style annotations into a new style consistent with the entity bundle v2 format.

This is intended to support some models that were saved as serialized entity bundle JSON (Submissions). we don't need to support newer types here e.g. BOOLEAN because they did not exist at the time that annotation JSON was saved in this form.

PARAMETER	DESCRIPTION
annotations	A parsed JSON dictionary of old style annotations.

RETURNS	DESCRIPTION
A v2 Annotation-style dictionary.






#### Tables  synapseclient.table

Tables
Synapse Tables enable storage of tabular data in Synapse in a form that can be queried using a SQL-like query language.

A table has a Schema and holds a set of rows conforming to that schema.

A Schema defines a series of Column of the following types:

STRING
DOUBLE
INTEGER
BOOLEAN
DATE
ENTITYID
FILEHANDLEID
LINK
LARGETEXT
USERID
Read more information about using Table in synapse in the tutorials section.

Classes
 SchemaBase
Bases: Entity

This is the an Abstract Class for EntityViewSchema and Schema containing the common methods for both. You can not create an object of this type.


##### Functions
has_columns()
Does this schema have columns specified?

class Schema
Bases: SchemaBase

A Schema is an Entity that defines a set of columns in a table.

ATTRIBUTE	DESCRIPTION
name	The name for the Table Schema object

description	User readable description of the schema

columns	A list of Column objects or their IDs

parent	The project in Synapse to which this table belongs

properties	A map of Synapse properties

annotations	A map of user defined annotations

local_state	Internal use only
TYPE: dict

Example:

```
cols = [Column(name='Isotope', columnType='STRING'),
        Column(name='Atomic Mass', columnType='INTEGER'),
        Column(name='Halflife', columnType='DOUBLE'),
        Column(name='Discovered', columnType='DATE')]

schema = syn.store(Schema(name='MyTable', columns=cols, parent=project))
```

class MaterializedViewSchema
Bases: SchemaBase

A MaterializedViewSchema is an Entity that defines a set of columns in a materialized view along with the SQL statement.

ATTRIBUTE	DESCRIPTION
name	The name for the Materialized View Schema object

description	User readable description of the schema

definingSQL	The synapse SQL statement that defines the data in the materialized view. The SQL contain JOIN clauses on multiple tables.

columns	A list of Column objects or their IDs

parent	The project in Synapse to which this Materialized View belongs

properties	A map of Synapse properties

annotations	A map of user defined annotations

local_state	Internal use only
TYPE: dict

Example:

```
defining_sql = "SELECT * FROM syn111 F JOIN syn2222 P on (F.patient_id = P.patient_id)"
schema = syn.store(MaterializedViewSchema(name='MyTable', parent=project, definingSQL=defining_sql))
```

class ViewBase
Bases: SchemaBase

This is a helper class for EntityViewSchema and SubmissionViewSchema containing the common methods for both.

class Dataset
Bases: ViewBase

A Dataset is an Entity that defines a flat list of entities as a tableview (a.k.a. a "dataset").

ATTRIBUTE	DESCRIPTION
name	The name for the Dataset object

description	User readable description of the schema

columns	A list of Column objects or their IDs

parent	The Synapse Project to which this Dataset belongs

properties	A map of Synapse properties

annotations	A map of user defined annotations

dataset_items	A list of items characterized by entityId and versionNumber

folder	A list of Folder IDs

local_state	Internal use only
TYPE: dict

###### Using Dataset
####### Load Dataset

```
from synapseclient import Dataset
Create a Dataset with pre-defined DatasetItems. Default Dataset columns are used if no schema is provided.


dataset_items = [
    {{'entityId': "syn000", 'versionNumber': 1}},
    {{...}},
]

dataset = syn.store(Dataset(
    name="My Dataset",
    parent=project,
    dataset_items=dataset_items))
Add/remove specific Synapse IDs to/from the Dataset


dataset.add_item({{'entityId': "syn111", 'versionNumber': 1}})
dataset.remove_item("syn000")
dataset = syn.store(dataset)
Add a list of Synapse IDs to the Dataset


new_items = [
    {{'entityId': "syn222", 'versionNumber': 2}},
    {{'entityId': "syn333", 'versionNumber': 1}}
]
dataset.add_items(new_items)
dataset = syn.store(dataset)
```

Folders can easily be added recursively to a dataset, that is, all files within the folder (including sub-folders) will be added. Note that using the following methods will add files with the latest version number ONLY. If another version number is desired, use add_item or add_items.

Check items in a Dataset
To get the number of entities in the dataset, use len().

```
print(f"{{dataset.name}} has {{len(dataset)}} items.")
```

method  has_item

has_item(item_id: str) -> bool
Check if has dataset item

PARAMETER	DESCRIPTION
item_id	A single dataset item Synapse ID
TYPE: str


#### 
Exceptions
 synapseclient.core.exceptions
Contains all of the exceptions that can be thrown within this Python client as well as handling error cases for HTTP requests.

Classes
class SynapseError
Bases: Exception

Generic exception thrown by the client.

class SynapseMd5MismatchError
Bases: SynapseError, IOError

Error raised when MD5 computed for a download file fails to match the MD5 of its file handle.

class SynapseFileNotFoundError
Bases: SynapseError

Error thrown when a local file is not found in Synapse.

class SynapseNotFoundError
Bases: SynapseError

Error thrown when a requested resource is not found in Synapse.

class SynapseTimeoutError
Bases: SynapseError

Timed out waiting for response from Synapse.

class SynapseAuthenticationError
Bases: SynapseError

Authentication errors.

class SynapseAuthorizationError
Bases: SynapseError

Authorization errors.

class SynapseNoCredentialsError
Bases: SynapseAuthenticationError

No credentials for authentication

class SynapseFileCacheError
Bases: SynapseError

Error related to local file storage.

class SynapseMalformedEntityError
Bases: SynapseError

Unexpected structure of Entities.

class SynapseUnmetAccessRestrictions
Bases: SynapseError

Request cannot be completed due to unmet access restrictions.

class SynapseProvenanceError
Bases: SynapseError

Incorrect usage of provenance objects.

class SynapseHTTPError
Bases: SynapseError, HTTPError

Wraps recognized HTTP errors. See HTTPError <http://docs.python-requests.org/en/latest/api/?highlight=exceptions#requests.exceptions.HTTPError>_

class SynapseUploadAbortedException
Bases: SynapseError

Raised when a worker thread detects the upload was aborted and stops further processing.

class SynapseDownloadAbortedException
Bases: SynapseError

Raised when a worker thread detects the download was aborted and stops further processing.

class SynapseUploadFailedException
Bases: SynapseError

Raised when an upload failed. Should be chained to a cause Exception