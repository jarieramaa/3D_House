""" 
This module contains the main function that is called when the program is run.
"""

import address
import manage_tif
import os

import show_3d_house


os.system('cls' if os.name == 'nt' else 'clear')

#TODO these coordinates are for testing only
#coordinates = [[[152063.6619006768, 196432.9290343821], [152064.33991667628, 196435.54989838228], [152058.34490867704, 196436.96609038487], [152055.61902067065, 196425.62989837676], [152061.46964468062, 196424.2372583747], [152061.4747646749, 196424.23623437434], [152063.6619006768, 196432.9290343821]]]

def main():
    coordinates, address_title = address.get_address()
    dsm_tif, dtm_tif  = manage_tif.get_tif(coordinates)

    polygon = manage_tif.get_polygon(coordinates)
    raster_chm = manage_tif.mask_tif_files(dsm_tif,dtm_tif,polygon)
    show_3d_house.show_3d_house(address_title, raster_chm)


main()




