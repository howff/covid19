#!/bin/bash

for cityname in 'Aberdeen City' \
 'Aberdeenshire' \
 'Angus' \
 'Argyll and Bute' \
 'City of Edinburgh' \
 'Clackmannanshire' \
 'Dumfries and Galloway' \
 'Dundee City' \
 'East Ayrshire' \
 'East Dunbartonshire' \
 'East Lothian' \
 'East Renfrewshire' \
 'Falkirk' \
 'Fife' \
 'Glasgow City' \
 'Highland' \
 'Inverclyde' \
 'Midlothian' \
 'Moray' \
 'Na h-Eileanan Siar' \
 'North Ayrshire' \
 'North Lanarkshire' \
 'Orkney Islands' \
 'Perth and Kinross' \
 'Renfrewshire' \
 'Scottish Borders' \
 'Shetland Islands' \
 'South Ayrshire' \
 'South Lanarkshire' \
 'Stirling' \
 'West Dunbartonshire' \
 'West Lothian'; do

  ./filter_iz_shapefile_to_city.py "$cityname"

done
