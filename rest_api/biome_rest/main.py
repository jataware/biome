from typing import Annotated

from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel

from .integrations import initialize_adhoc

integrations = initialize_adhoc()
app = FastAPI()


def raise_on_invalid_integration(integration: str) -> None:
    if integration not in [
            integration_data["slug"]
            for (integration_data, _) in integrations.apis.values()
        ]:
        raise HTTPException(status_code=403, detail=f"The requested integration `{integration}` does not exist.")

ListIntegrationsOutput = Annotated[
    dict[str, dict[str, str]],
    Body(
        examples=[
            {
                "census_acs_(american_community_survey)_and_sf1": {
                    "Census ACS (American Community Survey) and SF1": "The Census ACS (American Community Survey) and SF1 (Decennial Census) API returns data that has been collected from \nthe Census Bureau, a database that contains information on the population of the United States.\nUse this to control for socioeconomic factors (or for other purposes).\n"
                },
                "nhanes_dietary_data": {
                    "NHANES Dietary Data": "API for accessing and analyzing NHANES dietary data, including food consumption patterns\nand processed food analysis across different survey cycles from 1999 to 2023, with demographic information.\n"
                },
                "chis_california_asthma": {
                    "CHIS California Asthma": "This dataset contains current asthma prevalence, the estimated percentage of \nCalifornians who have ever been diagnosed with asthma by a health care provider \nAND report they still have asthma and/or had an asthma episode or attack within \nthe past 12 months, statewide and by county. The data are stratified by age group \n(all ages, 0-17, 18+, 0-4, 5-17, 18-64, 65+) and reported for 2-year periods.\n"
                },
                "national_survey_of_children's_health_(nsch)": {
                    "National Survey of Children's Health (NSCH)": "You have access to knowledge from the National Survey of Children's Health (NSCH) data, available every year from \n2016 to 2023. This dataset API can help answer questions about children's health, healthcare access, family functioning, \nneighborhood characteristics, and social determinants of health for children aged 0-17 years in the United States.\n"
                },
                "cdc_tracking_network": {
                    "CDC Tracking Network": "The National Environmental Public Health Tracking Network (Tracking Network) \nbrings together health data and environmental data from national, state, county, \nand city sources and provides supporting information to make the data easier \nto understand.\nThe Tracking Network has data and information on environments and hazards, \nhealth effects, and population health.\nThis resource includes childhood emergency department visits and hospitalizations at the county level. It provides:\n- Age-stratified data including children under 18\n- County-level resolution\n- Information on asthma, and other conditions\n"
                },
                "human_protein_atlas": {
                    "Human Protein Atlas": "The Human Protein Atlas is a Swedish-based program initiated in 2003 with the aim to map all \nthe human proteins in cells, tissues, and organs using an integration of various omics \ntechnologies, including antibody-based imaging, mass spectrometry-based proteomics, \ntranscriptomics, and systems biology. All the data in the knowledge resource is open access \nto allow scientists both in academia and industry to freely access the data for exploration \nof the human proteome.\n\nThe Human Protein Atlas consists of eight separate resources, each focusing on a particular \naspect of the genome-wide analysis of the human proteins:\n\n- The Tissue resource, showing the distribution of the proteins across all major tissues and \n  organs in the human body\n- The Brain resource, exploring the distribution of proteins in various regions of the \n  mammalian brain \n- The Single Cell resource, showing expression of protein-coding genes in immune cells and \n  human single cell types based on bulk and single cell RNA-seq\n- The Subcellular resource, showing the subcellular localization of proteins in single cells\n- The Cancer resource, showing the impact of protein levels for the survival of patients \n  with cancer\n- The Blood resource, describing proteins detected in blood and showing protein levels in \n  blood in patients with different diseases\n- The Cell line resource, showing expression of protein-coding genes in human cancer cell \n  lines\n- The Structure & Interaction resource, showing predicted 3D structures and exploring \n  protein-coding genes in the context of protein-protein and metabolic interaction networks.\n\nThe Human Protein Atlas program has already contributed to several thousands of publications \nin the field of human biology and disease and is selected by the organization ELIXIR as a \nEuropean core resource due to its fundamental importance for a wider life science community. \nIn addition the Human Protein Atlas has been appointed Global Core Biodata Resource (GCBR) \nby the Global Biodata Coalition. The Human Protein Atlas consortium is mainly funded by the \nKnut and Alice Wallenberg Foundation.\n"
                },
            }
        ]
    )
]

@app.get("/list_integrations")
def list_integrations() -> ListIntegrationsOutput:
    return {
        slug: {
            integration_data.get('name', integration_data["slug"]): integration_data["description"]
        } for slug, (integration_data, _) in integrations.apis.items()
    }

class IntegrationDocumentationOutput(BaseModel):
    response: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "response": "To fetch RNA-seq z-scores for multiple studies using the cBioPortal API, you need to follow these steps:\n\n1. **Identify the studies and their RNA-seq z-score molecular profiles**: Each study has a unique identifier (e.g., `aml_target_gdc`) and a specific molecular profile for RNA-seq z-scores (e.g., `aml_target_gdc_mrna_seq_tpm_Zscores`). You need to know both for each study you want to query.\n\n2. **Get the list of sample IDs for each study**: For each study, you should fetch the sample list that corresponds to RNA-seq data. This is typically done by retrieving all sample lists for the study and selecting the one with a category like `all_cases_with_mrna_rnaseq_data`. Then, fetch the actual sample IDs from that list.\n\n3. **Fetch the z-score data**: For each study, use the `/api/molecular-profiles/{molecularProfileId}/molecular-data/fetch` endpoint. In your request, provide:\n   - The molecular profile ID for RNA-seq z-scores\n   - The list of sample IDs you obtained\n   - The Entrez Gene IDs (or gene symbols) for the genes of interest\n\n4. **Repeat for each study**: Perform the above steps for each study you want to include.\n\n5. **Combine the results**: After fetching the data for all studies, you can combine the results into a single table or dataframe for further analysis.\n\n**Key points:**\n- You must provide explicit sample IDs in your request for each study.\n- Z-scores are precomputed and available for each study’s RNA-seq data.\n- If you have many samples, it’s best to fetch data in chunks to avoid timeouts or very large requests.\n- The process is the same for any genes or studies; just adjust the gene IDs and study/profile IDs as needed.\n\nIn summary: For each study, get the relevant sample IDs, then request the RNA-seq z-scores for your genes of interest using the appropriate molecular profile, and finally combine the results from all studies."
                }
            ]
        }
    }

@app.get("/consult_integration_documentation/{integration}")
def consult_integration_documentation(integration: str, query: str) -> IntegrationDocumentationOutput:
    raise_on_invalid_integration(integration)
    try:
        response = integrations.ask_api(integration, query)
        return IntegrationDocumentationOutput(response=response)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

class IntegrationCodeOutput(BaseModel):
    response: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "response": """import requests

url = "https://www.cbioportal.org/api/studies"
response = requests.get(url)

if response.status_code == 200:
    studies = response.json()
    colorectal_studies = [study for study in studies if study['cancerTypeId'].lower() in ['coadread', 'coad', 'read']]
    print(f"Found {len(colorectal_studies)} colorectal cancer studies.")
    print("\nStudy Details:")
    for study in colorectal_studies:
        print(f"\nName: {study['name']}")
        print(f"Study ID: {study['studyId']}")
        print(f"Description: {study['description']}")
        print(f"Cancer Type ID: {study['cancerTypeId']}")
        print("-" * 80)
""".replace('\n', r'\n')
                }
            ]
        }
    }

@app.get("/draft_integration_code/{integration}")
def draft_integration_code(integration: str, query: str) -> IntegrationCodeOutput:
    raise_on_invalid_integration(integration)
    try:
        response = integrations.use_api(integration, query)
        return IntegrationCodeOutput(response=response)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
