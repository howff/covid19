#!/usr/bin/env python3

import csv, os, sys

dir="../shapefiles"

usage = 'usage: LocalAuthorityName (eg. glasgow, dundee, angus, fife)'
try:
	cityname = sys.argv[1]
except:
	print(usage)
	exit(1)

if cityname == "glasgow" : cityname="Glasgow City"
elif cityname == "dundee" : cityname="Dundee City"
elif cityname == "angus" : cityname="Angus"
elif cityname == "fife" : cityname="Fife"
elif cityname == "perth" : cityname="Perth and Kinross"
elif cityname == "eastdun" : cityname="East Dunbartonshire"

print(cityname)

# Read SG_IntermediateZone_list.csv to get list of local authority names
# CSV columns are:
# _id,IntZone,IntZoneName,CA,CAName,HSCP,HSCPName,HB,HBName,Country
fd = open(os.path.join(dir, 'SG_IntermediateZone_list.csv'), 'r')

zone_set=set()
for row in csv.DictReader(fd):
    if row["CAName"] == cityname:
        zone_set.add(row["IntZone"])

# Extract all the IntZone codes (eg. S02001847) from the CSV for the given city
# and create an ogr SQL file called "ogr.sql"
with open(os.path.join(dir, 'ogr.sql'), 'w') as fd:
    for zone in zone_set:
        fd.write(f"InterZone='{zone}' OR\n")
    fd.write("InterZone='fake'\n")

# Extract all the boundaries of the Intermediate Zones for the given region into a new shapefile

#echo "Creating $dir/${name}_IZ.shp"
#gdal="docker run --rm -v /mnt/hgfs/OneDrive/Data/Geospatial/SG_IntermediateZoneBdry_2011:/data osgeo/gdal:ubuntu-small-latest"
#$gdal  ogr2ogr  -where @/data/$name.ogrsql  /data/${name}_IZ.shp  /data/SG_IntermediateZone_Bdry_2011.shp

local_path = os.path.realpath(dir)
docker_path = '/data'

cmd = f'docker run --rm -v {local_path}:{docker_path} osgeo/gdal:ubuntu-small-latest ogr2ogr -where @/data/ogr.sql "/data/{cityname}_IZ.shp" /data/SG_IntermediateZone_Bdry_2011.shp'

print('Running: %s' % cmd)
os.system(cmd)
