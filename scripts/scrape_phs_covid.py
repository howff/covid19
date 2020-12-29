#!/usr/bin/env python3
# Download the number of cases in the most recent 7 day period
# for each Intermediate Zone in each of the listed regions.
# To do: extract the actual date range of the data from the tooltip text.
# To do: allow the date to be specified so we can go back in time.

import requests
from bs4 import BeautifulSoup
import json
import time
import re
import logging, sys

# Configuration:

# The name must match the dropdown menu in the dashboard
cities_list = [
    { "name": "Dundee City",         "num_iz":  31 },
    { "name": "Glasgow City",        "num_iz": 136 },
    { "name": "East Dunbartonshire", "num_iz":  28 },
    { "name": "Angus",               "num_iz":  26 },
    { "name": "Fife",                "num_iz":  104 },
    { "name": "Perth & Kinross",     "num_iz":  35 } # NB note use of & not 'and'
]

data_host = "https://public.tableau.com"

date_str = time.strftime('%Y%m%d')


# ---------------------------------------------------------------------
# Log to stderr

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------
# Parse the tooltipHtml to extract the population and number of cases

def parse_tooltip_html(ttt_html):
    soup = BeautifulSoup(ttt_html, "html.parser")
    #with open('j.html', 'w') as fd:
    #    fd.write(ttt_html)

    nei_soup = soup.find('span', text='Neighbourhood: ')
    if nei_soup:
        neighbourhood = nei_soup.find_next().text
    pop_soup = soup.find('span', text='Population: ')
    if pop_soup:
        pop = pop_soup.find_next().text
    c_soup = soup.find('span', text='Number of positive cases over 7 days:')
    if c_soup:
        cases = c_soup.find_next().text
        if not re.match(' *[0-9]+ *', cases):
            cases = c_soup.find_next().find_next().text

    neighbourhood = re.sub('^\s+', '', neighbourhood) # leading whitespace
    neighbourhood = re.sub('\s+$', '', neighbourhood) # trailing whitespace
    pop = int(re.sub('[\s,]+', '', pop))              # any spaces or comma
    if re.match('[01]-[234]', cases):                 # match 0-2 and 1-4 etc-
        cases = '2'                                   # PHS fudges the numbers so guess at 2
    cases = int(re.sub('\s+', '', cases))             # any whitespace
    per100k = int(int(cases) * 100000 / int(pop))
    #print(f'{neighbourhood} {pop} {cases} {per100k}')
    return (neighbourhood, pop, cases, per100k)


# ---------------------------------------------------------------------
# Select a new sheet in the workbook

def change_sheet(sheet):
    log.debug(f'POST sheet {sheet}')
    #print('POST sheet_id Cases by neighbourhood')
    r = requests.post(dataUrl, data= { "sheet_id": sheet })
    #print(f'Response {r.status_code}')

# ---------------------------------------------------------------------
# Simulate changing the region from the dropdown menu

def change_region(city_name):
    log.debug(f'POST select {city_name}')
    r = requests.post(f'{data_host}{vizql_root}/sessions/{tableauData["sessionid"]}/commands/tabdoc/set-parameter-value', data= {
        "globalFieldName": "[Parameters].[Parameter 1 1]",
        "valueString": city_name
    })
    #print(f'Response {r.status_code}')



# ---------------------------------------------------------------------
# GET the home page
log.debug('GET Overview')
r = requests.get(
    f"{data_host}/views/COVID-19DailyDashboard_15960160643010/Overview",
    params= {
        ":showVizHome":"no",
    }
)

# Extract the sessionId
soup = BeautifulSoup(r.text, "html.parser")
tableauData = json.loads(soup.find("textarea",{"id": "tsConfigContainer"}).text)
dataUrl = f'{data_host}{tableauData["vizql_root"]}/bootstrapSession/sessions/{tableauData["sessionid"]}'
sheet_id = tableauData["sheetId"] # Overview
vizql_root = tableauData["vizql_root"] # /vizql/w/COVID-19DailyDashboard_15960160643010/v/Overview

# Choose a different sheet
sheet_id = 'Cases by neighbourhood'
change_sheet(sheet_id)
data = []

# Loop through all regions
for city in cities_list:
    city_name = city['name']
    num_iz = city['num_iz']
    csv_name = f'{date_str}_{city_name}.csv'.replace('&', 'and')
    log.info(f'CITY {city_name} getting {num_iz} zones into {csv_name}')
    # Create CSV file
    csv_fd = open(csv_name, 'w')
    csv_fd.write('Per100k,Cases,Pop,IZ\n')

    change_region(city_name)
    data = []

    # Loop through all Intermediate Zones
    for tupleId in range(1, num_iz):
        #print(f'Getting neighbourhood number {tupleId}')
        time.sleep(0.5) #for throttling

        r = requests.post(f'{data_host}{vizql_root}/sessions/{tableauData["sessionid"]}/commands/tabsrv/render-tooltip-server',
            data = {
            "worksheet": "IZ_map",
            "dashboard": "Cases by neighbourhood",
            "tupleIds": f"[{tupleId}]",
            "vizRegionRect": json.dumps({"r":"viz","x":209,"y":267,"w":0,"h":0,"fieldVector":None}),
            "allowHoverActions": "false",
            "allowPromptText": "true",
            "allowWork": "false",
            "useInlineImages": "true"
        })
        ttt = r.json()["vqlCmdResponse"]["cmdResultList"][0]["commandReturn"]["tooltipText"]
        if 'htmlTooltip' in ttt:
            ttt_html = json.loads(ttt)['htmlTooltip']
            neighbourhood, pop, cases, per100k = parse_tooltip_html(ttt_html)
            print('%4d,%3d,%4d,"%s"' % (per100k, cases, pop, neighbourhood))
            csv_fd.write('%4d,%3d,%4d,"%s"\n' % (per100k, cases, pop, neighbourhood))
        else:
            print('ERROR: No htmlTooltip found in response')
            #log.debug(ttt)
    csv_fd.close()

