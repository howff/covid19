#!/bin/bash

name="$1"
if [ "$name" == "glasgow" ]; then cityname="Glasgow City"
elif [ "$name" == "dundee" ]; then cityname="Dundee City"
elif [ "$name" == "angus" ]; then cityname="Angus"
elif [ "$name" == "fife" ]; then cityname="Fife"
elif [ "$name" == "perth" ]; then cityname="Perth and Kinross"
elif [ "$name" == "eastdun" ]; then cityname="East Dunbartonshire"
else echo usage: $0 localauthorityname eg. dundee or glasgow
fi

dir="/mnt/hgfs/OneDrive/Data/Geospatial/SG_IntermediateZoneBdry_2011"

# CSV columns are:
# _id,IntZone,IntZoneName,CA,CAName,HSCP,HSCPName,HB,HBName,Country
# Extract all the IntZone codes (eg. S02001847) from the CSV for the given city
# and create an ogr SQL file
echo "Creating $dir/$name.ogrsql"
cat $dir/SG_IntermediateZone_list.csv | \
  python3 -c $'import sys,csv\nfor row in csv.DictReader(sys.stdin):\n if (row["CAName"]=="'"${cityname}"'"): print(row["IntZone"])' | \
  sort -u | \
  sed -e "s/^/OR InterZone='/" -e '1s/OR //' -e "s/$/'/" > $dir/$name.ogrsql

# Extract all the boundaries of the Intermediate Zones for the given region into a new shapefile

echo "Creating $dir/${name}_IZ.shp"
gdal="docker run --rm -v /mnt/hgfs/OneDrive/Data/Geospatial/SG_IntermediateZoneBdry_2011:/data osgeo/gdal:ubuntu-small-latest"
$gdal  ogr2ogr  -where @/data/$name.ogrsql  /data/${name}_IZ.shp  /data/SG_IntermediateZone_Bdry_2011.shp
