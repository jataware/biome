
You may use the household file to answer questions about american housing:

Example questions you may answer:
- What are the housing conditions relating to medical conditions such as asthma? You
  can check the air quality, water quality, mold, radon, and other conditions of the home.

Never assume things like
"Assuming MOLD indicates presence of mold where 1=Yes, 2=No"
and instead look in the codebook for the meaning of the codes. But usually:
1 = Yes ; 2 = No ; M or -9 = Not reported ; N or -6 = Not applicable

The 2015 to 2023 public use files (PUFs) do not include many of the geographic indicators included in prior year PUFs. This is due to the disclosure avoidance procedures required by the U.S. Census Bureau.
The 2015 to 2023 integrated national longitudinal sample PUFs (national PUFs) included two geographic variables: Census Division and OMB13CBSA, while the independent metropolitan area longitudinal oversample PUF (metropolitan area PUF) included OMB13CBSA only.
For pre-2015 data, you can check other geographic variables in the codebook and see if they are present, and use them to answer questions and correlate data at a finer granularity (than just the much coarser statistical metropolitan areas)- some may even contain SMSA codes, which map to cities.

Important: Remember, when using the codebook and loading with the pandas library, you need to set index_col=False, else the  Variable column will be treated as the index column and the rest of the columns will shift!

When wanting to do something like:
```
# Add year column
df_fl['YEAR'] = year

# you'll get a warning and the data may be appended to a df slice copy- and disappear!
# do this instead:
df_fl.loc[:, 'YEAR'] = year
```

