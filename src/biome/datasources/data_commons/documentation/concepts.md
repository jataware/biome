# Concepts

## Schema

To allow data from hundreds of organizations around the world, in a myriad of models and formats to be interoperable and queryable in a unified way, Data Commons needs to have a common way of understanding and representing this data. To do so, it applies a schema, or vocabulary to all its data, that is largely derived from earlier schemes developed for semantic understanding of web pages – most notably, the data models and schemas of Schema.org (which were in turn based on earlier schemes such as Microformats and Resource Description Framework (RDF)).

The Data Commons schema is in fact a superset of Schema.org schemas, with a particular emphasis on time series and statistical data. Every data set must have an associated schema, written in Meta Content Format (MCF) language, that maps the provider’s data to existing concepts in the Data Commons.

## Knowledge Graph

Data Commons models the world as a directed labeled graph, consisting of a set of nodes and edges with labels, known as properties. This general framework allows Data Commons to represent information about a wide range of domains: from time series about demographics and employment, to hurricanes, to protein structures.

As a simple example, here are a set of nodes and edges that represent the following statements:

California is a state
Santa Clara county and Berkeley are contained in the state of California
The latitude of Berkeley, CA is 37.8703

Each node consists of some kind of entity or value, and each edge describes some kind of property. More specifically, each node consists of the following objects:

* One or more types: an entity, event, statistical variable, or statistical observation
* A unique identifier, known as a DCID
* Various properties
* A provenance

As in other knowledge graphs, each pair of connected nodes is a triple consisting of a subject node, predicate (or “edge”) and object node. The Data Commons knowledge graph is made up of billions of triples. The triple is not generally exposed in Data Commons as a concept that you need to know (although it can be queried from some APIs).

You can get all the information about a node and its edges by looking at the Knowledge Graph browser. If you know the DCID for a node, you can access it directly by typing https://datacommons.org/browser/DCID.

Every node entry shows a list of outgoing edges, or properties, and incoming edges. Properties are discussed in more detail below.

## Type

Every node has at least one type, where each type may be a sub-class of multiple types. For entities and events, their type is typically another entity. For example, Berkeley is a type of City. At the root, all types are instances of the Class type. For statistical variables and observations, their type is always StatisticalVariable and StatVarObservation, respectively.

## Entity

An entity represents a persistent, physical thing in the real world. While Data Commons has information about a wide variety of types of entities (cities, states, countries, schools, companies, facilities, etc.), most of the information today is about places. Data Commons contains a catalog of about 2.9 million places. In addition to basic metadata like the location, type and containment information, many places also contain information about their shape, area, etc. For a list of available place types, take a look at the place types page.

## Event

An event is what it sounds like: an occurrence at a specific point in time, such as an extreme weather event, a criminal incident, an election, etc.

## Statistical variable

In Data Commons, even statistical measurements and time series data are modeled as nodes. A statistical variable represents any type of metric, statistic, or measurement that can be taken at a place and time, such as a count, an average, a percentage, etc. A statistical variable for a specific place is a time series, consisting of a set of observed values over a time period.

Data Commons comprises hundreds of thousands of statistical variables, which you can view using the Statistical Variable Explorer.

The type of a statistical variable is always the special sub-class StatisticalVariable. For example, the metric Median Age of Female Population is a node whose type is a statistical variable.

A statistical variable can be simple, such as Total Population, or more complex, such as Hispanic Female Population. Complex variables may be broken down into constituent parts, or not.

## Unique identifier: DCID

Every node has a unique identifier, called a Data Commons ID, or DCID. In the Knowledge Graph browser, you can view the DCID for any node or edge. For example, the DCID for the city of Berkeley is geoid/0606000:

## Property

Every node also contains properties or characteristics that describe its entity, event, or statistical variable. Each property is actually an edge to another node, with a label. If the object node is a primUnique identifier: DCID

Every node has a unique identifier, called a Data Commons ID, or DCID. In the Knowledge Graph browser, you can view the DCID for any node or edge. For example, the DCID for the city of Berkeley is geoid/0606000:
For example, in this node for the city of Addis Ababa, Ethiopia, the typeOf and containedInPlace edges link to other entities, namely City and Ethiopia, whereas all the other values are terminal.

Note that the DCID for a property is the same as its name.

## Observation

An observation is a single measured value for a statistical variable, at or during a specified period of time, for a specific entity.

For example, the value of the statistical variable Median Age of Female Population for the city of San Antonio, Texas in 2014 could have an observation Observation_Median_Age_Person_Female_SanAntonio_TX_2014. The type of an observation is always the special sub-class StatVarObservation.

Time series made up of many observations underlie the data available in the Timeline Explorer and timeline graphs. For example, here is the median income in Berkeley, CA over a period of ten years, according to the US Census Bureau:

## Provenance, Source, Dataset

Every node and triple also have some important properties that indicate the origin of the data.

Provenance: All triples have a provenance, typically the URL of the data provider’s website; for example, www.abs.gov.au. In addition, all entity types also have a provenance, defined with a DCID, such as AustraliaStatistics. It also (For many property types, which are defined by the Data Commons schema, their provenance is always datacommons.org.)

Source: This is a property of a provenance, and a datasex variables may be broken down into constituent parts, or not.
Dataset: This is the name of a specific dataset provided by a provider. Many sources provide multiple datasets. For example, the source Australian Bureau of Statistics provides two datasets, Australia Statistics (not to be confused with the provenance above), and Australia Subnational Administrative Boundaries.

Note that a given statistical variable may have multiple provenances, since many data sets define the same variables. You can see the list of all the data sources for a given statistical variable in the Statistical Variable Explorer. For example, the explorer shows multiple sources (Censuses from India, Mexico, Vietnam, OECD, World Bank, etc.) for the variable Life Expectancy:
