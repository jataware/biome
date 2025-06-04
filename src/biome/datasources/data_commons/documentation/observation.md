Observation

The Observation API fetches statistical observations. An observation is associated with an entity and variable at a particular date: for example, “population of USA in 2020”, “GDP of California in 2010”, and so on.

    Note: This endpoint returns Python dataclass objects, like other endpoints. To get Pandas DataFrames results, see Observation pandas which is a direct property method of the Client object.

Source code

    Request methods
    Response
        Response fields
        Response property methods
    fetch
        Signature
        Input parameters
        Examples
    fetch_available_statistical_variables
        Signature
        Input parameters
        Examples
    fetch_observations_by_entity_dcid
        Signature
        Input parameters
        Examples
    fetch_observations_by_entity_type
        Signature
        Input parameters
        Examples

Request methods

The following are the methods available for this endpoint.
Method 	Description
fetch 	Fetch observations for specified variables, dates, and entities by DCID or relation expression
fetch_available_statistical_variables 	Fetch the statistical variables available for a given entity or entities.
fetch_observations_by_entity_dcid 	Fetch observations for specified variables, dates and entities, by entity DCID.
fetch_observations_by_entity_type 	Fetch observations for specified variables and dates, by entity type and parent entity.
Response

With select=["date", "entity", "variable", "value"] in effect (the default), the response looks like this:

{
  "byVariable": {
    "VARIABLE_DCID_1": {
      "byEntity": {
        "ENTITY_DCID_1": {
          "orderedFacets": [
            {
              "facetId": "FACET_ID",
              "earliestDate" : "DATE_STRING",
              "latestDate" : "DATE_STRING",
              "obsCount" : "NUMBER_OF_OBSERVATIONS",
              "observations": [
                {
                  "date": "OBSERVATION_DATE",
                  "value": "OBSERVATION_VALUE"
                },
                ...
              ]
            },
            ...
        },
        ...
      },
      ...
    }
  "facets" {
    "FACET_ID": {
      "importName": "...",
      "provenanceUrl": "...",
      "measurementMethod": "...",
      "observationPeriod": "..."
    },
    ...
  }

With select=["variable", "entity"], the response looks like the following. Note the empty brackets after the entity DCIDs; this simply means that the facet and observation data have been omitted from the response.

{
  "byVariable": {
    "VARIABLE_DCID_1": {
      "byEntity": {
        "ENTITY_DCID_1": {},
        "ENTITY_DCID_2": {},
        ...
      }
    "VARIABLE_DCID_2": {
      ...
  }
}

With select=["variable", "entity", "facet"], the response looks like:

{
  "byVariable": {
    "VARIABLE_DCID_1": {
      "byEntity": {
        "ENTITY_DCID_1": {
          "orderedFacets": [
            {
              "facetId": "FACET_ID",
              "earliestDate" : "DATE_STRING",
              "latestDate" : "DATE_STRING",
              "obsCount" : "NUMBER_OF_OBSERVATIONS"
            },
            ...
        },
        ...
      },
      ...
    }
  "facets" {
    "FACET_ID": {
      "importName": "...",
      "provenanceUrl": "...",
      "measurementMethod": "...",
      "observationPeriod": "..."
    },
    ...
  }

There are additional methods you can call on the response to structure the data differently. See Response property methods for details.
Response fields
Name 	Type 	Description
orderedFacets 	list of objects 	Metadata about the observations returned, keyed first by variable, and then by entity. These include the date range, the number of observations included in the facet and so on.
observations 	list of objects 	Date and value pairs for the observations made in the time period.
facets 	object 	Various properties of reported facets, where available, including the provenance of the data, the import name, date range of observations, etc.
Response property methods

The following methods are available for responses that return NodeResponse objects.
Method 	Description
to_json 	Return the result as a JSON string. See Response formatting for details.
to_dict 	Return the result as a dictionary. See Response formatting for details.
get_data_by_entity 	Key the response data by entity rather than by variable. This is useful for queries that involve multiple entities.
to_observations_as_records 	Get the response data as a series of flat records. See Example 3 below for details.
fetch

Fetches observations for the specified variables, dates, and entities. You can specify entities by DCID or by relation expression.
Signature

fetch(variable_dcids, date, select, entity_dcids, entity_expression)

Input parameters
Name 	Type 	Description
variable_dcids
Required 	string or list of strings 	One or more DCIDs of the statistical variables to query.
date
Optional 	string or string literal 	The date (and time) for which the observations are being requested. By default this is set to "latest", which returns the latest observations. One observation is returned for each specified entity and variable, for each provenance of the data. Other allowed values are:
- A string in ISO-8601 format that specifies the date and time used by the target variable; for example, 2020 or 2010-12. To look up the format of a statistical variable, see Find the date format for a statistical variable.
- "all": Get all observations for the specified variables and entities
select
Optional 	list of string literals 	The fields to be returned in the results. By default this is set to ["date", "entity", "variable", "value"], which returns actual observations, with the date and value for each variable and entity queried. One observation is returned for every facet (dataset) in which the variable appears. Other valid options are:
- ["entity", "variable"]: Return no observations. You can use this to first check whether a given entity (or entities) has data for a given variable or variables, before fetching the observations.
- ["entity", "variable", "facet"]: Return no observations but return all the facets as well, which show the sources of the data.
entity_dcids 	string or list of strings 	One or more DCIDs of the entities to query. One of entity_dcids or entity_expression is required.
entity_expression 	string 	A relation expression that represents the entities to query. One of entity_dcids or entity_expression is required.
filter_facet_domains
Optional 	string or list of strings 	Comma-separated list of domain names. You can use this to filter results by provenance. To find relevant domain names, you can look up the provenanceUrl field in the facet ID of a previous observation response or the url field of the provenance in the knowledge graph browser.
filter_facet_ids
Optional 	string or list of strings 	Comma-separated list of existing facet IDs that you have obtained from previous observation API calls. You can use this to filter results by several properties, including dataset name, provenance, measurement method, etc.
Examples
Example 1: Look up whether a given entity (place) has data for a given variable

In this example, we check whether we have population data, broken down by male and female, for 4 countries, Mexico, Canada, Malaysia, and Singapore. We check if the entities have data for two variables, Count_Person_Male and Count_Person_Female, and use the select options of only entity and variable to omit observations.

Request:

client.observation.fetch(variable_dcids=["Count_Person_Female", "Count_Person_Male"], select=["entity", "variable"], entity_dcids=["country/CAN", "country/MEX", "country/SGP", "country/MYS"])

Response:

The response shows that Canada and Mexico are associated with this variable, but not Singapore or Malaysia. (The empty brackets just mean that the facets and observations have been omitted.)

{
   "byVariable" : {
      "Count_Person_Female" : {
         "byEntity" : {
            "country/CAN" : {},
            "country/MEX" : {}
         }
      },
      "Count_Person_Male" : {
         "byEntity" : {
            "country/CAN" : {},
            "country/MEX" : {}
         }
      }
   }
}

Example 2: Look up whether a given entity (place) has data for a given variable and show the sources

This example is the same as above, but we also get the facets, to see the sources of the available data.

Request:

client.observation.fetch(variable_dcids=["Count_Person_Female", "Count_Person_Male"], select=["entity", "variable", "facet"], entity_dcids=["country/CAN", "country/MEX", "country/SGP", "country/MYS"])

Response:

{
   "byVariable" : {
      "Count_Person_Female" : {
         "byEntity" : {
            "country/CAN" : {
               "orderedFacets" : [
                  {
                     "earliestDate" : "1990",
                     "facetId" : "4181918134",
                     "latestDate" : "2023",
                     "obsCount" : 34
                  },
                  {
                     "earliestDate" : "1990",
                     "facetId" : "1151455814",
                     "latestDate" : "2023",
                     "obsCount" : 34
                  },
                  {
                     "earliestDate" : "2021",
                     "facetId" : "1216205004",
                     "latestDate" : "2021",
                     "obsCount" : 1
                  }
               ]
            },
            "country/MEX" : {
               "orderedFacets" : [
                  {
                     "earliestDate" : "2021",
                     "facetId" : "3251078590",
                     "latestDate" : "2021",
                     "obsCount" : 1
                  },
                  {
                     "earliestDate" : "1990",
                     "facetId" : "4181918134",
                     "latestDate" : "2020",
                     "obsCount" : 31
                  },
                  {
                     "earliestDate" : "1990",
                     "facetId" : "1151455814",
                     "latestDate" : "2020",
                     "obsCount" : 31
                  },
                  {
                     "earliestDate" : "1990",
                     "facetId" : "3614729857",
                     "latestDate" : "2020",
                     "obsCount" : 6
                  }
               ]
            }
         }
      },
      "Count_Person_Male" : {
         "byEntity" : {
            "country/CAN" : {
               "orderedFacets" : [
                  {
                     "earliestDate" : "1990",
                     "facetId" : "4181918134",
                     "latestDate" : "2023",
                     "obsCount" : 34
                  },
                  {
                     "earliestDate" : "1990",
                     "facetId" : "1151455814",
                     "latestDate" : "2023",
                     "obsCount" : 34
                  },
                  {
                     "earliestDate" : "2021",
                     "facetId" : "1216205004",
                     "latestDate" : "2021",
                     "obsCount" : 1
                  }
               ]
            },
            "country/MEX" : {
               "orderedFacets" : [
                  {
                     "earliestDate" : "2021",
                     "facetId" : "3251078590",
                     "latestDate" : "2021",
                     "obsCount" : 1
                  },
                  {
                     "earliestDate" : "1990",
                     "facetId" : "4181918134",
                     "latestDate" : "2020",
                     "obsCount" : 31
                  },
                  {
                     "earliestDate" : "1990",
                     "facetId" : "1151455814",
                     "latestDate" : "2020",
                     "obsCount" : 31
                  },
                  {
                     "earliestDate" : "1990",
                     "facetId" : "3614729857",
                     "latestDate" : "2020",
                     "obsCount" : 6
                  }
               ]
            }
         }
      }
   },
   "facets" : {
      "1151455814" : {
         "importName" : "OECDRegionalDemography",
         "measurementMethod" : "OECDRegionalStatistics",
         "observationPeriod" : "P1Y",
         "provenanceUrl" : "https://stats.oecd.org/Index.aspx?DataSetCode=REGION_DEMOGR#"
      },
      "1216205004" : {
         "importName" : "CanadaStatistics",
         "provenanceUrl" : "https://www150.statcan.gc.ca/n1/en/type/data?MM=1"
      },
      "3251078590" : {
         "importName" : "MexicoCensus_AA2",
         "provenanceUrl" : "https://data.humdata.org/dataset/cod-ps-mex"
      },
      "3614729857" : {
         "importName" : "MexicoCensus",
         "provenanceUrl" : "https://www.inegi.org.mx/temas/"
      },
      "4181918134" : {
         "importName" : "OECDRegionalDemography_Population",
         "measurementMethod" : "OECDRegionalStatistics",
         "observationPeriod" : "P1Y",
         "provenanceUrl" : "https://data-explorer.oecd.org/vis?fs[0]=Topic%2C0%7CRegional%252C%20rural%20and%20urban%20development%23GEO%23&pg=40&fc=Topic&bp=true&snb=117&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_REG_DEMO%40DF_POP_5Y&df[ag]=OECD.CFE.EDS&df[vs]=2.0&dq=A.......&to[TIME_PERIOD]=false&vw=tb&pd=%2C"
      }
   }
}

Example 3: Get all observations for multiple entities specified by DCID, and return the results as flat records

In this example, we get all the observations for the 2 countries, Mexico and Canada, that have data forCount_Person_Male and Count_Person_Female. Each observation is returned as a single record.

Request:

client.observation.fetch(variable_dcids=["Count_Person_Female", "Count_Person_Male"], date="", select=["entity", "variable", "date", "value"], entity_dcids=["country/CAN", "country/MEX"])

Response:

[{'date': '2023',
  'entity': 'country/CAN',
  'variable': 'Count_Person_Female',
  'value': 20084054,
  'facetId': '4181918134',
  'importName': 'OECDRegionalDemography_Population',
  'measurementMethod': 'OECDRegionalStatistics',
  'observationPeriod': 'P1Y',
  'provenanceUrl': 'https://data-explorer.oecd.org/vis?fs[0]=Topic%2C0%7CRegional%252C%20rural%20and%20urban%20development%23GEO%23&pg=40&fc=Topic&bp=true&snb=117&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_REG_DEMO%40DF_POP_5Y&df[ag]=OECD.CFE.EDS&df[vs]=2.0&dq=A.......&to[TIME_PERIOD]=false&vw=tb&pd=%2C',
  'unit': None},
 {'date': '2021',
  'entity': 'country/CAN',
  'variable': 'Count_Person_Female',
  'value': 15839460,
  'facetId': '1216205004',
  'importName': 'CanadaStatistics',
  'measurementMethod': None,
  'observationPeriod': None,
  'provenanceUrl': 'https://www150.statcan.gc.ca/n1/en/type/data?MM=1',
  'unit': None},
 {'date': '2021',
  'entity': 'country/MEX',
  'variable': 'Count_Person_Female',
  'value': 65833180,
  'facetId': '3251078590',
  'importName': 'MexicoCensus_AA2',
  'measurementMethod': None,
  'observationPeriod': None,
  'provenanceUrl': 'https://data.humdata.org/dataset/cod-ps-mex',
  'unit': None},
 {'date': '2020',
  'entity': 'country/MEX',
  'variable': 'Count_Person_Female',
  'value': 64540634,
  'facetId': '4181918134',
  'importName': 'OECDRegionalDemography_Population',
  'measurementMethod': 'OECDRegionalStatistics',
  'observationPeriod': 'P1Y',
  'provenanceUrl': 'https://data-explorer.oecd.org/vis?fs[0]=Topic%2C0%7CRegional%252C%20rural%20and%20urban%20development%23GEO%23&pg=40&fc=Topic&bp=true&snb=117&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_REG_DEMO%40DF_POP_5Y&df[ag]=OECD.CFE.EDS&df[vs]=2.0&dq=A.......&to[TIME_PERIOD]=false&vw=tb&pd=%2C',
  'unit': None},
 {'date': '2020',
  'entity': 'country/MEX',
  'variable': 'Count_Person_Female',
  'value': 64540634,
  'facetId': '3614729857',
  'importName': 'MexicoCensus',
  'measurementMethod': None,
  'observationPeriod': None,
  'provenanceUrl': 'https://www.inegi.org.mx/temas/',
  'unit': None},
 {'date': '2023',
  'entity': 'country/CAN',
  'variable': 'Count_Person_Male',
  'value': 20013707,
  'facetId': '4181918134',
  'importName': 'OECDRegionalDemography_Population',
  'measurementMethod': 'OECDRegionalStatistics',
  'observationPeriod': 'P1Y',
  'provenanceUrl': 'https://data-explorer.oecd.org/vis?fs[0]=Topic%2C0%7CRegional%252C%20rural%20and%20urban%20development%23GEO%23&pg=40&fc=Topic&bp=true&snb=117&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_REG_DEMO%40DF_POP_5Y&df[ag]=OECD.CFE.EDS&df[vs]=2.0&dq=A.......&to[TIME_PERIOD]=false&vw=tb&pd=%2C',
  'unit': None},
 {'date': '2021',
  'entity': 'country/CAN',
  'variable': 'Count_Person_Male',
  'value': 15139730,
  'facetId': '1216205004',
  'importName': 'CanadaStatistics',
  'measurementMethod': None,
  'observationPeriod': None,
  'provenanceUrl': 'https://www150.statcan.gc.ca/n1/en/type/data?MM=1',
  'unit': None},
 {'date': '2021',
  'entity': 'country/MEX',
  'variable': 'Count_Person_Male',
  'value': 63139259,
  'facetId': '3251078590',
  'importName': 'MexicoCensus_AA2',
  'measurementMethod': None,
  'observationPeriod': None,
  'provenanceUrl': 'https://data.humdata.org/dataset/cod-ps-mex',
  'unit': None},
 {'date': '2020',
  'entity': 'country/MEX',
  'variable': 'Count_Person_Male',
  'value': 61473390,
  'facetId': '4181918134',
  'importName': 'OECDRegionalDemography_Population',
  'measurementMethod': 'OECDRegionalStatistics',
  'observationPeriod': 'P1Y',
  'provenanceUrl': 'https://data-explorer.oecd.org/vis?fs[0]=Topic%2C0%7CRegional%252C%20rural%20and%20urban%20development%23GEO%23&pg=40&fc=Topic&bp=true&snb=117&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_REG_DEMO%40DF_POP_5Y&df[ag]=OECD.CFE.EDS&df[vs]=2.0&dq=A.......&to[TIME_PERIOD]=false&vw=tb&pd=%2C',
  'unit': None},
 {'date': '2020',
  'entity': 'country/MEX',
  'variable': 'Count_Person_Male',
  'value': 61473390,
  'facetId': '3614729857',
  'importName': 'MexicoCensus',
  'measurementMethod': None,
  'observationPeriod': None,
  'provenanceUrl': 'https://www.inegi.org.mx/temas/',
  'unit': None}]

Example 4: Get the latest observations for entities specified by expression

In this example, we get the latest population counts for counties in California. We use a filter expression to specify “all contained places in California of type county”.

Request:

client.observation.fetch(variable_dcids="Count_Person", entity_expression="geoId/06<-containedInPlace+{typeOf:County}")

Response:

(truncated)

{
  "byVariable": {
    "Count_Person": {
      "byEntity": {
        "geoId/06003": {
          "orderedFacets": [
            {
              "facetId": "2176550201",
              "observations": [
                {
                  "date": "2021",
                  "value": 1235
                }
              ]
            },
          ]
        },
        "geoId/06009": {
          "orderedFacets": [
            {
              "facetId": "2176550201",
              "observations": [
                {
                  "date": "2021",
                  "value": 46221
                }
              ]
            },
          ]
        },
      }
    }
  },
  "facets": {
    "2176550201": {
      "importName": "USCensusPEP_Annual_Population",
      "measurementMethod" : "CensusPEPSurvey",
      "observationPeriod" : "P1Y",
      "provenanceUrl" : "https://www2.census.gov/programs-surveys/popest/tables"
    },
  }
}
...

fetch_available_statistical_variables

Look up the statistical variables available for one or more entities (places).
Signature

fetch_available_statistical_variables(entity_dcids)

Input parameters
Name 	Type 	Description
entity_dcids
Required 	string or list of strings 	See fetch for description.
Examples
Example 1: Look up the statistical variables available for a given entity (place)

In this example, we get a list of variables that are available (have observation data) for one country, Togo.

Request:

client.observation.fetch_available_statistical_variables(entity_dcids=["country/TGO"])

Response:

(truncated)

{
  "byVariable": {
    "AmountOutstanding_Debt_PubliclyGuaranteed_LongTermExternalDebt_LenderCountryCHE": {
      "byEntity": {
        "country/TGO": {

        }
      }
    },
    "worldBank/SP_DYN_CBRT_IN": {
      "byEntity": {
        "country/TGO": {

        }
      }
    },
    "MinTemp_Daily_GaussianMixture_5PctProb_LessThan_Atleast1DayAYear_CMIP6_MPI-ESM1-2-LR_SSP585": {
      "byEntity": {
        "country/TGO": {

        }
      }
    },
    "eia/INTL.2-12-BKWH.A": {
      "byEntity": {
        "country/TGO": {

        }
      }
    },
    "eia/INTL.4002-8-MMTCD.A": {
      "byEntity": {
        "country/TGO": {

        }
      }
    },
    "sdg/SE_AGP_CPRA.URBANISATION--R__EDUCATION_LEV--ISCED11_3__INCOME_WEALTH_QUANTILE--Q5": {
      "byEntity": {
        "country/TGO": {

        }
      }
    },
    "worldBank/BAR_PRM_ICMP_25UP_FE_ZS": {
      "byEntity": {
        "country/TGO": {

        }
      }
    },
    "Amount_Debt_JPY_LenderWestAfricanDevelopmentBank_AsAFractionOf_Amount_Debt_LenderWestAfricanDevelopmentBank": {
      "byEntity": {
        "country/TGO": {

        }
      }
    },
    "Amount_Debt_SDR_LenderOPECFundforInternationalDev_AsAFractionOf_Amount_Debt_LenderOPECFundforInternationalDev": {
      "byEntity": {
        "country/TGO": {

        }
      }
    },
    "MinTemp_Daily_GaussianMixture_1PctProb_LessThan_Atleast1DayAYear_CMIP6_MPI-ESM1-2-HR_Historical": {
      "byEntity": {
        "country/TGO": {

        }
      }
    },
    "worldBank/SH_FPL_SATM_ZS": {
      "byEntity": {
        "country/TGO": {

        }
      }
    },
    "worldBank/SP_POP_3539_MA": {
      "byEntity": {
        "country/TGO": {

        }
      }
    },
    "worldBank/UIS_REPP_1_G2_F": {
      "byEntity": {
        "country/TGO": {

        }
      }
    },
    "sdg/SG_PLN_RECRICTRY": {
      "byEntity": {
        "country/TGO": {

        }
      }
    },

fetch_observations_by_entity_dcid

Fetches observations for the specified variables, dates, and entities.
Signature

fetch_observations_by_entity_dcid(date, entity_dcids, variable_dcids, select, filter_facet_domains, filter_facet_ids)

Input parameters
Name 	Type 	Description
date
Required 	string or string literal 	See fetch for description.
entity_dcids
Required 	string or list of strings 	See fetch for description.
variable_dcids
Required 	string or list of strings 	See fetch for description.
select
Optional 	list of string literals 	See fetch for description.
filter_facet_domains
Optional 	string or list of strings 	See fetch for description.
filter_facet_ids
Optional 	string or list of strings 	See fetch for description.
Examples
Example 1: Get the latest observations for a single entity by DCID

In this example, we get all the latest population observations for one country, Canada. by its DCID using entity.dcids. Note that in the response, there are multiple facets returned, because this variable (representing a simple population count) is used in several datasets.

Request:

client.observation.fetch_observations_by_entity_dcid(date="latest", entity_dcids="country/CAN", variable_dcids="Count_Person")

    Tip: This example is the equivalent of client.observation.fetch(variable_dcids="Count_Person", entity_dcids="country/CAN").

Response:

{
  "byVariable": {
    "Count_Person": {
      "byEntity": {
        "country/CAN": {
          "orderedFacets": [
            {
              "facetId": "3981252704",
              "observations": [
                {
                  "date": "2023",
                  "value": 40097761
                }
              ],
              "obsCount": 1,
              "earliestDate": "2023",
              "latestDate": "2023"
            },
            {
              "facetId": "1151455814",
              "observations": [
                {
                  "date": "2023",
                  "value": 40097761
                }
              ],
              "obsCount": 1,
              "earliestDate": "2023",
              "latestDate": "2023"
            },
            {
              "facetId": "4181918134",
              "observations": [
                {
                  "date": "2023",
                  "value": 40097761
                }
              ],
              "obsCount": 1,
              "earliestDate": "2023",
              "latestDate": "2023"
            },
            {
              "facetId": "1216205004",
              "observations": [
                {
                  "date": "2021",
                  "value": 36991981
                }
              ],
              "obsCount": 1,
              "earliestDate": "2021",
              "latestDate": "2021"
            }
          ]
        }
      }
    }
  },
  "facets": {
    "3981252704": {
      "importName": "WorldDevelopmentIndicators",
      "provenanceUrl": "https://datacatalog.worldbank.org/dataset/world-development-indicators/",
      "observationPeriod": "P1Y"
    },
    "1151455814": {
      "importName": "OECDRegionalDemography",
      "provenanceUrl": "https://stats.oecd.org/Index.aspx?DataSetCode=REGION_DEMOGR#",
      "measurementMethod": "OECDRegionalStatistics",
      "observationPeriod": "P1Y"
    },
    "4181918134": {
      "importName": "OECDRegionalDemography_Population",
      "provenanceUrl": "https://data-explorer.oecd.org/vis?fs[0]=Topic%2C0%7CRegional%252C%20rural%20and%20urban%20development%23GEO%23&pg=40&fc=Topic&bp=true&snb=117&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_REG_DEMO%40DF_POP_5Y&df[ag]=OECD.CFE.EDS&df[vs]=2.0&dq=A.......&to[TIME_PERIOD]=false&vw=tb&pd=%2C",
      "measurementMethod": "OECDRegionalStatistics",
      "observationPeriod": "P1Y"
    },
    "1216205004": {
      "importName": "CanadaStatistics",
      "provenanceUrl": "https://www150.statcan.gc.ca/n1/en/type/data?MM=1"
    }
  }
}

Example 2: Get the latest observations for a single entity, filtering by provenance

In this example, we again get the latest observations for Count_Person, but this time for the U.S., filtering for a single source, namely the U.S. government census, represented by its domain name, www2.census.gov.

Request:

client.observation.fetch_observations_by_entity_dcid(date="latest", entity_dcids="country/USA", variable_dcids="Count_Person", filter_facet_domains="www2.census.gov")

    Tip: This example is the equivalent of client.observation.fetch(variable_dcids="Count_Person", entity_dcids="country/USA", filter_facet_domains="www2.census.gov").

Response:

{
   "byVariable" : {
      "Count_Person" : {
         "byEntity" : {
            "country/USA" : {
               "orderedFacets" : [
                  {
                     "earliestDate" : "2024",
                     "facetId" : "2176550201",
                     "latestDate" : "2024",
                     "obsCount" : 1,
                     "observations" : [
                        {
                           "date" : "2024",
                           "value" : 340110988
                        }
                     ]
                  }
               ]
            }
         }
      }
   },
   "facets" : {
      "2176550201" : {
         "importName" : "USCensusPEP_Annual_Population",
         "measurementMethod" : "CensusPEPSurvey",
         "observationPeriod" : "P1Y",
         "provenanceUrl" : "https://www2.census.gov/programs-surveys/popest/tables"
      }
   }
}

Example 3: Get the observations at a particular date for given entities by DCID

This gets observations for the populations of the U.S.A. and California in 2015. It uses the same variable as the previous example, two entities, and a specific date.

Request:

client.observation.fetch_observations_by_entity_dcid(date="2015", entity_dcids=["country/USA", "geoId/06"], variable_dcids="Count_Person")

    Tip: This example is the equivalent of client.observation.fetch(variable_dcids="Count_Person", date="2015", entity_dcids=["country/USA", "geoId/06"])

Response:

{
  "byVariable": {
    "Count_Person": {
      "byEntity": {
        "country/USA": {
          "orderedFacets": [
            {
              "facetId": "2176550201",
              "observations": [
                {
                  "date": "2015",
                  "value": 320738994
                }
              ],
              "obsCount": 1,
              "earliestDate": "2015",
              "latestDate": "2015"
            },
            {
              "facetId": "2645850372",
              "observations": [
                {
                  "date": "2015",
                  "value": 320098094
                }
              ],
              "obsCount": 1,
              "earliestDate": "2015",
              "latestDate": "2015"
            },
            {
              "facetId": "3981252704",
              "observations": [
                {
                  "date": "2015",
                  "value": 320738994
                }
              ],
              "obsCount": 1,
              "earliestDate": "2015",
              "latestDate": "2015"
            },
            {
              "facetId": "1151455814",
              "observations": [
                {
                  "date": "2015",
                  "value": 320635163
                }
              ],
              "obsCount": 1,
              "earliestDate": "2015",
              "latestDate": "2015"
            },
            ...
        "geoId/06": {
          "orderedFacets": [
            {
              "facetId": "2176550201",
              "observations": [
                {
                  "date": "2015",
                  "value": 38904296
                }
              ],
              "obsCount": 1,
              "earliestDate": "2015",
              "latestDate": "2015"
            },
            {
              "facetId": "1145703171",
              "observations": [
                {
                  "date": "2015",
                  "value": 38421464
                }
              ],
              "obsCount": 1,
              "earliestDate": "2015",
              "latestDate": "2015"
            },
            {
              "facetId": "1151455814",
              "observations": [
                {
                  "date": "2015",
                  "value": 38918045
                }
              ],
              "obsCount": 1,
              "earliestDate": "2015",
              "latestDate": "2015"
            },
            {
              "facetId": "4181918134",
              "observations": [
                {
                  "date": "2015",
                  "value": 38918045
                }
              ],
              "obsCount": 1,
              "earliestDate": "2015",
              "latestDate": "2015"
            },
            {
              "facetId": "10983471",
              "observations": [
                {
                  "date": "2015",
                  "value": 38421464
                }
              ],
              "obsCount": 1,
              "earliestDate": "2015",
              "latestDate": "2015"
            },
            ...
            {
              "facetId": "2458695583",
              "observations": [
                {
                  "date": "2015",
                  "value": 39144818
                }
              ],
              "obsCount": 1,
              "earliestDate": "2015",
              "latestDate": "2015"
            }
          ]
        }
      }
    }
  },
  "facets": {
    "1226172227": {
      "importName": "CensusACS1YearSurvey",
      "provenanceUrl": "https://www.census.gov/programs-surveys/acs/data/data-via-ftp.html",
      "measurementMethod": "CensusACS1yrSurvey"
    },
    "2458695583": {
      "importName": "WikidataPopulation",
      "provenanceUrl": "https://www.wikidata.org/wiki/Wikidata:Main_Page",
      "measurementMethod": "WikidataPopulation"
    },
    "3981252704": {
      "importName": "WorldDevelopmentIndicators",
      "provenanceUrl": "https://datacatalog.worldbank.org/dataset/world-development-indicators/",
      "observationPeriod": "P1Y"
    },
    "4181918134": {
      "importName": "OECDRegionalDemography_Population",
      "provenanceUrl": "https://data-explorer.oecd.org/vis?fs[0]=Topic%2C0%7CRegional%252C%20rural%20and%20urban%20development%23GEO%23&pg=40&fc=Topic&bp=true&snb=117&df[ds]=dsDisseminateFinalDMZ&df[id]=DSD_REG_DEMO%40DF_POP_5Y&df[ag]=OECD.CFE.EDS&df[vs]=2.0&dq=A.......&to[TIME_PERIOD]=false&vw=tb&pd=%2C",
      "measurementMethod": "OECDRegionalStatistics",
      "observationPeriod": "P1Y"
    },
    "10983471": {
      "importName": "CensusACS5YearSurvey_SubjectTables_S2601A",
      "provenanceUrl": "https://data.census.gov/cedsci/table?q=S2601A&tid=ACSST5Y2019.S2601A",
      "measurementMethod": "CensusACS5yrSurveySubjectTable"
    },
    "1964317807": {
      "importName": "CensusACS5YearSurvey_SubjectTables_S0101",
      "provenanceUrl": "https://data.census.gov/table?q=S0101:+Age+and+Sex&tid=ACSST1Y2022.S0101",
      "measurementMethod": "CensusACS5yrSurveySubjectTable"
    },
    "2517965213": {
      "importName": "CensusPEP",
      "provenanceUrl": "https://www.census.gov/programs-surveys/popest.html",
      "measurementMethod": "CensusPEPSurvey"
    },
    "2825511676": {
      "importName": "CDC_Mortality_UnderlyingCause",
      "provenanceUrl": "https://wonder.cdc.gov/ucd-icd10.html"
    },
    "1151455814": {
      "importName": "OECDRegionalDemography",
      "provenanceUrl": "https://stats.oecd.org/Index.aspx?DataSetCode=REGION_DEMOGR#",
      "measurementMethod": "OECDRegionalStatistics",
      "observationPeriod": "P1Y"
    },
    ...
  }
}

Example 4: Get all observations for selected entities by DCID

This example gets all observations for populations with doctoral degrees in the states of Wisconsin and Minnesota, represented by statistical variable Count_Person_EducationalAttainmentDoctorateDegree.

Request:

client.observation.fetch_observations_by_entity_dcid(date="all", entity_dcids=["geoId/55", "geoId/27"],  variable_dcids="Count_Person_EducationalAttainmentDoctorateDegree")

    Tip: This example is the equivalent of client.observation.fetch(variable_dcids="Count_Person_EducationalAttainmentDoctorateDegree", date="all", entity_dcids=["geoId/55", "geoId/27"])

Response:

{
   "byVariable" : {
      "Count_Person_EducationalAttainmentDoctorateDegree" : {
         "byEntity" : {
            "geoId/27" : {
               "orderedFacets" : [
                  {
                     "earliestDate" : "2012",
                     "facetId" : "1145703171",
                     "latestDate" : "2023",
                     "obsCount" : 12,
                     "observations" : [
                        {
                           "date" : "2012",
                           "value" : 40961
                        },
                        {
                           "date" : "2013",
                           "value" : 42511
                        },
                        {
                           "date" : "2014",
                           "value" : 44713
                        },
                        {
                           "date" : "2015",
                           "value" : 47323
                        },
                        {
                           "date" : "2016",
                           "value" : 50039
                        },
                        {
                           "date" : "2017",
                           "value" : 52737
                        },
                        {
                           "date" : "2018",
                           "value" : 54303
                        },
                        {
                           "date" : "2019",
                           "value" : 55185
                        },
                        {
                           "date" : "2020",
                           "value" : 56170
                        },
                        {
                           "date" : "2021",
                           "value" : 58452
                        },
                        {
                           "date" : "2022",
                           "value" : 60300
                        },
                        {
                           "date" : "2023",
                           "value" : 63794
                        }
                     ]
                  }
               ]
            },
            "geoId/55" : {
               "orderedFacets" : [
                  {
                     "earliestDate" : "2012",
                     "facetId" : "1145703171",
                     "latestDate" : "2023",
                     "obsCount" : 12,
                     "observations" : [
                        {
                           "date" : "2012",
                           "value" : 38052
                        },
                        {
                           "date" : "2013",
                           "value" : 38711
                        },
                        {
                           "date" : "2014",
                           "value" : 40133
                        },
                        {
                           "date" : "2015",
                           "value" : 41387
                        },
                        {
                           "date" : "2016",
                           "value" : 42590
                        },
                        {
                           "date" : "2017",
                           "value" : 43737
                        },
                        {
                           "date" : "2018",
                           "value" : 46071
                        },
                        {
                           "date" : "2019",
                           "value" : 47496
                        },
                        {
                           "date" : "2020",
                           "value" : 49385
                        },
                        {
                           "date" : "2021",
                           "value" : 52306
                        },
                        {
                           "date" : "2022",
                           "value" : 53667
                        },
                        {
                           "date" : "2023",
                           "value" : 55286
                        }
                     ]
                  }
               ]
            }
         }
      }
   },
   "facets" : {
      "1145703171" : {
         "importName" : "CensusACS5YearSurvey",
         "measurementMethod" : "CensusACS5yrSurvey",
         "provenanceUrl" : "https://www.census.gov/programs-surveys/acs/data/data-via-ftp.html"
      }
   }
}

Example 5: Get the latest observations for a single entity, filtering for specific dataset

This example gets the latest population count of Brazil. It filters for a single dataset from the World Bank, using the facet ID 3981252704.

Request:

client.observation.fetch_observations_by_entity_dcid(date="latest", entity_dcids="country/BRA", variable_dcids="Count_Person", filter_facet_ids="3981252704")

    Tip: This example is equivalent to client.observation.fetch(variable_dcids="Count_Person", entity_dcids="country/BRA", filter_facet_ids="3981252704")

Response:

{
   "byVariable" : {
      "Count_Person" : {
         "byEntity" : {
            "country/BRA" : {
               "orderedFacets" : [
                  {
                     "earliestDate" : "2023",
                     "facetId" : "3981252704",
                     "latestDate" : "2023",
                     "obsCount" : 1,
                     "observations" : [
                        {
                           "date" : "2023",
                           "value" : 211140729
                        }
                     ]
                  }
               ]
            }
         }
      }
   },
   "facets" : {
      "3981252704" : {
         "importName" : "WorldDevelopmentIndicators",
         "observationPeriod" : "P1Y",
         "provenanceUrl" : "https://datacatalog.worldbank.org/dataset/world-development-indicators/"
      }
   }
}

fetch_observations_by_entity_type

Fetch observations for multiple entities (places) grouped by parent and type.
Signature

fetch_observations_by_entity_type(date, entity_dcids, variable_dcids, select, filter_facet_domains, filter_facet_ids)

Input parameters
Name 	Type 	Description
date
Required 	string or string literal 	See fetch for description.
parent_entity
Required 	string 	The DCID of the parent entities to query; for example, africa for African countries, or Earth for all countries.
entity_type
Required 	string 	The DCID of the type of the entities to query; for example, Country or Region.
variable_dcids
Required 	string or list of strings 	See fetch for description.
select
Optional 	list of string literals 	See fetch for description.
filter_facet_domains
Optional 	string or list of strings 	See fetch for description.
filter_facet_ids
Optional 	string or list of strings 	See fetch for description.
Examples
Example 1: Get all observations for a selected variable, for child entities of a selected entity

Ths example gets all observatons for the proportion of population below the international poverty line for all countries in Africa.

Request:

client.observation.fetch_observations_by_entity_type(date="all", parent_entity="africa", entity_type="Country", variable_dcids="sdg/SI_POV_DAY1")

    Tip: This example is equivalent to client.observation.fetch(variable_dcids="sdg/SI_POV_DAY1", date="all", entity_expression="africa<-containedInPlace+{typeOf:Country}")

Response:

(truncated)

{
   "byVariable" : {
      "sdg/SI_POV_DAY1" : {
         "byEntity" : {
            "country/AGO" : {
               "orderedFacets" : [
                  {
                     "earliestDate" : "2000",
                     "facetId" : "3549866825",
                     "latestDate" : "2018",
                     "obsCount" : 3,
                     "observations" : [
                        {
                           "date" : "2000",
                           "value" : 21.4
                        },
                        {
                           "date" : "2008",
                           "value" : 14.6
                        },
                        {
                           "date" : "2018",
                           "value" : 31.1
                        }
                     ]
                  }
               ]
            },
            "country/BDI" : {
               "orderedFacets" : [
                  {
                     "earliestDate" : "1992",
                     "facetId" : "3549866825",
                     "latestDate" : "2013",
                     "obsCount" : 4,
                     "observations" : [
                        {
                           "date" : "1992",
                           "value" : 75.1
                        },
                        {
                           "date" : "1998",
                           "value" : 79.4
                        },
                        {
                           "date" : "2006",
                           "value" : 71.8
                        },
                        {
                           "date" : "2013",
                           "value" : 65.1
                        }
                     ]
                  }
               ]
            },
            "country/BEN" : {
               "orderedFacets" : [
                  {
                     "earliestDate" : "2003",
                     "facetId" : "3549866825",
                     "latestDate" : "2018",
                     "obsCount" : 4,
                     "observations" : [
                        {
                           "date" : "2003",
                           "value" : 53.1
                        },
                        {
                           "date" : "2011",
                           "value" : 54.3
                        },
                        {
                           "date" : "2015",
                           "value" : 50.7
                        },
                        {
                           "date" : "2018",
                           "value" : 19.9
                        }
                     ]
                  }
               ]
            },
            "country/BFA" : {
               "orderedFacets" : [
                  {
                     "earliestDate" : "1994",
                     "facetId" : "3549866825",
                     "latestDate" : "2018",
                     "obsCount" : 6,
                     "observations" : [
                        {
                           "date" : "1994",
                           "value" : 82.1
                        },
                        {
                           "date" : "1998",
                           "value" : 79.9
                        },
                        {
                           "date" : "2003",
                           "value" : 54.7
                        },
                        {
                           "date" : "2009",
                           "value" : 52.6
                        },
                        {
                           "date" : "2014",
                           "value" : 39.6
                        },
                        {
                           "date" : "2018",
                           "value" : 30.5
                        }
                     ]
                  }
               ]
            },
            "country/BWA" : {
               "orderedFacets" : [
                  {
                     "earliestDate" : "1985",
                     "facetId" : "3549866825",
                     "latestDate" : "2015",
                     "obsCount" : 5,
                     "observations" : [
                        {
                           "date" : "1985",
                           "value" : 41.8
                        },
                        {
                           "date" : "1993",
                           "value" : 34.1
                        },
                        {
                           "date" : "2002",
                           "value" : 29.1
                        },
                        {
                           "date" : "2009",
                           "value" : 17.7
                        },
                        {
                           "date" : "2015",
                           "value" : 15.4
                        }
                     ]
                  }
               ]
            },
            "country/CAF" : {
               "orderedFacets" : [
                  {
                     "earliestDate" : "1992",
                     "facetId" : "3549866825",
                     "latestDate" : "2008",
                     "obsCount" : 2,
                     "observations" : [
                        {
                           "date" : "1992",
                           "value" : 82.2
                        },
                        {
                           "date" : "2008",
                           "value" : 61.9
                        }
                     ]
                  }
               ]
            },
            "country/CIV" : {
               "orderedFacets" : [
                  {
                     "earliestDate" : "1985",
                     "facetId" : "3549866825",
                     "latestDate" : "2018",
                     "obsCount" : 11,
                     "observations" : [
                        {
                           "date" : "1985",
                           "value" : 8.2
                        },
                        {
                           "date" : "1986",
                           "value" : 4.4
                        },
                        {
                           "date" : "1987",
                           "value" : 9.4
                        },
                        {
                           "date" : "1988",
                           "value" : 13.4
                        },
                        {
                           "date" : "1992",
                           "value" : 27.1
                        },
                        {
                           "date" : "1995",
                           "value" : 25.9
                        },
                        {
                           "date" : "1998",
                           "value" : 30.4
                        },
                        {
                           "date" : "2002",
                           "value" : 29.1
                        },
                        {
                           "date" : "2008",
                           "value" : 34.4
                        },
                        {
                           "date" : "2015",
                           "value" : 33.4
                        },
                        {
                           "date" : "2018",
                           "value" : 11.4
                        }
                     ]
                  }
               ]
            },
            "country/CMR" : {
               "orderedFacets" : [
                  {
                     "earliestDate" : "1996",
                     "facetId" : "3549866825",
                     "latestDate" : "2014",
                     "obsCount" : 4,
                     "observations" : [
                        {
                           "date" : "1996",
                           "value" : 50.4
                        },
                        {
                           "date" : "2001",
                           "value" : 25.7
                        },
                        {
                           "date" : "2007",
                           "value" : 31.4
                        },
                        {
                           "date" : "2014",
                           "value" : 25.7
                        }
                     ]
                  }
               ]
            },
            "country/COD" : {
               "orderedFacets" : [
                  {
                     "earliestDate" : "2004",
                     "facetId" : "3549866825",
                     "latestDate" : "2012",
                     "obsCount" : 2,
                     "observations" : [
                        {
                           "date" : "2004",
                           "value" : 91.5
                        },
                        {
                           "date" : "2012",
                           "value" : 69.7
                        }
                     ]
                  }
               ]
            },
            "country/COG" : {
               "orderedFacets" : [
                  {
                     "earliestDate" : "2005",
                     "facetId" : "3549866825",
                     "latestDate" : "2011",
                     "obsCount" : 2,
                     "observations" : [
                        {
                           "date" : "2005",
                           "value" : 49.6
                        },
                        {
                           "date" : "2011",
                           "value" : 35.4
                        }
                     ]
                  }
               ]
            },
            "country/COM" : {
               "orderedFacets" : [
                  {
                     "earliestDate" : "2004",
                     "facetId" : "3549866825",
                     "latestDate" : "2014",
                     "obsCount" : 2,
                     "observations" : [
                        {
                           "date" : "2004",
                           "value" : 14.6
                        },
                        {
                           "date" : "2014",
                           "value" : 18.6
                        }
                     ]
                  }
               ]
            },
   "facets" : {
      "3549866825" : {
         "importName" : "UN_SDG",
         "measurementMethod" : "SDG_G_G",
         "provenanceUrl" : "https://unstats.un.org/sdgs/dataportal",
         "unit" : "SDG_PERCENT"
      }
   }
}
