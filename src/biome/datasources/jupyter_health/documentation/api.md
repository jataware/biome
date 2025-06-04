# JupyterHealth Client API

## Notes

get_ methods return single records

list_ methods return generators of items

## API

enum jupyterhealth_client.Code(value)

Enum of recognized coding values

Can be used to filter Observations to on a given record type, e.g. with list_observations.

Valid values are as follows:

BLOOD_PRESSURE = <Code.BLOOD_PRESSURE: 'omh:blood-pressure:4.0'>

BLOOD_GLUCOSE = <Code.BLOOD_GLUCOSE: 'omh:blood-glucose:4.0'>

HEART_RATE = <Code.HEART_RATE: 'omh:heart-rate:2.0'>

`class jupyterhealth_client.JupyterHealthClient(url: str = '$JHE_URL', *, token: str | None = None)`

Client for JupyterHealth data Exchange

get_organization(id: int) → dict[str, Any]

Get a single organization by id.

The ROOT organization has id=0.

Example:

```
# A top-level organization:
{'id': 20011,
 'name': 'UC Berkeley',
 'type': 'edu',
 'partOf': 0}
```

```
# BIDS is part of UC Berkeley
{'id': 20013,
 'name': 'Berkeley Institute for Data Science (BIDS)',
 'type': 'edu',
 'partOf': 20011}
```

get_patient(id: int) → dict[str, Any]

Get a single patient by id.

Example:

```
{'id': 45439,
 'jheUserId': 19259,
 'identifier': 'some-external-id',
 'nameFamily': 'Williams',
 'nameGiven': 'Heather',
 'birthDate': '1967-12-09',
 'telecomPhone': None,
 'telecomEmail': 'heather.williams@example.edu',
 'organizationId': 20026,
 'birthdate': datetime.date(1989, 7, 3)}
```

get_patient_by_external_id(external_id: str) → dict[str, Any]

Get a single patient by external id.

For looking up the JHE Patient record by an external (e.g. EHR) patient id.

get_patient_consents(patient_id: int) → dict[str, Any]

Return patient consent status.

Example:

```
{
    "patient": {
        "id": 48098,
        "jheUserId": 17823,
        "identifier": "some-external-id",
        "nameFamily": "Dorsey",
        "nameGiven": "Brittany",
        "birthDate": "1967-12-09",
        "telecomPhone": None,
        "telecomEmail": "brittany.dorsey@example.edu",
        "organizationId": 20026,
        "birthdate": datetime.date(1977, 2, 8),
    },
    "consolidatedConsentedScopes": [
        {
            "id": 50002,
            "codingSystem": "https://w3id.org/openmhealth",
            "codingCode": "omh:blood-pressure:4.0",
            "text": "Blood pressure",
        },
        {
            "id": 50005,
            "codingSystem": "https://w3id.org/openmhealth",
            "codingCode": "omh:heart-rate:2.0",
            "text": "Heart Rate",
        },
    ],
    "studiesPendingConsent": [],
    "studies": [
        {
            "id": 30013,
            "name": "iHealth Blood Pressure Study",
            "description": "Blood Pressure Study using data from iHealth cuff",
            "organization": {"id": 20026, "name": "BIDS - URAP", "type": "edu"},
            "dataSources": [
                {
                    "id": 70001,
                    "name": "iHealth",
                    "type": "personal_device",
                    "supportedScopes": [],
                }
            ],
            "scopeConsents": [
                {
                    "code": {
                        "id": 50002,
                        "codingSystem": "https://w3id.org/openmhealth",
                        "codingCode": "omh:blood-pressure:4.0",
                        "text": "Blood pressure",
                    },
                    "consented": True,
                    "consentedTime": "2025-03-12T16:48:56.342402Z",
                },
                {
                    "code": {
                        "id": 50005,
                        "codingSystem": "https://w3id.org/openmhealth",
                        "codingCode": "omh:heart-rate:2.0",
                        "text": "Heart Rate",
                    },
                    "consented": True,
                    "consentedTime": "2025-03-12T16:48:56.342402Z",
                },
            ],
        }
    ],
}
```

get_study(id: int) → dict[str, Any]

Get a single study by id.

Example:

```
{'id': 30001,
 'name': 'iHealth Blood Pressure Study',
 'description': 'Blood Pressure Study using data from iHealth cuff',
 'organization': {'id': 20002, 'name': 'Sample Org', 'type': 'edu'}}
```

get_user() → dict[str, Any]

Get the current user.

Example:

```
{'id': 10001,
 'email': 'user@example.edu',
 'firstName': 'User',
 'lastName': 'Name',
 'patient': None}
```

list_observations(patient_id: int | None = None, study_id: int | None = None, code: Code | str | None = None, limit: int | None = 2000) → Generator[dict]

Fetch observations for given patient and/or study.

At least one of patient_id and study_id is required.

code is optional, and can be selected from enum jupyterhealth_client.Code.

An observation contains a valueAttachment field, which is a base64-encoded JSON record of the actual measurement.

Observations can be tidied to a dataframe-friendly flat dictionary with tidy_observation().

Example:

```
{
    "resourceType": "Observation",
    "id": "63602",
    "meta": {"lastUpdated": "2025-03-12T16:00:50.952478+00:00"},
    "identifier": [
        {
            "value": "u-u-i-d",
            "system": "https://commonhealth.org",
        }
    ],
    "status": "final",
    "subject": {"reference": "Patient/43373"},
    "code": {
        "coding": [
            {
                "code": "omh:blood-glucose:4.0",
                "system": "https://w3id.org/openmhealth",
            }
        ]
    },
    "valueAttachment": {"data": "eyJib...==\n", "contentType": "application/json"},
}
```

Example of an unpacked valueAttachment:

```
{
    "body": {
        "blood_glucose": {"unit": "MGDL", "value": 109},
        "effective_time_frame": {"date_time": "2025-02-15T17:28:33.271Z"},
        "temporal_relationship_to_meal": "unknown",
    },
    "header": {
        "uuid": "u-u-i-d-2",
        "modality": "self-reported",
        "schema_id": {"name": "blood-glucose", "version": "3.1", "namespace": "omh"},
        "creation_date_time": "2025-03-12T15:47:30.510Z",
        "external_datasheets": [
            {"datasheet_type": "manufacturer", "datasheet_reference": "Health Connect"}
        ],
        "source_data_point_id": "u-u-i-d-3",
        "source_creation_date_time": "2025-02-15T17:28:33.271Z",
    },
}
```

list_observations_df(patient_id: int | None = None, study_id: int | None = None, code: Code | None = None, limit: int | None = 2000) → DataFrame

Wrapper around list_observations, returns a DataFrame.

Observations are passed through tidy_observation to create a flat dictionary.

Key columns tend to be:

effective_time_frame_date_time

{measurement_type}_value (e.g. systolic_blood_pressure_value)

subject_reference e.g. Patient/1234 identifies the patient (for multi-patient queries)

code_coding_0_code specifies the coding (e.g. the enums in {class}`Code`)

list_organizations() → Generator[dict[str, dict[str, Any]]]

Iterate over all organizations.

Includes all organizations, including those of which I am not a member. The ROOT organization has id=0.

list_patients() → Generator[dict[str, dict[str, Any]]]

Iterate over all patients.

Patient ids are the keys that may be passed to e.g. list_observations().

list_studies() → Generator[dict[str, dict[str, Any]]]

Iterate over studies.

Only returns studies I have access to (i.e. owned by my organization(s)).

exception jupyterhealth_client.RequestError(requests_error: HTTPError)

Subclass of request error that shows the actual error

jupyterhealth_client.tidy_observation(observation: dict) → dict

Given an Observation from JupyterHealth (as returned by list_observations()), return a flat dictionary.

Expands the base64 valueAttachment and reshapes data to a one-level dictionary, appropriate for pandas.from_records. Nested keys are joined with _, so:

```
{"a": {"b": 5}}
```

becomes:

```
{"a_b": 5}
```

any fields ending with ‘date_time’ are parsed as timestamps. To avoid problems with plotting libraries, all date_time fields are presented in UTC, and a separate _date_time_local field is the local timestamp in the observed timezone with timezone info removed.

Example output:

```
{
    "code": "omh:blood-glucose:4.0",
    "resourceType": "Observation",
    "id": 64914,
    "meta_lastUpdated": Timestamp("2025-03-12 16:00:50.952478+0000", tz="UTC"),
    "identifier_0_value": "u-u-i-d-4",
    "identifier_0_system": "https://commonhealth.org",
    "status": "final",
    "subject_reference": "Patient/46007",
    "code_coding_0_code": "omh:blood-glucose:4.0",
    "code_coding_0_system": "https://w3id.org/openmhealth",
    "uuid": "u-u-i-d-5",
    "modality": "self-reported",
    "schema_id_name": "blood-glucose",
    "schema_id_version": "3.1",
    "schema_id_namespace": "omh",
    "creation_date_time": Timestamp("2025-03-12 15:47:30.510000+0000", tz="UTC"),
    "external_datasheets_0_datasheet_type": "manufacturer",
    "external_datasheets_0_datasheet_reference": "Health Connect",
    "source_data_point_id": "u-u-i-d-6",
    "source_creation_date_time": Timestamp("2025-02-15 17:28:33.271000+0000", tz="UTC"),
    "blood_glucose_unit": "MGDL",
    "blood_glucose_value": 97,
    "effective_time_frame_date_time": Timestamp(
        "2025-02-15 17:28:33.271000+0000", tz="UTC"
    ),
    "temporal_relationship_to_meal": "unknown",
    "creation_date_time_local": Timestamp("2025-03-12 15:47:30.510000"),
    "source_creation_date_time_local": Timestamp("2025-02-15 17:28:33.271000"),
    "effective_time_frame_date_time_local": Timestamp("2025-02-15 17:28:33.271000"),
}
```
