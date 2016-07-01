# PhotoscanUtilities

Copyright (c) 2015, Scott Arko 
 
This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Library General Public
License as published by the Free Software Foundation; either
version 2 of the License, or (at your option) any later version.
 
This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Library General Public License for more details.
 
You should have received a copy of the GNU Library General Public
License along with this library; if not, write to the
Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.



This is a set of utilties for working with both modern and historic aerial photography 
in the Agisoft Photoscan environment.


Modules:

1)  prepHistoric.py 

This module requires both saa\_func\_lib.py and set\_loc.py (note the backslashes are just to control crazy vi behavior).  

prepHistoric.py is designed to take a list of input tif files or a directory containing tif files and prepare them for 
processing.  It reads through the images, identifies the best commmon size and crops the images to the common size.  It 
has various options for importing metadata, clipping the imagery, and overwriting in place.  Version 1.0 has not been tested over a 
variety of data sets yet, so errors are to be expected.  See prepHistoric-README.txt for more information.  






