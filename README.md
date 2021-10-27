# Welcome to tennis_stats!

This is a collection of CLI tools to scrape and analyse tennis players 
player statistics as can be found on wikipedia.

## Intro

There are two main use-cases for the CLI:

1. Scrape wikipedia using the command `generatedataframe` to generate a new dataframe and perform
data analysis.

2. Use a ready-made dataframe scraped from wikipedia on 22.10.2021
and perform data analysis.  The ready-made dataframe was scraped
   using the same `generatedataframe` command from our CLI.
   

### 1. Scrape wikipedia
Before scraping one may set the following parameters:

playergender, earliest ...

The default settings for the parameters are:

To check the current settings use ...

This will generate a pandas dataframe with the following columns:

The data sources are these tables for the player names and wikilinks
The career record,.. are from the player card of each player

The default earliest birth year of 1950 was chosen to maximise 
the amount of available information.

### 2. Use the ready-made dataframe
The ready-made dataframes `tennis_stats/pickled-dataframes/females-final.pkl`
and `tennis_stats/pickled-dataframes/males-final.pkl` were obtained 
as described above with the default settings.

To load these dataframes use the command

```
usedefaultframe female
```
to load the female players dataframe and 

```
usedefaultframe male
```
to load the male players dataframe

### 3. Perform data analysis

#### Frame methods
Filters
#### Analysis
plots