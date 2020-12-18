#!/bin/bash

source env/bin/activate

if [ ! -f "../data/$(date +%Y%m%d)_Dundee City.csv" ]; then
	./scrape_phs_covid.py
        mv $(date +%Y%m%d)_*.csv ../data
fi

./plot_city.py --city 'Dundee City'
./plot_city.py --city 'Glasgow City'
./plot_city.py --city 'East Dunbartonshire'
./plot_city.py --city 'Angus'
./plot_city.py --city 'Fife'
./plot_city.py --city 'Perth and Kinross'

convert -trim "../images/Dundee City.png" "../images/Dundee_City.jpg"
convert -trim "../images/Glasgow City.png" "../images/Glasgow_City.jpg"
convert -trim "../images/East Dunbartonshire.png" "../images/East_Dunbartonshire.jpg"
convert -trim "../images/Angus.png" "../images/Angus.jpg"
convert -trim "../images/Fife.png" "../images/Fife.jpg"
convert -trim "../images/Perth and Kinross.png" "../images/Perth_and_Kinross.jpg"

./upload_images.sh
