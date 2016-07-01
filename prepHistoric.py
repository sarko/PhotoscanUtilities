#!/opt/local/bin/python2.7 
###############################################################################
# prepHistoric.py 
#
# Project:   
# Purpose:  Routine for preparing historic aerial imagery for use in Agisoft Photoscan
#          
# Author:   Scott Arko
#
###############################################################################
# Copyright (c) 2015, Scott Arko 
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
# 
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
###############################################################################
# Notes:
#

#####################
#
# Import all needed modules right away
#
#####################

from osgeo import gdal
import numpy as np
import saa_func_lib as saa
import sys, os, re
import pylab as plt


#####################
#
# Function definitions
#
#####################

def usage():
    print '************************************'
    print ' Usage:  prepHistoric.py [-meta <EEmetafile.txt>] [-overwrite] [-d <dirToProcess>] infiles'
    print '************************************'
    print ' You can either specify a directory to be processed using the -d option or files in a list.  Wildcards are fine.'

#####################
#
# Parse command line options
#
#####################

cl = sys.argv
meta = False
overwrite = False
procDir = False
clip = False
infiles = []
i=1

if len(cl) == 1:
    usage()
    sys.exit()

while i < len(cl):
    if cl[i].rstrip() == '-meta':
        meta = True
        metafile = cl[i+1].rstrip()
        i=i+1
    elif cl[i].rstrip() == '-h' or cl[i].rstrip() == '-help':
        usage()
        sys.exit()
    elif cl[i].rstrip() == '-overwrite':
        overwrite = True
    elif cl[i].rstrip() == '-d':
        procDir = True
        inDir = cl[i+1].rstrip()
        i+=1
    elif cl[i].rstrip() == '-clip':
        clip = True
    else:
        infiles.append(cl[i].rstrip())
    i+=1

if meta == True:
    try: 
        import pyexiv2
        from set_loc import to_deg,set_gps_location
    except:
        meta=False
        print '**************'
        print ' You do not seem to have pyexiv2 installed, which means you cannot export '
        print ' EXIF metadata into your files.  Please install piexiv2 and reprocess your data'
        print ' Note:  Your files will still be cropped and set to the same dimension, just not geocoded'
        print '**************'

if clip == True:
    try: 
        from scipy.signal import medfilt2d,convolve2d
    except:
        clip=False
        print '**************'
        print ' You do not seem to have scipy.signal installed, which means you cannot clip your images'
        print ' Note:  Your files will still be cropped with basic settings and set to the same dimension'
        print '**************'

#####################
#
#  Read metadata file (if used)
#
#####################

if meta == True:
    mdata = open(metafile,'r').readlines()
    h = mdata[0]
    header = re.split(',',h)

    exif = {'EXIF_GPSVersionID':'0x3 0x2 00 00',
            'EXIF_GPSAltitude':'(0)',
            'EXIF_GPSAltitudeRef':'00',
            'EXIF_GPSLatitude':'(0)',
            'EXIF_GPSLatitudeRef':'N',
            'EXIF_GPSLongitude':'(0)',
            'EXIF_GPSLongitudeRef':'W' }

#####################
#
#  Read files from inDir (if defined)
#
#####################

if procDir == True:
    infiles = []
    allFiles = os.listdir(inDir)
    for item in allFiles:
        if item[-4:] == '.tif':
            infiles.append(inDir+'/'+item)


#####################
#
#  Clip images based on image content. Note:  This is EXPERIMENTAL and may fail for 
# any number of reasons
#
#####################
outfiles = []
if clip == True:
    for i in range(0,len(infiles)):
        print 'Reading clip data'
        (x1,y1,trans,proj,r) = saa.read_gdal_file(saa.open_gdal_file(infiles[i]),1)
        (x1,y1,trans,proj,g) = saa.read_gdal_file(saa.open_gdal_file(infiles[i]),2)
        (x1,y1,trans,proj,b) = saa.read_gdal_file(saa.open_gdal_file(infiles[i]),3)
   
        print 'Converting to float'
        r = r.astype(np.float32)
        g = g.astype(np.float32)
        b = b.astype(np.float32)
   
        print 'Calculating Euclidean distance'
        d1 = np.sqrt(np.power(r,2) + np.power(g,2) + np.power(b,2))
   
        print 'Median filtering'
        #d2 = medfilt2d(d1,5)
        d2 = d1

        s1 = d1.shape

        d1 = None
        t1 = np.zeros(s1[0])
        t2 = np.zeros(s1[1])

        for j in range(0,s1[0]):
            t = d2[j,:]
            t1[j] = len(t[t>150])
    
        for j in range(0,s1[1]):
            t = d2[:,j]
            t2[j] = len(t[t>150])

        #plt.plot(t1)
        #plt.figure()
        #plt.plot(t2)
        #plt.show()

        d2 = None
        t1 = t1 - (.25*np.mean(t1))
        t2 = t2 - (.25*np.mean(t2))

        print .25*np.mean(t1)
        print .25*np.mean(t2)

        z1 = np.where(np.diff(np.sign(t1)))[0]
        z2 = np.where(np.diff(np.sign(t2)))[0]

        print z1
        print z2

        ymin = max(z1[z1<500])
        ymax = min(z1[z1>9000])

        xmin = max(z2[z2<500])
        xmax = min(z2[z2>9000])

        print xmin,xmax,ymin,ymax

        r1 = r[ymin:ymax,xmin:xmax]
        g1 = g[ymin:ymax,xmin:xmax]
        b1 = b[ymin:ymax,xmin:xmax]

        r = None
        g = None
        b = None

        outfile = 'file-%03d.tif' % i
        outfiles.append(outfile)
        print outfile

        saa.write_gdal_file_rgb(outfile,trans,proj,r1,g1,b1)

if clip == True:
    tfiles = outfiles
    camount = 0
else:
    tfiles = infiles
    camount = 300

#####################
#
#  get minimum x/y size
#  The minimum values will be our starting point for resizing everything
#
#####################

xSize = np.zeros(len(tfiles))
ySize = np.zeros(len(tfiles))

for i in range(0,len(tfiles)):
    (xSize[i],ySize[i],trans,proj) = saa.read_gdal_file_geo(saa.open_gdal_file(tfiles[i]))

xmin = xSize.min()
ymin = ySize.min()

#####################
#
# Our size will be xmin and ymin minus 300 pixels (150 on either side)
# Since we are assuming these are all USGS high resolution scans, this is a fair value
#
#####################

xmin = int(xmin - camount)
ymin = int(ymin - camount)

for i in range(0,len(tfiles)):
    x = xSize[i]
    y = ySize[i]
    xd = int((x - xmin)/2)
    yd = int((y - ymin)/2)
    (x1,y1,trans,proj,r) = saa.read_gdal_file(saa.open_gdal_file(tfiles[i]),band=1)
    (x1,y1,trans,proj,g) = saa.read_gdal_file(saa.open_gdal_file(tfiles[i]),band=2)
    (x1,y1,trans,proj,b) = saa.read_gdal_file(saa.open_gdal_file(tfiles[i]),band=3)
    r = r[yd:ymin+yd,xd:xmin+xd]
    g = g[yd:ymin+yd,xd:xmin+xd]
    b = b[yd:ymin+yd,xd:xmin+xd]
    # Write over file if you asked for it
    if overwrite == True:
        outfile = infiles[i]
    else:
        outfile = infiles[i].replace('.tif','-a.tif')
    if meta == True:
        test = infiles[i][0:-4]
        print test
        for line in mdata:
            temp = re.split(',',line)
            if test in temp[1]:
                print header.index('Center Latitude dec')
                lat = float(temp[header.index('Center Latitude dec')])
                lon = float(temp[header.index('Center Longitude dec')])
                alt = temp[header.index('Flying Height in Feet')]
                alt = float(alt)/3.28
    saa.write_gdal_file_rgb(outfile,trans,proj,r,g,b)
    if meta == True:
        set_gps_location(outfile,lat,lon,alt)
    
os.system('rm file*.tif')












