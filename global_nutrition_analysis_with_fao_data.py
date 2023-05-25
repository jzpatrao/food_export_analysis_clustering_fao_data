#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Data-Cleaning" data-toc-modified-id="Data-Cleaning-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Data Cleaning</a></span></li><li><span><a href="#New-variables" data-toc-modified-id="New-variables-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>New variables</a></span><ul class="toc-item"><li><span><a href="#great_import_from_undern_countries" data-toc-modified-id="great_import_from_undern_countries-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>great_import_from_undern_countries</a></span></li></ul></li><li><span><a href="#Identify-major-trends" data-toc-modified-id="Identify-major-trends-3"><span class="toc-item-num">3&nbsp;&nbsp;</span>Identify major trends</a></span></li></ul></div>

# * Project description

# In[14]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# In[3]:


# Get the current working directory
current_directory = os.getcwd()

# Read the CSV file into a DataFrame
veg_2014 = pd.read_csv(os.path.join(current_directory, "veg_2014.csv"))
veg_2018 = pd.read_csv(os.path.join(current_directory, "veg_2018.csv"))
veg = veg_2014.append(veg_2018)


# In[4]:


veg.head()


# In[5]:


# Import dataset of animal based food
ani = pd.read_csv(os.path.join(current_directory, "ani.csv"))
ani.head()


# <a id="task_2_item_1"></a>

# In[6]:


# Create a new column 'primary_key' for table 'veg'. It is the combination of 'Area Code', 'Element Code', 'Item Code', and 'Year'.
veg["primary_key"] = veg["Area Code (FAO)"].astype(str) + veg["Element Code"].astype(str) + veg["Item Code"].astype(str) + veg["Year"].astype(str)
veg.set_index("primary_key", verify_integrity=True)


# In[7]:


# Create a new column 'primary_key' for table 'ani'. It is the combination of 'Area Code', 'Element Code', 'Item Code', and 'Year'.
ani["primary_key"] = ani["Area Code (FAO)"].astype(str) + ani["Element Code"].astype(str) + ani["Item Code"].astype(str) + ani["Year"].astype(str)
ani.set_index("primary_key", verify_integrity=True)


# In[8]:


# Import the dataset downloaded from FAO, containing total population number of each country from 1950 till 2018.
population = pd.read_csv(os.path.join(current_directory,"population.csv"))
population.head()


# In[9]:


# Select data for the years 2014 and 2018.
population_20142018 = population[population["Year"].isin([2014, 2018])]

population_20142018.head()


# In[10]:


# Calculate global population per year using groupby and sum.
global_population = population_20142018.groupby("Year")["Value"].sum()
global_population


# In[12]:


# Identify potential duplicated big values by creating a separate table of countries with population over 1 billion.
pop_big = population_20142018[population_20142018["Value"] > 1000000]
pop_big


# Mainland China's population is accounted for twice for each year since *'China'* and *'China mainland*' both show up in the result set.<br> 
#     Deleting *'China'* population (Area Code *351*) as it contains already mainland population plus Hongkong, Macao and Taiwan population.

# In[18]:


# Removing the duplicated entry for China population
population_20142018 = population_20142018[population_20142018["Area Code (FAO)"] != 351]
population_20142018.groupby("Year")["Value"].sum()


# In[23]:


world_population_20142018 = (
    population_20142018.groupby("Year")["Value"].sum().to_frame()
)
world_population_20142018.reset_index(inplace=True)
world_population_20142018


# In[24]:


# Multiplying result by 1000 as per FAO unit instruction 
world_population_20142018["Value"] = world_population_20142018["Value"] * 1000
world_population_20142018


# In[26]:


# Creating variables for total world population for 2014 and 2018, for future use.
world_population_total_2014 = world_population_20142018.iloc[0, 1]
world_population_total_2018 = world_population_20142018.iloc[1, 1]

print(f"World population 2014: {world_population_total_2014}")
print(f"World population 2018: {world_population_total_2018}")


# Identify relations between variables: Domestic supply quantity, Production, Import Quantity, Stock Variation and Export Quantity.

# In[20]:


ani.Element.value_counts()


# Looking at the elemant description, in combination with definition description from FAO, I would suspect that:<br> 
#     - Domestic supply quantity = Food supply quantity + Feed + Seed + Losses + Processing + Other uses + Residuals <br>
# also<br>
#     - Domestic supply quantity = Production + Import Quantity + Stock Variation - Export Quantity

# Let's verify above theory with an example: wheat (item code 2511) ~ France.

# In[19]:


wheat_in_france = veg[(veg["Item Code"] == 2511) & (veg["Area"] == "France")]
wheat_in_france.head()


# In[27]:


wheat_in_france = wheat_in_france.pivot_table(
    index=("Year"), columns="Element", values="Value", aggfunc="sum"
)
wheat_in_france


# In[28]:


# electing relavent columns from *wheat_in_france* to make calculation easier to read.
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


# Verifying if the following equation is true:<br>
# Domestic supply quantity = Food supply quantity + Feed + Seed + Losses + Processing + Other uses + Residuals

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


# Equation checks out.

# Verifying if the second equation is true:<br>
# Domestic supply quantity = Production + Import Quantity + Stock Variation - Export Quantity

# In[30]:


wheat_in_france["compare"] = (
    wheat_in_france["Production"]
    + wheat_in_france["Import Quantity"]
    + wheat_in_france["Stock Variation"].abs()
    - wheat_in_france["Export Quantity"]
)
wheat_in_france


# Result values in column 'compare' are slightly different from 'Domestic supply quantity', but within acceptable range. This might be a mathematical discrepancy.

# <a id='Task_3'></a>

# # Data Cleaning
# Add variable ‘origin’ to tables *veg* and *ani*. Appends *veg* and *ani* to one table *temp*. Renaming of *temp* s columns with Laura's guideline in mind. Transformation of *temp* to a pivot table so that the elements are now columns of the new table. Renaming columns according to Laura's guideline: lower-case, no spaces (use underscore instead), no special characters, no accented characters.
# Index columns need to be normal columns. Rename table *food*. <br>
# From now on, table *food* will be the main table I work with.

# In[31]:


# Add variable ‘origin’
ani["origin"] = "animal"
veg["origin"] = "vegetal"


# In[34]:


# Appends veg and ani to one table
df_temp = ani.append(veg)
df_temp.head()


# In[36]:


# Rename columns
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


# In[37]:


# Pivot dataframe so that entries in elements becomes columns 
data = df_temp.pivot_table(
    index=["country_code", "country", "item_code", "item", "year", "origin"],
    columns=["element"],
    values=["value"],
    aggfunc=sum,
)
data.head()


# In[39]:


# Renaming of data’s columns 
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


# In[41]:


# Reset index
food = data.reset_index()
food.head()


# # New variables 

# In[45]:


population_20142018_pivot = population_20142018.pivot_table(
    index=(["Area Code (FAO)", "Area", "Year"]), columns="Element", values="Value"
)
population_20142018_to_be_merged = population_20142018_pivot.reset_index()
population_20142018_to_be_merged


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

food.head()


# In[48]:


# food_supply_kcal = food_supply_kcalcapitaday * population * 365
food["food_supply_kcal"] = food["food_supply_kcalcapitaday"] * food["population"] * 365


# In[49]:


# food_supply_kgprotein = protein_supply_quantity_gcapitaday / 1000 * population * 365
food["food_supply_kgprotein"] = (
    food["protein_supply_quantity_gcapitaday"] / 1000 * food["population"] * 365
)


# In[51]:


# food_supply_kg =  food supply expressed in kg
food["food_supply_kg"] = food["food"] * 1000000
food[["country", "year", "food_supply_kg"]].head()


# <a id='task_4_item_3'></a>

# In[53]:


# ratio_kcalkg = food_supply_kcal / food_supply_kg
food["ratio_kcalkg"] = food["food_supply_kcal"] / food["food_supply_kg"]


# In[54]:


# protein_percentage = food_supply_kgprotein / food_supply_kg 
food["protein_percentage"] = food["food_supply_kgprotein"] / food["food_supply_kg"]


# In[55]:


food[["country", "year", "ratio_kcalkg", "protein_percentage"]].head()


# In[56]:


# dom_sup_kcal = domestic_supply_quantity * 1000000 * ratio_kcalkg <br>
# dom_sup_kgprot = domestic_supply_quantity * 1000000 * protein_percentage
food["dom_sup_kcal"] = food["domestic_supply_quantity"] * 1000000 * food["ratio_kcalkg"]
food["dom_sup_kgprot"] = (
    food["domestic_supply_quantity"] * 1000000 * food["protein_percentage"]
)


# ## great_import_from_undern_countries
# A boolean variable - do the 200 highest imports of the 25 most
# exported items come from countries with more than 10% malnourishment?

# In[59]:


# Import food security indicator dataset downloaded from FAO website.
food_secu = pd.read_csv(os.path.join(current_directory, "food_security_indicators.csv"))
food_secu.head()


# In[60]:


# Select relevent columns
food_secu = food_secu[
    ["Area Code (FAO)", "Area", "Item Code", "Item", "Year", "Unit", "Value"]
]

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


# In[65]:


# Values in column *'item'* turns into columns
food_secu_pivot = food_secu.pivot_table(index=["country_code", "country", "year"], values=["value", "unit"], columns="item")
food_secu_pivot.columns = food_secu_pivot.columns.droplevel(0)
food_secu_pivot.head()


# In[67]:


food_secu_subset = food_secu_pivot.reset_index()
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

food_secu_subset.drop(columns=["col1", "col2"], axis=1, inplace=True)

food_secu_subset.head()


# In[72]:


# Inserting undernourish data into table *food*.
food["country_code"] = food["country_code"].astype(str)
food["year"] = food["year"].astype(str)
food_secu_subset["country_code"] = food_secu_subset["country_code"].astype(str)
food_secu_subset["year"] = food_secu_subset["year"].astype(str)
food = pd.merge(
    food, food_secu_subset, on=["country", "country_code", "year"], how="inner"
)

food.head()


# In[74]:


# Identify countries with undernourishement of 10%.
food["undernourish_percent"] = food["undernourish_percent"].replace("<2.5", "2.0")
food["undernourish_percent"] = food["undernourish_percent"].astype(float)

undernourish_country = food[food["undernourish_percent"] > 10]
undernourish_country.head()


# In[78]:


# Identify contries with top undernourishment percentage
undernourish_country = undernourish_country.sort_values(
    by="undernourish_percent", ascending=False
)

print(f"Countries with undernourishment population over 10% of total population: \n{undernourish_country.country.unique().item()}")


# In[79]:


# Groupby table *undernourish_country* by year/item, then sort by export_quantity to identify top 25 most exported items.
top_25_export_by_undernourished_countries = (
    undernourish_country.groupby(["item_code", "item", "year"])["export_quantity"]
    .sum()
    .sort_values(ascending=False)
    .to_frame()
)
top_25_export_by_undernourished_countries.reset_index(inplace=True)
top_25_export_by_undernourished_countries.head()


# In[81]:


# Identify the top 25 most exported items by undernourished countries in year 2014.
top_25_export_by_undernourished_countries_2014 = top_25_export_by_undernourished_countries[
    top_25_export_by_undernourished_countries["year"] == "2014"
]
top_25_export_by_undernourished_countries_2014 = top_25_export_by_undernourished_countries_2014.sort_values(
    by="export_quantity", ascending=False
).head(
    25
)
print(f"The top 25 most exported items by undernourished countries in 2014: \n{top_25_export_by_undernourished_countries_2014}")


# In[82]:


# Identify the top 25 most exported items by undernourished countries in year 2018.
top_25_export_by_undernourished_countries_2018 = top_25_export_by_undernourished_countries[
    top_25_export_by_undernourished_countries["year"] == "2018"
]
top_25_export_by_undernourished_countries_2018 = top_25_export_by_undernourished_countries_2018.sort_values(
    by="export_quantity", ascending=False
).head(
    25
)
print(f"The top 25 most exported items by undernourished countries in 2018: \n{top_25_export_by_undernourished_countries_2018}")


# In[83]:


# the 200 highest import quantities among these 25 items
food_subset2 = food[
    food["item_code"].isin(top_25_export_by_undernourished_countries["item_code"])
]
food_subset2.head()


# In[85]:


top_200_import = (
    food_subset2.groupby(["country", "year"], as_index=False)
    .import_quantity.sum()
    .sort_values(by="import_quantity", ascending=False)
    .head(200)
)
top_200_import.head()


# In[87]:


# For the 200 corresponding lines in table *food*, set “True” for the variable, and “False” for the other lines.
food["great_import_from_undern_countries"] = np.where(
    food.index.isin(top_200_import.index), True, False
)

food["great_import_from_undern_countries"].value_counts()


# # Identify major trends 

# Question: considering only plant products, what proportion of the global domestic supply is used as :<br>
# food<br>
# feed<br>
# losses<br>
# other uses<br>

# In[90]:


# Creating a subset of dataframe *food* that contain only plant products.
food_plant = food[food["origin"] == "vegetal"]
food_plant.head()


# In[92]:


# Keeping only relevant columns
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


# In[94]:


# Replacing zeros and inf  with NaN 
food_plant = food_plant.replace(0, np.nan)
food_plant = food_plant.replace([np.inf, -np.inf], np.nan)


# In[96]:


# Group dataframe by year then sum up values for all columns
food_plant_total_by_year = food_plant.groupby(["year"]).sum()
food_plant_total_by_year


# In[97]:


# Calculating propotions of each element by dividing each element agains domestic supply quantity
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

food_plant_total_by_year


# <hr style="border:1px solid blalck"> </hr>

# The number of humans on earth could be fed if all the plant-based food supply (crops), including food and feed, was used for human consumption. <br>
# i.e domestic_supply_plant_kcal / average_kcalcapitayear

# In[99]:


avg_dietary_energy = pd.read_csv(os.path.join(current_directory,"Average_dietary_energy_requirement.csv"))
avg_dietary_energy.head()


# In[101]:


average_kcalcap = avg_dietary_energy.groupby("Year")["Value"].mean().round(2).to_frame()
average_kcalcap


# In[103]:


average_kcalcap.reset_index(inplace=True)
average_kcalcap = average_kcalcap.rename(
    columns={"Value": "avg_kcalcaptday", "Year": "year"}
)
average_kcalcap["avg_kcalcaptyr"] = average_kcalcap["avg_kcalcaptday"] * 365
average_kcalcap


# Creating a subset from dataframe *food_plant_total_by_year*, which contains data of total global domestic calories supply by plant food and global domestic protein supply by plant food.

# In[106]:


# As its name suggest, this shows the population that can be fed by crops
population_fed_by_crops = food_plant_total_by_year[["dom_sup_kcal", "dom_sup_kgprot"]]
population_fed_by_crops.reset_index(inplace=True)

population_fed_by_crops = population_fed_by_crops.join(
    average_kcalcap["avg_kcalcaptyr"]
)

population_fed_by_crops["population_fed_kcal"] = (
    population_fed_by_crops["dom_sup_kcal"] / population_fed_by_crops["avg_kcalcaptyr"]
)
population_fed_by_crops["population_fed_kcal"] = population_fed_by_crops[
    "population_fed_kcal"
].map(int)

population_fed_by_crops


# Now moving onto potential number of people fed by plant food, in terms of protein. An external source states that an average person needs 51g of protein per kilogram of body weight day. Multiply by average body weight 62kg (according to external source). [Click here to view the information source.](https://www.webmd.com/food-recipes/protein)<br>  
# Adding this information to the dataset *population_fed_by_crops*.

# In[111]:


population_fed_by_crops.insert(
    4, "avg_protkgcaptyr", [(51 / 1000) * 365, (51 / 1000) * 365]
)

population_fed_by_crops["population_fed_prot"] = (
    population_fed_by_crops["dom_sup_kgprot"]
    / population_fed_by_crops["avg_protkgcaptyr"]
)
population_fed_by_crops["population_fed_prot"] = population_fed_by_crops[
    "population_fed_prot"
].map(int)

# In proportion to world's population
population_fed_by_crops["proportion_kcal"] = (
    population_fed_by_crops["population_fed_kcal"] / world_population_20142018["Value"]
)
population_fed_by_crops["proportion_protein"] = (
    population_fed_by_crops["population_fed_prot"] / world_population_20142018["Value"]
)


population_fed_by_crops


# The number of humans could be fed with the global food supply? Give the results in terms of calories and protein. 
# i.e. global food supply / average food requirement per person

# In[120]:


# Selecting only relevant columns 'year', 'food_supply_kg', 'ratio_kcalkg' and 'protein_percentage'.
global_food_kcal_protein_by_year = food[
    ["year", "food_supply_kg", "ratio_kcalkg", "protein_percentage"]
]
global_food_kcal_protein_by_year


# In[121]:


# food supply in terms of calories and proteins
# food_supply_kcal = food_supply_kg * ratio_kcalkg
# food_supply_protein = food_supply_kg * protein_percentage
global_food_kcal_protein_by_year["food_supply_kcal"] = (
    global_food_kcal_protein_by_year["food_supply_kg"]
    * global_food_kcal_protein_by_year["ratio_kcalkg"]
)
global_food_kcal_protein_by_year["food_supply_protein"] = (
    global_food_kcal_protein_by_year["food_supply_kg"]
    * global_food_kcal_protein_by_year["protein_percentage"]
)

global_food_kcal_protein_by_year


# In[123]:


# Dropping irelevant columns
global_food_kcal_protein_by_year = global_food_kcal_protein_by_year.drop(
    columns=["food_supply_kg", "ratio_kcalkg", "protein_percentage"]
)

# Replacing 'inf' cells with NaN
global_food_kcal_protein_by_year = global_food_kcal_protein_by_year.replace(
    [np.inf, -np.inf], np.nan
)

global_food_kcal_protein_by_year = global_food_kcal_protein_by_year.groupby(
    "year"
).sum()
global_food_kcal_protein_by_year = global_food_kcal_protein_by_year.reset_index()

global_food_kcal_protein_by_year


# In[127]:


average_kcal_protein_intake_captyr = population_fed_by_crops[
    ["year", "avg_kcalcaptyr", "avg_protkgcaptyr"]
]
average_kcal_protein_intake_captyr


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


# Expressing these two results as a percentage of the world's population.<br>
# First, recalling world population variables.

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


# From the collected data on undernutrition, what proportion of the world's population is considered undernourished?

# In[135]:


food.undernourish_million.value_counts()


# In[136]:


# Replacing value "<0.1" with "0.09" 
food["undernourish_million"] = food["undernourish_million"].replace("<0.1", 0.09)
food["undernourish_million"] = food["undernourish_million"].astype(float)


# In[137]:


food.undernourish_million.value_counts()


# In[139]:


undernourish_population = (
    food.groupby(["year", "country"])["undernourish_million"].mean().to_frame()
)
undernourish_population = undernourish_population.reset_index()
undernourish_population


# In[140]:


# Groupby year then aggregate
undernourish_population = (
    undernourish_population.groupby("year")["undernourish_million"].sum().to_frame()
)
undernourish_population = undernourish_population.reset_index()

undernourish_population["undernourish_million"] = (
    undernourish_population["undernourish_million"] * 1000000
)
undernourish_population = undernourish_population.rename(
    columns={"undernourish_million": "undernourish_population"}
)

undernourish_population


# In[143]:


# Calculating undernourish percentage
undernourish_population["undernourish_population_percentage"] = (
    undernourish_population["undernourish_population"]
    / world_population_20142018["Value"]
)
undernourish_population


# Now considering the 25 items most exported by the countries with a high rate of undernutrition, which three of them:
# - have the greatest other_uses to domestic_supply_quantity ratio and what are they used for?
# - have the greatest feed to (food+feed) ratio and what are they used for?

# In[146]:


# Selecting items from table *food* that are the 25 most exported by undernurished countries
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

top_25_item_exp_by_undernour_2014


# In[148]:


# Joinning 2014 and 2018 tables together
top_25_item_exp_by_undernour = top_25_item_exp_by_undernour_2014.append(
    top_25_item_exp_by_undernour_2018
)

top_25_item_exp_by_undernour


# In[151]:


# Selecting columns relevant
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
top_25_item_exp_by_undernour.head()


# In[152]:


# Group by year/ item
top_3_otheruse_domsupply_ratio = top_25_item_exp_by_undernour.groupby(
    ["item_code", "item", "year"]
).sum()
top_3_otheruse_domsupply_ratio


# In[153]:


# To get other_uses to domestic_supply_quantity ratio
top_3_otheruse_domsupply_ratio["otheruse_domsupply_ratio"] = (
    top_3_otheruse_domsupply_ratio["other_uses"]
    / top_3_otheruse_domsupply_ratio["domestic_supply_quantity"]
)
top_3_otheruse_domsupply_ratio


# In[154]:


# Sort table by other_uses to domestic_supply_quantity ratio, per year, in descending order
top_3_otheruse_domsupply_ratio.reset_index(inplace=True)
top_3_otheruse_domsupply_ratio.sort_values(
    by="otheruse_domsupply_ratio", ascending=False
).head()


# To answer the question:'what are they used for?', anwsers are:<br>
# Alcohol: unknown<br>
# Oilcrops: unknown<br>
# Palm Oil: processing/feed
# 

# The biggest feed to (food+feed) ratio and what are they used for?

# In[156]:


# Add variable feed / (food+feed) for each item/ year pairing
feed_to_foodfeed_ratio = top_25_item_exp_by_undernour.groupby(
    ["item_code", "item", "year"]
).sum()
feed_to_foodfeed_ratio


# In[157]:


feed_to_foodfeed_ratio["ratio"] = feed_to_foodfeed_ratio["feed"] / (
    feed_to_foodfeed_ratio["food"] + feed_to_foodfeed_ratio["feed"]
)
feed_to_foodfeed_ratio


# In[158]:


# Items with the highest feed / (food+feed) ratio 
feed_to_foodfeed_ratio.sort_values(by="ratio", ascending=False)


# They are used for:
#     Maize and products: feed / losses / prodction / seed<br>
#     Pelagic Fish: feed / production / seed<br>
#     Pulses: feed / losses / production<br>
# 

# Taking only grains (cereals) for food and feed into account, what proportion (in terms of weight) is used for feed?

# In[160]:


# A subset with only cereals products 
cereals = food[
    food["item_code"].isin([2520, 2518, 2517, 2516, 2515, 2514, 2513, 2805, 2511])
]
cereals


# In[161]:


# Replacing zeros and inf values with NaN
#cereals = cereals.replace(0, np.nan)
cereals = cereals.replace([np.inf, -np.inf], np.nan)


# In[162]:


cereals_food_feed_ratio = cereals.groupby("year")["food", "feed"].sum()
cereals_food_feed_ratio


# In[163]:


# The ratios per year
cereals_food_feed_ratio["ratio"] = cereals_food_feed_ratio["feed"] / (
    cereals_food_feed_ratio["food"] + cereals_food_feed_ratio["feed"]
)
cereals_food_feed_ratio


# <hr style="border:1px solid blalck"> </hr>

# Question: how many tons of grains (cereals) could be released if the US reduced its production of animal products by 10%? Convert this quantity to kcal, and the number of potentially fed humans. <br>
# i.e. 10% of the the feed amount from cereals in the US, converted to kcal, then divid by average person calorie requirement

# In[165]:


# 10% of US_cereal_feed
US_cereals = food[
    (food["country"] == "United States of America")
    & (food["item_code"].isin([2520, 2518, 2517, 2516, 2515, 2514, 2513, 2805, 2511]))
]
US_cereals


# In[166]:


# Add a variable that convert feed from kg to kcal
US_cereals["feed_kcal"] = US_cereals["feed"] * 1000000 * US_cereals["ratio_kcalkg"]


# In[167]:


# Group table by year, then sum up feed amount in kcal.
US_cereals_feed_ten_percent = US_cereals.groupby("year")["feed_kcal"].sum().to_frame()
US_cereals_feed_ten_percent.reset_index(inplace=True)
US_cereals_feed_ten_percent


# In[168]:


# Calculate 10 percent
US_cereals_feed_ten_percent["ten_percent_kcal"] = (
    US_cereals_feed_ten_percent["feed_kcal"] * 0.1
)
US_cereals_feed_ten_percent


# In[169]:


# The amount of humans that amount of calories can feed
US_cereals_feed_ten_percent["population_fed"] = (
    US_cereals_feed_ten_percent["ten_percent_kcal"] / average_kcalcap["avg_kcalcaptyr"]
)
US_cereals_feed_ten_percent


# Questiohn: in Thailand, what proportion of cassava is exported? What is the proportion of undernutrition?

# In[170]:


# proportion of cassava (item_code: 2532) export in Thailand.
thai_cassava = food[(food["item_code"] == 2532) & (food["country"] == "Thailand")]

thai_cassava_exp_proportion = thai_cassava["export_quantity"] / (
    thai_cassava["production"] + thai_cassava["import_quantity"]
)
thai_cassava_exp_proportion


# In[172]:


# Porpotion of undernutrition in Thailand
thai_undernourish = thai_cassava["undernourish_percent"]
thai_undernourish


# The end. <br>
# Thank you.
