#!/bin/bash

source env/bin/activate

if [ ! -f "../data/$(date +%Y%m%d)_Dundee City.csv" ]; then
	./scrape_phs_covid.py
fi

./plot_city.py 'Dundee City'
./plot_city.py 'Glasgow City'
./plot_city.py 'East Dunbartonshire'

convert -trim "../images/Dundee City.png" "../images/Dundee_City.jpg"
convert -trim "../images/Glasgow City.png" "../images/Glasgow_City.jpg"
convert -trim "../images/East Dunbartonshire.png" "../images/East_Dunbartonshire.jpg"

./upload_images.sh
