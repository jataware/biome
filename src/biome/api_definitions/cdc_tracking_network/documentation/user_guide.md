The Data Application Program Interface (API) is an additional way to query data stored by the Environmental Public Health Tracking Network. The API provides a standard URL interface with a Javascript Object Notation (JSON) formatted response. An error object is returned with an invalid call. An empty object is returned with no data.

# Introduction
The Tracking Network’s environmental public health data are organized into three, tiered categories: content areas, indicators, and
measures. The Tracking Network houses over 500 unique measures that are grouped under one or more indicators. Each indicator belongs to one or more content areas.
```
Content Area
↓
Indicator(s)
↓
Measure(s)
```
This user guide outlines the process of navigating from content areas to measures of interest, as well as determining desired location,
times, and strata for the measures. This document contains four sections:
- Functions: Definition and format of all currently available functions
- Examples: Example calls and descriptions of all available functions
- Schema: Defines the structure and types of the JSON object returned by each function
- Appendix: Glossary and tables of all available parameters that might be passed to various functions

New users will find the Functions and Examples sections most helpful. The Schema and Appendix sections provide information about
the types of data available, including measures, times, and stratifications.

# Overviews

This section provides an overview of the current calls available through the Tracking Network's API. Each call will have the following
information in the following order:
- Definition: Explanation of the call and what it returns
- Format: The URL structure the call uses
- Parameters: A list of variables that must/may be passed in the call to get data back
- References: A list of calls that reference the return of the call
Note: The “getCoreHolder” call can also use a “POST” http request, not just a “GET” http request. Information about the “POST” request format is provided in its section.

## Content Areas Overview
### Definition:
Returns all content areas and their associated ID currently available through the API.

### Format:
ephtracking.cdc.gov/apigateway/api/v1/contentareas/json[?apiToken]

### Parameters:
apiToken (optional)


## Indicators Overview
### Definition:
Return all indicators and their associated ID available within a content area.

### Format:
ephtracking.cdc.gov/apigateway/api/v1/indicators/{{contentAreaId}}[?apiToken]

### Parameters:
contentAreaId
apiToken (optional)
Valid Content Area ID—Invalid entry will return an empty data set.
Called via "apiToken=TOKEN" where TOKEN is the unique identifier supplied by the Environmental Public Health

## Measures Overview
### Definition:
Return all measures and their associated IDs within an indicator.

### Format:
ephtracking.cdc.gov/apigateway/api/v1/measures/{{indicatorId}}[?apiToken]

### Parameters:
indicatorId
apiToken (optional)
Valid Indicator ID—Invalid entry will return an empty data set.


## Geographic Types Overview
### Definition:
Lists all geographic types and their associated IDs available for a measure.

### Format:
ephtracking.cdc.gov/apigateway/api/v1/geographicTypes/{{measureId}}[?apiToken]

### Parameters:
`measureId`
Requires a valid measureID.
`apiToken` (optional)

## Stratification Types Overview
### Definition:
Lists all stratification types for a measure and geographic type, including the stratification type’s column name and local IDs
within the column.

### Format:
ephtracking.cdc.gov/apigateway/api/v1/stratificationTypes/{{measureId}}/{{geographicTypeId}}/{{isSmoothed}}[?apiToken]

### Parameters:
`measureId`
Requires a valid measureID.
`geographicTypeId`
Requires a valid geographicTypeID.
`isSmoothed`
Requires either a one or zero (true or false) for having data that is geographically smoothed.
NOTE: The majority of measures do not have smoothing value.
`apiToken` (optional)

## Stratification Level Overview
### Definition:
Lists all available stratification levels and their associated stratification types for a measure and geography level.

### Format:
ephtracking.cdc.gov/apigateway/api/v1/stratificationlevel/{{measureId}}/{{geographicTypeId}}/{{isSmoothed}}[?apiToken]

### Parameters:
`measureId`
Requires a valid measureID.
`geographicTypeId`
Requires a valid geographicTypeID.
`isSmoothed`
Requires either a one or zero (true or false) for having data that is geographically smoothed.
NOTE: The majority of measures do not have smoothing value.
`apiToken` (optional)

## Geographic Items Overview
### Definition:
Lists all available geographic items for some geographic type and measure. Flag geographic rollup to only view unique parent geographic items.
### Format:
```
https://ephtracking.cdc.gov/apigateway/api/v1/geographicItems/{measureID}/{geographicTypeId}/{geographicRollup}
[?apiToken]
```

### Parameters:
`measureId`
Requires a valid measureID.
`geographicTypeId`
Requires a valid geographicTypeID.
`geographicRollup`
Requires either a one or zero (true or false) to include geographicRollup.
`apiToken` (optional)

## Temporal Items Overview
### Definition:
Listing all available temporal items for a measure for some set of locations of a geographic type.

### Format:
```
https://ephtracking.cdc.gov/apigateway/api/v1/temporalItems/{{measureID}}/{{geographicTypeId}}/{{geographicTypeIdFilter}}/
{{geographicItemsFilter}}[?apiToken]
```

### Parameters:
`measureId`
Requires a valid measureID.
`geographicTypeId`
Requires a valid geographicTypeID.
`geographicTypeIdFilter`
Filter to retrieve only filtered geographicTypeId's.
`geographicItemsFilter`
Filter to retrieve only certain geographicItems.
`apiToken` (optional)

## Get Core Holder Overview
### Definition:
Returns metadata and all data points associated with a measure for a certain set of temporal items, geographic items, and a stratification level and its optional stratification items.

### GET Format:
```
https://ephtracking.cdc.gov/apigateway/api/v1/getCoreHolder/{{measureId}}/{{stratificationLevelId}}/
{{geographicTypeIdFilter}}/{{geographicItemsFilter}}/{{temporalTypeIdFilter}}/{{temporalItemsFilter}}/{{isSmoothed}}/
{{getFullCoreHolder}}[?stratificationLevelLocalIds][?apiToken]
```

### POST Format
#### URL:
```
ephtracking.cdc.gov/apigateway/api/v1/getCoreHolder/{{measureId}}/{{stratificationLevelId}}/{{isSmoothed}}/
{{getFullCoreHolder}}[?stratificationLevelLocalIds][?apiToken]
```
#### Header:
Accept: application/json
#### Body:
```
{{
"geographicTypeIdFilter" : "string",
"geographicItemsFilter" : "string",
"temporalTypeIdFilter" : "string",
"temporalItemsFilter" : "string"
"embedId": "string"
}}
```

### Parameters:
`version`
Only "v1" is valid for this version.
`measureId`
Requires a valid measureID.
`stratificationLevelId`
Requires a valid stratificationLevelId.
`geographicTypeIdFilter`
Requires a valid geographicTypeID or ALL.
`geographicItemsFilter`
Filter to retrieve only certain geographicItems.
`temporal`
Requires a valid temporal entry (e.g., years) separated by comma.
`isSmoothed`
Requires either a one or zero (true or false) for having data that is geographically smoothed.
NOTE: The majority of measures do not have smoothing value.
`getFullCoreHolder`
Requires either a one or zero (true or false) for fetching the full core holder.
NOTE: Do not need full core holder for most purposes.
`stratificationLevelLocalIds` (optional)
Called via "COLUMNNAME=LOCALID". where COLUMNNAME is the internal name of the column and LOCALID is a
comma separated list of all the strata IDs you wish to use to build the strata.
See HERE for some examples on specifics of where to get this information and how to use it.
`apiToken` (optional)

## Measure Search Overview
### Definition:
Returns the full relational view of content areas, indicators, measures, and their associated IDs available through the API.
Additionally, this returns a list of keywords associated with each triplet.

### Format:
https://ephtracking.cdc.gov/apigateway/api/v1/measuresearch[?apiToken]

### Parameters:
`apiToken` (optional)

## All Temporal Types Overview
### Definition:
Returns all temporal types that can be queried through the API.

### Format:
https://ephtracking.cdc.gov/apigateway/api/v1/allTemporalTypes[?apiToken]

### Parameters:
apiToken (optional)

## All Geographic Types Overview
### Definition:
Returns all geographic types that can be queried through the API.

### Format:
https://ephtracking.cdc.gov/apigateway/api/v1/allGeographicTypes[?apiToken]

### Parameters:
`apiToken` (optional)

## All Stratification Types Overview
### Definition:
Returns all stratification types that can be queried through the API.

### Format:
https://ephtracking.cdc.gov/apigateway/api/v1/allStratificationTypes[?apiToken]

### Parameters:
`apiToken` (optional)

## All Stratification Levels Overview
### Definition:
Returns all stratification levels that can be queried through the API.

### Format:
https://ephtracking.cdc.gov/apigateway/api/v1/allStratificationLevels[?apiToken]

### Parameters:
`apiToken` (optional)


## Search Measure by Temporal Items Overview
### Definition:
Returns all measures with data available for all queried temporal items of a given temporal type.

### Format:
ephtracking.cdc.gov/apigateway/api/v1/searchMeasureByTemporalItems/{{temporalTypeId}}/{{temporalItemIdFilter}}
[?contentAreaIdFilter][&indicatorIdFilter][&apiToken]

### Parameters:
`version`
Only "v1" is valid for this version.
`temporalTypeId`
The temporal type of the passed geographic items.
`temporalItemIdFilter`
The list of temporal items to test measures against.
`contentAreaIdFilter` (optional)
Optional additional filter that only returns measures that belong to the list of passed content areas.
`indicatorIdFilter` (optional)
Optional additional filter that only returns measures that belong to the list of passed indicators.
When used with contentAreaIdFilter, it will return and indication if it belongs to either the indicator or content area. It is
not exclusively one or the other.
`apiToken` (optional)

## Search Measure by Geographic Items Overview
### Definition:
Returns all measures with data available for all queried geographic items of geographic type.

### Format:
ephtracking.cdc.gov/apigateway/api/v1/searchMeasureByGeographicItems/{{geographicTypeId}}/{{geographicItemIdFilter}}
[?contentAreaIdFilter][&indicatorIdFilter][&apiToken]

### Parameters:
`geographicTypeId`
The geographic type of the passed geographic items.
`geographicItemIdFilter`
The list of geographic items to test measures against.
`contentAreaIdFilter` (optional)
Optional additional filter that only returns measures that belong to the list of passed content areas.
`indicatorIdFilter` (optional)
Optional additional filter that only returns measures that belong to the list of passed indicators.
Used with contentAreaIdFilter will return belonging to either the indicator or content area. Not exclusively one or the
other.
`apiToken` (optional)

## Search Temporal Items by Measure Overview
### Definition:
Returns all temporal items of a specified temporal type that have data available for all queried measures.

### Format:
ephtracking.cdc.gov/apigateway/api/v1/searchTemporalItemsByMeasure/{{temporalTypeId}}/{{measureIdFilter}}
[?parentTemporalId][&apiToken]

### Parameters:
`temporalTypeId`
The temporal type you are searching for.
`measureIdFilter`
The list of measure items to search for geographic items.
`parentTemporalId` (optional)
Optional filter that will only return temporal items whose parent temporal ID is in the filter.
`apiToken` (optional)

## Search Geographic Items by Measure Overview
### Definition:
Returns all geographic items of a specified geographic type that have data available for all passed measure IDs.

### Format:
ephtracking.cdc.gov/apigateway/api/v1/searchGeographicItemsByMeasure/{{geographicTypeId}}/{{measureIdFilter}}
[?parentGeographicId][&apiToken]

### Parameters:
`geographicTypeId`
The geographic type you are searching for.
`measureIdFilter`
The list of measure items to search for geographic items.
`parentGeographicId` (optional)
Optional filter that will only return geographic items whose parent geographic ID is in the filter.
`apiToken` (optional)

# Examples

The following examples show how to use the Tracking Network’s API. The first showcases the process to querying our data in the same way CDC's interactive Data Explorer does, starting with selecting a content area and ending with our query to getCoreHolder to fetch data. Subsequent calls after getCoreHolder provide advanced queries/information about our API. They exist to help you discover measures/data that may be useful but are not required to get basic use out of the API.

Multiple examples for calls are given to showcase some of the different options with each query made through that call. The call to getCoreHolder is broken into three subsections to accommodate the various options available through the core holder call. They are as follows:
- Querying Different Geographic Types
- Querying Different Temporal Types
- Querying Different Stratification Types
Each subsection of the core holder call gives examples and information specific to the data type we are showcasing.

## Content Area Example
Start by viewing the available content areas provided by the tracking network.

### Format:
ephtracking.cdc.gov/apigateway/api/v1/contentareas/json[?apiToken]

### Example A
Lists all currently available content areas tracked by the Tracking Network's API.

### Parameters A
GET Request A
ephtracking.cdc.gov/apigateway/api/v1/contentareas/json

## Indicator Examples
Select a content area and view all indicators that belong to that content area.

### Format:
ephtracking.cdc.gov/apigateway/api/v1/indicators/{{contentAreaId}}[?apiToken]

### Example A
View all available indicators within the Cancer
content area.

#### Parameters
`contentAreaId` = 9

#### GET Request
ephtracking.cdc.gov/apigateway/api/v1/indicators/9

### Example B
View all available indicators within the Covid-19
content area.

#### Parameters
`contentAreaId` = 33

#### GET Request
ephtracking.cdc.gov/apigateway/api/v1/indicators/3


## Measure Examples
Select an indicator and view all measures that describe that indicator

View all available measures within the Incidence of Thyroid Cancers indicator.

### Format
ephtracking.cdc.gov/apigateway/api/v1/measures/{{indicatorID}}[?apiToken]

### Parameters
`indicatorID` = 25

### GET Request
ephtracking.cdc.gov/apigateway/api/v1/measures/25

## Geographic Types Examples
Once you have a measure you want, you will need to get some information about how you would like to query that measure. We start by finding the geographic type (state, county, national, etc.) that we want to query the measure for.

### Format:
ephtracking.cdc.gov/apigateway/api/v1/geographicTypes/{{measureID}}[?apiToken]

### Example A
View geography levels for the Age-adjusted Incidence Rate of Thyroid Cancer.

#### Parameters
`measureID` = 66

#### GET Request
ephtracking.cdc.gov/apigateway/api/v1/geographicTypes/66


## Stratification Types Examples
After you figure out which geographic type you want, you may need to investigate which stratification types you will want in addition to the location. This isn’t required but is important for creating advanced strata for your core holder queries.

You will need the columnName and stratificationItem’s localId’s for the call to getCoreHolder if you choose to add additional stratification types to your final strata.

### Format:
ephtracking.cdc.gov/apigateway/api/v1/stratificationTypes/{{measureId}}/{{geographicTypeId}}/{{isSmoothed}}[?apiToken]

### Example A
View stratification types for the Age-adjusted Incidence Rate of Thyroid Cancer by State

#### Parameters
measureID = 66
geographicTypeId = 1
isSmoothed = 0

#### GET Request
ephtracking.cdc.gov/apigateway/api/v1/stratificationTypes/66/1/0

### Notes:
- Some measures do not have additional strata to be grouped by; see the second example for "…State-issued Stay-at-home
Orders by County” which returns an empty list.

## Stratification Level Examples
The stratification level is the combination of our geographic type and all the optional stratification types we want to use. You will need
the stratification level ID for the call to getCoreHolder.

### Format:
ephtracking.cdc.gov/apigateway/api/v1/stratificationlevel/{{measureId}}/{{geographicTypeId}}/{{isSmoothed}}[?apiToken]

### Example A
View allowed stratifications for the Age-adjusted Incidence Rate of Thyroid Cancer by State Level.

#### Parameters
measureID = 66
geographicTypeId = 1
isSmoothed = 0

#### GET Request

https://ephtracking.cdc.gov/apigateway/api/v1/stratificationlevel/66/1/0

### Notes:
Some stratification levels have additional strata that need to be specified as the stratification type.
- Notice that the first example has sex as a stratum that must be defined.
- Notice that the second example has no strata in the stratification type; it is defined entirely by geography.
- To see an example of the strata being used you can view the Data Explorer and navigate to the "Age-adjusted Incidence Rate of Thyroid Cancer". The "Advanced Options" is what your strata choices will allow.


## Geographic Items Examples
Using the geographic type’s ID we selected, we can determine which geographic items we want to query data for.

### Format:
ephtracking.cdc.gov/apigateway/api/v1/geographicItems/{measureID}/{geographicTypeId}/{geographicRollup}[?apiToken]

### Example A
View all counties available for State-issued Stay-at-home Orders.

#### Parameters
`measureID` = 927
`geographicTypeId` = 2
`geographicRollup` = 0

#### GET Request
https://ephtracking.cdc.gov/apigateway/api/v1/geographicItems/927/2/0

### Notes:
- Use the geographic rollup option to view parent geographic information available for a chosen geographic level and measure.
- The geographicId typically corresponds to the locations FIPS code, a list of FIPS codes for 2020 can be found at census.gov (or use the `us` python library to get the FIPS codes)

## Temporal Items Examples
With the set of geographic items and their geographic type, we can then query for the temporal items we would like to query for each of these locations.

### Format:
ephtracking.cdc.gov/apigateway/api/v1/temporalItems/{{measureID}}/{{geographicTypeId}}/{{geographicTypeIdFilter}}/
{{geographicItemsFilter}}[?apiToken]

### Example
View temporals available for Appling, Georgia; Antrim, Michigan; and Cherokee, Texas for the State-issued Stay-at-home Orders.

#### Parameters
`measureID` = 927
`geographicTypeId` = 2
`geographicTypeIdFilter` = 2
`geographicItemsFilter` = 13001,26009,48073

#### GET Request
https://ephtracking.cdc.gov/apigateway/api/v1/temporalItems/927/2/2/13001,26009,48073

### Notes:
- The parent temporal properties are null unless a parent is available (daily/monthly/weekly temporal items).

## Core Holder Examples
Using parameters returned from our previous calls, we are ready to query the database for some data about a measure for some set of times and locations. We can also add optional parameters to group our data into more advanced strata.

### GET Request:
ephtracking.cdc.gov/apigateway/api/v1/getCoreHolder/{{measureId}}/{{stratificationLevelId}}/
{{geographicTypeIdFilter}}/{{geographicItemsFilter}}/{{temporalTypeIdFilter}}/{{isSmoothed}}/
{{getFullCoreHolder}}[?stratificationLevelLocalIds][?apiToken]

### POST Request
ephtracking.cdc.gov/apigateway/api/v1/getCoreHolder/{{measureId}}/{{stratificationLevelId}}/{{isSmoothed}}/
{{getFullCoreHolder}}[?stratificationLevelLocalIds][?apiToken]

#### Body:
```
{{
"geographicTypeIdFilter" : "string",
"geographicItemsFilter" : "string",
"temporalTypeIdFilter" : "string",
"temporalItemsFilter" : "string"
"embedId": "string"
}}
```

### Example A
Query the Age-adjusted Incidence Rate of Thyroid Cancer per 100,000 People for the year 2011 for all available states.

### Parameters A
`measureID` = 66
`stratificationLevelId` = 1
`geographicTypeIdFilter` = ALL
`geographicItemsFilter` = ALL
`temporalItemsFilter`= 2011

#### GET Request A
GET https://ephtracking.cdc.gov/apigateway/api/v1/getCoreHolder/66/1/ALL/ALL/2011/0/0

#### POST Request A
```
POST ephtracking.cdc.gov/apigateway/api/v1/getCoreHolder/66/1/0/0
{
"geographicTypeIdFilter": "ALL",
"geographicItemsFilter": "ALL",
"temporalTypeIdFilter": null,
"temporalItemsFilter": "2011",
"embedId": null
}
```

### Notes
Data points from the core holder are returned in one of several table result objects depending on the type of data you are querying.
- The default return table is tableResult; other tables will contain additional fields related specifically to that type of data. You can see all available table results in the Core Holder Glossary.

### Querying Different Geographic Types
The first two examples make calls to the "Age-adjusted Incidence Rate of Thyroid Cancer by State" measure's core holder data for all states or individual states for the two years we are interested in.

### Example
Query State-issued Stay-at-home Orders, for Dec 31, 2020, for
the counties Appling, Georgia; Antrim, Michigan; and Cherokee,
Texas.

#### Parameters
`measureID` = 927
`stratificationLevelId` = 2
`geographicTypeIdFilter` = 2
`geographicItemsFilter` = 13001,26009,48073
`temporalItemsFilter` = 20201231

#### GET Request
https://ephtracking.cdc.gov/apigateway/api/v1/getCoreHolder/927/2/2/13001,26009,48073/8/20201231/0/0

#### POST Request
```
POST https://ephtracking.cdc.gov/apigateway/api/v1/getCoreHolder/927/2/2/13001,26009,48073/8/20201231/0/0
{{
    "geographicTypeIdFilter": "2",
    "geographicItemsFilter": "13001,26009,48073",
    "temporalTypeIdFilter": "8",
    "temporalItemsFilter": "20201231",
    "embedId": null
}}
```

### Notes
- To get all values for all geographic locations for a selected stratificationLevel you need to set both the geographicTypeIdFilter to "ALL" and the geographicItemsFilter to "ALL".
- Requesting data for many different locations can quickly exceed the maximum URL length (~2000 characters). It is recommended to use a POST request for your calls to getCoreHolder. This allows you to pass the geographicItemsFilter in the body of the POST method instead of in the URL.


## Querying Different Temporal Types
Different measures have different temporal types. To query these temporal types, we use the returns of the temporals function in our getCoreHolder query.

### Example
Query State-issued Stay-at-home Orders, for the last 3 days of 2020 for all counties in the U.S.

#### Parameters
measureID = 9
stratificationLevelId = 2
geographicTypeIdFilter = ALL
geographicItemsFilter = ALL
temporalItemsFilter = 2021

#### GET Request
```
https://ephtracking.cdc.gov/apigateway/api/v1/getCoreHolder/927/2/ALL/ALL/8/20201231,20201230,20201229/0/0
```

#### POST Request

```
POST https://ephtracking.cdc.gov/apigateway/api/v1/getCoreHolder/927/2/ALL/ALL/8/20201231,20201230,20201229/0/0
{{
"geographicTypeIdFilter": "ALL",
"geographicItemsFilter": "ALL",
"temporalTypeIdFilter": "8",
"temporalItemsFilter": "20201231,20201230,20201229",
"embedId": null
}}
```

### Notes:
- For the time being, dates must be passed in individually, ranges such as (20200601-20200630) or requesting a specific month
- Even though months do not work for daily values, you can pass a year for all days in that year.
- Requesting data for many different times can quickly exceed the maximum URL length (~2000 characters). It is recommended to use a POST request for your calls to getCoreHolder. This allows you to pass the temporalItemsFilter in the body of the POST method instead of in the URL.

## Querying Different Stratification Types
Our last set of examples will show you how to fetch data from the core holder for advanced strata such as age, ethnicity, etc., or a combination of multiple strata. To create advanced strata, we need three things:

- The stratificationLevelId of the strata that can be found with the stratificationlevel call.
- The columnName of the stratum's localIds that make up the stratification level we are interested in; this can be found with either stratificationlevel or measurestratification calls.
- The localId's of the stratum we want to view; this can be found with measurestratification call.

Previous examples have only used stratification levels 1 and 2, which are the stratum for state and state X county. No additional parameters are needed apart from a geographic type and geographic items for these queries. Adding additional strata to get the strata we want requires appending optional parameters to our URL. We can append multiple stratification types and multiple strata within each stratification type to create our strata.

### Example F
View core holder data of all states in the years 2020 for the Age-adjusted Incidence Rate of Thyroid Cancer of people who are Black or Asian/Pacific Islander.

### Parameters F
`measureID` = 66
`stratificationLevelId` = 43
`geographicTypeIdFilter` = all
`geographicItemsFilter` = all
`temporalItemsFilter`= 2020
`stratificationLevelLocalIds:RaceEthnicityId`=1,2

#### GET Request
https://ephtracking.cdc.gov/apigateway/api/v1/getCoreHolder/66/8/all/all/1/2020/0/0?RaceEthnicityId=1,2

#### POST Request
```
POST https://ephtracking.cdc.gov/apigateway/api/v1/getCoreHolder/66/8/all/all/1/2020/0/0?RaceEthnicityId=1,2
{{
"geographicTypeIdFilter": "all",
"geographicItemsFilter": "all",
"temporalTypeIdFilter": "1",
"temporalItemsFilter": "2020",
"embedId": null
}}
```

### Notes:
- You can specify multiple different stratification types by concatenation with ‘&’ and multiple strata within a stratification type as
comma separated values of each stratum’s localId.
- To know what the full stratification of a data point is you need to check the data points groupById with the lookupList objected
returned by in the core holder.


## Measure Search Example
You may want to query for all the measures available through the API. This query gives a list of all relations between all content areas, indicators, and measures and provides keywords associated with each relation.

### Format:
https://ephtracking.cdc.gov/apigateway/api/v1/measuresearch[?apiToken]

### Example
Returns the full relational view of content areas, indicators, measures, and their associated IDs available through the API.
Additionally, it returns a list of keywords associated with each triplet.

## All Temporal Types Example
You may want to use our API to query for all the temporal types a measure may be tracked for.

### Format:
https://ephtracking.cdc.gov/apigateway/api/v1/allTemporalTypes


## Search Measure by Temporal Items Examples
You may want to query for measures that have data available for all entries in a set of temporal items. Optionally, limit what measures are returned to a specific set of indicators and/or content areas (union).

### Format:
```
ephtracking.cdc.gov/apigateway/api/v1/searchMeasureByTemporalItems/{{temporalTypeId}}/{{temporalItemIdFilter}}
[?contentAreaIdFilter][&indicatorIdFilter][&apiToken]
```

### Example
View measures that have data available for the months of January and February in the year 2014 for the Stroke Systems of Care: Pre-hospital Policy Interventions indicators.

### Parameters
temporalTypeId = 4
temporalItemIdFilter = 201401, 201402
contentAreaIdFilter = Null
indicatorIdFilter = 169

#### GET Request
https://ephtracking.cdc.gov/apigateway/api/v1/searchMeasureByTemporalItems/4/201401,201402?indicatorIdFilter=169

### Notes:
- Using the optional contentAreaIdFilter or indicatorIdFilter will speed up the query.


## Search Measure by Geographic Items Examples
You may want to query for measures that have data available for all entries in a set of geographic items. Optionally, limit what measures are returned to a specific set of indicators and/or content areas (Union).

### Format:
ephtracking.cdc.gov/apigateway/api/v1/searchGeographicItems/{{geographicTypeId}}/{{geographicItemIdFilter}}
[?contentAreaIdFilter][&indicatorIdFilter][&apiToken]

### Example A
View measures that have data available for the states of California and Ohio.

#### Parameters A
geographicTypeId = 1
geographicItemIdFilter = 06, 39
contentAreaIdFilter = Null
indicatorIdFilter = Null

#### GET Request
https://ephtracking.cdc.gov/apigateway/api/v1/searchMeasureByGeographicItems/1/06,39

### Example B
View measures that have data available for Los Angeles County in the Air Quality content area.

#### Parameters B
geographicTypeId = 2
geographicItemIdFilter = 6037
contentAreaIdFilter = 11
indicatorIdFilter = Null

#### GET Request
https://ephtracking.cdc.gov/apigateway/apiv1/searchMeasureByGeographicItems/2/6037?contentAreaIdFilter=11

### Example C
View measures that have data available for the state of Georgia in both the Air Quality content area and the Incidence of Leukemia indicators.

#### Parameters C
geographicTypeId = 1
geographicItemIdFilter = 13
contentAreaIdFilter = 11
indicatorIdFilter = 20

#### GET Request
https://ephtracking.cdc.gov/apigateway/apiv1/searchMeasureByGeographicItems/1/13?contentAreaIdFilter=11&indicatorIdFilter=20

### Notes:
- Using the optional contentAreaIdFilter or indicatorIdFilter will speed up the query

## Search Temporal Items by Measure Examples
You may want to query which temporal items have data available for all entries in a set of measures. Optionally, filter by the parentTemporalId to limit the returned temporal items to a specific year.

### Format:
ephtracking.cdc.gov/apigateway/api/v1/searchTemporalItemsByMeasure/{{temporalTypeId}}/{{measureIdFilter}}
[?parentTemporalId][&apiToken]

### Example

View year temporals available for the "Percent of Cancer Risk Estimates by Source" measure.

#### Parameters
temporalTypeId = 1
measureIdFilter = 479
parentTemporalId = Null

#### GET Request
https://ephtracking.cdc.gov/apigateway/api/v1/searchTemporalItemsByMeasure/1/479,480

### Notes:
- Minimum temporal IDs are populated in multiyear or weekly measures.

# Schemas
The following section defines the schema of the return type for each currently available call to the Tracking Network’s API. The glossary
contains definitions of the parameters. Click the parameters to jump to the appropriate glossary section.

## Content Areas Schema
```
{{
    "type": "array,
    "items": {{
        "type": "object",
        "properties": {{
            "id": {{
                "type": "integer"
            }},
            "name": {{
                "type": "integer"
            }},
            "shortName": {{
                "type": "string"
            }}
        }}
    }}
}}
```

## Indicators Schema
```
{{
    "type": "array,
    "items": {{
        "type": "object",
        "properties": {{
            "id": {{
                "type": "integer"
            }},
            "name": {{
                "type": "integer"
            }},
            "shortName": {{
                "type": "string"
            }},
            "externalURL": {{
                "type": "integer"
            }},
            "externalURLText": {{
                "type": "string"
            }}
        }}
    }}
}}
```


## Measures Schema
```
{{
    "type": "array,
    "items": {{
        "type": "object",
        "properties": {{
            "id": {{
                "type": "integer"
            }},
            "name": {{
                "type": "integer"
            }},
            "shortName": {{
                "type": "string"
            }},
            "externalURL": {{
                "type": "integer"
            }},
            "externalURLText": {{
                "type": "string"
            }}
        }}
    }}
}}
```


## Geographic Types Schema
```
{{
    "type": "array,
    "items": {{
        "type": "object",
        "properties": {{
            "id": {{
                "type": "integer"
            }},
            "geographicTypeId": {{
                "type": "integer"
            }},
            "geographicType": {{
                "type": "string"
            }},
            "selectOptionsTypeId": {{
                "type": "integer"
            }},
            "selectOptionsType": {{
                "type": "string"
            }},
            "smoothingLevelId": {{
                "type": "integer"
            }},
            "smoothingLevel": {{
                "type": "string"
            }}
        }}
    }}
}}
```

## Stratification Types Schema
```
{{
    "type": "array,
    "items": {{
        "type": "object",
        "properties": {{
            "displayName": {{
                "type": "string"
            }},
            "isDisplayed": {{
                "type": "boolean"
            }},
            "isRequired": {{
                "type": "boolean"
            }},
            "isGrouped": {{
                "type": "boolean"
            }},
            "displayAllValues": {{
                "type": "boolean"
            }},
            "selectOneItem": {{
                "type": "boolean"
            }},
            "stratificationItem": {{
                "type": "array,
                "items": {{
                    "type": "object",
                    "properties": {{
                        "name": {{
                            "type": "string"
                        }},
                        "longName": {{
                            "type": "string"
                        }},
                        "isDefault": {{
                            "type": "boolean"
                        }},
                        "useLongName": {{
                            "type": "boolean"
                        }},
                        "localId": {{
                            "type": "integer"
                        }}
                    }}
                }}
            }}
        }}
    }}
}}
```

## Stratification Level Schema
```
{{
    "type": "array,
    "items": {{
        "type": "object",
        "properties": {{
            "id": {{
                "type": "integer"
            }},
            "name": {{
                "type": "string"
            }},
            "abbreviation": {{
                "type": "string"
            }},
            "geographicTypeId": {{
                "type": "string"
            }},
            "stratificationType": {{
                "type": "array,
                "items": {{
                    "type": "object",
                    "properties": {{
                        "id": {{
                            "type": "integer"
                        }},
                        "name": {{
                            "type": "string"
                        }},
                        "abbreviation": {{
                            "type": "string"
                        }},
                        "columnName": {{
                            "type": "string"
                        }}
                    }}
                }}
            }}
        }}
    }}
}}
```

## Geographyic Items Schema
```
{{
    "type": "array,
    "items": {{
        "type": "object",
        "properties": {{
            "parentGeographicId": {{
                "type": "integer"
            }},
            "parentName": {{
                "type": "string"
            }},
            "parentAbbreviation": {{
                "type": "string"
            }},
            "childGeographicId": {{
                "type": "string"
            }},
            "childName": {{
                "type": "string"
            }},
            "childAbbreviation": {{
                "type": "string"
            }},
            "id": {{
                "type": "integer"
            }}
        }}
    }}
}}
```

## Temporal Items Schema
```
{{
    "type": "array,
    "items": {{
        "type": "object",
        "properties": {{
            "id": {{
                "type": "integer"
            }},
            "parentTemporalId": {{
                "type": "integer"
            }},
            "parentTemporal": {{
                "type": "string"
            }},
            "parentMinimumTemporalId": {{
                "type": "integer"
            }},
            "parentTemporalTypeId": {{
                "type": "integer"
            }},
            "parentTemporalType": {{
                "type": "string"
            }},
            "temporalId": {{
                "type": "integer"
            }},
            "minimumTemporalId": {{
                "type": "integer"
            }},
            "minimumTemporal": {{
                "type": "integer"
            }},
            "temporal": {{
                "type": "string"
            }},
            "temporalTypeId": {{
                "type": "integer"
            }},
            "temporalType": {{
                "type": "string"
            }},
            "parentTemporalDisplay": {{
                "type": "string"
            }},
            "temporalDescription": {{
                "type": "string"
            }},
            "temporalColumnName": {{
                "type": "string"
            }}
        }}
    }}
}}
```

## Core Holder Schema
```
{{
    "type": "object",
    "properties": {{
        "legendResult": {{
            "type": "array",
            "items": {{ }}
            "dataClassificationType": {{
                "type": "null",
                "tableResultClass": {{
                    "type": "string"
                }},
                "tableReturnType": {{
                    "type": "string"
                }},
                "tableResult": {{
                    "type": "array",
                    "items": {{
                        "type" : "object",
                        "properties": {{
                            "id": {{
                                "type": "string"
                            }},
                            "dataValue": {{
                                "type": "string"
                            }},
                            "displayValue": {{
                                "type": "string"
                            }},
                            "year": {{
                                "type": "string"
                            }},
                            "temporalTypeId": {{
                                "type": "integer"
                            }},
                            "temporal": {{
                                "type": "string"
                            }},
                            "temporalDescription": {{
                                "type": "string"
                            }},
                            "temporalColumnName": {{
                                "type": "string"
                            }},
                            "temporalRollingColumnName": {{
                                "type": "string"
                            }},
                            "temporalId": {{
                                "type": "integer"
                            }},
                            "minimumTemporal": {{
                                "type": "string"
                            }},
                            "minimumTemporalId": {{
                                "type": "integer"
                            }},
                            "parentTemporalTypeId": {{
                                "type": "integer"
                            }},
                            "parentTemporalType": {{
                                "type": "string"
                            }},
                            "parentTemporal": {{
                                "type": "string"
                            }},
                            "parentTemporalId": {{
                                "type": "integer"
                            }},
                            "groupById": {{
                                "type": "string"
                            }},
                            "geographicTyped": {{
                                "type": "integer"
                            }},
                            "calculationType": {{
                                "type": "string"
                            }},
                            "noDataId": {{
                                "type": "intenger"
                            }},
                            "hatchingId": {{
                                "type": "intenger"
                            }},
                            "hatching": {{
                                "type": "null"
                            }},
                            "suppressionFlag": {{
                                "type": "string"
                            }},
                            "noDataBreakGroup": {{
                                "type": "intenger"
                            }},
                            "confidenceIntervalLow": {{
                                "type": "null"
                            }},
                            "confidenceIntervalHigh": {{
                                "type": "null"
                            }},
                            "confidenceIntervalName": {{
                                "type": "null"
                            }},
                            "standardError": {{
                                "type": "null"
                            }},
                            "standardErrorName": {{
                                "type": "null"
                            }},
                            "secondaryValue": {{
                                "type": "null"
                            }},
                            "secondaryValueName": {{
                                "type": "null"
                            }},
                            "categoryId": {{
                                "type": "intenger"
                            }},
                            "category": {{
                                "type": "null"
                            }},
                            "categoryName": {{
                                "type": "null"
                            }},
                            "title": {{
                                "type": "string"
                            }},
                            "rollover": {{
                                "type": "array",
                                "items": {{
                                    "type": "string"
                                }}
                            }},
                            "confidenceIntervalHighName": {{
                                "type": "string"
                            }},
                            "confidenceIntervalDisplay": {{
                                "type": "string"
                            }},
                            "standardErrorDisplay": {{
                                "type": "string"
                            }},
                            "secondaryValueDisplay": {{
                                "type": "string"
                            }},
                            "confidenceIntervalLowName": {{
                                "type": "string"
                            }},
                            "parentGeoId": {{
                                "type": "integer"
                            }},
                            "geo": {{
                                "type": "string"
                            }},
                            "geoId": {{
                                "type": "string"
                            }},
                            "parentGeo": {{
                                "type": "string"
                            }},
                            "geoAbbreviation": {{
                                "type": "string"
                            }},
                            "parentGeoAbbreviation": {{
                                "type": "string"
                            }}
                        }}
                    }}
                }}
            }}
        }}
    }}
}}
```

## Benchmark Information Schema
```
{{
    "type": "object",
    "properties": {{
        "id": {{
            "type": "intenger"
        }},
        "measureId": {{
            "type": "intenger"
        }},
        "benchmarkId": {{
            "type": "intenger"
        }},
        "measureGeographicTypeId": {{
            "type": "intenger"
        }},
        "units": {{
            "type": "null"
        }},
        "geographicDisplay": {{
            "type": "string"
        }},
        "benchmarkName": {{
            "type": "string"
        }},
        "benchmarkShortName": {{
            "type": "string"
        }},
        "multipleSelectionActionId": {{
            "type": "intenger"
        }},
        "multipleSelectionAction": {{
            "type": "string"
        }},
        "active": {{
            "type": "boolean"
        }},
        "hasMap": {{
            "type": "boolean"
        }},
        "hasTable": {{
            "type": "boolean"
        }},
        "hasChart": {{
            "type": "boolean"
        }},
        "title": {{
            "type": "string"
        }},
        "benchmarkFullName": {{
            "type": "string"
        }},
        "geographicTypeDisplay": {{
            "type": "string"
        }},
        "benchmarkResult": {{
            "type": "array",
            "items": {{
                "type": "object",
                "properties": {{
                    "id": {{
                        "type": "string"
                    }},
                    "dataValue": {{
                        "type": "string"
                    }},
                    "displayValue": {{
                        "type": "string"
                    }},
                    "year": {{
                        "type": "string"
                    }},
                    "groupById": {{
                        "type": "string"
                    }},
                    "geographicTypeId": {{
                        "type": "intenger"
                    }},
                    "calculationType": {{
                        "type": "null"
                    }},
                    "rollover": {{
                        "type": "array",
                        "items": {{
                            "type": "string"
                        }}
                    }},
                    "parentGeoId": {{
                        "type": "null"
                    }},
                    "geo": {{
                        "type": "null"
                    }},
                    "geoId": {{
                        "type": "null"
                    }},
                    "parentGeo": {{
                        "type": "null"
                    }},
                    "geoAbbreviation": {{
                        "type": "null"
                    }},
                    "parentGeoAbbreviation": {{
                        "type": "null"
                    }}
                }}
            }}
        }},
        "standard": {{
            "type": "array",
            "items": {{ }}
        }},
        "aggregateResult": {{
            "type": "null",
        }},
        "lookupList": {{
            "type": "array",
            "items": {{
                "type": "map",
                "entries": {{
                    "entries": {{
                        "key": {{
                            "groupById": {{
                                "type": "integer"
                            }},
                            "value": {{
                                "type": "object",
                                "properties": {{
                                    "columnName": {{
                                        "type": "string"
                                    }},
                                    "itemName": {{
                                        "type": "string"
                                    }},
                                    "localId": {{
                                        "type": "integer"
                                    }},
                                    "uid": {{
                                        "type": "null"
                                    }},
                                    "stratificationTypeId": {{
                                        "type": "integer"
                                    }},
                                    "name": {{
                                        "type": "string"
                                    }}
                                }}
                            }}
                        }}
                    }}
                }}
            }}
        }},
        "measureInformationDTO": {{
            "type": "object",
            "properties": {{ }}
        }},
        "measureStratificationLevel": {{
            "type": "object",
            "properties": {{ }}
        }},
        "publicAPIUrl": {{
            "type": "string"
        }},
        "publicAPIServerUrl": {{
            "type": "string"
        }},
        "fullPublicAPIUrl": {{
            "type": "string"
        }}
    }}
}}
```

## Measure Search Schema
```
{{
    "type": "array",
    "items": {{
        "type": "object",
        "properties": {{
            "contentAreaId": {{
                "type": "integer"
            }},
            "contentAreaName": {{
                "type": "string"
            }},
            "indicatorId": {{
                "type": "integer"
            }},
            "indicatorName": {{
                "type": "string"
            }},
            "measureId": {{
                "type": "integer"
            }},
            "measureName": {{
                "type": "string"
            }},
            "indicatorStatusId": {{
                "type": "integer"
            }},
            "contentAreaStatusId": {{
                "type": "integer"
            }},
            "keywords": {{
                "type": "string"
            }}
        }}
    }}
}}
```

## All Temporal Types Schema
```
{{
    "type": "array",
    "items": {{
        "type": "object",
        "properties": {{
            "temporalTypeId": {{
                "type": "integer"
            }},
            "name": {{
                "type": "string"
            }},
            "parentTemporalTypeId": {{
                "type": "integer"
            }}
        }}
    }}
}}
```

## All Geographic Types Schema
```
{{
    "type": "array",
    "items": {{
        "type": "object",
        "properties": {{
            "geographicTypeId": {{
                "type": "integer"
            }},
            "name": {{
                "type": "string"
            }},
            "abbreviation": {{
                "type": "string"
            }},
            "parentGeographicTypeId": {{
                "type": "integer"
            }}
        }}
    }}
}}
```

## All Stratification Types Schema
```
{{
    "type": "array",
    "items": {{
        "type": "object",
        "properties": {{
            "id": {{
                "type": "integer"
            }},
            "name": {{
                "type": "string"
            }},
            "abbreviation": {{
                "type": "string"
            }},
            "columnName": {{
                "type": "string"
            }}
        }}
    }}
}}
```

## All Stratification Levels Schema
```
{{
    "type": "array",
    "items": {{
        "type": "object",
        "properties": {{
            "id": {{
                "type": "integer"
            }},
            "name": {{
                "type": "string"
            }},
            "abbreviation": {{
                "type": "string"
            }}
        }}
    }}
}}
```

## Search Measure by Temporal Items Schema
```
{{
    "type": "array",
    "items": {{
        "type": "object",
        "properties": {{
            "id": {{
                "type": "integer"
            }},
            "name": {{
                "type": "string"
            }},
            "shortName": {{
                "type": "string"
            }}
        }}
    }}
}}
```

## Search Measure by Geographic Items Schema
```
{{
    "type": "array",
    "items": {{
        "type": "object",
        "properties": {{
            "id": {{
                "type": "integer"
            }},
            "name": {{
                "type": "string"
            }},
            "shortName": {{
                "type": "string"
            }}
        }}
    }}
}}
```

## Search Temporal Items by Measure Schema
```
{{
    "type": "array",
    "items": {{
        "type": "object",
        "properties": {{
            "id": {{
                "type": "integer"
            }},
            "parentTemporalId": {{
                "type": "integer"
            }},
            "parentTemporal": {{
                "type": "string"
            }},
            "parentMinimumTemporalId": {{
                "type": "integer"
            }},
            "parentTemporalTypeId": {{
                "type": "integer"
            }},
            "parentTemporalType": {{
                "type": "string"
            }},
            "temporalId": {{
                "type": "integer"
            }},
            "minimumTemporalId": {{
                "type": "integer"
            }},
            "minimumTemporal": {{
                "type": "integer"
            }},
            "temporal": {{
                "type": "string"
            }},
            "temporalTypeId": {{
                "type": "integer"
            }},
            "temporalType": {{
                "type": "string"
            }},
            "parentTemporalDisplay": {{
                "type": "string"
            }}
        }}
    }}
    }}
}}
```

## Search Geographic Items by Measure Schema
```
{{
    "type": "array",
    "items": {{
        "type": "object",
        "properties": {{
            "parentGeographicId": {{
                "type": "integer"
            }},
            "parentName": {{
                "type": "string"
            }},
            "parentAbbreviation": {{
                "type": "string"
            }},
            "childGeographicId": {{
                "type": "string"
            }},
            "childName": {{
                "type": "string"
            }},
            "childAbbreviation": {{
                "type": "string"
            }},
            "id": {{
                "type": "integer"
            }}
        }}
    }}
}}
```