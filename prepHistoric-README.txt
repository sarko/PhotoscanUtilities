README file for prepHistoric.py


License Header: 


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


Dependencies:

prepHistoric.py requires a number of python libraries to function properly.  Beyond the normal python 2.7 installation it requires the following modules:
	numpy — required for any function
	scipy — required if you are clipping the images
	pyexiv2 — required if you are inserting metadata into the images
	osgeo  — required for any function

These are all open-source libraries that can be obtained and installed for free.  

Beyond the python modules above, you also need the associated files set_loc.py and saa_func_lib.py.  These have utility functions in them that are called directly from prepHistoric.py.  They must either be in the same directory as prepHistoric.py or in a directory included in your PYTHONPATH environment variable.  


Purpose:

The purpose of prepHistoric.py is to prepare high resolution historic aerial images from the USGS in such a way as to make them usable in Agisoft Photoscan.  The primary functions it performs for a set of images are 1) identifies the best common size for the images and crops them to this size 2) Inserts location metadata into the EXIF fields in the image so that the positions can be read directly by Photoscan 3) Clips the images to include only the image content and then performs the cropping stated in 1).  

The last function, image clipping, is experimental and should be used with some caution and plenty of verification.  It is designed to work only on CIR imagery and likely will fail with black and white imagery.  


Usage:

prepHistoric.py [-meta <EarthExplorerMetadata.csv>] [-overwrite] [-d <dirToProcess>] [-clip] [infiles]


The program is made to run under a couple of modes.  The only required option is either -d followed by a directory that includes a set of .tif files or a set of .tif files specified as infiles above. This can either be an actual list of files or you can use wildcards (57*.tif, *.tif, etc).  You can process from 1 to as many files as you have time for.  

options:

  -meta <EarthExplorerMetadata.csv>

The -meta option allows you to specify a .csv file from EarthExplorer that contains the metadata for the scenes being processed.  It will extract the position information from the metadata file for each scene and insert it into the EXIF tags for the processed images.  This allows Photoscan to read the position data directly.  

  -overwrite

The -overwrite option will overwrite the files in place.  In other words your cropped file will have the same name as the input file.  If this is not selected, the files will have -a added to the file suffix.  As an example 578422090.tif would become 578422090-a.tif after processing if this option is not included.  

  -clip

The -clip option is highly experimental and should be treated as such.  It attempts to identify the borders of the actual image data and clips the image to this border.  This helps to minimize the file size and masking needed in Photoscan.  It has been tested on a limited number of scenes and seems to function well.  However, it assumes 3-band CIR imagery and will certainly fail with black and white imagery. 