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

# Default values if you don't supply any arguments
data_dir = '../data'
shp_dir = '../shapefiles'
img_dir = '../images'
figure_size = (30, 18)
verbose = False

# Argument parsing
parser = argparse.ArgumentParser(description='five_miles')
parser.add_argument('-v', dest='verbose', action="store_true", help='verbose')
parser.add_argument('--la', dest='la', action="store", help="Local Authority name, eg. Dundee City", default="")
parser.add_argument('--data-dir', dest='data_dir', action="store", help="Path to directory of CSV files", default=data_dir)
parser.add_argument('--shp-dir', dest='shp_dir', action="store", help="Path to directory of Shapefiles", default=shp_dir)
parser.add_argument('--image-dir', dest='img_dir', action="store", help="Path to directory of image files", default=img_dir)
parser.add_argument('--resolution', dest='res', action="store", help="Resolution", default='16')
args = parser.parse_args()
if args.data_dir: data_dir = args.data_dir
if args.shp_dir: shp_dir = args.shp_dir
if args.img_dir: img_dir = args.img_dir
if not args.la:
	print('ERROR: must supply local authority name with --la')
	exit(1)
la = args.la

# Map from LA name into all the IZ codes
# eg. Dundee City -> S12000042
iz_file=os.path.join(data_dir, 'IntermediateZones.csv')
iz_df = pd.read_csv(iz_file)
iz_list = iz_df[iz_df['CAName']==la]['IntZone'].tolist()

# Read the shapefile
#   InterZone  Name  TotPop2011  ResPop2011  HHCnt2011
shp_scot_df = geopandas.read_file(f'{shp_dir}/SG_IntermediateZone_Bdry_2011.shp')
# Subset to just the set of IZ we need
shp_la_df = shp_scot_df.loc[shp_scot_df['InterZone'].isin(iz_list)]

# Reproject to a CRS in metres not degrees, use UK = 27700
shp_la_df = shp_la_df.to_crs(epsg=27700) # 27700 for UK and 3857 for Web Mercator

# Set up a plot canvas
fig, ax = plt.subplots(figsize = figure_size)

# Dissolve to get just the LA which we plot underneath
dissolved = geopandas.GeoDataFrame(crs=shp_la_df.crs, geometry=[geopandas.GeoSeries(shp_la_df.geometry).geometry.unary_union])
# Reproject to web Mercator
dissolved = dissolved.to_crs(epsg=3857)
# Plot the LA
dissolved.plot(ax=ax, alpha=0.5, edgecolor='k')

# Now buffer and plot on top
# XXX could re-use the dissolved above but this shows how to chain union and buffer together:
buffered = geopandas.GeoDataFrame(crs=shp_la_df.crs, geometry=[geopandas.GeoSeries(shp_la_df.geometry).geometry.unary_union.buffer(8050)])
# Reproject to web Mercator
buffered = buffered.to_crs(epsg=3857)
# Plot on top
buffered.plot(ax=ax, alpha=0.5, edgecolor='k')

# Add a basemap
ctx.add_basemap(ax)

# Tidy up plot
ax.set_axis_off()

# Save the image
png_file = f'{img_dir}/Five_miles_from_{la}.png'
plt.savefig(png_file)
