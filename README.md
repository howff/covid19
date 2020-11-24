# covid19

Experiments in plotting Covid-19 data

## Scrape data from the Public Health Scotland dashboard

The PHS dashboard:

https://public.tableau.com/profile/phs.covid.19#!/vizhome/COVID-19DailyDashboard_15960160643010/Overview

All the data has been made public on this dashboard but I don't like the visualisation so here's a script to scrape the data and visualise it differently. Note that PHS has already reduced the quality of the data to preserve privacy, for example where there's less than 5 cases in a zone they report "1-4" so this script uses a value of 3 instead.

The dashboard divides Scotland into regions (local authorities) and within each region there are Intermediate Zones of roughly equal population. The script queries a subset of the regions (you can modify it with more) and downloads the numbers for each zone into a CSV file. The CSV files are dated so you can run the script each day.

Run `scripts/scrape_phs_covid.py` to scrape the data - three regions are defined in the script but you can change them. It will write one CSV file per region. Each row in the file has four columns: Per100k,Cases,Pop,IZ (cases per 100k population in the last seven days, cases in the last 7 days, population of the IZ, name of the IZ)

## Plotting the data

* (Split the shapefile of intermediate zones into separate files, one for each local authority)
* Load the shapefile of intermediate zones into QGIS
* Load the CSV file as a vector layer
* Open the properties of the shapefile layer and in the Join tab make a join with the CSV layer, using the IZ name as the join key
* Open the layer styling and change from point to categorical, select the newly joined attribute Per100k, change colour, make transparent
* Install the QuickWebMap plugin and use the Web menu to add OSM mapping underneath

## Example

![Glasgow cases per 100k](image/glasgow_IZ_colour_by_casesPer100k-crop.png)

## List of Regions

See the dashboard for the list of regions.

## To do

Turn the visualisation into a script, or even a streamlit web app
