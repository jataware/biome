import json
import logging
import re
import requests
from time import sleep
import asyncio

from archytas.tool_utils import AgentRef, LoopControllerRef, tool
from typing import Any, Optional

from beaker_kernel.lib.agent import BaseAgent
from beaker_kernel.lib.context import BaseContext

from dataclasses import dataclass, asdict
from typing import Literal


logger = logging.getLogger(__name__)

BIOME_URL = "http://biome_api:8082"

def dynamic_docstring(docstring):
    def decorator(fn):
        fn.__doc__ = docstring
        return fn
    return decorator

@dataclass
class fetchAllClinicalDataInStudyUsingPOSTPathParameters:
    studyId : str 


@dataclass
class fetchAllClinicalDataInStudyUsingPOSTQueryParameters:
    clinicalDataType : Literal['SAMPLE', 'PATIENT'] | None = 'SAMPLE'
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'


@dataclass
class getTagsForMultipleStudiesUsingPOSTPathParameters:
    pass


@dataclass
class getTagsForMultipleStudiesUsingPOSTQueryParameters:
    pass


@dataclass
class fetchStudiesUsingPOSTPathParameters:
    pass


@dataclass
class fetchStudiesUsingPOSTQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'


@dataclass
class fetchSamplesUsingPOSTPathParameters:
    pass


@dataclass
class fetchSamplesUsingPOSTQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'


@dataclass
class fetchSampleListsUsingPOSTPathParameters:
    pass


@dataclass
class fetchSampleListsUsingPOSTQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'


@dataclass
class fetchPatientsUsingPOSTPathParameters:
    pass


@dataclass
class fetchPatientsUsingPOSTQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'


@dataclass
class fetchMutationsInMultipleMolecularProfilesUsingPOSTPathParameters:
    pass


@dataclass
class fetchMutationsInMultipleMolecularProfilesUsingPOSTQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'
    pageSize : int | None = 10000000
    pageNumber : int | None = 0
    sortBy : Literal['entrezGeneId', 'center', 'mutationStatus', 'validationStatus', 'tumorAltCount', 'tumorRefCount', 'normalAltCount', 'normalRefCount', 'aminoAcidChange', 'startPosition', 'endPosition', 'referenceAllele', 'variantAllele', 'proteinChange', 'mutationType', 'ncbiBuild', 'variantType', 'refseqMrnaId', 'proteinPosStart', 'proteinPosEnd', 'keyword'] | None = None
    direction : Literal['ASC', 'DESC'] | None = 'ASC'


@dataclass
class fetchMutationsInMolecularProfileUsingPOSTPathParameters:
    molecularProfileId : str 


@dataclass
class fetchMutationsInMolecularProfileUsingPOSTQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'
    pageSize : int | None = 10000000
    pageNumber : int | None = 0
    sortBy : Literal['entrezGeneId', 'center', 'mutationStatus', 'validationStatus', 'tumorAltCount', 'tumorRefCount', 'normalAltCount', 'normalRefCount', 'aminoAcidChange', 'startPosition', 'endPosition', 'referenceAllele', 'variantAllele', 'proteinChange', 'mutationType', 'ncbiBuild', 'variantType', 'refseqMrnaId', 'proteinPosStart', 'proteinPosEnd', 'keyword'] | None = None
    direction : Literal['ASC', 'DESC'] | None = 'ASC'


@dataclass
class fetchAllMolecularDataInMolecularProfileUsingPOSTPathParameters:
    molecularProfileId : str 


@dataclass
class fetchAllMolecularDataInMolecularProfileUsingPOSTQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'


@dataclass
class getGenePanelDataUsingPOSTPathParameters:
    molecularProfileId : str 


@dataclass
class getGenePanelDataUsingPOSTQueryParameters:
    pass


@dataclass
class fetchDiscreteCopyNumbersInMolecularProfileUsingPOSTPathParameters:
    molecularProfileId : str 


@dataclass
class fetchDiscreteCopyNumbersInMolecularProfileUsingPOSTQueryParameters:
    discreteCopyNumberEventType : Literal['HOMDEL_AND_AMP', 'HOMDEL', 'AMP', 'GAIN', 'HETLOSS', 'DIPLOID', 'ALL'] | None = 'HOMDEL_AND_AMP'
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'


@dataclass
class fetchMolecularProfilesUsingPOSTPathParameters:
    pass


@dataclass
class fetchMolecularProfilesUsingPOSTQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'


@dataclass
class fetchMolecularDataInMultipleMolecularProfilesUsingPOSTPathParameters:
    pass


@dataclass
class fetchMolecularDataInMultipleMolecularProfilesUsingPOSTQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'


@dataclass
class fetchGenesUsingPOSTPathParameters:
    pass


@dataclass
class fetchGenesUsingPOSTQueryParameters:
    geneIdType : Literal['ENTREZ_GENE_ID', 'HUGO_GENE_SYMBOL'] | None = 'ENTREZ_GENE_ID'
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'


@dataclass
class fetchGenericAssayMetaUsingPOSTPathParameters:
    pass


@dataclass
class fetchGenericAssayMetaUsingPOSTQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'


@dataclass
class fetchGenericAssayDataInMolecularProfileUsingPOSTPathParameters:
    molecularProfileId : str 


@dataclass
class fetchGenericAssayDataInMolecularProfileUsingPOSTQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'


@dataclass
class fetchGenericAssayDataInMultipleMolecularProfilesUsingPOSTPathParameters:
    pass


@dataclass
class fetchGenericAssayDataInMultipleMolecularProfilesUsingPOSTQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'


@dataclass
class fetchGenePanelsUsingPOSTPathParameters:
    pass


@dataclass
class fetchGenePanelsUsingPOSTQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'


@dataclass
class fetchGenePanelDataInMultipleMolecularProfilesUsingPOSTPathParameters:
    pass


@dataclass
class fetchGenePanelDataInMultipleMolecularProfilesUsingPOSTQueryParameters:
    pass


@dataclass
class fetchCopyNumberSegmentsUsingPOSTPathParameters:
    pass


@dataclass
class fetchCopyNumberSegmentsUsingPOSTQueryParameters:
    chromosome : str | None = None
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'


@dataclass
class fetchClinicalDataUsingPOSTPathParameters:
    pass


@dataclass
class fetchClinicalDataUsingPOSTQueryParameters:
    clinicalDataType : Literal['SAMPLE', 'PATIENT'] | None = 'SAMPLE'
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'


@dataclass
class fetchClinicalAttributesUsingPOSTPathParameters:
    pass


@dataclass
class fetchClinicalAttributesUsingPOSTQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'


@dataclass
class getAllStudiesUsingGETPathParameters:
    pass


@dataclass
class getAllStudiesUsingGETQueryParameters:
    keyword : str | None = None
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'
    pageSize : int | None = 10000000
    pageNumber : int | None = 0
    sortBy : Literal['studyId', 'cancerTypeId', 'name', 'description', 'publicStudy', 'pmid', 'citation', 'groups', 'status', 'importDate'] | None = None
    direction : Literal['ASC', 'DESC'] | None = 'ASC'


@dataclass
class getStudyUsingGETPathParameters:
    studyId : str 


@dataclass
class getStudyUsingGETQueryParameters:
    pass


@dataclass
class getTagsUsingGETPathParameters:
    studyId : str 


@dataclass
class getTagsUsingGETQueryParameters:
    pass


@dataclass
class getAllSamplesInStudyUsingGETPathParameters:
    studyId : str 


@dataclass
class getAllSamplesInStudyUsingGETQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'
    pageSize : int | None = 10000000
    pageNumber : int | None = 0
    sortBy : Literal['sampleId', 'sampleType'] | None = None
    direction : Literal['ASC', 'DESC'] | None = 'ASC'


@dataclass
class getSampleInStudyUsingGETPathParameters:
    studyId : str 
    sampleId : str 


@dataclass
class getSampleInStudyUsingGETQueryParameters:
    pass


@dataclass
class getCopyNumberSegmentsInSampleInStudyUsingGETPathParameters:
    studyId : str 
    sampleId : str 


@dataclass
class getCopyNumberSegmentsInSampleInStudyUsingGETQueryParameters:
    chromosome : str | None = None
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'
    pageSize : int | None = 20000
    pageNumber : int | None = 0
    sortBy : Literal['chromosome', 'start', 'end', 'numberOfProbes', 'segmentMean'] | None = None
    direction : Literal['ASC', 'DESC'] | None = 'ASC'


@dataclass
class getAllClinicalDataOfSampleInStudyUsingGETPathParameters:
    studyId : str 
    sampleId : str 


@dataclass
class getAllClinicalDataOfSampleInStudyUsingGETQueryParameters:
    attributeId : str | None = None
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'
    pageSize : int | None = 10000000
    pageNumber : int | None = 0
    sortBy : Literal['clinicalAttributeId', 'value'] | None = None
    direction : Literal['ASC', 'DESC'] | None = 'ASC'


@dataclass
class getAllSampleListsInStudyUsingGETPathParameters:
    studyId : str 


@dataclass
class getAllSampleListsInStudyUsingGETQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'
    pageSize : int | None = 10000000
    pageNumber : int | None = 0
    sortBy : Literal['sampleListId', 'category', 'studyId', 'name', 'description'] | None = None
    direction : Literal['ASC', 'DESC'] | None = 'ASC'


@dataclass
class getAllPatientsInStudyUsingGETPathParameters:
    studyId : str 


@dataclass
class getAllPatientsInStudyUsingGETQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'
    pageSize : int | None = 10000000
    pageNumber : int | None = 0
    sortBy : Literal['patientId'] | None = None
    direction : Literal['ASC', 'DESC'] | None = 'ASC'


@dataclass
class getPatientInStudyUsingGETPathParameters:
    studyId : str 
    patientId : str 


@dataclass
class getPatientInStudyUsingGETQueryParameters:
    pass


@dataclass
class getAllSamplesOfPatientInStudyUsingGETPathParameters:
    studyId : str 
    patientId : str 


@dataclass
class getAllSamplesOfPatientInStudyUsingGETQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'
    pageSize : int | None = 10000000
    pageNumber : int | None = 0
    sortBy : Literal['sampleId', 'sampleType'] | None = None
    direction : Literal['ASC', 'DESC'] | None = 'ASC'


@dataclass
class getAllClinicalDataOfPatientInStudyUsingGETPathParameters:
    studyId : str 
    patientId : str 


@dataclass
class getAllClinicalDataOfPatientInStudyUsingGETQueryParameters:
    attributeId : str | None = None
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'
    pageSize : int | None = 10000000
    pageNumber : int | None = 0
    sortBy : Literal['clinicalAttributeId', 'value'] | None = None
    direction : Literal['ASC', 'DESC'] | None = 'ASC'


@dataclass
class getAllMolecularProfilesInStudyUsingGETPathParameters:
    studyId : str 


@dataclass
class getAllMolecularProfilesInStudyUsingGETQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'
    pageSize : int | None = 10000000
    pageNumber : int | None = 0
    sortBy : Literal['molecularProfileId', 'molecularAlterationType', 'datatype', 'name', 'description', 'showProfileInAnalysisTab'] | None = None
    direction : Literal['ASC', 'DESC'] | None = 'ASC'


@dataclass
class getAllClinicalDataInStudyUsingGETPathParameters:
    studyId : str 


@dataclass
class getAllClinicalDataInStudyUsingGETQueryParameters:
    attributeId : str | None = None
    clinicalDataType : Literal['SAMPLE', 'PATIENT'] | None = 'SAMPLE'
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'
    pageSize : int | None = 10000000
    pageNumber : int | None = 0
    sortBy : Literal['clinicalAttributeId', 'value'] | None = None
    direction : Literal['ASC', 'DESC'] | None = 'ASC'


@dataclass
class getAllClinicalAttributesInStudyUsingGETPathParameters:
    studyId : str 


@dataclass
class getAllClinicalAttributesInStudyUsingGETQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'
    pageSize : int | None = 10000000
    pageNumber : int | None = 0
    sortBy : Literal['clinicalAttributeId', 'displayName', 'description', 'datatype', 'patientAttribute', 'priority', 'studyId'] | None = None
    direction : Literal['ASC', 'DESC'] | None = 'ASC'


@dataclass
class getClinicalAttributeInStudyUsingGETPathParameters:
    studyId : str 
    clinicalAttributeId : str 


@dataclass
class getClinicalAttributeInStudyUsingGETQueryParameters:
    pass


@dataclass
class getSamplesByKeywordUsingGETPathParameters:
    pass


@dataclass
class getSamplesByKeywordUsingGETQueryParameters:
    keyword : str | None = None
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'
    pageSize : int | None = 10000000
    pageNumber : int | None = 0
    sortBy : Literal['sampleId', 'sampleType'] | None = None
    direction : Literal['ASC', 'DESC'] | None = 'ASC'


@dataclass
class getAllSampleListsUsingGETPathParameters:
    pass


@dataclass
class getAllSampleListsUsingGETQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'
    pageSize : int | None = 10000000
    pageNumber : int | None = 0
    sortBy : Literal['sampleListId', 'category', 'studyId', 'name', 'description'] | None = None
    direction : Literal['ASC', 'DESC'] | None = 'ASC'


@dataclass
class getSampleListUsingGETPathParameters:
    sampleListId : str 


@dataclass
class getSampleListUsingGETQueryParameters:
    pass


@dataclass
class getAllSampleIdsInSampleListUsingGETPathParameters:
    sampleListId : str 


@dataclass
class getAllSampleIdsInSampleListUsingGETQueryParameters:
    pass


@dataclass
class getAllPatientsUsingGETPathParameters:
    pass


@dataclass
class getAllPatientsUsingGETQueryParameters:
    keyword : str | None = None
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'
    pageSize : int | None = 10000000
    pageNumber : int | None = 0
    sortBy : Literal['patientId'] | None = None
    direction : Literal['ASC', 'DESC'] | None = 'ASC'


@dataclass
class getAllMolecularProfilesUsingGETPathParameters:
    pass


@dataclass
class getAllMolecularProfilesUsingGETQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'
    pageSize : int | None = 10000000
    pageNumber : int | None = 0
    sortBy : Literal['molecularProfileId', 'molecularAlterationType', 'datatype', 'name', 'description', 'showProfileInAnalysisTab'] | None = None
    direction : Literal['ASC', 'DESC'] | None = 'ASC'


@dataclass
class getMolecularProfileUsingGETPathParameters:
    molecularProfileId : str 


@dataclass
class getMolecularProfileUsingGETQueryParameters:
    pass


@dataclass
class getMutationsInMolecularProfileBySampleListIdUsingGETPathParameters:
    molecularProfileId : str 


@dataclass
class getMutationsInMolecularProfileBySampleListIdUsingGETQueryParameters:
    sampleListId : str 
    entrezGeneId : int | None = None
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'
    pageSize : int | None = 10000000
    pageNumber : int | None = 0
    sortBy : Literal['entrezGeneId', 'center', 'mutationStatus', 'validationStatus', 'tumorAltCount', 'tumorRefCount', 'normalAltCount', 'normalRefCount', 'aminoAcidChange', 'startPosition', 'endPosition', 'referenceAllele', 'variantAllele', 'proteinChange', 'mutationType', 'ncbiBuild', 'variantType', 'refseqMrnaId', 'proteinPosStart', 'proteinPosEnd', 'keyword'] | None = None
    direction : Literal['ASC', 'DESC'] | None = 'ASC'


@dataclass
class getAllMolecularDataInMolecularProfileUsingGETPathParameters:
    molecularProfileId : str 


@dataclass
class getAllMolecularDataInMolecularProfileUsingGETQueryParameters:
    sampleListId : str 
    entrezGeneId : int 
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'


@dataclass
class getDiscreteCopyNumbersInMolecularProfileUsingGETPathParameters:
    molecularProfileId : str 


@dataclass
class getDiscreteCopyNumbersInMolecularProfileUsingGETQueryParameters:
    sampleListId : str 
    discreteCopyNumberEventType : Literal['HOMDEL_AND_AMP', 'HOMDEL', 'AMP', 'GAIN', 'HETLOSS', 'DIPLOID', 'ALL'] | None = 'HOMDEL_AND_AMP'
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'


@dataclass
class getInfoUsingGETPathParameters:
    pass


@dataclass
class getInfoUsingGETQueryParameters:
    pass


@dataclass
class getServerStatusUsingGETPathParameters:
    pass


@dataclass
class getServerStatusUsingGETQueryParameters:
    pass


@dataclass
class getAllGenesUsingGETPathParameters:
    pass


@dataclass
class getAllGenesUsingGETQueryParameters:
    keyword : str | None = None
    alias : str | None = None
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'
    pageSize : int | None = 10000000
    pageNumber : int | None = 0
    sortBy : Literal['entrezGeneId', 'hugoGeneSymbol', 'type', 'cytoband', 'length'] | None = None
    direction : Literal['ASC', 'DESC'] | None = 'ASC'


@dataclass
class getGeneUsingGETPathParameters:
    geneId : str 


@dataclass
class getGeneUsingGETQueryParameters:
    pass


@dataclass
class getAliasesOfGeneUsingGETPathParameters:
    geneId : str 


@dataclass
class getAliasesOfGeneUsingGETQueryParameters:
    pass


@dataclass
class getGenericAssayMetaUsingGETPathParameters:
    molecularProfileId : str 


@dataclass
class getGenericAssayMetaUsingGETQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'


@dataclass
class getGenericAssayMeta_gaUsingGETPathParameters:
    genericAssayStableId : str 


@dataclass
class getGenericAssayMeta_gaUsingGETQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'


@dataclass
class getGenericAssayDataInMolecularProfileUsingGETPathParameters:
    molecularProfileId : str 
    genericAssayStableId : str 


@dataclass
class getGenericAssayDataInMolecularProfileUsingGETQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'


@dataclass
class getAllGenePanelsUsingGETPathParameters:
    pass


@dataclass
class getAllGenePanelsUsingGETQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'
    pageSize : int | None = 10000000
    pageNumber : int | None = 0
    sortBy : Literal['genePanelId', 'description'] | None = None
    direction : Literal['ASC', 'DESC'] | None = 'ASC'


@dataclass
class getGenePanelUsingGETPathParameters:
    genePanelId : str 


@dataclass
class getGenePanelUsingGETQueryParameters:
    pass


@dataclass
class getAllClinicalAttributesUsingGETPathParameters:
    pass


@dataclass
class getAllClinicalAttributesUsingGETQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'
    pageSize : int | None = 10000000
    pageNumber : int | None = 0
    sortBy : Literal['clinicalAttributeId', 'displayName', 'description', 'datatype', 'patientAttribute', 'priority', 'studyId'] | None = None
    direction : Literal['ASC', 'DESC'] | None = 'ASC'


@dataclass
class getAllCancerTypesUsingGETPathParameters:
    pass


@dataclass
class getAllCancerTypesUsingGETQueryParameters:
    projection : Literal['ID', 'SUMMARY', 'DETAILED', 'META'] | None = 'SUMMARY'
    pageSize : int | None = 10000000
    pageNumber : int | None = 0
    sortBy : Literal['cancerTypeId', 'name', 'dedicatedColor', 'shortName', 'parent'] | None = None
    direction : Literal['ASC', 'DESC'] | None = 'ASC'


@dataclass
class getCancerTypeUsingGETPathParameters:
    cancerTypeId : str 


@dataclass
class getCancerTypeUsingGETQueryParameters:
    pass

class BiomeAgent(BaseAgent):
    """
    You are a chat assistant that helps the analyst user with their questions. You are running inside of the Analyst UI which is a chat application
    sitting on top of a Jupyter notebook. This means the user will not be looking at code and will expect you to run code under the hood. Of course,
    power users may end up inspecting the code you you end up running and editing it.

    You have the ability to look up information regarding the environment via the tools that are provided. You should use these tools whenever are not able to
    satisfy the request to a high level of reliability. You should avoid guessing at how to do something in favor of using the provided tools to look up more
    information. Do not make assumptions, always check the documentation instead of assuming.

    Remember to use the full name of the tool, prefixed with BiomeAgent.
    You will have tools for interacting with web APIs.
    As a general rule, when interacting with APIs, try to use GET requests before POST requests. If a relevant tool exists for both
    GET and POST, try them both if one fails. 
    Do not stop after one failed API call and instead try other HTTP verbs or a different approach.
    Prefer GET tools over POST tools where possible.
    
    You are currently working in the Biome app. The Biome app is a collection of data sources where a data source is a profiled website targeted specifically
    at cancer research. The user can add new data sources or may ask you to browser the data sources and return relevant datasets or other info. An example
    of a flow could be looking through all the data sources, picking one, finding a dataset using the URL, and then finally loading that dataset into a pandas
    dataframe.
    """
    def __init__(self, context: BaseContext = None, tools: list = None, **kwargs):
        libraries = {
        }
        super().__init__(context, tools, **kwargs)
    
    # def update_job_status(self, job_id, status):
    #     self.context.send_response("iopub", 
    #             "job_status", {
    #                 "job_id": job_id,
    #                 "status": status 
    #             },
    #         )

    # # TODO: Formatting of these messages should be left to the Analyst-UI in the future. 
    # async def poll_query(self, job_id: str):
    #     # Poll result
    #     status = "queued"
    #     result = None
    #     while status == "queued":
    #         response = requests.get(f"{BIOME_URL}/jobs/{job_id}").json()
    #         status = response["status"]
    #         sleep(1)
        
    #     self.update_job_status(job_id, status)

    #     #asyncio.create_task(self.poll_query_logs(job_id))
    #     while status == "started":
    #         response = requests.get(f"{BIOME_URL}/jobs/{job_id}/logs").json()
    #         self.context.send_response("iopub",
    #             "job_logs", {
    #                 "job_id": job_id,
    #                 "logs": response,
    #             },
    #         )
    #         response = requests.get(f"{BIOME_URL}/jobs/{job_id}").json()
    #         status = response["status"]
    #         sleep(5)

    #     self.update_job_status(job_id, status)

    #     # Handle result
    #     if status != "finished":
    #         self.update_job_status(job_id, status)
    #         self.context.send_response("iopub", 
    #             "job_failure", {
    #                 "job_id": job_id,
    #                 "response": response
    #             },
    #         ) 

    #     result = response["result"] # TODO: Bubble up better cell type
    #     self.context.send_response("iopub",
    #         "job_response", {
    #             "job_id": job_id,
    #             "response": result['answer'],
    #             "raw": result
    #         },
    #     ) 

    # @tool(autosummarize=True)
    # async def search(self, query: str) -> list[dict[str, Any]]:
    #     """
    #     Search for data sources in the Biome app. Results will be matched semantically
    #     and string distance. Use this to find a data source. You don't need live
    #     web searches. If the user asks about data sources, use this tool.

    #     Be sure to use the `display_search` tool for the output. Ensure you always use `display_search` after.

    #     Args:
    #         query (str): The query used to find the datasource.
    #     Returns:
    #         list: A JSON-formatted string containing a list of strings.
    #               The list should contain only the `name` field and no other field
    #               of the data sources found, ordered from most relevant to least relevant.
    #               Ensure that only the name field is present.
    #               An example is provided surrounded in backticks.
    #               ```
    #               ["Proteomics Data Commons", ""Office of Cancer Clinical Proteomics Research", "UniProt"]
    #               ```
    #     """

    #     endpoint = f"{BIOME_URL}/sources"
    #     response = requests.get(endpoint, params={"query": query})
    #     raw_sources = response.json()['sources']
    #     sources = [
    #         # Include only necessary fields to ensure LLM context length is not exceeded.
    #         {
    #             "id": source["id"],
    #             "name": source["content"]["Web Page Descriptions"]["name"],
    #             "initials": source["content"]["Web Page Descriptions"]["initials"],
    #             "purpose": source["content"]["Web Page Descriptions"]["purpose"],
    #             "links": source["content"]["Information on Links on Web Page"],
    #             "base_url": source.get("base_url", None)
    #         } for source in raw_sources
    #     ]
    #     return sources

    # @tool(autosummarize=True)
    # async def display_search(self, results: list[str], agent:AgentRef, loop: LoopControllerRef):
    #     """
    #     Once search has been performed, this tool will display it to the user.
    #     Args:
    #         results (list): The query used to find the datasource.
    #     """
    #     # sometimes it wraps the output
    #     if isinstance(results, dict):
    #         results = results.get("results", results)
    #     endpoint = f"{BIOME_URL}/sources"
    #     response = requests.get(endpoint, params={
    #         "simple_query_string": {
    #             "fields": ["content.Web Page Descriptions.name"],
    #             "query": "|".join(results)
    #         }
    #     })
    #     raw_sources = response.json()['sources']
    #     sources = [
    #         {
    #             "id": source["id"],
    #             "name": source["content"]["Web Page Descriptions"]["name"],
    #             "initials": source["content"]["Web Page Descriptions"]["initials"],
    #             "purpose": source["content"]["Web Page Descriptions"]["purpose"],
    #             "links": source["content"]["Information on Links on Web Page"],
    #             "base_url": source.get("base_url", None),
    #             "logo": source.get("logo", None)
    #         } for source in raw_sources
    #     ]
    #     # match sources to ordering from previous llm step by dict to avoid n^2

    #     sources_map = { source.get("name", ""): source for source in sources }
    #     ordered_sources = [sources_map[name] for name in results]
    #     self.context.send_response("iopub",
    #         "data_sources", {
    #             "sources": ordered_sources
    #         },
    #     )
    #     loop.set_state(loop.STOP_SUCCESS)

    # # TODO(DESIGN): Deal with long running jobs in tools
    # #
    # # Option 1: We can return the job id and the agent can poll for the result.
    # # This will require a job status tool. Once the status is done, we can either
    # # check the result if it's a query or check the data source if it's a scan.
    # # This feels a bit messy though that the job creation has a similar return
    # # output on queue but getting the result is very different for each job.
    # #
    # # Option 2: We can wait for the job and return it to the agent when it's done
    # #
    # # Option 3: We can maybe leverage new widgets in the Analyst UI??
    # #

    # # CHOOSING OPTION 1 FOR THE TIME BEING
    # @tool()
    # async def query_page(self, task: str, base_url: str, agent: AgentRef, loop: LoopControllerRef):
    #     """
    #     Run an action over a *specific* source in the Biome app and return the results.
    #     Find the url from a data source by using `search` tool first and
    #     picking the most relevant one.

    #     This kicks off a long-running job so you'll have to just return the ID to the user
    #     instead of the result. 

    #     This can be used to ask questions about a data source or download some kind
    #     of artifact from it. This tool just kicks off a job where an AI crawls the website
    #     and performs the task.

    #     Args:
    #         task (str): Task given in natural language to perform over URL.
    #         base_url (str): URL to run query over.
    #     """
    #     response = requests.post( f"{BIOME_URL}/jobs/query", json={"user_task": task, "url": base_url})
    #     job_id = response.json()["job_id"]
    #     self.context.send_response("iopub",
    #         "job_create", {
    #             "job_id": job_id,
    #             "task": task,
    #             "url": base_url
    #         },
    #     )
    #     asyncio.create_task(self.poll_query(job_id))
    #     loop.set_state(loop.STOP_SUCCESS)

    # @tool()
    # async def scan(self, base_url: str, agent:AgentRef, loop: LoopControllerRef) -> str:
    #     """
    #     Profiles the given web page and adds it to the data sources in the Biome app.

    #     This kicks off a long-running job so you'll have to just return the ID to the user
    #     instead of the result. 

    #     Args:
    #         base_url (str): The url to scan and add as a data source.
    #     Returns:
    #         str: Job ID to poll for the result. 
    #     """
    #     response = requests.post( f"{BIOME_URL}/jobs/scan", json={"uris": [base_url]})
    #     job_id = response.json()["job_id"]
    #     asyncio.create_task(self.poll_query(job_id))
    #     return job_id


    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Fetch clinical data by patient IDs or sample IDs (specific study)

        Args:
            target_var (str): The target variable to save the results to.
            path_params (fetchAllClinicalDataInStudyUsingPOSTPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                fetchAllClinicalDataInStudyUsingPOSTPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {fetchAllClinicalDataInStudyUsingPOSTPathParameters.__annotations__}
                    ```
            query_params (fetchAllClinicalDataInStudyUsingPOSTQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                fetchAllClinicalDataInStudyUsingPOSTQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {fetchAllClinicalDataInStudyUsingPOSTQueryParameters.__annotations__}
                    ```
    ''' + '''        
            request_body (str): The JSON string containing the request body to be sent with a POST request.
                Ensure that this is valid JSON. The expected format for the API call is given in an OpenAPI spec,
                enclosed within backticks:
                    ```
                    {'type': 'object', 'properties': {'ids': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'maxLength': 10000000, 'minLength': 1, 'type': 'string'}}, 'attributeIds': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'maxLength': 10000000, 'minLength': 1, 'type': 'string'}}}, 'description': 'List of patient or sample IDs and attribute IDs'}
                    ```''')
    async def fetchAllClinicalDataInStudyUsingPOST(
            self, 
            target_var: str,
            path_params: fetchAllClinicalDataInStudyUsingPOSTPathParameters, # type: ignore
            query_params: fetchAllClinicalDataInStudyUsingPOSTQueryParameters, # type: ignore
            request_body: str,
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/studies/{studyId}/clinical-data/fetch',
                "target_var": target_var, 
                'operation': 'post', 'path_params': path_params, 'query_params': query_params, 'request_body': request_body
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'post', 'path_params': path_params, 'query_params': query_params, 'request_body': request_body
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "e": str(evaluation),
                    'r': str(response),
                    't': str(type(response))
                }
            },
        )
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "sc": response.status_code,
                }
            },
        )
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        agent.messages = agent.messages[:-1]
        if response.status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call fetchAllClinicalDataInStudyUsingPOST to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response.json()) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call fetchAllClinicalDataInStudyUsingPOST failed with status code {response.status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template


    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Fetch clinical data by patient IDs or sample IDs (specific study)

        Args:
            target_var (str): The target variable to save the results to.
            path_params (fetchAllClinicalDataInStudyUsingPOSTPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                fetchAllClinicalDataInStudyUsingPOSTPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {fetchAllClinicalDataInStudyUsingPOSTPathParameters.__annotations__}
                    ```
            query_params (fetchAllClinicalDataInStudyUsingPOSTQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                fetchAllClinicalDataInStudyUsingPOSTQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {fetchAllClinicalDataInStudyUsingPOSTQueryParameters.__annotations__}
                    ```
    ''' + '''        
            request_body (str): The JSON string containing the request body to be sent with a POST request.
                Ensure that this is valid JSON. The expected format for the API call is given in an OpenAPI spec,
                enclosed within backticks:
                    ```
                    {'type': 'object', 'properties': {'ids': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'maxLength': 10000000, 'minLength': 1, 'type': 'string'}}, 'attributeIds': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'maxLength': 10000000, 'minLength': 1, 'type': 'string'}}}, 'description': 'List of patient or sample IDs and attribute IDs'}
                    ```''')
    async def fetchAllClinicalDataInStudyUsingPOST(
            self, 
            target_var: str,
            path_params: fetchAllClinicalDataInStudyUsingPOSTPathParameters, # type: ignore
            query_params: fetchAllClinicalDataInStudyUsingPOSTQueryParameters, # type: ignore
            request_body: str,
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/studies/{studyId}/clinical-data/fetch',
                "target_var": target_var, 
                'operation': 'post', 'path_params': path_params, 'query_params': query_params, 'request_body': request_body
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'post', 'path_params': path_params, 'query_params': query_params, 'request_body': request_body
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call fetchAllClinicalDataInStudyUsingPOST to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call fetchAllClinicalDataInStudyUsingPOST failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get the study tags by IDs

        Args:
            target_var (str): The target variable to save the results to.
    ''' + '''        
            request_body (str): The JSON string containing the request body to be sent with a POST request.
                Ensure that this is valid JSON. The expected format for the API call is given in an OpenAPI spec,
                enclosed within backticks:
                    ```
                    {'type': 'array', 'description': 'List of Study IDs', 'items': {'type': 'string'}}
                    ```''')
    async def getTagsForMultipleStudiesUsingPOST(
            self, 
            target_var: str,
            request_body: str,
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/studies/tags/fetch',
                "target_var": target_var, 
                'operation': 'post', 'request_body': request_body
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'post', 'request_body': request_body
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getTagsForMultipleStudiesUsingPOST to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getTagsForMultipleStudiesUsingPOST failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Fetch studies by IDs

        Args:
            target_var (str): The target variable to save the results to.
            query_params (fetchStudiesUsingPOSTQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                fetchStudiesUsingPOSTQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {fetchStudiesUsingPOSTQueryParameters.__annotations__}
                    ```
    ''' + '''        
            request_body (str): The JSON string containing the request body to be sent with a POST request.
                Ensure that this is valid JSON. The expected format for the API call is given in an OpenAPI spec,
                enclosed within backticks:
                    ```
                    {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'description': 'List of Study IDs', 'items': {'maxLength': 10000000, 'minLength': 1, 'type': 'string'}}
                    ```''')
    async def fetchStudiesUsingPOST(
            self, 
            target_var: str,
            query_params: fetchStudiesUsingPOSTQueryParameters, # type: ignore
            request_body: str,
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/studies/fetch',
                "target_var": target_var, 
                'operation': 'post', 'query_params': query_params, 'request_body': request_body
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'post', 'query_params': query_params, 'request_body': request_body
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call fetchStudiesUsingPOST to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call fetchStudiesUsingPOST failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Fetch samples by ID

        Args:
            target_var (str): The target variable to save the results to.
            query_params (fetchSamplesUsingPOSTQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                fetchSamplesUsingPOSTQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {fetchSamplesUsingPOSTQueryParameters.__annotations__}
                    ```
    ''' + '''        
            request_body (str): The JSON string containing the request body to be sent with a POST request.
                Ensure that this is valid JSON. The expected format for the API call is given in an OpenAPI spec,
                enclosed within backticks:
                    ```
                    {'type': 'object', 'properties': {'sampleIdentifiers': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'$ref': '#/components/schemas/SampleIdentifier'}}, 'sampleListIds': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'maxLength': 10000000, 'minLength': 1, 'type': 'string'}}, 'uniqueSampleKeys': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'maxLength': 10000000, 'minLength': 1, 'type': 'string'}}}, 'description': 'List of sample identifiers'}
                    ```''')
    async def fetchSamplesUsingPOST(
            self, 
            target_var: str,
            query_params: fetchSamplesUsingPOSTQueryParameters, # type: ignore
            request_body: str,
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/samples/fetch',
                "target_var": target_var, 
                'operation': 'post', 'query_params': query_params, 'request_body': request_body
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'post', 'query_params': query_params, 'request_body': request_body
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call fetchSamplesUsingPOST to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call fetchSamplesUsingPOST failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Fetch sample lists by ID

        Args:
            target_var (str): The target variable to save the results to.
            query_params (fetchSampleListsUsingPOSTQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                fetchSampleListsUsingPOSTQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {fetchSampleListsUsingPOSTQueryParameters.__annotations__}
                    ```
    ''' + '''        
            request_body (str): The JSON string containing the request body to be sent with a POST request.
                Ensure that this is valid JSON. The expected format for the API call is given in an OpenAPI spec,
                enclosed within backticks:
                    ```
                    {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'description': 'List of sample list IDs', 'items': {'maxLength': 10000000, 'minLength': 1, 'type': 'string'}}
                    ```''')
    async def fetchSampleListsUsingPOST(
            self, 
            target_var: str,
            query_params: fetchSampleListsUsingPOSTQueryParameters, # type: ignore
            request_body: str,
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/sample-lists/fetch',
                "target_var": target_var, 
                'operation': 'post', 'query_params': query_params, 'request_body': request_body
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'post', 'query_params': query_params, 'request_body': request_body
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call fetchSampleListsUsingPOST to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call fetchSampleListsUsingPOST failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        

        Args:
            target_var (str): The target variable to save the results to.
            query_params (fetchPatientsUsingPOSTQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                fetchPatientsUsingPOSTQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {fetchPatientsUsingPOSTQueryParameters.__annotations__}
                    ```
    ''' + '''        
            request_body (str): The JSON string containing the request body to be sent with a POST request.
                Ensure that this is valid JSON. The expected format for the API call is given in an OpenAPI spec,
                enclosed within backticks:
                    ```
                    {'type': 'object', 'properties': {'patientIdentifiers': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'$ref': '#/components/schemas/PatientIdentifier'}}, 'uniquePatientKeys': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'maxLength': 10000000, 'minLength': 1, 'type': 'string'}}}, 'description': 'List of patient identifiers'}
                    ```''')
    async def fetchPatientsUsingPOST(
            self, 
            target_var: str,
            query_params: fetchPatientsUsingPOSTQueryParameters, # type: ignore
            request_body: str,
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/patients/fetch',
                "target_var": target_var, 
                'operation': 'post', 'query_params': query_params, 'request_body': request_body
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'post', 'query_params': query_params, 'request_body': request_body
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call fetchPatientsUsingPOST to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call fetchPatientsUsingPOST failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Fetch mutations in multiple molecular profiles by sample IDs

        Args:
            target_var (str): The target variable to save the results to.
            query_params (fetchMutationsInMultipleMolecularProfilesUsingPOSTQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                fetchMutationsInMultipleMolecularProfilesUsingPOSTQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {fetchMutationsInMultipleMolecularProfilesUsingPOSTQueryParameters.__annotations__}
                    ```
    ''' + '''        
            request_body (str): The JSON string containing the request body to be sent with a POST request.
                Ensure that this is valid JSON. The expected format for the API call is given in an OpenAPI spec,
                enclosed within backticks:
                    ```
                    {'type': 'object', 'properties': {'sampleMolecularIdentifiers': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'$ref': '#/components/schemas/SampleMolecularIdentifier'}}, 'molecularProfileIds': {'type': 'array', 'items': {'type': 'string'}}, 'entrezGeneIds': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'maximum': 10000000, 'minimum': 1, 'type': 'integer', 'format': 'int32'}}}, 'description': 'List of Molecular Profile IDs or List of Molecular Profile ID / Sample ID pairs, and List of Entrez Gene IDs'}
                    ```''')
    async def fetchMutationsInMultipleMolecularProfilesUsingPOST(
            self, 
            target_var: str,
            query_params: fetchMutationsInMultipleMolecularProfilesUsingPOSTQueryParameters, # type: ignore
            request_body: str,
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/mutations/fetch',
                "target_var": target_var, 
                'operation': 'post', 'query_params': query_params, 'request_body': request_body
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'post', 'query_params': query_params, 'request_body': request_body
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call fetchMutationsInMultipleMolecularProfilesUsingPOST to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call fetchMutationsInMultipleMolecularProfilesUsingPOST failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Fetch mutations in a molecular profile

        Args:
            target_var (str): The target variable to save the results to.
            path_params (fetchMutationsInMolecularProfileUsingPOSTPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                fetchMutationsInMolecularProfileUsingPOSTPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {fetchMutationsInMolecularProfileUsingPOSTPathParameters.__annotations__}
                    ```
            query_params (fetchMutationsInMolecularProfileUsingPOSTQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                fetchMutationsInMolecularProfileUsingPOSTQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {fetchMutationsInMolecularProfileUsingPOSTQueryParameters.__annotations__}
                    ```
    ''' + '''        
            request_body (str): The JSON string containing the request body to be sent with a POST request.
                Ensure that this is valid JSON. The expected format for the API call is given in an OpenAPI spec,
                enclosed within backticks:
                    ```
                    {'type': 'object', 'properties': {'sampleIds': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'maxLength': 10000000, 'minLength': 1, 'type': 'string'}}, 'sampleListId': {'type': 'string'}, 'entrezGeneIds': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'maximum': 10000000, 'minimum': 1, 'type': 'integer', 'format': 'int32'}}}, 'description': 'List of Sample IDs/Sample List ID and Entrez Gene IDs'}
                    ```''')
    async def fetchMutationsInMolecularProfileUsingPOST(
            self, 
            target_var: str,
            path_params: fetchMutationsInMolecularProfileUsingPOSTPathParameters, # type: ignore
            query_params: fetchMutationsInMolecularProfileUsingPOSTQueryParameters, # type: ignore
            request_body: str,
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/molecular-profiles/{molecularProfileId}/mutations/fetch',
                "target_var": target_var, 
                'operation': 'post', 'path_params': path_params, 'query_params': query_params, 'request_body': request_body
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'post', 'path_params': path_params, 'query_params': query_params, 'request_body': request_body
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call fetchMutationsInMolecularProfileUsingPOST to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call fetchMutationsInMolecularProfileUsingPOST failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Fetch molecular data in a molecular profile

        Args:
            target_var (str): The target variable to save the results to.
            path_params (fetchAllMolecularDataInMolecularProfileUsingPOSTPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                fetchAllMolecularDataInMolecularProfileUsingPOSTPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {fetchAllMolecularDataInMolecularProfileUsingPOSTPathParameters.__annotations__}
                    ```
            query_params (fetchAllMolecularDataInMolecularProfileUsingPOSTQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                fetchAllMolecularDataInMolecularProfileUsingPOSTQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {fetchAllMolecularDataInMolecularProfileUsingPOSTQueryParameters.__annotations__}
                    ```
    ''' + '''        
            request_body (str): The JSON string containing the request body to be sent with a POST request.
                Ensure that this is valid JSON. The expected format for the API call is given in an OpenAPI spec,
                enclosed within backticks:
                    ```
                    {'type': 'object', 'properties': {'sampleIds': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'maxLength': 10000000, 'minLength': 1, 'type': 'string'}}, 'sampleListId': {'type': 'string'}, 'entrezGeneIds': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'maximum': 10000000, 'minimum': 1, 'type': 'integer', 'format': 'int32'}}}, 'description': 'List of Sample IDs/Sample List ID and Entrez Gene IDs'}
                    ```''')
    async def fetchAllMolecularDataInMolecularProfileUsingPOST(
            self, 
            target_var: str,
            path_params: fetchAllMolecularDataInMolecularProfileUsingPOSTPathParameters, # type: ignore
            query_params: fetchAllMolecularDataInMolecularProfileUsingPOSTQueryParameters, # type: ignore
            request_body: str,
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/molecular-profiles/{molecularProfileId}/molecular-data/fetch',
                "target_var": target_var, 
                'operation': 'post', 'path_params': path_params, 'query_params': query_params, 'request_body': request_body
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'post', 'path_params': path_params, 'query_params': query_params, 'request_body': request_body
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call fetchAllMolecularDataInMolecularProfileUsingPOST to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call fetchAllMolecularDataInMolecularProfileUsingPOST failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get gene panel data

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getGenePanelDataUsingPOSTPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getGenePanelDataUsingPOSTPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getGenePanelDataUsingPOSTPathParameters.__annotations__}
                    ```
    ''' + '''        
            request_body (str): The JSON string containing the request body to be sent with a POST request.
                Ensure that this is valid JSON. The expected format for the API call is given in an OpenAPI spec,
                enclosed within backticks:
                    ```
                    {'type': 'object', 'properties': {'sampleIds': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'maxLength': 10000000, 'minLength': 1, 'type': 'string'}}, 'sampleListId': {'type': 'string'}}, 'description': 'List of Sample IDs/Sample List ID and Entrez Gene IDs'}
                    ```''')
    async def getGenePanelDataUsingPOST(
            self, 
            target_var: str,
            path_params: getGenePanelDataUsingPOSTPathParameters, # type: ignore
            request_body: str,
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/molecular-profiles/{molecularProfileId}/gene-panel-data/fetch',
                "target_var": target_var, 
                'operation': 'post', 'path_params': path_params, 'request_body': request_body
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'post', 'path_params': path_params, 'request_body': request_body
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getGenePanelDataUsingPOST to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getGenePanelDataUsingPOST failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Fetch discrete copy number alterations in a molecular profile by sample ID

        Args:
            target_var (str): The target variable to save the results to.
            path_params (fetchDiscreteCopyNumbersInMolecularProfileUsingPOSTPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                fetchDiscreteCopyNumbersInMolecularProfileUsingPOSTPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {fetchDiscreteCopyNumbersInMolecularProfileUsingPOSTPathParameters.__annotations__}
                    ```
            query_params (fetchDiscreteCopyNumbersInMolecularProfileUsingPOSTQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                fetchDiscreteCopyNumbersInMolecularProfileUsingPOSTQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {fetchDiscreteCopyNumbersInMolecularProfileUsingPOSTQueryParameters.__annotations__}
                    ```
    ''' + '''        
            request_body (str): The JSON string containing the request body to be sent with a POST request.
                Ensure that this is valid JSON. The expected format for the API call is given in an OpenAPI spec,
                enclosed within backticks:
                    ```
                    {'type': 'object', 'properties': {'sampleIds': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'maxLength': 10000000, 'minLength': 1, 'type': 'string'}}, 'sampleListId': {'type': 'string'}, 'entrezGeneIds': {'maxItems': 50000, 'minItems': 1, 'type': 'array', 'items': {'maximum': 50000, 'minimum': 1, 'type': 'integer', 'format': 'int32'}}}, 'description': 'List of Sample IDs/Sample List ID and Entrez Gene IDs'}
                    ```''')
    async def fetchDiscreteCopyNumbersInMolecularProfileUsingPOST(
            self, 
            target_var: str,
            path_params: fetchDiscreteCopyNumbersInMolecularProfileUsingPOSTPathParameters, # type: ignore
            query_params: fetchDiscreteCopyNumbersInMolecularProfileUsingPOSTQueryParameters, # type: ignore
            request_body: str,
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/molecular-profiles/{molecularProfileId}/discrete-copy-number/fetch',
                "target_var": target_var, 
                'operation': 'post', 'path_params': path_params, 'query_params': query_params, 'request_body': request_body
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'post', 'path_params': path_params, 'query_params': query_params, 'request_body': request_body
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call fetchDiscreteCopyNumbersInMolecularProfileUsingPOST to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call fetchDiscreteCopyNumbersInMolecularProfileUsingPOST failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Fetch molecular profiles

        Args:
            target_var (str): The target variable to save the results to.
            query_params (fetchMolecularProfilesUsingPOSTQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                fetchMolecularProfilesUsingPOSTQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {fetchMolecularProfilesUsingPOSTQueryParameters.__annotations__}
                    ```
    ''' + '''        
            request_body (str): The JSON string containing the request body to be sent with a POST request.
                Ensure that this is valid JSON. The expected format for the API call is given in an OpenAPI spec,
                enclosed within backticks:
                    ```
                    {'type': 'object', 'properties': {'studyIds': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'maxLength': 10000000, 'minLength': 1, 'type': 'string'}}, 'molecularProfileIds': {'maxItems': 10000000, 'minItems': 1, 'uniqueItems': True, 'type': 'array', 'items': {'maxLength': 10000000, 'minLength': 1, 'type': 'string'}}}, 'description': 'List of Molecular Profile IDs or List of Study IDs'}
                    ```''')
    async def fetchMolecularProfilesUsingPOST(
            self, 
            target_var: str,
            query_params: fetchMolecularProfilesUsingPOSTQueryParameters, # type: ignore
            request_body: str,
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/molecular-profiles/fetch',
                "target_var": target_var, 
                'operation': 'post', 'query_params': query_params, 'request_body': request_body
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'post', 'query_params': query_params, 'request_body': request_body
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call fetchMolecularProfilesUsingPOST to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call fetchMolecularProfilesUsingPOST failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Fetch molecular data

        Args:
            target_var (str): The target variable to save the results to.
            query_params (fetchMolecularDataInMultipleMolecularProfilesUsingPOSTQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                fetchMolecularDataInMultipleMolecularProfilesUsingPOSTQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {fetchMolecularDataInMultipleMolecularProfilesUsingPOSTQueryParameters.__annotations__}
                    ```
    ''' + '''        
            request_body (str): The JSON string containing the request body to be sent with a POST request.
                Ensure that this is valid JSON. The expected format for the API call is given in an OpenAPI spec,
                enclosed within backticks:
                    ```
                    {'type': 'object', 'properties': {'sampleMolecularIdentifiers': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'$ref': '#/components/schemas/SampleMolecularIdentifier'}}, 'molecularProfileIds': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'maxLength': 10000000, 'minLength': 1, 'type': 'string'}}, 'entrezGeneIds': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'maximum': 10000000, 'minimum': 1, 'type': 'integer', 'format': 'int32'}}}, 'description': 'List of Molecular Profile ID and Sample ID pairs or List of MolecularProfile IDs and Entrez Gene IDs'}
                    ```''')
    async def fetchMolecularDataInMultipleMolecularProfilesUsingPOST(
            self, 
            target_var: str,
            query_params: fetchMolecularDataInMultipleMolecularProfilesUsingPOSTQueryParameters, # type: ignore
            request_body: str,
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/molecular-data/fetch',
                "target_var": target_var, 
                'operation': 'post', 'query_params': query_params, 'request_body': request_body
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'post', 'query_params': query_params, 'request_body': request_body
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call fetchMolecularDataInMultipleMolecularProfilesUsingPOST to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call fetchMolecularDataInMultipleMolecularProfilesUsingPOST failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Fetch genes by ID

        Args:
            target_var (str): The target variable to save the results to.
            query_params (fetchGenesUsingPOSTQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                fetchGenesUsingPOSTQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {fetchGenesUsingPOSTQueryParameters.__annotations__}
                    ```
    ''' + '''        
            request_body (str): The JSON string containing the request body to be sent with a POST request.
                Ensure that this is valid JSON. The expected format for the API call is given in an OpenAPI spec,
                enclosed within backticks:
                    ```
                    {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'description': 'List of Gene IDs', 'items': {'maxLength': 10000000, 'minLength': 1, 'type': 'string'}}
                    ```''')
    async def fetchGenesUsingPOST(
            self, 
            target_var: str,
            query_params: fetchGenesUsingPOSTQueryParameters, # type: ignore
            request_body: str,
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/genes/fetch',
                "target_var": target_var, 
                'operation': 'post', 'query_params': query_params, 'request_body': request_body
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'post', 'query_params': query_params, 'request_body': request_body
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call fetchGenesUsingPOST to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call fetchGenesUsingPOST failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Fetch meta data for generic-assay by ID

        Args:
            target_var (str): The target variable to save the results to.
            query_params (fetchGenericAssayMetaUsingPOSTQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                fetchGenericAssayMetaUsingPOSTQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {fetchGenericAssayMetaUsingPOSTQueryParameters.__annotations__}
                    ```
    ''' + '''        
            request_body (str): The JSON string containing the request body to be sent with a POST request.
                Ensure that this is valid JSON. The expected format for the API call is given in an OpenAPI spec,
                enclosed within backticks:
                    ```
                    {'type': 'object', 'properties': {'molecularProfileIds': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'maxLength': 10000000, 'minLength': 1, 'type': 'string'}}, 'genericAssayStableIds': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'maxLength': 10000000, 'minLength': 1, 'type': 'string'}}}, 'description': 'List of Molecular Profile ID or List of Stable ID'}
                    ```''')
    async def fetchGenericAssayMetaUsingPOST(
            self, 
            target_var: str,
            query_params: fetchGenericAssayMetaUsingPOSTQueryParameters, # type: ignore
            request_body: str,
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/generic_assay_meta/fetch',
                "target_var": target_var, 
                'operation': 'post', 'query_params': query_params, 'request_body': request_body
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'post', 'query_params': query_params, 'request_body': request_body
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call fetchGenericAssayMetaUsingPOST to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call fetchGenericAssayMetaUsingPOST failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        fetch generic_assay_data in a molecular profile

        Args:
            target_var (str): The target variable to save the results to.
            path_params (fetchGenericAssayDataInMolecularProfileUsingPOSTPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                fetchGenericAssayDataInMolecularProfileUsingPOSTPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {fetchGenericAssayDataInMolecularProfileUsingPOSTPathParameters.__annotations__}
                    ```
            query_params (fetchGenericAssayDataInMolecularProfileUsingPOSTQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                fetchGenericAssayDataInMolecularProfileUsingPOSTQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {fetchGenericAssayDataInMolecularProfileUsingPOSTQueryParameters.__annotations__}
                    ```
    ''' + '''        
            request_body (str): The JSON string containing the request body to be sent with a POST request.
                Ensure that this is valid JSON. The expected format for the API call is given in an OpenAPI spec,
                enclosed within backticks:
                    ```
                    {'type': 'object', 'properties': {'sampleIds': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'maxLength': 10000000, 'minLength': 1, 'type': 'string'}}, 'sampleListId': {'type': 'string'}, 'genericAssayStableIds': {'type': 'array', 'items': {'type': 'string'}}}, 'description': 'List of Sample IDs/Sample List ID and Generic Assay IDs'}
                    ```''')
    async def fetchGenericAssayDataInMolecularProfileUsingPOST(
            self, 
            target_var: str,
            path_params: fetchGenericAssayDataInMolecularProfileUsingPOSTPathParameters, # type: ignore
            query_params: fetchGenericAssayDataInMolecularProfileUsingPOSTQueryParameters, # type: ignore
            request_body: str,
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/generic_assay_data/{molecularProfileId}/fetch',
                "target_var": target_var, 
                'operation': 'post', 'path_params': path_params, 'query_params': query_params, 'request_body': request_body
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'post', 'path_params': path_params, 'query_params': query_params, 'request_body': request_body
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call fetchGenericAssayDataInMolecularProfileUsingPOST to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call fetchGenericAssayDataInMolecularProfileUsingPOST failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Fetch generic_assay_data

        Args:
            target_var (str): The target variable to save the results to.
            query_params (fetchGenericAssayDataInMultipleMolecularProfilesUsingPOSTQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                fetchGenericAssayDataInMultipleMolecularProfilesUsingPOSTQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {fetchGenericAssayDataInMultipleMolecularProfilesUsingPOSTQueryParameters.__annotations__}
                    ```
    ''' + '''        
            request_body (str): The JSON string containing the request body to be sent with a POST request.
                Ensure that this is valid JSON. The expected format for the API call is given in an OpenAPI spec,
                enclosed within backticks:
                    ```
                    {'type': 'object', 'properties': {'sampleMolecularIdentifiers': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'$ref': '#/components/schemas/SampleMolecularIdentifier'}}, 'molecularProfileIds': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'maxLength': 10000000, 'minLength': 1, 'type': 'string'}}, 'genericAssayStableIds': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'maxLength': 10000000, 'minLength': 1, 'type': 'string'}}}, 'description': 'List of Molecular Profile ID and Sample ID pairs or List of MolecularProfile IDs and Generic Assay IDs'}
                    ```''')
    async def fetchGenericAssayDataInMultipleMolecularProfilesUsingPOST(
            self, 
            target_var: str,
            query_params: fetchGenericAssayDataInMultipleMolecularProfilesUsingPOSTQueryParameters, # type: ignore
            request_body: str,
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/generic_assay_data/fetch',
                "target_var": target_var, 
                'operation': 'post', 'query_params': query_params, 'request_body': request_body
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'post', 'query_params': query_params, 'request_body': request_body
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call fetchGenericAssayDataInMultipleMolecularProfilesUsingPOST to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call fetchGenericAssayDataInMultipleMolecularProfilesUsingPOST failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get gene panel

        Args:
            target_var (str): The target variable to save the results to.
            query_params (fetchGenePanelsUsingPOSTQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                fetchGenePanelsUsingPOSTQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {fetchGenePanelsUsingPOSTQueryParameters.__annotations__}
                    ```
    ''' + '''        
            request_body (str): The JSON string containing the request body to be sent with a POST request.
                Ensure that this is valid JSON. The expected format for the API call is given in an OpenAPI spec,
                enclosed within backticks:
                    ```
                    {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'description': 'List of Gene Panel IDs', 'items': {'maxLength': 10000000, 'minLength': 1, 'type': 'string'}}
                    ```''')
    async def fetchGenePanelsUsingPOST(
            self, 
            target_var: str,
            query_params: fetchGenePanelsUsingPOSTQueryParameters, # type: ignore
            request_body: str,
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/gene-panels/fetch',
                "target_var": target_var, 
                'operation': 'post', 'query_params': query_params, 'request_body': request_body
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'post', 'query_params': query_params, 'request_body': request_body
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call fetchGenePanelsUsingPOST to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call fetchGenePanelsUsingPOST failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Fetch gene panel data

        Args:
            target_var (str): The target variable to save the results to.
    ''' + '''        
            request_body (str): The JSON string containing the request body to be sent with a POST request.
                Ensure that this is valid JSON. The expected format for the API call is given in an OpenAPI spec,
                enclosed within backticks:
                    ```
                    {'type': 'object', 'properties': {'sampleMolecularIdentifiers': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'$ref': '#/components/schemas/SampleMolecularIdentifier'}}, 'molecularProfileIds': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'maxLength': 10000000, 'minLength': 1, 'type': 'string'}}}, 'description': 'Gene panel data filter object'}
                    ```''')
    async def fetchGenePanelDataInMultipleMolecularProfilesUsingPOST(
            self, 
            target_var: str,
            request_body: str,
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/gene-panel-data/fetch',
                "target_var": target_var, 
                'operation': 'post', 'request_body': request_body
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'post', 'request_body': request_body
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call fetchGenePanelDataInMultipleMolecularProfilesUsingPOST to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call fetchGenePanelDataInMultipleMolecularProfilesUsingPOST failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Fetch copy number segments by sample ID

        Args:
            target_var (str): The target variable to save the results to.
            query_params (fetchCopyNumberSegmentsUsingPOSTQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                fetchCopyNumberSegmentsUsingPOSTQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {fetchCopyNumberSegmentsUsingPOSTQueryParameters.__annotations__}
                    ```
    ''' + '''        
            request_body (str): The JSON string containing the request body to be sent with a POST request.
                Ensure that this is valid JSON. The expected format for the API call is given in an OpenAPI spec,
                enclosed within backticks:
                    ```
                    {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'description': 'List of sample identifiers', 'items': {'$ref': '#/components/schemas/SampleIdentifier'}}
                    ```''')
    async def fetchCopyNumberSegmentsUsingPOST(
            self, 
            target_var: str,
            query_params: fetchCopyNumberSegmentsUsingPOSTQueryParameters, # type: ignore
            request_body: str,
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/copy-number-segments/fetch',
                "target_var": target_var, 
                'operation': 'post', 'query_params': query_params, 'request_body': request_body
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'post', 'query_params': query_params, 'request_body': request_body
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call fetchCopyNumberSegmentsUsingPOST to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call fetchCopyNumberSegmentsUsingPOST failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Fetch clinical data by patient IDs or sample IDs (all studies)

        Args:
            target_var (str): The target variable to save the results to.
            query_params (fetchClinicalDataUsingPOSTQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                fetchClinicalDataUsingPOSTQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {fetchClinicalDataUsingPOSTQueryParameters.__annotations__}
                    ```
    ''' + '''        
            request_body (str): The JSON string containing the request body to be sent with a POST request.
                Ensure that this is valid JSON. The expected format for the API call is given in an OpenAPI spec,
                enclosed within backticks:
                    ```
                    {'type': 'object', 'properties': {'identifiers': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'$ref': '#/components/schemas/ClinicalDataIdentifier'}}, 'attributeIds': {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'items': {'maxLength': 10000000, 'minLength': 1, 'type': 'string'}}}, 'description': 'List of patient or sample identifiers and attribute IDs'}
                    ```''')
    async def fetchClinicalDataUsingPOST(
            self, 
            target_var: str,
            query_params: fetchClinicalDataUsingPOSTQueryParameters, # type: ignore
            request_body: str,
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/clinical-data/fetch',
                "target_var": target_var, 
                'operation': 'post', 'query_params': query_params, 'request_body': request_body
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'post', 'query_params': query_params, 'request_body': request_body
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call fetchClinicalDataUsingPOST to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call fetchClinicalDataUsingPOST failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Fetch clinical attributes

        Args:
            target_var (str): The target variable to save the results to.
            query_params (fetchClinicalAttributesUsingPOSTQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                fetchClinicalAttributesUsingPOSTQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {fetchClinicalAttributesUsingPOSTQueryParameters.__annotations__}
                    ```
    ''' + '''        
            request_body (str): The JSON string containing the request body to be sent with a POST request.
                Ensure that this is valid JSON. The expected format for the API call is given in an OpenAPI spec,
                enclosed within backticks:
                    ```
                    {'maxItems': 10000000, 'minItems': 1, 'type': 'array', 'description': 'List of Study IDs', 'items': {'maxLength': 10000000, 'minLength': 1, 'type': 'string'}}
                    ```''')
    async def fetchClinicalAttributesUsingPOST(
            self, 
            target_var: str,
            query_params: fetchClinicalAttributesUsingPOSTQueryParameters, # type: ignore
            request_body: str,
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/clinical-attributes/fetch',
                "target_var": target_var, 
                'operation': 'post', 'query_params': query_params, 'request_body': request_body
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'post', 'query_params': query_params, 'request_body': request_body
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call fetchClinicalAttributesUsingPOST to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call fetchClinicalAttributesUsingPOST failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get all studies

        Args:
            target_var (str): The target variable to save the results to.
            query_params (getAllStudiesUsingGETQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllStudiesUsingGETQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllStudiesUsingGETQueryParameters.__annotations__}
                    ```
    ''')
    async def getAllStudiesUsingGET(
            self, 
            target_var: str,
            query_params: getAllStudiesUsingGETQueryParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/studies',
                "target_var": target_var, 
                'operation': 'get', 'query_params': query_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'query_params': query_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getAllStudiesUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getAllStudiesUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get a study

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getStudyUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getStudyUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getStudyUsingGETPathParameters.__annotations__}
                    ```
    ''')
    async def getStudyUsingGET(
            self, 
            target_var: str,
            path_params: getStudyUsingGETPathParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/studies/{studyId}',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getStudyUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getStudyUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get the tags of a study

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getTagsUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getTagsUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getTagsUsingGETPathParameters.__annotations__}
                    ```
    ''')
    async def getTagsUsingGET(
            self, 
            target_var: str,
            path_params: getTagsUsingGETPathParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/studies/{studyId}/tags',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getTagsUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getTagsUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get all samples in a study

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getAllSamplesInStudyUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllSamplesInStudyUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllSamplesInStudyUsingGETPathParameters.__annotations__}
                    ```
            query_params (getAllSamplesInStudyUsingGETQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllSamplesInStudyUsingGETQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllSamplesInStudyUsingGETQueryParameters.__annotations__}
                    ```
    ''')
    async def getAllSamplesInStudyUsingGET(
            self, 
            target_var: str,
            path_params: getAllSamplesInStudyUsingGETPathParameters, # type: ignore
            query_params: getAllSamplesInStudyUsingGETQueryParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/studies/{studyId}/samples',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getAllSamplesInStudyUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getAllSamplesInStudyUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get a sample in a study

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getSampleInStudyUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getSampleInStudyUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getSampleInStudyUsingGETPathParameters.__annotations__}
                    ```
    ''')
    async def getSampleInStudyUsingGET(
            self, 
            target_var: str,
            path_params: getSampleInStudyUsingGETPathParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/studies/{studyId}/samples/{sampleId}',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getSampleInStudyUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getSampleInStudyUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get copy number segments in a sample in a study

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getCopyNumberSegmentsInSampleInStudyUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getCopyNumberSegmentsInSampleInStudyUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getCopyNumberSegmentsInSampleInStudyUsingGETPathParameters.__annotations__}
                    ```
            query_params (getCopyNumberSegmentsInSampleInStudyUsingGETQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getCopyNumberSegmentsInSampleInStudyUsingGETQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {getCopyNumberSegmentsInSampleInStudyUsingGETQueryParameters.__annotations__}
                    ```
    ''')
    async def getCopyNumberSegmentsInSampleInStudyUsingGET(
            self, 
            target_var: str,
            path_params: getCopyNumberSegmentsInSampleInStudyUsingGETPathParameters, # type: ignore
            query_params: getCopyNumberSegmentsInSampleInStudyUsingGETQueryParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/studies/{studyId}/samples/{sampleId}/copy-number-segments',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getCopyNumberSegmentsInSampleInStudyUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getCopyNumberSegmentsInSampleInStudyUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get all clinical data of a sample in a study

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getAllClinicalDataOfSampleInStudyUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllClinicalDataOfSampleInStudyUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllClinicalDataOfSampleInStudyUsingGETPathParameters.__annotations__}
                    ```
            query_params (getAllClinicalDataOfSampleInStudyUsingGETQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllClinicalDataOfSampleInStudyUsingGETQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllClinicalDataOfSampleInStudyUsingGETQueryParameters.__annotations__}
                    ```
    ''')
    async def getAllClinicalDataOfSampleInStudyUsingGET(
            self, 
            target_var: str,
            path_params: getAllClinicalDataOfSampleInStudyUsingGETPathParameters, # type: ignore
            query_params: getAllClinicalDataOfSampleInStudyUsingGETQueryParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/studies/{studyId}/samples/{sampleId}/clinical-data',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getAllClinicalDataOfSampleInStudyUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getAllClinicalDataOfSampleInStudyUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get all sample lists in a study

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getAllSampleListsInStudyUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllSampleListsInStudyUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllSampleListsInStudyUsingGETPathParameters.__annotations__}
                    ```
            query_params (getAllSampleListsInStudyUsingGETQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllSampleListsInStudyUsingGETQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllSampleListsInStudyUsingGETQueryParameters.__annotations__}
                    ```
    ''')
    async def getAllSampleListsInStudyUsingGET(
            self, 
            target_var: str,
            path_params: getAllSampleListsInStudyUsingGETPathParameters, # type: ignore
            query_params: getAllSampleListsInStudyUsingGETQueryParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/studies/{studyId}/sample-lists',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getAllSampleListsInStudyUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getAllSampleListsInStudyUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get all patients in a study

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getAllPatientsInStudyUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllPatientsInStudyUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllPatientsInStudyUsingGETPathParameters.__annotations__}
                    ```
            query_params (getAllPatientsInStudyUsingGETQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllPatientsInStudyUsingGETQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllPatientsInStudyUsingGETQueryParameters.__annotations__}
                    ```
    ''')
    async def getAllPatientsInStudyUsingGET(
            self, 
            target_var: str,
            path_params: getAllPatientsInStudyUsingGETPathParameters, # type: ignore
            query_params: getAllPatientsInStudyUsingGETQueryParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/studies/{studyId}/patients',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getAllPatientsInStudyUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getAllPatientsInStudyUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get a patient in a study

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getPatientInStudyUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getPatientInStudyUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getPatientInStudyUsingGETPathParameters.__annotations__}
                    ```
    ''')
    async def getPatientInStudyUsingGET(
            self, 
            target_var: str,
            path_params: getPatientInStudyUsingGETPathParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/studies/{studyId}/patients/{patientId}',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getPatientInStudyUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getPatientInStudyUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get all samples of a patient in a study

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getAllSamplesOfPatientInStudyUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllSamplesOfPatientInStudyUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllSamplesOfPatientInStudyUsingGETPathParameters.__annotations__}
                    ```
            query_params (getAllSamplesOfPatientInStudyUsingGETQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllSamplesOfPatientInStudyUsingGETQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllSamplesOfPatientInStudyUsingGETQueryParameters.__annotations__}
                    ```
    ''')
    async def getAllSamplesOfPatientInStudyUsingGET(
            self, 
            target_var: str,
            path_params: getAllSamplesOfPatientInStudyUsingGETPathParameters, # type: ignore
            query_params: getAllSamplesOfPatientInStudyUsingGETQueryParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/studies/{studyId}/patients/{patientId}/samples',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getAllSamplesOfPatientInStudyUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getAllSamplesOfPatientInStudyUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get all clinical data of a patient in a study

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getAllClinicalDataOfPatientInStudyUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllClinicalDataOfPatientInStudyUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllClinicalDataOfPatientInStudyUsingGETPathParameters.__annotations__}
                    ```
            query_params (getAllClinicalDataOfPatientInStudyUsingGETQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllClinicalDataOfPatientInStudyUsingGETQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllClinicalDataOfPatientInStudyUsingGETQueryParameters.__annotations__}
                    ```
    ''')
    async def getAllClinicalDataOfPatientInStudyUsingGET(
            self, 
            target_var: str,
            path_params: getAllClinicalDataOfPatientInStudyUsingGETPathParameters, # type: ignore
            query_params: getAllClinicalDataOfPatientInStudyUsingGETQueryParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/studies/{studyId}/patients/{patientId}/clinical-data',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getAllClinicalDataOfPatientInStudyUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getAllClinicalDataOfPatientInStudyUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get all molecular profiles in a study

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getAllMolecularProfilesInStudyUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllMolecularProfilesInStudyUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllMolecularProfilesInStudyUsingGETPathParameters.__annotations__}
                    ```
            query_params (getAllMolecularProfilesInStudyUsingGETQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllMolecularProfilesInStudyUsingGETQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllMolecularProfilesInStudyUsingGETQueryParameters.__annotations__}
                    ```
    ''')
    async def getAllMolecularProfilesInStudyUsingGET(
            self, 
            target_var: str,
            path_params: getAllMolecularProfilesInStudyUsingGETPathParameters, # type: ignore
            query_params: getAllMolecularProfilesInStudyUsingGETQueryParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/studies/{studyId}/molecular-profiles',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getAllMolecularProfilesInStudyUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getAllMolecularProfilesInStudyUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get all clinical data in a study

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getAllClinicalDataInStudyUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllClinicalDataInStudyUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllClinicalDataInStudyUsingGETPathParameters.__annotations__}
                    ```
            query_params (getAllClinicalDataInStudyUsingGETQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllClinicalDataInStudyUsingGETQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllClinicalDataInStudyUsingGETQueryParameters.__annotations__}
                    ```
    ''')
    async def getAllClinicalDataInStudyUsingGET(
            self, 
            target_var: str,
            path_params: getAllClinicalDataInStudyUsingGETPathParameters, # type: ignore
            query_params: getAllClinicalDataInStudyUsingGETQueryParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/studies/{studyId}/clinical-data',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getAllClinicalDataInStudyUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getAllClinicalDataInStudyUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get all clinical attributes in the specified study

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getAllClinicalAttributesInStudyUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllClinicalAttributesInStudyUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllClinicalAttributesInStudyUsingGETPathParameters.__annotations__}
                    ```
            query_params (getAllClinicalAttributesInStudyUsingGETQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllClinicalAttributesInStudyUsingGETQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllClinicalAttributesInStudyUsingGETQueryParameters.__annotations__}
                    ```
    ''')
    async def getAllClinicalAttributesInStudyUsingGET(
            self, 
            target_var: str,
            path_params: getAllClinicalAttributesInStudyUsingGETPathParameters, # type: ignore
            query_params: getAllClinicalAttributesInStudyUsingGETQueryParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/studies/{studyId}/clinical-attributes',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getAllClinicalAttributesInStudyUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getAllClinicalAttributesInStudyUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get specified clinical attribute

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getClinicalAttributeInStudyUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getClinicalAttributeInStudyUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getClinicalAttributeInStudyUsingGETPathParameters.__annotations__}
                    ```
    ''')
    async def getClinicalAttributeInStudyUsingGET(
            self, 
            target_var: str,
            path_params: getClinicalAttributeInStudyUsingGETPathParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/studies/{studyId}/clinical-attributes/{clinicalAttributeId}',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getClinicalAttributeInStudyUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getClinicalAttributeInStudyUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get all samples matching keyword

        Args:
            target_var (str): The target variable to save the results to.
            query_params (getSamplesByKeywordUsingGETQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getSamplesByKeywordUsingGETQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {getSamplesByKeywordUsingGETQueryParameters.__annotations__}
                    ```
    ''')
    async def getSamplesByKeywordUsingGET(
            self, 
            target_var: str,
            query_params: getSamplesByKeywordUsingGETQueryParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/samples',
                "target_var": target_var, 
                'operation': 'get', 'query_params': query_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'query_params': query_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getSamplesByKeywordUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getSamplesByKeywordUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get all sample lists

        Args:
            target_var (str): The target variable to save the results to.
            query_params (getAllSampleListsUsingGETQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllSampleListsUsingGETQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllSampleListsUsingGETQueryParameters.__annotations__}
                    ```
    ''')
    async def getAllSampleListsUsingGET(
            self, 
            target_var: str,
            query_params: getAllSampleListsUsingGETQueryParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/sample-lists',
                "target_var": target_var, 
                'operation': 'get', 'query_params': query_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'query_params': query_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getAllSampleListsUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getAllSampleListsUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get sample list

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getSampleListUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getSampleListUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getSampleListUsingGETPathParameters.__annotations__}
                    ```
    ''')
    async def getSampleListUsingGET(
            self, 
            target_var: str,
            path_params: getSampleListUsingGETPathParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/sample-lists/{sampleListId}',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getSampleListUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getSampleListUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get all sample IDs in a sample list

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getAllSampleIdsInSampleListUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllSampleIdsInSampleListUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllSampleIdsInSampleListUsingGETPathParameters.__annotations__}
                    ```
    ''')
    async def getAllSampleIdsInSampleListUsingGET(
            self, 
            target_var: str,
            path_params: getAllSampleIdsInSampleListUsingGETPathParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/sample-lists/{sampleListId}/sample-ids',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getAllSampleIdsInSampleListUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getAllSampleIdsInSampleListUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get all patients

        Args:
            target_var (str): The target variable to save the results to.
            query_params (getAllPatientsUsingGETQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllPatientsUsingGETQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllPatientsUsingGETQueryParameters.__annotations__}
                    ```
    ''')
    async def getAllPatientsUsingGET(
            self, 
            target_var: str,
            query_params: getAllPatientsUsingGETQueryParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/patients',
                "target_var": target_var, 
                'operation': 'get', 'query_params': query_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'query_params': query_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getAllPatientsUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getAllPatientsUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get all molecular profiles

        Args:
            target_var (str): The target variable to save the results to.
            query_params (getAllMolecularProfilesUsingGETQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllMolecularProfilesUsingGETQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllMolecularProfilesUsingGETQueryParameters.__annotations__}
                    ```
    ''')
    async def getAllMolecularProfilesUsingGET(
            self, 
            target_var: str,
            query_params: getAllMolecularProfilesUsingGETQueryParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/molecular-profiles',
                "target_var": target_var, 
                'operation': 'get', 'query_params': query_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'query_params': query_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getAllMolecularProfilesUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getAllMolecularProfilesUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get molecular profile

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getMolecularProfileUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getMolecularProfileUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getMolecularProfileUsingGETPathParameters.__annotations__}
                    ```
    ''')
    async def getMolecularProfileUsingGET(
            self, 
            target_var: str,
            path_params: getMolecularProfileUsingGETPathParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/molecular-profiles/{molecularProfileId}',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getMolecularProfileUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getMolecularProfileUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get mutations in a molecular profile by Sample List ID

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getMutationsInMolecularProfileBySampleListIdUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getMutationsInMolecularProfileBySampleListIdUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getMutationsInMolecularProfileBySampleListIdUsingGETPathParameters.__annotations__}
                    ```
            query_params (getMutationsInMolecularProfileBySampleListIdUsingGETQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getMutationsInMolecularProfileBySampleListIdUsingGETQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {getMutationsInMolecularProfileBySampleListIdUsingGETQueryParameters.__annotations__}
                    ```
    ''')
    async def getMutationsInMolecularProfileBySampleListIdUsingGET(
            self, 
            target_var: str,
            path_params: getMutationsInMolecularProfileBySampleListIdUsingGETPathParameters, # type: ignore
            query_params: getMutationsInMolecularProfileBySampleListIdUsingGETQueryParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/molecular-profiles/{molecularProfileId}/mutations',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getMutationsInMolecularProfileBySampleListIdUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getMutationsInMolecularProfileBySampleListIdUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get all molecular data in a molecular profile

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getAllMolecularDataInMolecularProfileUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllMolecularDataInMolecularProfileUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllMolecularDataInMolecularProfileUsingGETPathParameters.__annotations__}
                    ```
            query_params (getAllMolecularDataInMolecularProfileUsingGETQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllMolecularDataInMolecularProfileUsingGETQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllMolecularDataInMolecularProfileUsingGETQueryParameters.__annotations__}
                    ```
    ''')
    async def getAllMolecularDataInMolecularProfileUsingGET(
            self, 
            target_var: str,
            path_params: getAllMolecularDataInMolecularProfileUsingGETPathParameters, # type: ignore
            query_params: getAllMolecularDataInMolecularProfileUsingGETQueryParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/molecular-profiles/{molecularProfileId}/molecular-data',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getAllMolecularDataInMolecularProfileUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getAllMolecularDataInMolecularProfileUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get discrete copy number alterations in a molecular profile

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getDiscreteCopyNumbersInMolecularProfileUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getDiscreteCopyNumbersInMolecularProfileUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getDiscreteCopyNumbersInMolecularProfileUsingGETPathParameters.__annotations__}
                    ```
            query_params (getDiscreteCopyNumbersInMolecularProfileUsingGETQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getDiscreteCopyNumbersInMolecularProfileUsingGETQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {getDiscreteCopyNumbersInMolecularProfileUsingGETQueryParameters.__annotations__}
                    ```
    ''')
    async def getDiscreteCopyNumbersInMolecularProfileUsingGET(
            self, 
            target_var: str,
            path_params: getDiscreteCopyNumbersInMolecularProfileUsingGETPathParameters, # type: ignore
            query_params: getDiscreteCopyNumbersInMolecularProfileUsingGETQueryParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/molecular-profiles/{molecularProfileId}/discrete-copy-number',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getDiscreteCopyNumbersInMolecularProfileUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getDiscreteCopyNumbersInMolecularProfileUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get information about the running instance

        Args:
            target_var (str): The target variable to save the results to.
    ''')
    async def getInfoUsingGET(
            self, 
            target_var: str,
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/info',
                "target_var": target_var, 
                'operation': 'get', 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getInfoUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getInfoUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get the running status of the server

        Args:
            target_var (str): The target variable to save the results to.
    ''')
    async def getServerStatusUsingGET(
            self, 
            target_var: str,
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/health',
                "target_var": target_var, 
                'operation': 'get', 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getServerStatusUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getServerStatusUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get all genes

        Args:
            target_var (str): The target variable to save the results to.
            query_params (getAllGenesUsingGETQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllGenesUsingGETQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllGenesUsingGETQueryParameters.__annotations__}
                    ```
    ''')
    async def getAllGenesUsingGET(
            self, 
            target_var: str,
            query_params: getAllGenesUsingGETQueryParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/genes',
                "target_var": target_var, 
                'operation': 'get', 'query_params': query_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'query_params': query_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getAllGenesUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getAllGenesUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get a gene

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getGeneUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getGeneUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getGeneUsingGETPathParameters.__annotations__}
                    ```
    ''')
    async def getGeneUsingGET(
            self, 
            target_var: str,
            path_params: getGeneUsingGETPathParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/genes/{geneId}',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getGeneUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getGeneUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get aliases of a gene

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getAliasesOfGeneUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAliasesOfGeneUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAliasesOfGeneUsingGETPathParameters.__annotations__}
                    ```
    ''')
    async def getAliasesOfGeneUsingGET(
            self, 
            target_var: str,
            path_params: getAliasesOfGeneUsingGETPathParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/genes/{geneId}/aliases',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getAliasesOfGeneUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getAliasesOfGeneUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Fetch meta data for generic-assay by ID

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getGenericAssayMetaUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getGenericAssayMetaUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getGenericAssayMetaUsingGETPathParameters.__annotations__}
                    ```
            query_params (getGenericAssayMetaUsingGETQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getGenericAssayMetaUsingGETQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {getGenericAssayMetaUsingGETQueryParameters.__annotations__}
                    ```
    ''')
    async def getGenericAssayMetaUsingGET(
            self, 
            target_var: str,
            path_params: getGenericAssayMetaUsingGETPathParameters, # type: ignore
            query_params: getGenericAssayMetaUsingGETQueryParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/generic-assay-meta/{molecularProfileId}',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getGenericAssayMetaUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getGenericAssayMetaUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Fetch meta data for generic-assay by ID

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getGenericAssayMeta_gaUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getGenericAssayMeta_gaUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getGenericAssayMeta_gaUsingGETPathParameters.__annotations__}
                    ```
            query_params (getGenericAssayMeta_gaUsingGETQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getGenericAssayMeta_gaUsingGETQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {getGenericAssayMeta_gaUsingGETQueryParameters.__annotations__}
                    ```
    ''')
    async def getGenericAssayMeta_gaUsingGET(
            self, 
            target_var: str,
            path_params: getGenericAssayMeta_gaUsingGETPathParameters, # type: ignore
            query_params: getGenericAssayMeta_gaUsingGETQueryParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/generic-assay-meta/generic-assay/{genericAssayStableId}',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getGenericAssayMeta_gaUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getGenericAssayMeta_gaUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get generic_assay_data in a molecular profile

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getGenericAssayDataInMolecularProfileUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getGenericAssayDataInMolecularProfileUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getGenericAssayDataInMolecularProfileUsingGETPathParameters.__annotations__}
                    ```
            query_params (getGenericAssayDataInMolecularProfileUsingGETQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getGenericAssayDataInMolecularProfileUsingGETQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {getGenericAssayDataInMolecularProfileUsingGETQueryParameters.__annotations__}
                    ```
    ''')
    async def getGenericAssayDataInMolecularProfileUsingGET(
            self, 
            target_var: str,
            path_params: getGenericAssayDataInMolecularProfileUsingGETPathParameters, # type: ignore
            query_params: getGenericAssayDataInMolecularProfileUsingGETQueryParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/generic-assay-data/{molecularProfileId}/generic-assay/{genericAssayStableId}',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 'query_params': query_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getGenericAssayDataInMolecularProfileUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getGenericAssayDataInMolecularProfileUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get all gene panels

        Args:
            target_var (str): The target variable to save the results to.
            query_params (getAllGenePanelsUsingGETQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllGenePanelsUsingGETQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllGenePanelsUsingGETQueryParameters.__annotations__}
                    ```
    ''')
    async def getAllGenePanelsUsingGET(
            self, 
            target_var: str,
            query_params: getAllGenePanelsUsingGETQueryParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/gene-panels',
                "target_var": target_var, 
                'operation': 'get', 'query_params': query_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'query_params': query_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getAllGenePanelsUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getAllGenePanelsUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get gene panel

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getGenePanelUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getGenePanelUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getGenePanelUsingGETPathParameters.__annotations__}
                    ```
    ''')
    async def getGenePanelUsingGET(
            self, 
            target_var: str,
            path_params: getGenePanelUsingGETPathParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/gene-panels/{genePanelId}',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getGenePanelUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getGenePanelUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get all clinical attributes

        Args:
            target_var (str): The target variable to save the results to.
            query_params (getAllClinicalAttributesUsingGETQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllClinicalAttributesUsingGETQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllClinicalAttributesUsingGETQueryParameters.__annotations__}
                    ```
    ''')
    async def getAllClinicalAttributesUsingGET(
            self, 
            target_var: str,
            query_params: getAllClinicalAttributesUsingGETQueryParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/clinical-attributes',
                "target_var": target_var, 
                'operation': 'get', 'query_params': query_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'query_params': query_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getAllClinicalAttributesUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getAllClinicalAttributesUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get all cancer types

        Args:
            target_var (str): The target variable to save the results to.
            query_params (getAllCancerTypesUsingGETQueryParameters): The parameters that go in the query arguments in the URL for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getAllCancerTypesUsingGETQueryParameters is in the following structure, surrounded by backticks:
                    ```
                    {getAllCancerTypesUsingGETQueryParameters.__annotations__}
                    ```
    ''')
    async def getAllCancerTypesUsingGET(
            self, 
            target_var: str,
            query_params: getAllCancerTypesUsingGETQueryParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.


        if isinstance(query_params, dict):
            query_params: dict = {
                k: v 
                    for k, v in query_params.items() 
                    if v is not None
            }
        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/cancer-types',
                "target_var": target_var, 
                'operation': 'get', 'query_params': query_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'query_params': query_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getAllCancerTypesUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getAllCancerTypesUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

    # this file is loaded as a python format string, -not- a jinja template. 
    # these opening comments are stripped on load.
    # escape curly braces as { } because single braces will be injected
    # in an f-string,
    #   triple-brace var will turn into a single brace var interpolation in code.
    #
    # this tool wraps an API call with a name for discovery in beaker.
    # there is a matching procedure in procedure.py_template

    @tool()
    @dynamic_docstring(docstring=f'''
        Get a cancer type

        Args:
            target_var (str): The target variable to save the results to.
            path_params (getCancerTypeUsingGETPathParameters): The parameters that go in the URL path substitution for the API call.
                Use default values where possible, unless the user wishes to override
                or provide something in their operation. 
                getCancerTypeUsingGETPathParameters is in the following structure, surrounded by backticks:
                    ```
                    {getCancerTypeUsingGETPathParameters.__annotations__}
                    ```
    ''')
    async def getCancerTypeUsingGET(
            self, 
            target_var: str,
            path_params: getCancerTypeUsingGETPathParameters, # type: ignore
            agent: AgentRef 
        ):
        # params are actually a dict in the shape of the dataclass instead of the dataclass, 
        # but the docstring and function signature must match for archytas. 
        # the type hint is therefore a "lie" but this makes it run smoothly for signature checking.

        if isinstance(path_params, dict):
            path_params: dict = {
                k: v 
                    for k, v in path_params.items() 
                    if v is not None
            }

        try: 
            code = agent.context.get_code('general_api_request', {
                "url": 'https://cbioportal.org/api/cancer-types/{cancerTypeId}',
                "target_var": target_var, 
                'operation': 'get', 'path_params': path_params, 
            })
            self.context.send_response("iopub",
                "api_tool_call", {
                    "body": {
                        "target_var": str(target_var), 
                        "code": code,
                        'operation': 'get', 'path_params': path_params, 
                    }
                },
            )
        except Exception as e:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "code generation",
                        "exception": str(e)
                    }
                },
            )
        evaluation = await agent.context.evaluate(code)
        response = evaluation.get('return', None)
        if response is None:
            self.context.send_response("iopub",
                "api_tool_fail", {
                    "body": {
                        "location": "request",
                        "exception": "Response returned nothing."
                    }
                },
            )  
        self.context.send_response("iopub",
            "api_tool_call", {
                "body": {
                    "response": response
                }
            },
        )
        status_code = response.get('status_code')
        response_json = response.get('json')
        agent.messages = agent.messages[:-1]
        if status_code == 200:
            agent.add_context(f"""
                I have now just finished saving the API call getCancerTypeUsingGET to a variable {target_var}.
                The variable {target_var} now exists. The structure of it is enclosed in backticks:
                ```{str(response_json) or ''}```
                and you can use this for future API calls and operations.
                The task completed successfully.
            """)
        else:
            agent.add_context(f"""
                The API call getCancerTypeUsingGET failed with status code {status_code}.
                The target variable {target_var} was unchanged or left uncreated.
                The task has failed.
            """)

