
# Daily Values Service Details

## How the service works 

The service can return daily values for one or more sites in one request
Data for historical, as well as currently active sites are available.

With hundreds of thousands of qualifying sites across the nation, the amount of data available is very large.
No one user is allowed to download all of the data with a single call.
The service has consequently been engineered to facilitate common mass queries,
defaulting to returning a narrower set of data.
You are encouraged to make your queries efficient too, mindful that many others need 
access to the data at the same time. Always specify the minimum amount of data you need 
in your request, using built in filters and date ranges to the maximum extent possible.

## Enabling gzip compression 

If you can handle gzip compression, please place the following string into your HTTP request headers: Accept-Encoding: gzip, compress

## Output 

When using format=waterml (the default format), data are returned in XML using the WaterML 1.1 schema . WaterML is a schema that has recently been adopted by the Open Geospatial Consortium . The crucial data are the instantaneous values, which can be found inside the <value> tag, which is nested inside the <timeSeries> tag, such as in this example:

```
<ns1:values>
  <ns1:value qualifiers="P" dateTime="2011-05-02">14.8</ns1:value>
  <ns1:qualifier qualifierID="0" ns1:network="NWIS" ns1:vocabulary="uv_rmk_cd">
    <ns1:qualifierCode>P</ns1:qualifierCode>
    <ns1:qualifierDescription>Provisional data subject to revision.</ns1:qualifierDescription>
  </ns1:qualifier>
  <ns1:method methodID="0">
    <ns1:methodDescription>sensor:null:7</ns1:methodDescription>
  </ns1:method>
</ns1:values>
```

By itself this imparts no information as to what the daily value represents, other than the statistic is provisional because qualifiers=“P”. We do know the value is 14.8 and it represents a daily value for May 2, 2011. We also need to know what was measured. The key to figuring this out is to examine the outer <timeSeries> tag, which contains some important information, shown below in bold:


```
<ns1:timeSeries name="USGS:01646500:00010:00002">
...
</ns1:timeSeries>
```

The name attribute contains a sequence of useful information with key fields delimited by colons. The pattern is <agencyCd>:<siteNo>:<parameterCd>:<statisticsCd>.

So this node contains data about site number 01646500 (Little Falls Pumping Station on the Potomac River) monitored by the USGS. Specifically it has a calculated daily statistic for USGS parameter 00010, which is water temperature in degrees Celsius. How do we know this? It is made clear inside the <variable> node within the <timeSeries> node.

```
<ns1:variable ns1:oid="45807042">
  <ns1:variableCode network="NWIS" vocabulary="NWIS:UnitValues" default="true" variableID="45807042">00010</ns1:variableCode>
  <ns1:variableName>Temperature, water, &#176;C</ns1:variableName>
  <ns1:variableDescription>Temperature, water, degrees Celsius</ns1:variableDescription>
  <ns1:valueType>Derived Value</ns1:valueType>
  <ns1:unit>
    <ns1:unitAbbreviation>deg C</ns1:unitAbbreviation>
  </ns1:unit>
  <ns1:options>
    <ns1:option name="Statistic" optionCode="00002">Minimum</ns1:option>
  </ns1:options><ns1:noDataValue>-999999.0</ns1:noDataValue>
</ns1:variable>
```

Since a daily value is a computation of many regular timeseries measurements, the next question is what statistic is being measured? A mean temperature? Maximum temperature? Minimum temperature? The statistics code is 00002, which the <options> tag nested inside the <variable> tag tells us is minimum (see above).

Putting it altogether, this means that for this site, the provisional minimum water temperature on May 2, 2011 was 14.8 degrees Celsius, or about 59 degrees Fahrenheit.

With other output formats, the location of the data will depend on the syntax of the format. You will need to inspect the format to locate the relevant data.


## Error Codes

Since this system uses Hypertext Transfer Protocol (HTTP), any application errors are reported in the HTTP headers.

200	OK	The request was successfully executed and some data should have been returned.

400	Bad_Request	This often occurs if the URL arguments are inconsistent. An accompanying error should describe why the request was bad. Reasons include:
Using startDT and endDT with the period argument.
Mixing startDt and endDt arguments where startDt includes a time zone and endDt does not

304	Not_Modified	This indicates your request was redirected using the proper URL. This may occur if the "path" of your URL is not fully qualified. Ideally a / is placed before the ? in the URL. Adding in this slash may make this go away. However, the request should still be processed. If this becomes annoying, you may also be able to tell your client program to automatically follow redirects.

403	Access_Forbidden	This should only occur if for some reason the USGS has blocked your Internet Protocol (IP) address from using the service. This can happen if we believe that your use of the service is so excessive that it is seriously impacting others using the service. To get unblocked, send us the URL you are using along with your client's IP using this form. We may require changes to your query and frequency of use in order to give you access to the service again.

404	Not_Found	Returned if and only if the query expresses a combination of elements where data do not exist. For multi-site queries, if any data are found, it is returned for those site/parameters/date ranges where there are data. Conditions that would return a 404 Not Found include:
The site number(s) are invalid
The site number(s) exists but they do not serve time-series data
The site number(s) are valid but the requested parameter(s) are not served for these sites
No values exist for the requested date range. For example, a gage might be down for a period of time due to storm damage when it would normally have data.

## URL Format 

The URL must always be in this format:

```
https://waterservices.usgs.gov/nwis/dv/?<arguments>
```

where <arguments> are one or more HTTP GET parameter names and values based on the information below.

## Specifying the URL Arguments

You specify the arguments that go in <arguments>.

- Each URL argument name is followed by an equal sign followed by one or more values for that argument. 
- Where multiple values are allowed for the same argument, you can separate values with commas.
- URL arguments are separated by ampersands (&)
- The order of the URL arguments does not matter
- If a URL argument name does not match one of the names below, a HTTP 400 error code is returned

Here is an example of a valid URL that should return data:

- https://waterservices.usgs.gov/nwis/dv/?site=01646500

URL argument names and argument values can be in upper, lower or mixed case. They will all be handled correctly. All of the following will yield the same result:

- https://waterservices.usgs.gov/nwis/dv/?stateCd=ny
- https://waterservices.usgs.gov/nwis/dv/?statecd=ny
- https://waterservices.usgs.gov/nwis/dv/?STATECD=ny
- https://waterservices.usgs.gov/nwis/dv/?stateCd=NY
- https://waterservices.usgs.gov/nwis/dv/?STATECD=NY
- https://waterservices.usgs.gov/nwis/dv/?stateCd=Ny

## URL argument conventions

The following conventions are used below to document URL argument values:

```
arg1=[ a {,x | ,y} | b | c,d,...]
```

- square brackets [] are used to show a set of possible choices, with the pipe symbol | delineating exclusive choices. You must select one and only one of these choices.
- curved brackets {} are used to show optional elements. They also may be delineated with | indicating exclusive choices. If used, you may select one and only one of these choices.
- ... indicates more than item may be specified if items are delineated by commas. Note the limitation on the maximum number of argument values allowed below.

In the above example, these would be the allowed legal values:

- arg1=a
- arg1=a,x
- arg1=a,y
- arg1=b
- arg1=c
- arg1=c,d
- arg1=c,d,e,f
- arg1=e,f

## Major Filters

### Single Site Queries

Want to only query one site? Use site (or sites) as your major filter, and put only one site number in the list! Example:

```
https://waterservices.usgs.gov/nwis/dv/?site=01646500
```

### Multiple Site Queries

- Every multiple site query requires a major filter. Pick the major filter (sites, stateCd, huc, bBox or counties) that best retrieves the data for the sites that you are interested in.
- Further refine the query with minor filters, if needed.

Major Filter

(select one of the following)

Meaning	Minimum Number of Argument Values	Maximum Number of Argument Values	Examples
sites(aliases: site, location)	A list of site numbers. You can specify unlimited sites, up to any limit imposed by the application server or your client. Sites are comma separated. Sites may be prefixed with an optional agency code followed by a colon. If you don't know the site numbers you need, you can find relevant sites with the NWIS Mapper or on the USGS Water Data for the Nation site.	1	Unlimited (see caveat)	&site=01646500
&sites=USGS:01646500
&sites=01646500,06306300
stateCd
(alias: stateCds)	U.S. postal service (2-digit) state code. USPS List of State Codes.	1	1	&stateCd=NY
huc
(alias: hucs)	A list of hydrologic unit codes (HUC) or aggregated watersheds. Only 1 major HUC can be specified per request. A major HUC has two digits. Minor HUCs must be eight digits in length. Not all sites are associated with a HUC. List of HUCs.	1	1 Major, 10 Minor	&huc=01,02070010
bBox	A contiguous range of decimal latitude and longitude, starting with the west longitude, then the south latitude, then the east longitude, and then the north latitude with each value separated by a comma. The product of the range of latitude and longitude cannot exceed 25 degrees. Whole or decimal degrees must be specified, up to six digits of precision. Minutes and seconds are not allowed. Remember: western longitude (which includes almost all of the United States) is specified in negative degrees. Caution: many sites outside the continental US do not have latitude and longitude referenced to NAD83 and therefore can not be found using these arguments. Certain sites are not associated with latitude and longitude due to homeland security concerns and cannot be found using this filter.	1	1	&bBox=-83,36.5,-81,38.5
countyCd
(alias: countyCds)	A list of county numbers, in a 5 digit numeric format. The first two digits of a county's code are the FIPS State Code. List of county codes. Some updates were made to the FIPS code standards in 2021. NIST has provided replacement standards.	1	20	&countyCd=51059,51061

### FIPS State Codes

Alabama	AL	01	State; counties
Alaska	AK	02	State; boroughs
American Samoa	AS	60	Outlying area under U.S. sovereignty
American Samoa *		03	(FIPS 5-1 reserved code)
Arizona	AZ	04	State; counties
Arkansas	AR	05	State; counties
Baker Island		81	Minor outlying island territory
California	CA	06	State; counties
Canal Zone *		07	(FIPS 5-1 reserved code)
Colorado	CO	08	State; counties
Connecticut	CT	09	State; counties
Delaware	DE	10	State; counties
District of Columbia	DC	11	Federal district[4]
Florida	FL	12	State; counties
Federated States of Micronesia	FM	64	Freely Associated State
Georgia	GA	13	State; counties
Guam *		14	(FIPS 5-1 reserved code)
Guam	GU	66	Outlying area under U.S. sovereignty
Hawaii	HI	15	State; counties
Howland Island		84	Minor outlying island territory
Idaho	ID	16	State; counties
Illinois	IL	17	State; counties
Indiana	IN	18	State; counties
Iowa	IA	19	State; counties
Jarvis Island		86	Minor outlying island territory
Johnston Atoll		67	Minor outlying island territory
Kansas	KS	20	State; counties
Kentucky	KY	21	State; counties
Kingman Reef		89	Minor outlying island territory
Louisiana	LA	22	State; parishes
Maine	ME	23	State; counties
Marshall Islands	MH	68	Freely Associated State
Maryland	MD	24	State; counties
Massachusetts	MA	25	State; counties
Michigan	MI	26	State; counties
Midway Islands		71	Minor outlying island territory
Minnesota	MN	27	State; counties
Mississippi	MS	28	State; counties
Missouri	MO	29	State; counties
Montana	MT	30	State; counties
Navassa Island		76	Minor outlying island territory
Nebraska	NE	31	State; counties
Nevada	NV	32	State; counties
New Hampshire	NH	33	State; counties
New Jersey	NJ	34	State; counties
New Mexico	NM	35	State; counties
New York	NY	36	State; counties
North Carolina	NC	37	State; counties
North Dakota	ND	38	State; counties
Northern Mariana Islands	MP	69	Outlying area under U.S. sovereignty
Ohio	OH	39	State; counties
Oklahoma	OK	40	State; counties
Oregon	OR	41	State; counties
Palau	PW	70	Freely Associated State
Palmyra Atoll		95	Minor outlying island territory
Pennsylvania	PA	42	State; counties
Puerto Rico *		43	(FIPS 5-1 reserved code)
Puerto Rico	PR	72	Outlying area under U.S. sovereignty
Rhode Island	RI	44	State; counties
South Carolina	SC	45	State; counties
South Dakota	SD	46	State; counties
Tennessee	TN	47	State; counties
Texas	TX	48	State; counties
U.S. Minor Outlying Islands	UM	74	Minor outlying island territories (aggregated)
Utah	UT	49	State; counties
Vermont	VT	50	State; counties
Virginia	VA	51	State; counties
Virgin Islands of the U.S. *		52	(FIPS 5-1 reserved code)
Virgin Islands of the U.S.	VI	78	Outlying area under U.S. sovereignty
Wake Island		79	Minor outlying island territory
Washington	WA	53	State; counties
West Virginia	WV	54	State; counties
Wisconsin	WI	55	State; counties
Wyoming	WY	56	State; counties

#### Statistics Codes (stat_cd)

Statistic Type Code	Statistic Type Name	Statistic Type Description
00001	MAXIMUM	MAXIMUM VALUES
00002	MINIMUM	MINIMUM VALUES
00003	MEAN	MEAN VALUES
00004	AM	VALUES TAKEN BETWEEN 0001 AND 1200
00005	PM	VALUES TAKEN BETWEEN 1201 AND 2400
00006	SUM	SUMMATION VALUES
00007	MODE	MODAL VALUES
00008	MEDIAN	MEDIAN VALUES
00009	STD	STANDARD DEVIATION VALUES
00010	VARIANCE	VARIANCE VALUES
00011	INSTANTANEOUS	RANDOM INSTANTANEOUS VALUES
00012	EQUIVALENT MEAN	EQUIVALENT MEAN VALUES
00013	SKEWNESS	SKEWNESS VALUES
01750	75.0 PERCENTILE	75.0 PERCENTILE
01900	90.0 PERCENTILE	90.0 PERCENTILE
01990	99.0 PERCENTILE	99.0 PERCENTILE
31655	OBSERVATION AT 1655	INSTANTANEOUS OBSERVATION AT 1655
31817	OBSERVATION AT 1817	INSTANTANEOUS OBSERVATION AT 1817

For percentile codes above, you'll see these start with a left padded 0, then a 1,
then the percentile value. For example, 01750 is 75.0 PERCENTILE.

Percentile codes are available and start from:
01001	0.1 PERCENTILE

and end at:
01999	99.9 PERCENTILE

Sample for observation codes, these range from:
30001	OBSERVATION AT 0001
to
32400	OBSERVATION AT 2400

#### Duration Codes

The API accepts ISO_8601 duration codes
Example: `P3Y6M4DT12H30M5S`

P is the duration designator (for period) placed at the start of the duration representation:
Y is the year designator that follows the value for the number of calendar years.
M is the month designator that follows the value for the number of calendar months.
W is the week designator that follows the value for the number of weeks.
D is the day designator that follows the value for the number of calendar days.

T is the time designator that precedes the time components of the representation:
H is the hour designator that follows the value for the number of hours.
M is the minute designator that follows the value for the number of minutes.
S is the second designator that follows the value for the number of seconds.

### Specifying Date Ranges

Many sites have periods of record that can be measured in decades, sometimes fifty years or more. Some sites have been measuring common parameters like streamflow continuously, others are seasonal in nature, and others have had periods when no funding was available to maintain the site so no data are available. Since daily values are by definition daily calculations, it makes no sense to request time periods in less than day increments. Please follow these rules for expressing dates with this service:

Table:

I want to...	Do this...	Syntax Rules	Examples

Get the latest daily values only	Nothing. Only the latest value is returned by default for each requested site, parameter and statistic.	
None, no argument needed
In some unusual cases like predictive gages, the daily value might be for the current day or a date in the future.
&stateCd=ny&parameterCd=00060 // Get the latest discharge daily values for all sites in New York state

Get a range of daily values from now	Specify the period argument	
period must be in ISO-8601 Duration format. Do not express in increments of less than a day. For example, period=P7D is allowed but period=PT2H is not.
periods must be deterministic. Days and weeks are deterministic (always the same duration), but months and years or not.
Beware that there there are typically no daily values for today because the day is not yet finished, hence no daily statistic can be derived. This means in most cases if period=P7D, six daily values beginning with yesterday will be retrieved.
Data are always returned up to the most recent value, which in the case of a predictive gage might be in the future.
&period=P7D // Retrieve last seven days up from now to most recent instantaneous value)
&period=P520W // Retrieves approximately ten years of data (520 weeks is about 10 years)

Get a range of daily values from an explicit begin or end date	Use the startDT and endDT arguments	
Both startDt and endDt must be in ISO-8601 Date format
Do not express dates in increments of less than a day
Do not supply time zones. The time zone is whatever time zone is in effect at the site.
startDt must always be supplied
If endDT is not provided, endDT is the most recent daily value
startDT must be chronologically at or before endDT
&startDT=2010-11-22&endDT=2010-11-22 // One day of daily values only
&startDT=1990-01-01&endDT=1999-12-31 // All daily values for the 1990s
&startDT=2010-11-22 // Ends with most recent daily value
&endDt=1999-12-31 // Not allowed because of start date is ambiguous

### Format (format)

Syntax	
format=[waterml{,1.1} | waterml,2.0 | rdb{,1.0} | json{,1.1}]
Default	waterml

#### Examples

`&format=json` // WaterML 1.1 translated into JSON
`&format=json,1.1`
`&format=json,2.0` // A JSON version of WaterML2 is not presently available. Will cause an error.

### indent

Used to specify whether block structured data formats (&format=waterml|json only) should include indentation for easy viewing. Four space characters are inserted for every level of indentation. Otherwise the parameter is ignored.

Syntax	indent=[on|off]

Default	off

#### Examples

&format=json&format=on // Indented JSON wanted
&format=json&format=off // JSON wanted, no indentation

## Minor Filters

Additional filters can be applied after specifying a major filter. This further reduces the set of expected results. Users are encouraged to use minor filters because it allows more efficient use of this service.

### Parameter Code (parameterCd)

URL Argument Name	parameterCd (aliases: variable, parameterCds, variables, var, vars, parmCd)
Description	
USGS time-series parameter code
All parameter codes are numeric and 5 characters in length. Parameter codes are used to identify the constituent measured and the units of measure.
Popular codes include stage (00065), discharge in cubic feet per second (00060) and water temperature in degrees Celsius (00010)
Complete list of USGS parameter codes (not all parameters are served by time-series sites)
Syntax	parameterCd|variable={parameterCd1,parameterCd2,...}
Default	returns all regular time-series parameters for the requested sites
Minimum argument values required	1
Maximum argument values allowed	100
Examples	
&parameterCd=00060 // discharge, cubic feet per second
&parameterCd=00060,00065 // discharge, cubic feet per second and gage height in feet
&variable=00060 // discharge, cubic feet per second
&variable=00060,00065 // discharge, cubic feet per second and gage height in feet

There are two types of parameter codes:

Fixed-value codes
The result value is a numeric code that represents a textual meaning. [ Tab-separated -- saved to file || Tab-separated -- display to screen || HTML ]

Numeric codes
The result is a numeric value for chemical, physical, and biological data.

The following table shows an example of several parameter codes and definitions. This table also illustrates how several parameter codes may exist for one type of measurement.

Parameter Code
Parameter Definition
00910	Calcium, water, unfiltered, milligrams per liter as calcium carbonate
00915	Calcium, water, filtered, milligrams per liter
00916	Calcium, water, unfiltered, recoverable, milligrams per liter
91051	Calcium, water, filtered, micrograms per liter

Available groups:

- Information 
- Physical 
- Inorganic, major non-metal 
- Inorganic, minor metals 
- Nutrient 
- Microbiological 
- Sediment 
- Organics, pesticide 
- Toxicity 

You may use codes that you know of, or ask the user to look or relevant codes under:
https://help.waterdata.usgs.gov/codes-and-parameters/parameters

and provide them, as they are an extensive list.

### Statistics Code (statCd)

Description	
Selects sites based on the statistics codes desired, such as minimum, maximum or mean
Using statCd without parameterCd is possible, but is not logical. statCd is useful only in refining data about parameters collected at a site.
All stat codes are five numeric characters in length
List of stat codes
Syntax	statCd=[ all | { statCd1,statCd2,... } ]
Default	all - all statistics codes served for the sites and parameters requested
Minimum argument values required	1
Maximum argument values allowed	20
Examples	
&stateCd=ri&parameterCd=00060,00065&statCd=00003 // latest daily mean streamflow and gage height for Rhode Island

### Site Status (siteStatus) 

URL Argument Name	siteStatus
Description	
Selects sites based on whether or not they are active. If a site is active, it implies that it is being actively maintained. A site is considered active if:

it has collected time-series (automated) data within the last 183 days (6 months)
it has collected discrete (manually collected) data within 397 days (13 months)
If it does not meet these criteria, it is considered inactive. Some exceptions apply. If a site is flagged by a USGS water science center as discontinued, it will show as inactive. A USGS science center can also flag a new site as active even if it has not collected any data.

The default is all (show both active and inactive sites).

Syntax	siteStatus=[ all | active | inactive ]
Default	all - sites of any activity status are returned
Minimum argument values required	1
Maximum argument values allowed	1
Examples	
&siteStatus=active

### Site Type (siteType) 

Site codes will be shared later (a couple sections down below)

### Site was modified since (modifiedSince) 

Returns all sites and their values only if any of the requested daily values have changed during the requested period.
The modifiedSince time period always begins with today and moves toward the past. It must be expressed in an ISO-8601 duration format.
If the modifiedSince argument is not specified in the generated URL, it has no effect on the query.
Only deterministic periods are allowed. Since months and years are not deterministic, do not use them.

Syntax	modifiedSince=ISO-8601-duration
Examples	
&stateCd=NY&modifiedSince=P1W - All NY daily values are retrieved only if any of their requested daily values were changed in the last week.

### Surface water filters 

Drainage Area (drainAreaMin and drainAreaMax)

URL Argument Names	
drainAreaMin (alias: drainAreaMinVa)
drainAreaMax (alias: drainAreaMaxVa)
Description	
These arguments allows you to select principally surface water sites where the associated sites' drainage areas (watersheds) are within a desired size, expressed in square miles or decimal fractions thereof.
Providing a value to drainAreaMin (minimum drainage area) means you want sites that have or exceed the drainAreaMin value
Providing a value to drainAreaMax (maximum drainage area) means you want sites that have or are less than the drainAreaMax value
The values may be expressed in decimals
If both the drainAreaMin and drainAreaMax are specified, sites at or between the minimum and maximum drainage areas values specified are returned
Caution: not all sites are associated with a drainage area.
Caution: drainage area generally only applies to surface water sites. Use with other site types, such as groundwater sites, will likely retrieve no results.
Syntax	
drainAreaMin=minValue
drainAreaMax=maxValue
Default	All sites are retrieved, regardless of their drainage area
Minimum argument values required	1
Maximum argument values allowed	1
Examples	
&drainAreaMin=1000&drainAreaMax=5000 // Return sites where the drainage area is 1000 square miles or greater and is 5000 square miles or less.
