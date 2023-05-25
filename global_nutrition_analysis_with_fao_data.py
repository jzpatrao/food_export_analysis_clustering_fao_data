#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Overview" data-toc-modified-id="Overview-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Overview</a></span></li><li><span><a href="#Data-Cleaning" data-toc-modified-id="Data-Cleaning-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Data Cleaning</a></span></li><li><span><a href="#New-variables" data-toc-modified-id="New-variables-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>New variables</a></span><ul class="toc-item"><li><span><a href="#food_supply_kg" data-toc-modified-id="food_supply_kg-3.1"><span class="toc-item-num">3.1&nbsp;&nbsp;</span>food_supply_kg</a></span></li><li><span><a href="#ratio_kcalkg-and-protein_percentage" data-toc-modified-id="ratio_kcalkg-and-protein_percentage-3.2"><span class="toc-item-num">3.2&nbsp;&nbsp;</span>ratio_kcalkg and protein_percentage</a></span></li><li><span><a href="#dom_sup_kcal-and-dom_sup_kgprot" data-toc-modified-id="dom_sup_kcal-and-dom_sup_kgprot-3.3"><span class="toc-item-num">3.3&nbsp;&nbsp;</span>dom_sup_kcal and dom_sup_kgprot</a></span></li><li><span><a href="#great_import_from_undern_countries" data-toc-modified-id="great_import_from_undern_countries-3.4"><span class="toc-item-num">3.4&nbsp;&nbsp;</span>great_import_from_undern_countries</a></span></li></ul></li><li><span><a href="#Identify-major-trends" data-toc-modified-id="Identify-major-trends-4"><span class="toc-item-num">4&nbsp;&nbsp;</span>Identify major trends</a></span></li></ul></div>

# <a id="Top"></a>

# <hr style="border:1.5px solid black"> </hr>

# <a id='Task_2'></a>

# # Overview
# 
# - Identify the primary key of each table and test them.  
# > <font color='blue'>The primary keys of both tables *'veg'* and *'ani'* are combinations of *'Area Code'* + *'Element Code'* + *'Item Code'* + *'Year'*.  A new column 'pimary_key' was created for each table composed of these 4 columns. I then tested the integrity of the primary keys by setting the column *'primary_key'* as the index of each table, then run verify_integrity. [Click to see code](#task_2_item_1)</font>
# 
# - Create a dataframe containing information about each country's population. Calculate the total number of humans on the planet.  
# > <font color='blue'>A dataset was downloaded from FAO website under Annual population, which contains population numbers per country from year 1950 till 2018. I then selected data for the years 2014 and 2018 for this task. After that by using *.groupby* and *.sum()* I was able to calculate global population per each year. However, the result values were too high to match reality. Therefore I plotted the table to look at potential anomolies. Sure enough duplicated big values showed up on the graph. I then created a table of countries with population numbers over 1 billion. It turned out, mainland China's population is accounted for twice for each yearin this dataset. I then deleted duplicated values.Then re-calculated world population. Finally multiplying result numbers by 1000 as FAO population values are in unit of 1000 person.  [Click to see code](#task_2_item_2) </font>
# 
# - Among the documents on the Food Balance Sheets that you have downloaded, you will find redundant information concerning the 11 elements.  Identify these redundancies and give your answer as a mathematical formula. Have a look at the Food Balance Sheets then click on “definitions and standards”
#     - The expected formula is a simple three term equation involving each of the 11 amounts seen above:  a1+a2+[...]=b1+[...]=c1+c2+[...] . For this equation, give the example of wheat in France.
#     
# > <font color='blue'>Looking at the elemant descriptions on Food Balance Sheet, I suspected that:<br>
# >> - Domestic supply quantity = Food supply quantity + Feed + Seed + Losses + Processing + Other uses + Residuals<br>
# also<br>
# >> - Domestic supply quantity = Production + Import Quantity + Stock Variation - Export Quantity<br>
#     
# <font color='blue'>I created a subset of the table *food* containing only data of wheat in France. Then I performed some data cleaning on the subset to have a clear overview of the numbers of these elements. Finally I created two new columns using equitions mentioned above compare whether they are correct. In the end the results were satisfactory.[Click to see code](#task_2_item_3) </font>

# <hr style="border:1.5px solid blalck"> </hr>

# <font color='blue'>Importing necessary libraries.</font>

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[2]:


# Import dataset of plant based food
veg_2014 = pd.read_csv("\\veg_2014.csv")
veg_2018 = pd.read_csv("\\veg_2018.csv")
veg = veg_2014.append(veg_2018)


# In[5]:


veg.head()


# In[7]:


# Import dataset of animal based food
ani = pd.read_csv("\\ani.csv")
ani.head()


# <a id="task_2_item_1"></a>

# <hr style="border:1px solid blalck"> </hr>

# <font color='blue'>Creating a new column 'primary_key' for table *veg*. It is the combination of 'Area Code', Element Code', 'Item Code' and 'Year'.</font>

# In[9]:


# Create primary key column
veg["primary_key"] = (
    veg["Area Code (FAO)"].astype(str)
    + veg["Element Code"].astype(str)
    + veg["Item Code"].astype(str)
    + veg["Year"].astype(str)
)
veg.set_index("primary_key", verify_integrity=True)


# In[10]:


# Create primary key column
ani["primary_key"] = (
    ani["Area Code (FAO)"].astype(str)
    + ani["Element Code"].astype(str)
    + ani["Item Code"].astype(str)
    + ani["Year"].astype(str)
)
ani.set_index("primary_key", verify_integrity=True)


# <a id="task_2_item_2"></a>

# <font color='blue'>Import dataset downloaded from FAO, containing total population number of each country from 1950 till 2018.</font>

# In[11]:


population = pd.read_csv("\\population.csv")
population.head()


# <font color='blue'> Selecting data for the years 2014 and 2018.</font>

# In[12]:


population_20142018 = population[population["Year"].isin([2014, 2018])]


# In[13]:


population_20142018


#  <font color='blue'> Using *.groupby* and *.sum()* to calculate global population per year</font>

# In[14]:


population_20142018.groupby("Year")["Value"].sum()


# <font color='blue'>Hmm... result values seem too high to match reality. Checking value distribution through a graph </font>

# In[15]:


x = population_20142018["Area"]
y = population_20142018["Value"]
plt.figure(figsize=(10, 5))
plt.scatter(x, y, color="blue")
plt.show()


# <font color='blue'>Potential duplicated big values detected looking at the graph.<br> 
# Creating a seperate table of countries with population over 1 billion</font>

# In[16]:


pop_big = population_20142018[population_20142018["Value"] > 1000000]
pop_big


# <font color='blue'>Mainland China's population is accounted for twice for each year since *'China'* and *'China mainland*' both show up in the result set.<br> 
#     Deleting *'China'* population (Area Code *351*) as it contains already mainland population plus Hongkong, Macao and Taiwan population.</font>

# In[17]:


population_20142018 = population_20142018[population_20142018["Area Code (FAO)"] != 351]


# <font color='blue'>Re-calculating world population </font>

# In[18]:


population_20142018.groupby("Year")["Value"].sum()


# In[19]:


world_population_20142018 = (
    population_20142018.groupby("Year")["Value"].sum().to_frame()
)
world_population_20142018.reset_index(inplace=True)
world_population_20142018


# <font color='blue'>Multiplying result by 1000 as per FAO unit instruction </font>

# In[20]:


world_population_20142018["Value"] = world_population_20142018["Value"] * 1000
world_population_20142018


# <font color='blue'>Creating variables for total world population for 2014 and 2018, for future use.</font>

# In[21]:


world_population_total_2014 = world_population_20142018.iloc[0, 1]
world_population_total_2018 = world_population_20142018.iloc[1, 1]


# In[23]:


world_population_total_2018


# ----

# <font color='blue'> Identify relations between variables: Domestic supply quantity, Production, Import Quantity, Stock Variation and Export Quantity.</font>

# In[24]:


ani.Element.value_counts()


#  <font color='blue'>Looking at the elemant description, in combination with definition description from FAO, I would suspect that:<br> 
#     - Domestic supply quantity = Food supply quantity + Feed + Seed + Losses + Processing + Other uses + Residuals <br>
# also<br>
#     - Domestic supply quantity = Production + Import Quantity + Stock Variation - Export Quantity</font>

# <font color='blue'> Let's verify above theory with an example: wheat (item code 2511) ~ France.</font>

# In[25]:


veg.head()


# In[26]:


wheat_in_france = veg[(veg["Item Code"] == 2511) & (veg["Area"] == "France")]
wheat_in_france


# In[27]:


wheat_in_france = wheat_in_france.pivot_table(
    index=("Year"), columns="Element", values="Value", aggfunc="sum"
)
wheat_in_france


# <font color='blue'>Selecting relavent columns from *wheat_in_france* to make calculation easier to read. </font>

# In[28]:


wheat_in_france = wheat_in_france[
    [
        "Domestic supply quantity",
        "Export Quantity",
        "Import Quantity",
        "Feed",
        "Food",
        "Losses",
        "Other uses (non-food)",
        "Processing",
        "Production",
        "Residuals",
        "Seed",
        "Stock Variation",
    ]
]
wheat_in_france


# <font color='blue'>Verifying if the following equation is true:<br>
# Domestic supply quantity = Food supply quantity + Feed + Seed + Losses + Processing + Other uses + Residuals</font>

# In[29]:


wheat_in_france["compare"] = (
    wheat_in_france["Food"]
    + wheat_in_france["Feed"]
    + wheat_in_france["Seed"]
    + wheat_in_france["Losses"]
    + wheat_in_france["Processing"]
    + wheat_in_france["Residuals"]
    + wheat_in_france["Other uses (non-food)"]
)
wheat_in_france


# <font color='blue'>Equation checks out.</font>

# <font color='blue'>
# Verifying if the second equation is true:<br>
# Domestic supply quantity = Production + Import Quantity + Stock Variation - Export Quantity </font>

# In[30]:


wheat_in_france["compare"] = (
    wheat_in_france["Production"]
    + wheat_in_france["Import Quantity"]
    + wheat_in_france["Stock Variation"].abs()
    - wheat_in_france["Export Quantity"]
)
wheat_in_france


# <font color='blue'> Result values in column 'compare' are slightly different from 'Domestic supply quantity', but within acceptable range. This might be a mathematical discrepancy. </font>

# <a id='Task_3'></a>

# # Data Cleaning
# <font color='blue'>Add variable ‘origin’ to tables *veg* and *ani*. Appends *veg* and *ani* to one table *temp*. Renaming of *temp* s columns with Laura's guideline in mind. Transformation of *temp* to a pivot table so that the elements are now columns of the new table. Renaming columns according to Laura's guideline: lower-case, no spaces (use underscore instead), no special characters, no accented characters.
# Index columns need to be normal columns. Rename table *food*. <br>
# From now on, table *food* will be the main table I work with.[Click to see code](#task_3)</font>

# In[31]:


# Add variable ‘origin’
ani["origin"] = "animal"
veg["origin"] = "vegetal"


# In[32]:


ani.head(3)


# In[33]:


veg.head(3)


#  <font color='blue'>Appends veg and ani to one table </font>

# In[34]:


temp = ani.append(veg)
temp.head()


# In[35]:


temp.columns


# In[36]:


temp.columns = [
    "xx",
    "xx2",
    "country_code",
    "country",
    "xx3",
    "element",
    "item_code",
    "item",
    "xx4",
    "year",
    "unit",
    "value",
    "xx5",
    "xx6",
    "primary_key",
    "origin",
]


# <font color='blue'>Transformation of ‘temp’ to a pivot table </font>

# In[37]:


data = temp.pivot_table(
    index=["country_code", "country", "item_code", "item", "year", "origin"],
    columns=["element"],
    values=["value"],
    aggfunc=sum,
)
data.head()


# <font color='blue'>Renaming of data’s columns according to Laura's guideline:<br>
# *lower-case, no spaces (use underscore instead), no special characters, no accented characters*.</font>

# In[38]:


data.columns


# In[39]:


data.columns = [
    "domestic_supply_quantity",
    "export_quantity",
    "fat_supply_quantity_gcapitaday",
    "feed",
    "food",
    "food_supply_kcalcapitaday",
    "food_supply_quantity_kgcapitayr",
    "import_quantity",
    "losses",
    "other_uses",
    "processing",
    "production",
    "protein_supply_quantity_gcapitaday",
    "residuals",
    "seed",
    "stock_variation",
    "tourist_consumption",
]


# In[40]:


data.head(3)


# <font color='blue'>Index columns need to be normal columns</font>

# In[41]:


food = data.reset_index()
food


# <hr style="border:1px solid blalck"> </hr>

# # New variables 
# <font color='blue'>
# 
# Before starting working on adding variables, I dropped unecessary columns to make further work easier.<br>
# - Add variables : food_supply_kcal & food_supply_kgprotein<br>
# Using table *population_20142018* (from task 2), inserted total global population data into table *food*. <br>
# food_supply_kcal = food_supply_kcalcapitaday * population * 365<br>
# food_supply_kgprotein = protein_supply_quantity_gcapitaday / 1000 * population * 365<br>
#     
# 
# - Add variable : food_supply_kg<br>
# Definition: food supply expressed in kg<br>
# food_supply_kg = food * 1000000 <br>
# 
# - Add variables : ratio_kcalkg and protein_percentage<br>
# Definition: "energy:weight" ratio of each item expressed in kcal/kg and the protein percentage of each item.<br>
# ratio_kcalkg = food_supply_kcal / food_supply_kg<br>
# protein_percentage = food_supply_kgprotein / food_supply_kg<br>
# 
# - Add variables: dom_sup_kcal and dom_sup_kgprot<br>
# Definition: Global domestic supply in kcal, and global domestic supply in kg of protein<br>
# dom_sup_kcal = domestic_supply_quantity * 1000000 * ratio_kcalkg<br>
# dom_sup_kgprot = domestic_supply_quantity * 1000000 * protein_percentage<br>
# 
# - Add variables: great_import_from_undern_countries<br>
# Definition: (A boolean variable) true or false - do the 200 highest imports of the 25 most exported items come from countries with more than 10% malnourishment?<br>
# 
# </font>

# <hr style="border:1px solid blalck"> </hr>

# food supply expressed in kcal and food supply expressed in kg of protein.
# Use the following information:
# - Each country’s population
# - food_supply_kcalcapitaday
# - protein_supply_quantity_gcapitaday
# 

# In[45]:


population_20142018_pivot = population_20142018.pivot_table(
    index=(["Area Code (FAO)", "Area", "Year"]), columns="Element", values="Value"
)
population_20142018_to_be_merged = population_20142018_pivot.reset_index()
population_20142018_to_be_merged


# <font color='blue'>Renaming *population_20142018* columns to match main table *food*, in anticipation for merging. Also multiplying *'population'* values by 1000 (the FAO data unit for population) to represent accurate number.</font>

# In[46]:


population_20142018_to_be_merged.columns = [
    "country_code",
    "country",
    "year",
    "population",
]

population_20142018_to_be_merged["population"] = (
    population_20142018_to_be_merged["population"] * 1000
)

population_20142018_to_be_merged


# In[47]:


food = pd.merge(
    food,
    population_20142018_to_be_merged,
    on=["country_code", "country", "year"],
    how="inner",
)

food


# In[48]:


# food_supply_kcal = food_supply_kcalcapitaday * population * 365
food["food_supply_kcal"] = food["food_supply_kcalcapitaday"] * food["population"] * 365


# In[49]:


# food_supply_kgprotein = protein_supply_quantity_gcapitaday / 1000 * population * 365
food["food_supply_kgprotein"] = (
    food["protein_supply_quantity_gcapitaday"] / 1000 * food["population"] * 365
)


# <a id="task_4_item_2"></a>

# In[50]:


food[["country", "year", "food_supply_kcal", "food_supply_kgprotein"]].head()


# <hr style="border:1px solid blalck"> </hr>

# ## food_supply_kg
# Definition: food supply expressed in kg

# In[51]:


food["food_supply_kg"] = food["food"] * 1000000


# In[52]:


food[["country", "year", "food_supply_kg"]].head()


# <a id='task_4_item_3'></a>

# ## ratio_kcalkg and protein_percentage

# <font color='blue'>ratio_kcalkg = food_supply_kcal / food_supply_kg </font>

# In[53]:


food["ratio_kcalkg"] = food["food_supply_kcal"] / food["food_supply_kg"]


# <font color='blue'>protein_percentage = food_supply_kgprotein / food_supply_kg </font>

# In[54]:


food["protein_percentage"] = food["food_supply_kgprotein"] / food["food_supply_kg"]


# In[55]:


food[["country", "year", "ratio_kcalkg", "protein_percentage"]].head()


# <hr style="border:1px solid blalck"> </hr>

# ## dom_sup_kcal and dom_sup_kgprot
# dom_sup_kcal = domestic_supply_quantity * 1000000 * ratio_kcalkg <br>
# dom_sup_kgprot = domestic_supply_quantity * 1000000 * protein_percentage

# In[56]:


food["dom_sup_kcal"] = food["domestic_supply_quantity"] * 1000000 * food["ratio_kcalkg"]
food["dom_sup_kgprot"] = (
    food["domestic_supply_quantity"] * 1000000 * food["protein_percentage"]
)


# In[58]:


food[["country", "year", "dom_sup_kcal", "dom_sup_kgprot"]].head()


# <hr style="border:1px solid blalck"> </hr>

# ## great_import_from_undern_countries
# A boolean variable - do the 200 highest imports of the 25 most
# exported items come from countries with more than 10% malnourishment?

# <font color='blue'>Import food security indicator dataset downloaded from FAO website. </font>

# In[59]:


food_secu = pd.read_csv("\\food_security_indicators.csv")
food_secu.head()


# In[60]:


food_secu = food_secu[
    ["Area Code (FAO)", "Area", "Item Code", "Item", "Year", "Unit", "Value"]
]


# In[61]:


# Replacing string values in column Year with integer values for future aggregate operations.
food_secu["Year"].value_counts()


# In[62]:


food_secu["Year"] = food_secu["Year"].replace(
    ["2017-2019", "2013-2015"], ["2018", "2014"]
)


# In[63]:


# Renaming columns to match column names of table food.
food_secu.columns = [
    "country_code",
    "country",
    "item_code",
    "item",
    "year",
    "unit",
    "value",
]


# In[64]:


food_secu.head()


# <font color='blue'>Pivot table so that values in column *'item'* becomes the new columns, in line with the format of table *food*.</font>

# In[65]:


food_secu_pivot = food_secu.pivot(
    index=["country_code", "country", "year"], values=["value", "unit"], columns="item"
)
food_secu_pivot.head()


# In[66]:


food_secu_pivot.columns = food_secu_pivot.columns.droplevel(0)
food_secu_pivot.head()


# In[67]:


food_secu_subset = food_secu_pivot.reset_index()


# In[68]:


food_secu_subset.head()


# In[69]:


food_secu_subset.columns = [
    "country_code",
    "country",
    "year",
    "undernourish_million",
    "undernourish_percent",
    "col1",
    "col2",
]


# In[70]:


food_secu_subset.drop(columns=["col1", "col2"], axis=1, inplace=True)


# In[71]:


food_secu_subset.head()


#  <font color='blue'>Inserting undernourish data into table *food*.</font>

# In[72]:


food["country_code"] = food["country_code"].astype(str)
food["year"] = food["year"].astype(str)
food_secu_subset["country_code"] = food_secu_subset["country_code"].astype(str)
food_secu_subset["year"] = food_secu_subset["year"].astype(str)
food = pd.merge(
    food, food_secu_subset, on=["country", "country_code", "year"], how="inner"
)


# In[73]:


food.head()


# <font color='blue'>Identify countries with undernourishement of 10%.</font>

# In[74]:


food["undernourish_percent"] = food["undernourish_percent"].replace("<2.5", "2.0")


# In[75]:


food["undernourish_percent"] = food["undernourish_percent"].astype(float)


# In[76]:


undernourish_country = food[food["undernourish_percent"] > 10]


# In[77]:


undernourish_country.head()


# <font color='blue'>Identify contries with most undernourishment percentage...</font>

# In[78]:


undernourish_country = undernourish_country.sort_values(
    by="undernourish_percent", ascending=False
)

undernourish_country.country.unique()


# <font color='blue'>Groupby table *undernourish_country* by year/item, then sort by export_quantity to identify top 25 most exported items.</font>

# In[79]:


top_25_export_by_undernourished_countries = (
    undernourish_country.groupby(["item_code", "item", "year"])["export_quantity"]
    .sum()
    .sort_values(ascending=False)
    .to_frame()
)
top_25_export_by_undernourished_countries


# In[80]:


top_25_export_by_undernourished_countries.reset_index(inplace=True)
top_25_export_by_undernourished_countries


# <font color='blue'>Identify the top 25 most exported items by undernourished countries in year 2014.</font>

# In[81]:


top_25_export_by_undernourished_countries_2014 = top_25_export_by_undernourished_countries[
    top_25_export_by_undernourished_countries["year"] == "2014"
]
top_25_export_by_undernourished_countries_2014 = top_25_export_by_undernourished_countries_2014.sort_values(
    by="export_quantity", ascending=False
).head(
    25
)
top_25_export_by_undernourished_countries_2014


# <font color='blue'>Identify the top 25 most exported items by undernourished countries in year 2018.</font>

# In[82]:


top_25_export_by_undernourished_countries_2018 = top_25_export_by_undernourished_countries[
    top_25_export_by_undernourished_countries["year"] == "2018"
]
top_25_export_by_undernourished_countries_2018 = top_25_export_by_undernourished_countries_2018.sort_values(
    by="export_quantity", ascending=False
).head(
    25
)
top_25_export_by_undernourished_countries_2018


# <font color='blue'>From table *food*, selecting the 200 highest import quantities among these 25 items.</font>

# In[83]:


food_subset2 = food[
    food["item_code"].isin(top_25_export_by_undernourished_countries["item_code"])
]


# In[84]:


food_subset2


# In[85]:


top_200_import = (
    food_subset2.groupby(["country", "year"], as_index=False)
    .import_quantity.sum()
    .sort_values(by="import_quantity", ascending=False)
    .head(200)
)


# In[86]:


top_200_import


# <font color='blue'>For the 200 corresponding lines in table *food*, set “True” for the variable, and “False” for the other lines.</font>

# In[87]:


food["great_import_from_undern_countries"] = np.where(
    food.index.isin(top_200_import.index), True, False
)


# In[88]:


food.head()


# In[89]:


food["great_import_from_undern_countries"].value_counts()


# [Back to task overview](#Task_4) <br>
# [Back to top](#Top)

# <hr style="border:1.5px solid blalck"> </hr>

# <a id="Task_5"></a>

# # Identify major trends 

# Question: considering only plant products, what proportion of the global domestic supply is used as :<br>
# food<br>
# feed<br>
# losses<br>
# other uses<br>

# <font color='blue'> Creating a subset of dataframe *food* that contain only plant products.</font>

# In[90]:


food_plant = food[food["origin"] == "vegetal"]


# In[91]:


food_plant


# <font color='blue'>Keeping only relevant columns of said subset to simplify future analysis</font>

# In[92]:


food_plant = food_plant[
    [
        "year",
        "domestic_supply_quantity",
        "food",
        "feed",
        "losses",
        "processing",
        "seed",
        "other_uses",
        "dom_sup_kcal",
        "dom_sup_kgprot",
    ]
]


# In[93]:


food_plant


# <font color='blue'>Replacing zeros with NaN to avoid division-by-zero scenarios, also replacing inf values with NaN in anticipation for aggregate functions.</font>

# In[94]:


food_plant = food_plant.replace(0, np.nan)
food_plant = food_plant.replace([np.inf, -np.inf], np.nan)


# In[95]:


food_plant


# <font color='blue'>Group dataframe by year then sum up values for all columns</font>

# In[96]:


food_plant_total_by_year = food_plant.groupby(["year"]).sum()
food_plant_total_by_year


# <font color='blue'>Calculating propotions of each element by dividing each element agains domestic supply quantity.</font>

# In[97]:


food_plant_total_by_year["food_percentage"] = (
    food_plant_total_by_year["food"]
    / food_plant_total_by_year["domestic_supply_quantity"]
).round(2)
food_plant_total_by_year["feed_percentage"] = (
    food_plant_total_by_year["feed"]
    / food_plant_total_by_year["domestic_supply_quantity"]
).round(2)
food_plant_total_by_year["losses_percentage"] = (
    food_plant_total_by_year["losses"]
    / food_plant_total_by_year["domestic_supply_quantity"]
).round(2)
food_plant_total_by_year["other_uses_percentage"] = (
    food_plant_total_by_year["other_uses"]
    / food_plant_total_by_year["domestic_supply_quantity"]
).round(2)


# In[98]:


food_plant_total_by_year


# <font color='blue'>As per calculation, the propotions are:
# 
#     
# |      | food | feed | losses | other uses |
# |------|------|------|--------|------------|
# | 2014 | 0.46 | 0.14 | 0.06   | 0.08       |
# | 2018 | 0.45 | 0.14 | 0.06   | 0.09       |
#     
# 
# </font>

# <hr style="border:1px solid blalck"> </hr>

# Question: how many humans on earth could be fed if all the plant-based food supply (crops), including food and feed, was used for human consumption? Give the results in terms of calories, and protein. Express these two results as a percentage of the world's population.

# <font color='blue'> The anwser is: domestic_supply_plant_kcal / average_kcalcapitayear </font>

# In[99]:


avg_dietary_energy = pd.read_csv(
    "C:\\Users\\jackiepod\\Desktop\\Openclassrooms\\Project_4\\Average_dietary_energy_requirement.csv"
)


# In[100]:


avg_dietary_energy.head()


# In[101]:


average_kcalcap = avg_dietary_energy.groupby("Year")["Value"].mean().round(2).to_frame()


# In[102]:


average_kcalcap


# In[103]:


average_kcalcap.reset_index(inplace=True)


# In[104]:


average_kcalcap = average_kcalcap.rename(
    columns={"Value": "avg_kcalcaptday", "Year": "year"}
)
average_kcalcap["avg_kcalcaptyr"] = average_kcalcap["avg_kcalcaptday"] * 365


# In[105]:


average_kcalcap


# <a id="task_5_item_2.2"></a>

# <font color='blue'> Creating a subset from dataframe *food_plant_total_by_year*, which contains data of total global domestic calories supply by plant food and global domestic protein supply by plant food.</font>

# In[106]:


population_fed_by_crops = food_plant_total_by_year[["dom_sup_kcal", "dom_sup_kgprot"]]
population_fed_by_crops.reset_index(inplace=True)
population_fed_by_crops


# <font color='blue'>Joining average calories intake data with *population_fed_by_crops*.</font>

# In[107]:


population_fed_by_crops = population_fed_by_crops.join(
    average_kcalcap["avg_kcalcaptyr"]
)


# In[108]:


population_fed_by_crops


# <font color='blue'>Calculating potential number of people fed by plant food in terms of calories.</font>

# In[109]:


population_fed_by_crops["population_fed_kcal"] = (
    population_fed_by_crops["dom_sup_kcal"] / population_fed_by_crops["avg_kcalcaptyr"]
)
population_fed_by_crops["population_fed_kcal"] = population_fed_by_crops[
    "population_fed_kcal"
].map(int)


# In[110]:


population_fed_by_crops


# <font color='blue'>Now moving onto potential number of people fed by plant food, in terms of protein. An external source states that an average person needs 51g of protein per kilogram of body weight day. Multiply by average body weight 62kg (according to external source). [Click here to view the information source.](https://www.webmd.com/food-recipes/protein)<br>  
# Adding this information to the dataset *population_fed_by_crops*.</font>

# In[111]:


population_fed_by_crops.insert(
    4, "avg_protkgcaptyr", [(51 / 1000) * 365, (51 / 1000) * 365]
)


# In[112]:


population_fed_by_crops


# In[113]:


population_fed_by_crops["population_fed_prot"] = (
    population_fed_by_crops["dom_sup_kgprot"]
    / population_fed_by_crops["avg_protkgcaptyr"]
)
population_fed_by_crops["population_fed_prot"] = population_fed_by_crops[
    "population_fed_prot"
].map(int)


# In[114]:


population_fed_by_crops


# <font color='blue'>in proportion to world's population...</font>

# In[115]:


world_population_20142018


# In[116]:


population_fed_by_crops["proportion_kcal"] = (
    population_fed_by_crops["population_fed_kcal"] / world_population_20142018["Value"]
)
population_fed_by_crops["proportion_protein"] = (
    population_fed_by_crops["population_fed_prot"] / world_population_20142018["Value"]
)


# In[117]:


population_fed_by_crops


# <hr style="border:1px solid blalck"> </hr>

# Question: how many humans could be fed with the global food supply? Give the results in terms of calories and protein. Express these two results as a percentage of the world's population.

# <font color='blue'>
# The answer to this question is the following formula expressed in calories and protein: <br>
# global food supply / average food requirement per person<br>
# Calorie and protein requirement is already available from previous task. What is missing is data of global food supply in calories and protein.
# </font>

# <font color='blue'>First need to get data of global food supply in calories and protein by year. Using the table *food*.</font>

# In[120]:


# Selecting only relevant columns 'year', 'food_supply_kg', 'ratio_kcalkg' and 'protein_percentage'.
global_food_kcal_protein_by_year = food[
    ["year", "food_supply_kg", "ratio_kcalkg", "protein_percentage"]
]
global_food_kcal_protein_by_year


# <font color='blue'>
# Calculalting food supply in terms of calories and proteins.<br>
#     food_supply_kcal = food_supply_kg * ratio_kcalkg<br>
#     food_supply_protein = food_supply_kg * protein_percentage<br>
# </font>

# In[121]:


global_food_kcal_protein_by_year["food_supply_kcal"] = (
    global_food_kcal_protein_by_year["food_supply_kg"]
    * global_food_kcal_protein_by_year["ratio_kcalkg"]
)
global_food_kcal_protein_by_year["food_supply_protein"] = (
    global_food_kcal_protein_by_year["food_supply_kg"]
    * global_food_kcal_protein_by_year["protein_percentage"]
)


# In[122]:


global_food_kcal_protein_by_year


# <font color='blue'> Dropping irelevant columns to simplify work.</font>

# In[123]:


global_food_kcal_protein_by_year = global_food_kcal_protein_by_year.drop(
    columns=["food_supply_kg", "ratio_kcalkg", "protein_percentage"]
)
global_food_kcal_protein_by_year


# <font color='blue'>Replacing 'inf' cells with NaN, to avoid errors with .groupby / .sum method
# </font>

# In[124]:


global_food_kcal_protein_by_year = global_food_kcal_protein_by_year.replace(
    [np.inf, -np.inf], np.nan
)


# In[125]:


global_food_kcal_protein_by_year = global_food_kcal_protein_by_year.groupby(
    "year"
).sum()
global_food_kcal_protein_by_year = global_food_kcal_protein_by_year.reset_index()
global_food_kcal_protein_by_year


# <font color='blue'> Retriving average calorie and protein requirement data from previous task. Using table *population_fed_by_crops*. </font>

# In[126]:


population_fed_by_crops


# In[127]:


average_kcal_protein_intake_captyr = population_fed_by_crops[
    ["year", "avg_kcalcaptyr", "avg_protkgcaptyr"]
]
average_kcal_protein_intake_captyr


#  <font color='blue'>Create a table with the number of people potentially by global food supply, in terms of calories and protein, using tables *average_kcal_protein_intake_captyr* and *global_food_kcal_protein_by_year*. </font>

# In[128]:


average_kcal_protein_intake_captyr


# In[129]:


global_food_kcal_protein_by_year


# In[130]:


global_food_kcal_protein_by_year["population_fed_kcal"] = (
    global_food_kcal_protein_by_year["food_supply_kcal"]
    / average_kcal_protein_intake_captyr["avg_kcalcaptyr"]
)
global_food_kcal_protein_by_year["population_fed_protein"] = (
    global_food_kcal_protein_by_year["food_supply_protein"]
    / average_kcal_protein_intake_captyr["avg_protkgcaptyr"]
)
global_food_kcal_protein_by_year


# <font color='blue'>
# Expressing these two results as a percentage of the world's population.<br>
# First, recalling world population variables.
# </font>

# In[131]:


world_population_20142018


# In[132]:


global_food_kcal_protein_by_year["world_population"] = world_population_20142018[
    "Value"
]
global_food_kcal_protein_by_year


# In[133]:


global_food_kcal_protein_by_year["porpotion_against_world_population_kcal"] = (
    global_food_kcal_protein_by_year["population_fed_kcal"]
    / global_food_kcal_protein_by_year["world_population"]
)
global_food_kcal_protein_by_year["porpotion_against_world_population_protein"] = (
    global_food_kcal_protein_by_year["population_fed_protein"]
    / global_food_kcal_protein_by_year["world_population"]
)
global_food_kcal_protein_by_year


# [Back to task overview](#Task_5)

# <hr style="border:1px solid blalck"> </hr>

# <a id="task_5_item_2.4"></a>

# From the collected data on undernutrition, what proportion of the world's population is considered undernourished?

# <font color='blue'>Calculate undernourished population using table *food*, column *undernourish_million*.<br>
# First, take a look at the table again...</font>

# In[134]:


food.head()


# <font color='blue'>Checcking column values...</font>

# In[135]:


food.undernourish_million.value_counts()


# <font color='blue'>Replacing value "<0.1" with "0.09" </font>

# In[136]:


food["undernourish_million"] = food["undernourish_million"].replace("<0.1", 0.09)


# In[137]:


food.undernourish_million.value_counts()


# In[138]:


food["undernourish_million"] = food["undernourish_million"].astype(float)


# In[139]:


undernourish_population = (
    food.groupby(["year", "country"])["undernourish_million"].mean().to_frame()
)
undernourish_population = undernourish_population.reset_index()
undernourish_population


# <font color='blue'>Calculating undernourished population using .groupby and .sum </font>

# In[140]:


undernourish_population = (
    undernourish_population.groupby("year")["undernourish_million"].sum().to_frame()
)
undernourish_population = undernourish_population.reset_index()
undernourish_population


# <font color='blue'>Multiply result number by one million... </font>

# In[141]:


undernourish_population["undernourish_million"] = (
    undernourish_population["undernourish_million"] * 1000000
)
undernourish_population = undernourish_population.rename(
    columns={"undernourish_million": "undernourish_population"}
)
undernourish_population


# <font color='blue'>Calculating undernourish percentage, using table *world_population_20142018* .</font>

# In[142]:


world_population_20142018


# In[143]:


undernourish_population["undernourish_population_percentage"] = (
    undernourish_population["undernourish_population"]
    / world_population_20142018["Value"]
)
undernourish_population


# [Back to task overview](#Task_5)

# <hr style="border:1px solid blalck"> </hr>

# Question: considering the 25 items most exported by the countries with a high rate of undernutrition, which three of them:
# - have the greatest other_uses to domestic_supply_quantity ratio and what are they used for?
# - have the greatest feed to (food+feed) ratio and what are they used for?

# <font color='blue'>Create a subset of the main table *food*, which contains the 25 items most exported by undernourished countries for 2014/ 2018. The item lists are from previous task ( *top_25_export_by_undernourished_countries_2014* & *top_25_export_by_undernourished_countries_2018*).</font>

# In[145]:


top_25_export_by_undernourished_countries_2014


# <font color='blue'>Selecting items from table *food* that are the 25 most exported by undernurished countries.</font>

# In[146]:


top_25_item_exp_by_undernour_2014 = food[
    (food["year"] == "2014")
    & (
        food["item_code"].isin(
            top_25_export_by_undernourished_countries_2014["item_code"]
        )
    )
]
top_25_item_exp_by_undernour_2018 = food[
    (food["year"] == "2018")
    & (
        food["item_code"].isin(
            top_25_export_by_undernourished_countries_2018["item_code"]
        )
    )
]


# In[147]:


top_25_item_exp_by_undernour_2014


# <font color='blue'>Joinning 2014 and 2018 tables together.</font>

# In[148]:


top_25_item_exp_by_undernour = top_25_item_exp_by_undernour_2014.append(
    top_25_item_exp_by_undernour_2018
)


# In[149]:


top_25_item_exp_by_undernour


# <font color='blue'>Selecting columns relevant to the task at hand... </font>

# In[150]:


top_25_item_exp_by_undernour.columns


# In[151]:


top_25_item_exp_by_undernour = top_25_item_exp_by_undernour[
    [
        "item_code",
        "item",
        "year",
        "domestic_supply_quantity",
        "other_uses",
        "feed",
        "food",
        "losses",
        "processing",
        "production",
        "residuals",
        "seed",
    ]
]
top_25_item_exp_by_undernour


# <font color='blue'>Group by year/ item.</font>

# In[152]:


top_3_otheruse_domsupply_ratio = top_25_item_exp_by_undernour.groupby(
    ["item_code", "item", "year"]
).sum()
top_3_otheruse_domsupply_ratio


# <font color='blue'>To get other_uses to domestic_supply_quantity ratio.</font>

# In[153]:


top_3_otheruse_domsupply_ratio["otheruse_domsupply_ratio"] = (
    top_3_otheruse_domsupply_ratio["other_uses"]
    / top_3_otheruse_domsupply_ratio["domestic_supply_quantity"]
)
top_3_otheruse_domsupply_ratio


# <font color='blue'>Sort table by other_uses to domestic_supply_quantity ratio, per year, in descending order:</font>

# In[154]:


top_3_otheruse_domsupply_ratio.reset_index(inplace=True)
top_3_otheruse_domsupply_ratio.sort_values(
    by="otheruse_domsupply_ratio", ascending=False
).head(6)


# <font color='blue'>
# What are they used for?<br>
# Alcohol: unknown<br>
# Oilcrops: unknown<br>
# Palm Oil: processing/feed
# </font> 

# Question: the greatest feed to (food+feed) ratio and what are they used for?

# <font color='blue'>Again working with table *top_25_item_exp_by_undernour*, creating variable feed / (food+feed) for each item/ year pairing.</font>

# In[155]:


top_25_item_exp_by_undernour.head()


# In[156]:


feed_to_foodfeed_ratio = top_25_item_exp_by_undernour.groupby(
    ["item_code", "item", "year"]
).sum()
feed_to_foodfeed_ratio


# In[157]:


feed_to_foodfeed_ratio["ratio"] = feed_to_foodfeed_ratio["feed"] / (
    feed_to_foodfeed_ratio["food"] + feed_to_foodfeed_ratio["feed"]
)
feed_to_foodfeed_ratio


# <font color='blue'>Items with the highest feed / (food+feed) ratio are: </font>

# In[158]:


feed_to_foodfeed_ratio.sort_values(by="ratio", ascending=False)


# <font color='blue'> 
# They are used for:
#     Maize and products: feed / losses / prodction / seed<br>
#     Pelagic Fish: feed / production / seed<br>
#     Pulses: feed / losses / production<br>
# </font>

# <hr style="border:1px solid blalck"> </hr>

# Question: taking only grains (cereals) for food and feed into account, what proportion (in terms of weight) is used for feed?

# <font color='blue'>First, a table with only cereals products data are shown. I found on FAO the list of cereals products. They are: 2520 / 
# 2518 / 
# 2517 / 
# 2516 / 
# 2515 / 
# 2514 / 
# 2513 / 
# 2805 / 
# 2511.</font>

# In[159]:


food.head()


# In[160]:


cereals = food[
    food["item_code"].isin([2520, 2518, 2517, 2516, 2515, 2514, 2513, 2805, 2511])
]
cereals


# <font color='blue'>Replacing zeros and inf values with NaN.</font>

# In[161]:


cereals = cereals.replace(0, np.nan)
cereals = cereals.replace([np.inf, -np.inf], np.nan)


# In[162]:


cereals_food_feed_ratio = cereals.groupby("year")["food", "feed"].sum()
cereals_food_feed_ratio


# <font color='blue'>The ratios per year are:</font>

# In[163]:


cereals_food_feed_ratio["ratio"] = cereals_food_feed_ratio["feed"] / (
    cereals_food_feed_ratio["food"] + cereals_food_feed_ratio["feed"]
)
cereals_food_feed_ratio


# <hr style="border:1px solid blalck"> </hr>

# Question: how many tons of grains (cereals) could be released if the US reduced its production of animal products by 10%? Convert this quantity to kcal, and the number of potentially fed humans.

# <font color='blue'>The answer is 10% of the the feed amount from cereals in the US, converted to kcal, then divid by average person calorie requirement. <br>
# </font>

# In[164]:


average_kcalcap


# <font color='blue'>Now let's find out how much is 10% of US_cereal_feed.</font>

# In[165]:


US_cereals = food[
    (food["country"] == "United States of America")
    & (food["item_code"].isin([2520, 2518, 2517, 2516, 2515, 2514, 2513, 2805, 2511]))
]
US_cereals


# <font color='blue'>Creating a new variable for this table which convert feed from kg to kcal.</font>

# In[166]:


US_cereals["feed_kcal"] = US_cereals["feed"] * 1000000 * US_cereals["ratio_kcalkg"]


# <font color='blue'>Group table by year, then sum up feed amount in kcal.</font>

# In[167]:


US_cereals_feed_ten_percent = US_cereals.groupby("year")["feed_kcal"].sum().to_frame()
US_cereals_feed_ten_percent.reset_index(inplace=True)
US_cereals_feed_ten_percent


# <font color='blue'>10% of that is...</font>

# In[168]:


US_cereals_feed_ten_percent["ten_percent_kcal"] = (
    US_cereals_feed_ten_percent["feed_kcal"] * 0.1
)
US_cereals_feed_ten_percent


# <font color='blue'>So how many people can that amount of calorie feed?</font>

# In[169]:


US_cereals_feed_ten_percent["population_fed"] = (
    US_cereals_feed_ten_percent["ten_percent_kcal"] / average_kcalcap["avg_kcalcaptyr"]
)
US_cereals_feed_ten_percent


# <hr style="border:1px solid blalck"> </hr>

# Questiohn: in Thailand, what proportion of cassava is exported? What is the proportion of undernutrition?

# <font color='blue'>Find out proportion of cassava (item_code: 2532) export in Thailand.</font>

# In[170]:


thai_cassava = food[(food["item_code"] == 2532) & (food["country"] == "Thailand")]
thai_cassava


# In[171]:


thai_cassava_exp_proportion = thai_cassava["export_quantity"] / (
    thai_cassava["production"] + thai_cassava["import_quantity"]
)
thai_cassava_exp_proportion


# <font color='blue'>Porpotion of undernutrition, data given by Food Security Indicator table.</font>

# In[172]:


thai_undernourish = thai_cassava["undernourish_percent"]
thai_undernourish


# The end. <br>
# Thank you.

# <hr style="border:1.5px solid blalck"> </hr>
