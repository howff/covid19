#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import geopandas
import contextily as ctx
import glob
import sys
import os
import argparse
import time

city = 'Dundee City'
data_dir = '../data'
shp_dir = '../shapefiles'
img_dir = '../images'
figure_size = (30, 18)

if len(sys.argv)>1:
	city = sys.argv[1]
parser = argparse.ArgumentParser(description='plot_city')
parser.add_argument('-v', dest='verbose', action="store_true", help='verbose')
parser.add_argument('--city', dest='city', action="store", help="City name, eg. Dundee City", default="")
parser.add_argument('--data-dir', dest='data_dir', action="store", help="Path to directory of CSV files", default=data_dir)
parser.add_argument('--shp-dir', dest='shp_dir', action="store", help="Path to directory of Shapefiles", default=shp_dir)
parser.add_argument('--image-dir', dest='img_dir', action="store", help="Path to directory of image files", default=img_dir)
args = parser.parse_args()
if args.data_dir: data_dir = args.data_dir
if args.shp_dir: shp_dir = args.shp_dir
if args.img_dir: img_dir = args.img_dir
if not args.city:
	print('ERROR: must supply city name with --city')
	exit(1)
city = args.city

# find the most recently dated csv in the data dir
try:
	csv_file = sorted(glob.glob(f'{data_dir}/*_{city}.csv'))[-1]
except:
	print(f'ERROR: cannot find a csv file for {city} in {data_dir}')
	exit(2)
if args.verbose: print('Using %s' % csv_file)

# Read the data file and the shapefile
#   Per100k  Cases   Pop   IZ
csv_dat = pd.read_csv(csv_file)
#   InterZone  Name  TotPop2011  ResPop2011  HHCnt2011
shp_df = geopandas.read_file(f'{shp_dir}/{city}_IZ.shp')

# Join the two on a common column
joined_df = shp_df.merge(csv_dat, left_on = 'Name', right_on = 'IZ')
#joined_df.info() 

# Reproject to web Mercator
joined_df = joined_df.to_crs(epsg=3857)


# Plot the shapefile coloured by cases per 100k
#  use df.dropna().plot() if you've got NA
# Only use 20 shades of colour
# legend=False because we label each ploygon instead
ax = joined_df.plot(figsize=figure_size, alpha=0.5, edgecolor='k',
	scheme='quantiles', k=20, legend=False, column='Per100k', cmap='YlOrRd')
# Label each polygon with the cases
joined_df.apply(lambda x: ax.annotate(text=x.Per100k, xy=x.geometry.centroid.coords[0], ha='center'),axis=1);

# Add a default OSM basemap
ctx.add_basemap(ax) # zoom=12

# Tidy up plot
ax.set_axis_off()
#add title to the map
datestr = time.strftime('%Y-%m-%d',time.localtime())
ax.set_title(f'Cases per 100k for last 7 days ({datestr})', fontdict={'fontsize':20})
#move legend to an empty space
#ax.get_legend().set_bbox_to_anchor((.12,.12))
#ax.get_figure()

# Fixes to try and remove the white border don't work
#plt.show()
#plt.canvas.start_event_loop(sys.float_info.min) #workaround for Exception in Tkinter callback
#plt.figure().set_tight_layout(True)
#plt.figure().savefig('xx.png') #, bbox_inches="tight")
plt.savefig(f'{img_dir}/{city}.png')
if args.verbose: print('Wrote %s/%s.png' % (img_dir, city))

