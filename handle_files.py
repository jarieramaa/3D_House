import os
import shutil
from natsort import natsorted
from numpy import source
import shapefile
import pandas as pd
import re
from typing import Tuple

"""import rasterio
import numpy as np
from affine import Affine
from pyproj import Proj, transform"""

os.system("clear")
""" This module reads the downloaded files from different folders starting
from on location and it's subfolder (path_dsm) and copies all the necessary 
files to a one folder (destination_dsm)"""

# Paths
path_dsm = "/Users/jari/DATA/Projects/3D_House_DSM/"
destination_dsm = "/Users/jari/DATA/Projects/DSM/"
path_dtm = "/Users/jari/DATA/Projects/3D_House_DTM/"
destination_dtm = "/Users/jari/DATA/Projects/DTM/"

def copy_files(dsm:bool):
    """ copies files to DSM or DTM folder. 
    :dsm : a boolean value, if True DSM files are copied. Otherwise DTM files will be copied"""

    if dsm:
        source_path = path_dsm
        dest_path = destination_dsm
    else:
        source_path = path_dtm
        dest_path = destination_dtm
    
    counter = 0

    for path, dirs, files in os.walk(source_path):
        for filename in files:
            if (
                filename.endswith(".dbf")
                or filename.endswith(".prj")
                or filename.endswith(".sbn")
                or filename.endswith(".sbx")
                or filename.endswith(".shp")
                or filename.endswith(".shx")
                or filename.endswith(".tif")
            ):
                file_from = os.path.join(path, filename)
                file_to = dest_path + filename
                print("FILE FROM: ", file_from)
                print("FILE TO:", file_to)
                shutil.copy2(file_from, file_to)
                counter += 1
    print("Total count of files:", counter)

# copy_files(False)

def create_list_of_shp_files() -> Tuple[list, list]:
    """
    Searches all the files ending with .shp and adds those filenames to a list. Creates a sexond list that has tif-names.
    :return : two lists. First one is containing all the .shp filenames and second one generated .tif files.
    """
    # Creating a list of .shp files and sorting the list
    all_files = os.listdir(destination_dsm)
    shp_files=[]
    for filename in all_files:
        if filename.endswith(".shp"):
            shp_files.append(filename)
    shp_files = natsorted(shp_files)
    
    # Creating a list of .tif files in same order as .shp files
    tif_files = [] 
    pattern = "k[\d]+."
    regex_compiled = re.compile(pattern)
    for shp_file in shp_files:
        result = regex_compiled.findall(shp_file)[0] 
        tif_file = f"DHMVIIDSMRAS1m_{result}tif"
        tif_files.append(tif_file)
    
    # Checking that generated .tif filename actually exists
    for tif_file in tif_files:
        if not(tif_file in all_files):
            print("FILE DOESN'T EXISTS", tif_file)
            
    return shp_files, tif_files


def create_lambert_coordinates():
    """
    Creating lambert coordinates and saving it to a file
    """
    shp_files, tif_files = create_list_of_shp_files()
    left_list, bottom_list, right_list, top_list = [], [], [], []

    # Read the boundaries and add them to lists
    for filename in shp_files:
        sh = shapefile.Reader(os.path.join(destination_dtm, filename))
        left_list.append(round(sh.bbox[0], -3))
        bottom_list.append(round(sh.bbox[1], -3))
        right_list.append(round(sh.bbox[2], -3))
        top_list.append(round(sh.bbox[3], -3))

    # Create  a dataframe from the lists and save it to a CSV file  
    my_dataframe = pd.DataFrame(list(zip(left_list, bottom_list, right_list, top_list, tif_files, shp_files)), 
    columns = ['Left', 'Bottom', 'Right', 'Top', 'Tif_file', 'Shp_file'])
    my_dataframe.to_csv('./data/lambert_coordinates.csv')


create_lambert_coordinates()
#create_list_of_shp_files()










#sf = shapefile.Reader(fname)