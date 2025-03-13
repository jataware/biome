# Drug Adverse Event Overview
The openFDA drug adverse event API returns data that has been collected from the FDA Adverse Event Reporting System (FAERS), a database that contains information on adverse event and medication error reports submitted to FDA.

An adverse event is submitted to the FDA to report any undesirable experience associated with the use of a medical product in a patient. For drugs, this includes serious drug side effects, product use errors, product quality problems, and therapeutic failures for prescription or over-the-counter medicines and medicines administered to hospital patients or at outpatient infusion centers.

Adverse event reports use the ICH E2b/M2 version 2.1 standard.

# About the openFDA API

openFDA is an Elasticsearch-based API that serves public FDA data about nouns like drugs, devices, and foods.

Each of these nouns has one or more categories, which serve unique data-such as data about recall enforcement reports, or about adverse events. Every query to the API must go through one endpoint for one kind of data.

Not all data in openFDA has been validated for clinical or production use. And because openFDA only serves publicly available data, it does not contain data with Personally Identifiable Information about patients or other sensitive information.

"API" is an acronym for Application Programming Interface. An API call is any request sent to the API. Requests are typically sent to the API in one of two ways: 1. Manually using a web browser (such as navigating to the URL https://api.fda.gov/drug/label.json) or 2. Programmatically sending the request via executing code that sends the API call and processes the response. Continue reading this documentation for more details on how to compose an API call for openFDA specifically.

The API returns individual results as JSON by default. The JSON object has two sections:

- meta: Metadata about the query, including a disclaimer, link to data license, last-updated date, and total matching records, if applicable.
- results: An array of matching results, dependent on which endpoint was queried.

Your API key should be passed to the API as the value of the api_key parameter. Include it before other parameters, such as the search parameter. For example:

https://api.fda.gov/drug/event.json?api_key=yourAPIKeyHere&search=...

In the example below, we are searching the records in the drug adverse events endpoint for matches with headache in the reactionmeddrapt field. We are requesting to see the first 5 records that match."

https://api.fda.gov/drug/event.json?search=reactionmeddrapt:"headache"&limit=5&api_key=<api_key>

## Some key pointers
An openFDA API query always begins with the base endpoint, which in this case is: https://api.fda.gov/drug/event.json
Searches have a special syntax: search=field:term
Unless otherwise specified, the API will return only one matching record for a search. You can specify the number of records to be returned by using the limit parameter. The maximum limit allowed is 1000 for any single API call. If no limit is set, the API will return one matching record.

It is possible to construct very complex queries using the openFDA API. Review the "Construct the query" documentation to learn more about all the available query parameters, how to handle quotations, spaces, phrase matches, and groupings, how to search on dates and ranges, and more.

Example drug labeling API queries
To help get you started, we have provided some API query examples below. Use the Run query button to call the API and get back results. You can experiment by editing the example queries in the black text box.

## Example query

### One adverse event report (from drug labeling)
This query searches for all records in a certain date range, and asks for a single one. See the header fields reference for more about receivedate. Brackets [ ] are used to specify a range for date, number, or string fields.

- search for all records with receivedate between Jan 01, 2004 and Dec 31, 2008. limit to 1 record.
- see searchable fields for more about receivedate. Brackets [ ] are used to specify a range for date, number, or string fields:

```
https://api.fda.gov/drug/event.json?search=receivedate:[20040101+TO+20081231]&limit=1
```

## Example query

### One adverse event report with a drug from a certain pharmacologic class

This query searches records listing a drug of a certain pharmacologic class, and returns a single record. A record returned by this query may have multiple drugs listed. At least one of the drugs belongs to the pharmacologic class. See the openFDA fields reference for more about the kinds of searches they enable. Double quotation marks " " surround phrases that must match exactly. The plus sign + is used in place of a space character  .

A record returned by this query may have multiple drugs listed. At least one of the drugs belongs to the pharmacologic class. See searchable fields for more about the kinds of searches they enable.

Double quotation marks " " surround phrases that must match exactly. The plus sign + is used in place of a space character.

- search for all records with receivedate between Jan 01, 2004 and Dec 31, 2008. limit to 1 record.
- see searchable fields for more about receivedate. Brackets [ ] are used to specify a range for date, number, or string fields.

```
https://api.fda.gov/drug/event.json?search=patient.drug.openfda.pharm_class_epc:"nonsteroidal+anti-inflammatory+drug"&limit=1
```

## Example query

### Count of patient reactions

This query is similar to the prior one, but returns a count of the 1000 most frequently reported patient reactions. Multiple drugs in the records may match this class, and the drugs from this class may not be those which caused the associated adverse patient reactions. The suffix .exact is required by openFDA to count the unique full phrases in the field patient.reaction.reactionmeddrapt. Without it, the API will count each word in that field individually—difficulty sleeping would be counted as separate values, difficulty and sleeping. See the patient reaction reference for more about patient reactions in adverse event records.

The suffix .exact is required by openFDA to count the unique full phrases in the field patient.reaction.reactionmeddrapt. Without it, the API will count each word in that field individually—difficulty sleeping would be counted as separate values, difficulty and sleeping.
- search for all records with receivedate between Jan 01, 2004 and Dec 31, 2008. limit to 1 record.
- see searchable fields for more about receivedate. Brackets [ ] are used to specify a range for date, number, or string fields

Query:

```
https://api.fda.gov/drug/event.json?search=patient.drug.openfda.pharm_class_epc:"nonsteroidal+anti-inflammatory+drug"&count=patient.reaction.reactionmeddrapt.exact
```

## Understanding the API Results

For search queries (such as: https://api.fda.gov/drug/event.json?search=receivedate:[20040101+TO+20081231]&limit=1), the results section includes matching adverse event reports returned by the API.

### Each adverse event report consists of these major sections:

- Header: General information about the adverse event.
- Patient Information: Details on the patient who experienced the event, such as age, weight, sex, etc.
- Drugs: Information on the drugs taken while the event was experienced.
- Reactions: Information on the reactions experienced by the patient.
The order of these fields in the results can and will vary...

For count queries (such as: https://api.fda.gov/drug/event.json?count=patient.reaction.reactionmeddrapt.exact), the results section will look something like the following:

```
{
  "results": [
    {
      "term": "DRUG INEFFECTIVE",
      "count": 32584
    },
    {
      "term": "NAUSEA",
      "count": 27541
    },
    {
      "term": "FATIGUE",
      "count": 23341
    }
  ]
}
```


# Download API fields Example
```
{
  "meta": {
    "disclaimer": "openFDA is a beta research project and not for clinical use. While we make every effort to ensure that data is accurate, you should assume all results are unvalidated.",
    "license": "http://open.fda.gov/license",
    "last_updated": "2015-12-19"
  },
  "results": {
    "device": {
      "event": {
        "total_records": 33128,
        "export_date": "2015-12-19",
        "partitions": [
          {
            "size_mb": "0.56",
            "records": 795,
            "display_name": "2012 q2 (all)",
            "file": "http://download.open.fda.gov/device/event/2012q2/device-event-0001-of-0001.json.zip"
          },
          {
            "size_mb": "0.58",
            "records": 825,
            "display_name": "2012 q3 (all)",
            "file": "http://download.open.fda.gov/device/event/2012q3/device-event-0001-of-0001.json.zip"
          },
          {
            "…": "…"
          }
        ]
      }
    }
  }
}
```

# Construct Query Documentation

## Query parameters

The API supports five query parameters. The basic building block of queries is the search parameter. Use it to “filter” requests to the API by looking in specific fields for matches. Each endpoint has its own unique fields that can be searched.

- search: What to search for, in which fields. If you don’t specify a field to search, the API will search in every field.
- sort: Sort the results of the search by the specified field in ascending or descending order by using the :asc or :desc modifier.
- count: Count the number of unique values of a certain field, for all the records that matched the search parameter. By default, the API returns the 1000 most frequent values.
- limit: Return up to this number of records that match the search parameter. Currently, the largest allowed value for the limit parameter is 1000.
- skip: Skip this number of records that match the search parameter, then return the matching records that follow. Use in combination with limit to paginate results. Currently, the largest allowed value for the skip parameter is 25000. See Paging if you require paging through larger result sets.

## Query syntax

Queries to the openFDA API are made up of parameters joined by an ampersand &. Each parameter is followed by an equals sign = and an argument.

Searches have a special syntax: search=field:term. Note that there is only one equals sign = and there is a colon : between the field to search, and the term to search for.

Here are a few syntax patterns that may help if you’re new to this API.

- search=field:term: Search within a specific field for a term.
- search=field:term+AND+field:term: Search for records that match both terms.
- search=field:term+field:term: Search for records that match either of two terms.
- sort=report_date:desc: Sort records by a specific field in descending order.
- search=field:term&count=another_field: Search for matching records. Then within that set of records, count the number of times that the unique values of a field appear. Instead of looking at individual records, you can use the count parameter to count how often certain terms (like drug names or patient reactions) appear in the matching set of records.

Here are some example queries that demonstrate how these searches and the count parameter work, all using the drug adverse events endpoint:

### Example query

#### Matching all search terms

This query looks in the drug/event endpoint for a record where both fatigue was a reported patient reaction and the country in which the event happened was Canada. The key here is the +AND+ that joins the two search terms.

- Search for records where the field patient.reaction.reactionmeddrapt (patient reaction) contains fatigue and occurcountry (country where the event happened) was ca (the country code for Canada):

```
https://api.fda.gov/drug/event.json?search=patient.reaction.reactionmeddrapt:"fatigue"+AND+occurcountry:"ca"&limit=1
```

### Example query

#### Matching any search terms

This query looks in the drug/event endpoint for a record where either fatigue was a reported patient reaction or the country in which the event happened was Canada.

- Search for records where the field patient.reaction.reactionmeddrapt (patient reaction) contains fatigue or occurcountry (country where the event happened) was ca (the country code for Canada)

```
https://api.fda.gov/drug/event.json?search=patient.reaction.reactionmeddrapt:"fatigue"+occurcountry:"ca"&limit=1
```

### Example query

#### Counting records where certain terms occur

This query looks in the drug/event endpoint for all records. It then returns a count of the top patient reactions. For each reaction, the number of records that matched is summed, providing a useful summary.

- Search for all records

- Count the number of records matching the terms in patient.reaction.reactionmeddrapt.exact. The .exact suffix here tells the API to count whole phrases (e.g. injection site reaction) instead of individual words (e.g. injection, site, and reaction separately):

```
https://api.fda.gov/drug/event.json?count=patient.reaction.reactionmeddrapt.exact
```

## Advanced syntax

### Spaces
Queries use the plus sign + in place of the space character. Wherever you would use a space character, use a plus sign instead.

### Phrase matches
For phrase matches, use double quotation marks " " around the words. For example, "multiple+myeloma".

### Grouping
To group several terms together, use parentheses ( ). For example, patient.drug.medicinalproduct:(cetirizine+OR+loratadine+OR+diphenhydramine). To join terms as in a boolean AND, use the term +AND+. For example, (patient.drug.medicinalproduct:(cetirizine+OR+loratadine+OR+diphenhydramine))+AND+serious:2 requires that any of the drug names match and that the field serious also match.

## Wildcard search
Wildcard queries return data that contain terms matching a wildcard pattern.

A wildcard operator is a placeholder that matches one or more characters. At this point, openFDA supports the * ("star") wildcard operator, which matches zero or more characters. You can combine wildcard operators with other characters to create a wildcard pattern.

This feature is available on all API Endpoints.

Here are some example queries that demonstrate how wildcard searches work.

### Example query

#### Wildcard search against a regular field, case insensitive

This example query looks in the drug/ndc endpoint for drugs where brand_name contains words that begin with child, case insensitive. This will include drugs with brand names that contain "Child", "Children", "Childrens" among others.

- Search for records where the field brand_name contains child*, case-insensitive

```
https://api.fda.gov/drug/ndc.json?search=brand_name:child*&limit=10
```

## Dates and ranges
The openFDA API supports searching by range in date, numeric, or string fields.

- Specify an inclusive range by using square brackets [min+TO+max]. These include the values in the range. For example, [1+TO+5] will match 1 through 5.
- Dates are simple to search by via range. For instance, [2004-01-01+TO+2005-01-01] will search for records between Jan 1, 2004 and Jan 1, 2005.

## Missing (or not missing) values
\_missing\_: search modifier that matches when a field has no value (is empty).

\_exists\_: search modifier that matches when a field has a value (is not empty).

### Example query

#### Data is missing from a field

This query looks in the drug/event endpoint for records that are missing a company number, meaning that the report was submitted directly by a member of the public and not through a drug manufacturer.

- Search for records where the field companynumb is missing or empty

```
https://api.fda.gov/drug/event.json?search=_missing_:companynumb&limit=1
```

### Example query

#### Data in a field is present, regardless of the value

This query looks in the drug/event endpoint for records that have a company number, meaning that the report was submitted through a drug manufacturer.

- Search for records where the field companynumb has data in it

```
https://api.fda.gov/drug/event.json?search=_exists_:companynumb&limit=1
```

## Timeseries
The API supports count on date fields, which produces a timeseries at the granularity of day. The API returns a complete timeseries.

### Example query

#### Counting by date, returning a timeseries

This query looks in the drug/event endpoint for all records. It then returns a count of records per day, according to a certain date field (the receipt date of the adverse event report).

- Search for all records
- Count the number of records per day, according to the field receiptdate

```
https://api.fda.gov/drug/event.json?count=receiptdate
```


## Paging
openFDA is designed primarily for real-time queries. Using combinations of the skip/limit parameters you can page through a result set that has up to 26,000 hits. This limit is in place to protect openFDA infrastructure and is sufficient in most cases; however, sometimes it is desirable to navigate through a result set that exceeds 26,000 search matches. If you are unable to narrow your search criteria to decrease the number of hits, consider the following strategies to obtain data from large result sets:

### Search-After
Use the “Search After” feature that permits scrolling through a result set of unlimited size, up to the size of the dataset itself. The following are the basic steps you need to follow:

- Execute your initial query that produces a large number of matches. Make sure not to include the skip parameter, because skip and search_after do not work together (technical explanation is here). The initial query will return your first page of data. For example:

```
https://api.fda.gov/drug/event.json?search=patient.drug.openfda.product_type.exact:%22HUMAN%20PRESCRIPTION%20DRUG%22&limit=100&sort=receivedate:asc
```

- Extract the Link HTTP header contained in the response. Detailed information about the purpose and structure of the Link header can be found here. In short, this header will contain a rel="Next" URL representing the query you need to use to obtain the next page of data. Missing header indicates you are already on the last page. An example of extracting the header value using curl:

```
bash-3.2$ curl -sIg 'https://api.fda.gov/drug/event.json?search=patient.drug.openfda.product_type.exact:%22HUMAN%20PRESCRIPTION%20DRUG%22&limit=100&sort=receivedate:asc' | grep "Link: "
```
Link: <https://api.fda.gov/drug/event.json?search=patient.drug.openfda.product_type.exact%3A%22HUMAN%20PRESCRIPTION%20DRUG%22&limit=100&sort=receivedate%3Aasc&skip=0&search_after=0%3D1068076800000%3B1%3Dsafetyreport%25234022687>; rel="next"

- Use the extracted URL to obtain next page of data. Note it includes the search_after query parameter.
- Repeat the cycle until the Link header is no longer present in the response, which indicates you are on the last page.
