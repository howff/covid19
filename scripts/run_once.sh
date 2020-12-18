#!/bin/bash

for region in "Angus"  "Dundee City"  "East Dunbartonshire"  "Fife"  "Glasgow City"  "Perth and Kinross"; do
  u="`echo $region | sed 's/ /_/g'`"
  ./five_miles.py --la "$region"
  convert -trim  "../images/Five_miles_from_$region.png"  "../images/Five_miles_from_$u.jpg"
done
