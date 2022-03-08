"""
This module contains the main function that is called when the program is run.
"""
import os
import time

import manage_tif
import show_3d_house
import address_gui

# import address


os.system("cls" if os.name == "nt" else "clear")


def main():
    """
    This function is called when the program is run."""
    address_ui = address_gui.AddressGUI()

    house_address, draw_polygon = address_ui.get_address(False)
    address_ui.close_window()
    time_0 = address_ui.get_start_time
    time_1 = time.time()
    dsm_tif, dtm_tif = manage_tif.get_tif(house_address.coordinates)
    polygon = manage_tif.get_polygon(house_address.coordinates, draw_polygon)
    raster_chm = manage_tif.mask_tif_files(dsm_tif, dtm_tif, polygon)
    whole_address_title = f"{house_address.street} \
        {house_address.street_nbr}, \
        {house_address.post_code} \
        {house_address.municipality}".upper()

    show_3d_house.show_3d_house(whole_address_title, raster_chm)
    time_2 = time.time()
    print("Polygon area: ", polygon.area)
    print("Time used for API call ", time_1 - time_0)
    print("Time used (excluding API): ", time_2 - time_1)
    print("total time: ", time_2 - time_0)


if __name__ == "__main__":
    main()
