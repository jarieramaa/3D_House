""" 
This module contains the main function that is called when the program is run.
"""
import os

import manage_tif
import show_3d_house
import address_GUI
import address

os.system('cls' if os.name == 'nt' else 'clear')

#TODO these coordinates are for testing only
#coordinates = [[[152063.6619006768, 196432.9290343821], [152064.33991667628, 196435.54989838228], [152058.34490867704, 196436.96609038487], [152055.61902067065, 196425.62989837676], [152061.46964468062, 196424.2372583747], [152061.4747646749, 196424.23623437434], [152063.6619006768, 196432.9290343821]]]

def main():
    """
    This function is called when the program is run."""
    address_gui = address_GUI.Address_GUI()

    address, draw_polygon =  address_gui.get_address(True)
    address_gui.close_window()
    print("address.coordinates:", address.coordinates)
    dsm_tif, dtm_tif  = manage_tif.get_tif(address.coordinates)
    polygon = manage_tif.get_polygon(address.coordinates, draw_polygon)
    
    raster_chm = manage_tif.mask_tif_files(dsm_tif,dtm_tif,polygon)

    whole_address_title = f"{address.street} {address.street_nbr} {address.post_code} {address.municipality}".upper()

    show_3d_house.show_3d_house(whole_address_title, raster_chm)

if __name__ == "__main__":
    main()




