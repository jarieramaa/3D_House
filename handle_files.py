import os
import shutil
from natsort import natsorted
from numpy import source
import shapefile
import pandas as pd
import re

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

def copy_files(dsm):
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

def create_list_of_shp_files():
    """
    list of list. The second list has two filenames: one for .shp file and the other for .tif.
    These filenames will be written to a CSV file, so it's easy to open correct files later.
    """
    all_files = os.listdir(destination_dsm)
    filelist=[]
    pattern = "k[\d]+."
    regex_compiled = re.compile(pattern)
    
    for filename in all_files:
        if filename.endswith(".shp"):
            filepair = []
            result = regex_compiled.findall(filename)[0]
            tif_file = f"DHMVIIDSMRAS1m_{result}tif"
            filepair.append(filename)
            filepair.append(tif_file)
            filelist.append(filepair)
    filelist = natsorted(filelist)
    for i in filelist:
        print(".shp:",i[0], ", .tif:", i[1])
    return filelist


def create_lambert_coordinates():
    #testauksen vuoksi luetaan vain yksi tiedosto
    filelist = create_list_of_shp_files()
    counter = 1

    counter_list = []
    left_list = []
    bottom_list = []
    right_list = []
    top_list = []
    tif_list = []
    shpfile_list = []

    for filename in filelist:
        sh = shapefile.Reader(os.path.join(destination_dtm, filename[0]))
        counter_list.append(counter)
        left_list.append(round(sh.bbox[0], -3))
        bottom_list.append(round(sh.bbox[1], -3))
        right_list.append(round(sh.bbox[2], -3))
        top_list.append(round(sh.bbox[3], -3))
        tif_list.append(filename[1])
        shpfile_list.append(filename[0])
        counter += 1

    my_dataframe = pd.DataFrame(list(zip(counter_list, left_list, bottom_list, right_list, top_list, tif_list, shpfile_list)), 
    columns = ['counter', 'left', 'bottom', 'right', 'top', 'tif file', 'shpfile'])

    my_dataframe.to_csv('./data/lambert_coordinates.csv')

    print(counter_list[0])
    print(left_list[0])
    print(bottom_list[0])
    print(right_list[0])
    print(top_list[0])
    print(tif_list[0])
    print(shpfile_list[0])


create_lambert_coordinates()











#sf = shapefile.Reader(fname)