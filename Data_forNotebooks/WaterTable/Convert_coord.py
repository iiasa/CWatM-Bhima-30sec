# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 15:50:02 2017

@author: Luca
"""

# Import modules
import numpy as np
import xarray as xr
from xarray import Dataset
from scipy.interpolate import griddata
import netCDF4
import mpl_toolkits.basemap.pyproj as pyproj
import rasterio
import xlrd

# We import coordinates from another map of CWATM because coordinates of the lobith.tif file do not work
wgs84=pyproj.Proj("+init=EPSG:4326")            # Associated coord system
UTM=pyproj.Proj("+init=EPSG:32643")          # Projection system for the Upper Bhima basin

# Projection
#b=36.178699
#a=-5.4963
#x=pyproj.transform(wgs84, UTM32N, a, b) # Convert coordinates from wgs84 to UTM32N

wb1 = xlrd.open_workbook("UB_GW_Data.xlsx")    
sh1 = wb1.sheet_by_name(u'Sheet1')
lon=[]
lat=[]
for i in range (381):
    a=sh1.row_values(i+1)[4]
    b=sh1.row_values(i+1)[3]
    lon.append(a)
    lat.append(b)

z=[]
for i in range (381):
    a=sh1.row_values(i+1)[5]
    z.append(a)
wtd=[]
for i in range (381):
    a=sh1.row_values(i+1)[10]
    wtd.append(a)
    

x=[]
y=[]
for i in range (len(lat)):
    Coord=pyproj.transform(wgs84, UTM, lon[i], lat[i])
    x.append(Coord[0])
    y.append(Coord[1])

fichier = open("GW_level_x.txt", "w")
for i in range (len(lat)):
    fichier.write(str(x[i])) # In pptv
    fichier.write("\n") # Risque d'etre desature if 2 layers                   
fichier.close()

fichier = open("GW_level_y.txt", "w")
for i in range (len(lat)):
    fichier.write(str(y[i])) # In pptv
    fichier.write("\n") # Risque d'etre desature if 2 layers                   
fichier.close()

fichier = open("GW_level_z.txt", "w")
for i in range (len(lat)):
    fichier.write(str(z[i])) # In pptv
    fichier.write("\n") # Risque d'etre desature if 2 layers                   
fichier.close()

fichier = open("GW_level_wtd.txt", "w")
for i in range (len(lat)):
    fichier.write(str(wtd[i])) # In pptv
    fichier.write("\n") # Risque d'etre desature if 2 layers                   
fichier.close()
               
