# Web Documentation

Limited geographical identifiers: NHANES intentionally limits geographical identifiers in public-use files to protect participant confidentiality. The public datasets generally only include:
Census region (Northeast, Midwest, South, West)

Datasets contain data for persons who participated in the selected survey. The National Health and Nutrition Examination Survey (NHANES) datasets are labeled by cycle year. The website contains the public-use data files for each of National Center for Health Statistic's national surveys starting with the initial National Health Examination Survey (NHES) I dataset up to the most current dataset. Codebooks and documentation are part of each data file.

## NHANES Nutrition Data Collection

NHANES contains a wealth of nutrition information gathered in health interviews, health examinations, and laboratory testing. Survey participants 12 years and older provide their own interview responses. Proxy respondents report for children who are 5 years and younger and for other persons who cannot self-report; and proxy respondents assist children 6-11 years of age.

## NHANES Food and Nutrition-related data
- Dietary intake
- 24-hour dietary recall
- Food frequency questionnaire

Since the 1999-2000 survey cycle, participants completed a 24-hour dietary recall (First Day) interview during their health examination in the mobile examination center. 

## File types descritions:
1. Dietary Interview Individual Foods

Filename pattern: <year-cycle>_<REDACTED>_individual_foods.xpt

Contains the following columns:

SEQN: Participant sequence number
DR1ILINE: Food/individual component number
DR1EXMER: Interviewer ID code
DR1DBIH: Number of days between intake and HH interview
DR1LANG: Language respondent used mostly
DR1IFDCD: USDA food code
DR1DRSTZ: Dietary recall status code
DRABF: Breast-fed infant (either day)
DR1DAY: Intake day of the week
DRDINT: Number of intake days
DR1CCMTX / DR1CCMNM: Combination food type and number
DR1_020/DR1_030Z: Time and Name of eating occasion and time
DR1FS / DR1_040Z: Food source and where consumed
DR1IGRMS: Amount of food in grams
DR1IKCAL - DR1IP226: Food energy and nutrients contained in each amount of food consumed
WTDRD1: Dietary sample weights


2. Dietary Interview Food Codes

Filename pattern: <year-cycle>_<REDACTED>_food_codes.xpt

Contains the following columns:
DRXFDCD: a numeric value corresponding to the DR1IFDCD in the Dietary Interview Individual Foods file DR1IFF_ or DR2IFDCD in DR2IFF_
DRXFCSD: a short description (up to 60 characters) of the food code
DRXFDLD: a long description (up to 200 characters) of the food code

The individual foods files only contain records for participants with complete intakes considered to be reliable (DR1DRSTZ=1), those reporting water intake, and for breast fed children (DR1DRSTZ=4), excluding those fasting on recall day.

## Dietary Variable Naming Conventions
Some variables with different names and data file locations may have the same labels, as shown in the table below.

In the Individual Foods files, the fourth position of the variable name for nutrients is always the letter "I." Additionally, the number in the third position of the variable name identifies the collection day.

_Sample Individual Foods variables_:

Variable Label:          Calcium (mg)
Item ID / Variable Name: DR1ICALC	
Item ID Decoded:         DR = Dietary Recall; 1 = First Day; I = Individual Foods; CALC = Calcium

## Combination Codes

During the collection and coding of dietary recall data, many individual food codes are linked together using "combination" codes. These codes allow investigators to account for individual foods that are consumed simultaneously, such as sugar in coffee or milk on cereal, or for food mixtures that are reported as discrete ingredients, such as a homemade sandwich reported separately as bread, cheese, lettuce, and mayonnaise.

Combinations are defined using two separate variables. The first, the combination food number, flags foods as being eaten in combination. Each combination is given a unique combination food number, and these are listed in sequence (i.e., the first food combination reported by a participant is 1, the second is 2, and so on). The second variable, the combination food type, designates the type of combination, as shown below in the list.

### Combination Food Types
Code	Description
00	Non-combination
01	Beverage with additions
02	Cereal with additions
03	Bread/baked products with additions
04	Salad
05	Sandwiches
06	Soup
07	Frozen meals
08	Ice cream/frozen yogurt with additions
09	Dried beans and vegetable with additions
10	Fruit with additions
11	Tortilla products
12	Meat, poultry, fish
13	Lunchables
14	Chips with additions
90	Other mixtures
The following example shows the relationship of the combination food number and combination food type for three food items. Note that all the foods in a given combination are assigned the same combination food type code and combination food number.

### Combination Foods Example
Combinations eaten	Food Items reported	Combination food number	Combination food type
Cereal with fruit and milk	Frosted flakes cereal	01	02
Milk	01	02
Bananas	01	02
Coffee with sugar	Coffee	02	01
Sugar	02	01
Ham and cheese sandwich	Ham	03	05
Cheese	03	05
Bread	03	05
Mustard	03	05
Pickle	03	05
Foods with a value of 00 for both combination number and combination type are either discrete food items that were not eaten in combination or mixed dishes coded with a single food code.

### Mixed Dishes Code
Mixed dishes include food items such as stews, soups, casseroles, sandwiches, pasta with meats and sauces, pizzas, and tortilla dishes (such as enchiladas and burritos). As mentioned above, mixed dishes can be coded either by an individual food code or several food codes—representing the ingredients of the mixture—linked by a combination food number and combination food type.

Individual food codes representing mixed dishes are included in many food groups and subgroups of the coding scheme. Generally, mixtures represented by individual food codes are placed in food groups based on the primary component or ingredient in the mixture. For example, a cheeseburger on a bun is assigned to the "meat, poultry, fish" group because the hamburger is considered the main ingredient. Lasagna with meat is assigned to the "grain products" group because the noodles are considered the main ingredient.

Certain types of mixtures, such as sandwiches, salads, and soups, can be included in various food groups, depending on their main ingredient. Therefore, it is important to note all the possible food groups that could contain codes related to that mixture. For example, different kinds of sandwiches can be found in various food groups and subgroups.

# Doc Page

## Component Descriptions
The objective of the dietary interview component is to obtain detailed dietary intake information from NHANES participants. The dietary intake data are used to estimate the types and amounts of foods and beverages (including all types of water) consumed during the 24-hour period prior to the interview (midnight to midnight), and to estimate intakes of energy, nutrients, and other food components from those foods and beverages. Following the dietary recall, participants are asked questions on salt use, whether the person’s overall intake on the previous day was much more than usual, usual or much less than usual, and whether the participant is on any type of special diet. Questions on frequency of fish and shellfish consumed during the past 30 days are asked of participants 1 year or older, with the use of proxies for young children (see the Dietary Interview Procedure Manuals (cdc.gov) for more information on the proxy interview). 

### What's New with the August 2021-August 2023 WWEIA Release: 

In response to the COVID-19 pandemic, the mode of the first dietary recall changed from in-person during the MEC examination to telephone 3 to 7 days after the examination.

Individual Foods File (DR1IFF_L): Detailed information about each food/beverage item (including the description, amount of, and nutrient content) reported by each participant is included in the Individual Foods files.

The Individual Foods file includes one record for each food/beverage consumed by a participant. Each record is uniquely numbered within a participant’s set of records and contains the information listed below:

Number of days of complete intake obtained from participant;
Day of the week of the intake;
Whether the food/beverage was eaten in combination with other foods, such as in a sandwich;
Time of eating occasion/when the food was eaten;
Eating occasion name;
Where the food/beverage was obtained;
Whether the meal/snack was eaten at home or not;
A USDA Food and Nutrient Database for Dietary Studies (FNDDS) code identifying the food/beverage;
Amount of food/beverage consumed, in grams; and 
Food energy and 64 nutrients/food components (listed in Appendix 3) from each food/beverage as calculated using USDA's Food and Nutrient Database for Dietary Studies 2021-2023 (FNDDS 2021-2023).  

Descriptions for the USDA FNDDS food codes are provided in the Food Code Description file.