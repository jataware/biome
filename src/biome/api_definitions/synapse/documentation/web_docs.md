# Entities, Files, and Folders Oh My!

## Entity Model
See Scenarios: File / Folder API for driving use cases for this design. An entity is an object that represents either a file or a folder.  The attributes of file entities and folder entities are similar to the attributes of files and folders on a hard drive:

Folder - A folder is a container for either files or other folders.  A folder has metadata such as name, createdBy, createdOn but it cannot have actual data.
File - A file represents data.  A file has metadata like folders but it also has raw bytes of a data file.  A file cannot be a container for other files and folders.  Put another way, no entity can have a file entity as a parent.
The following class diagram (figure 1) is not meant to be exhaustive, but rather show the basic relationships of entities as related to files and folders.

We have updated the object model to incorporate feed back and consider how Competition objects (might be renamed to Evaluation objects) work with wiki markdown.

V2 Changes:

PageEntity has been removed completely.  Instead WikiPages can be a container of  WikiPages (child WikiPage keeps a 'wikiParentID').  This means there will be no 'wiki' specific entity.  This also means a Project's wiki is not special.
WikiPage no longer has the same ID as its parent entity.  Instead, a wiki page can be a component of an Entity (so the Entity keeps a 'wikiId').  This allows other non-Entity objects to also have a WikiPage.  For example, a Competition object can also have a WikiPage.
Study and Summary have been reclassified as folders (they were files).
V3 Changes:

Description added back to entity.  The description is meant to be a short plain text (not markdown) description of the entity.


## File Entity API
Note: All relative URLs in this document are assumed to point to be: https://repo-prod.sagebase.org/repo/v1.  The full URL will be provided whenever this is not the case.

GET /entity	- A caller can GET an entity if they have the READ permission on the Entity.  Note: If an Entity has a valid 'dataFileHandleId' and the the caller has READ permission on Entity the valid 'dataFileHandleId' will be returned.  The 'dataFileHandleId' will be returned, even if the caller does not have download permission on that entity.  This means a caller can determine the existence of a file even if they lack the permission to download it.

GET /entity/{{entityId}}/file	- The ability for a caller to download a file associated with an Entity is based on several factors including, READ permission on the Entity, signing the terms-of-use (ToU), and any special data restrictions applied to sensitive data.  A caller must meet all access requirements in order to download any file associated with an Entity.  For more information on data access see: Authentication and Authorization API

GET /entity/{{entityId}}/filehandles - To access the FileHandle associated with the 'dataFileHandleId', the caller must meet all of the download requirements of the actual data file (same as GET /entity/file).

/entity/{{enityId}}/file	GET	Attempt to download the raw file currently associated with the current version of the Entity.  Note: This call will result in a HTTP temporary redirect (307), to the real file URL if the caller meets all of the download requirements.

/entity/{{enityId}}/filepreview	GET	Attempt to download the preview of the file currently associated with the current version of the Entity.  Note: This call will result in a HTTP temporary redirect (307), to the real file URL if the caller meets all of the download requirements.

/entity/{{enityId}}/filehandles	GET	Get the FileHandles of the file currently associated with the current version of the Entity.  If a preview exists for the file then the handle of the preview and the file will be returned with this call.

/entity/{{entityId}}/version/{{versionNumber}}/file	GET	Attempt to download the raw file of an entity for a given version number of the entity. Note: This call will result in a HTTP temporary redirect (307), to the real file URL if the caller meets all of the download requirements.

/entity/{{entityId}}/version/{{versionNumber}}/filepreview	GET	Attempt to download preview of the file of an entity for a given version number of the entity. Note: This call will result in a HTTP temporary redirect (307), to the real file URL if the caller meets all of the download requirements.

/entity/{{entityId}}/version/{{versionNumber}}/filehandles	GET	Get the FileHandles of the file associated with the given version number of the entity.  If a preview exists for the file then the handle of the preview and the file will be returned with this call.

# FileHandle 
The FileHandle is an object that represents a file that has either been uploaded to Synapse, or resides external to Synapse.  The FileHandle provides basic metadata about file:


id	The unique identifier of a file handle.  This ID is used to reference a file handle.
fileName	The name of the file. This field is required.
etag	The etag of a file handle will change if the file handle changes.  For the most part FileHandles are immutable, with the only exception being assigning a preview FileHandle ID.
createdOn	The date on which the file handle was created.
createdBy	The ID of the user that created this FileHandle.  Only the user that created a FileHandle can assign it to a file entity or wiki attachment.
concreteType	FileHandle is an interface with at least three implementations.  This field is used to indicate which concrete implementation is used.

There are currently three concrete implementations of FileHandle:

ExternalFileHandle	org.sagebionetworks.repo.model.file.ExternalFileHandle
S3FileHandle	    org.sagebionetworks.repo.model.file.S3FileHandle
PreviewFileHandle	org.sagebionetworks.repo.model.file.PreviewFileHandle

ExternalFileHandle
An external file handle is used to represent an external URL.  Note that ExternalFileHandle implements HasPreviewId.  Synapse will try to automatically generate a preview for any external URL that can be publicly read.  The resulting preview file will be stored in Synapse and represented with a PrevewFileHandle.  The creator of the ExternalFileHandle will be listed as the creator of the preview.

S3FileHandle
When a file is stored in Synapse, by default it is stored in Amazon's S3.  The S3FileHandle captures the extra information about the S3 file.  Just like ExternalFileHandles, Synapse will attempt to automatically create a preview of all S3FileHandles.

PreviewFileHandle
When Synapse creates a preview file for either an ExternalFileHandle or an S3FileHandle, the resulting preview file will be stored in S3 and be assigned a PreviewFileHandle.  Currently, Synapse will generate previews based on the original file's contentType. See Internet Media Type.

HTTP Types
For any web services where a file is sent with a POST, the content-type must be 'multipart/form-data', see:HTTP Multipart.  The content-type of all service responses will be 'application/json'.

Note: Unless otherwise specified all FileHandle services use a new endpoint:  https://file-prod.sagebase.org/file/v1.  Also standard Synapse 'sessionToken' must be included in all requests.

/fileHandle/{{handleId}}	GET	Get the FileHandle for a given FileHandle ID.  Only the original creator of the FileHandle is authorized to get a FileHandle or assign a FileHandle to a Synapse Object such as WikiPage attachment or FileEntity.