import requests
import json 

# Define the endpoint URL
url = "https://portal.gdc.cancer.gov/auth/api/v0/graphql"

# Define the first query
query = """
query QueryBucketCounts($filters: FiltersArgument) {
  viewer {
    explore {
      cases {
        aggregations(
          filters:$filters,
          aggregations_filter_themselves: false
        ) {
          cases__project__program__name: project__program__name {
            buckets {
              doc_count
              key
            }
          }
          cases__project__project_id: project__project_id {
            buckets {
              doc_count
              key
            }
          }
          cases__disease_type: disease_type {
            buckets {
              doc_count
              key
            }
          }
          cases__diagnoses__primary_diagnosis: diagnoses__primary_diagnosis {
            buckets {
              doc_count
              key
            }
          }
          cases__primary_site: primary_site {
            buckets {
              doc_count
              key
            }
          }
          cases__diagnoses__tissue_or_organ_of_origin: diagnoses__tissue_or_organ_of_origin {
            buckets {
              doc_count
              key
            }
          }
          cases__demographic__gender: demographic__gender {
            buckets {
              doc_count
              key
            }
          }
          cases__demographic__race: demographic__race {
            buckets {
              doc_count
              key
            }
          }
          cases__demographic__ethnicity: demographic__ethnicity {
            buckets {
              doc_count
              key
            }
          }
          cases__demographic__vital_status: demographic__vital_status {
            buckets {
              doc_count
              key
            }
          }  
          cases__diagnoses__morphology: diagnoses__morphology {
            buckets {
              doc_count
              key
            }
          }
          cases__diagnoses__site_of_resection_or_biopsy: diagnoses__site_of_resection_or_biopsy {
            buckets {
              doc_count
              key
            }
          }
        cases__diagnoses__sites_of_involvement : diagnoses__sites_of_involvement {
            buckets {
                doc_count
                key
            }
          }
        cases__diagnoses__laterality : diagnoses__laterality {
            buckets {
                doc_count
                key
            }
          }          
          cases__diagnoses__prior_malignancy: diagnoses__prior_malignancy {
            buckets {
              doc_count
              key
            }
          }
          cases__diagnoses__prior_treatment: diagnoses__prior_treatment {
            buckets {
              doc_count
              key
            }
          }
          cases__diagnoses__synchronous_malignancy : diagnoses__synchronous_malignancy {
            buckets {
              doc_count
              key
            }
          }          
          cases__diagnoses__progression_or_recurrence: diagnoses__progression_or_recurrence {
            buckets {
              doc_count
              key
            }
          }   
          cases__diagnoses__residual_disease : diagnoses__residual_disease {
            buckets {
              doc_count
              key
            }
          }
          cases__diagnoses__ajcc_clinical_stage: diagnoses__ajcc_clinical_stage {
            buckets {
              doc_count
              key
            }
          }
          cases__diagnoses__ajcc_pathologic_stage: diagnoses__ajcc_pathologic_stage {
            buckets {
              doc_count
              key
            }
          }
          cases__diagnoses__ann_arbor_clinical_stage: diagnoses__ann_arbor_clinical_stage {
            buckets {
              doc_count
              key
            }
          }
          cases__diagnoses__ann_arbor_pathologic_stage: diagnoses__ann_arbor_pathologic_stage {
            buckets {
              doc_count
              key
            }
          }
          cases__diagnoses__cog_renal_stage: diagnoses__cog_renal_stage {
            buckets {
              doc_count
              key
            }
          }
          cases__diagnoses__enneking_msts_stage: diagnoses__enneking_msts_stage {
            buckets {
              doc_count
              key
            }
          }
          cases__diagnoses__figo_stage: diagnoses__figo_stage {
            buckets {
              doc_count
              key
            }
          }
          cases__diagnoses__igcccg_stage: diagnoses__igcccg_stage {
            buckets {
              doc_count
              key
            }
          }
          cases__diagnoses__inss_stage: diagnoses__inss_stage {
            buckets {
              doc_count
              key
            }
          }
          cases__diagnoses__iss_stage: diagnoses__iss_stage {
            buckets {
              doc_count
              key
            }
          }
          cases__diagnoses__masaoka_stage: diagnoses__masaoka_stage {
            buckets {
              doc_count
              key
            }
          }  
          cases__diagnoses__inpc_grade: diagnoses__inpc_grade {
            buckets {
              doc_count
              key
            }
          }
          cases__diagnoses__tumor_grade: diagnoses__tumor_grade {
            buckets {
              doc_count
              key
            }
          }
          cases__diagnoses__who_cns_grade: diagnoses__who_cns_grade {
            buckets {
              doc_count
              key
            }
          }        
          cases__diagnoses__cog_neuroblastoma_risk_group: diagnoses__cog_neuroblastoma_risk_group {
            buckets {
              doc_count
              key
            }
          }
          cases__diagnoses__cog_rhabdomyosarcoma_risk_group: diagnoses__cog_rhabdomyosarcoma_risk_group {
            buckets {
              doc_count
              key
            }
          }
          cases__diagnoses__eln_risk_classification: diagnoses__eln_risk_classification {
            buckets {
              doc_count
              key
            }
          }
          cases__diagnoses__international_prognostic_index: diagnoses__international_prognostic_index {
            buckets {
              doc_count
              key
            }
          }
          cases__diagnoses__wilms_tumor_histologic_subtype: diagnoses__wilms_tumor_histologic_subtype {
            buckets {
              doc_count
              key
            }
          }   
          cases__diagnoses__treatments__therapeutic_agents: diagnoses__treatments__therapeutic_agents {
            buckets {
              doc_count
              key
            }
          }
          cases__diagnoses__treatments__treatment_intent_type: diagnoses__treatments__treatment_intent_type {
            buckets {
              doc_count
              key
            }
          }
          cases__diagnoses__treatments__treatment_outcome: diagnoses__treatments__treatment_outcome {
            buckets {
              doc_count
              key
            }
          }
          cases__diagnoses__treatments__treatment_type: diagnoses__treatments__treatment_type {
            buckets {
              doc_count
              key
            }
          }
          cases__diagnoses__best_overall_response: diagnoses__best_overall_response {
            buckets {
              doc_count
              key
            }
          }          
          cases__exposures__alcohol_history: exposures__alcohol_history {
            buckets {
              doc_count
              key
            }
          }
          cases__exposures__alcohol_intensity: exposures__alcohol_intensity {
            buckets {
              doc_count
              key
            }
          }
          cases__exposures__tobacco_smoking_status: exposures__tobacco_smoking_status {
            buckets {
              doc_count
              key
            }
          }
          cases__samples__tissue_type: samples__tissue_type {
            buckets {
              doc_count
              key
            }
          }
          cases__samples__biospecimen_anatomic_site: samples__biospecimen_anatomic_site {
            buckets {
              doc_count
              key
            }
          }
          cases__samples__composition: samples__composition {
            buckets {
              doc_count
              key
            }
          }
          cases__samples__preservation_method: samples__preservation_method {
            buckets {
              doc_count
              key
            }
          }
          cases__samples__tumor_code: samples__tumor_code {
            buckets {
              doc_count
              key
            }
          }
          cases__samples__tumor_descriptor: samples__tumor_descriptor {
            buckets {
              doc_count
              key
            }
          }
          cases__samples__portions__analytes__aliquots__analyte_type: samples__portions__analytes__aliquots__analyte_type {
            buckets {
              doc_count
              key
            }
          }          
          files__data_category: files__data_category {
            buckets {
              doc_count
              key
            }
          }
          files__data_type: files__data_type {
            buckets {
              doc_count
              key
            }
          }
          files__experimental_strategy: files__experimental_strategy {
            buckets {
              doc_count
              key
            }
          }
          files__analysis__workflow_type: files__analysis__workflow_type {
            buckets {
              doc_count
              key
            }
          }
          files__data_format: files__data_format {
            buckets {
              doc_count
              key
            }
          }
          files__platform: files__platform {
            buckets {
              doc_count
              key
            }
          }
          files__access: files__access {
            buckets {
              doc_count
              key
            }
          }          
        }
      }
    }
  }
}
"""

variables = {
    "filters": {}
}

response = requests.post(url, json={"query": query, "variables": variables}).json()
cases = response['data']['viewer']['explore']['cases']['aggregations']

formatted = {k[7:].replace('__', ' '): [e['key'] for e in v['buckets']] for k,v in cases.items()}

for k, v in formatted.items():
    entry = '\n\t- '.join(v)
    print(f"{k}:\n\t- {entry}")
