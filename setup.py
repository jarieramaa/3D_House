""" This module reads the downloaded files from different folders starting
from on location and it's subfolder (path_dsm) and copies all the necessary
files to a one folder (destination_dsm)
"""

import os
import sys
import re
from typing import Tuple
import json
import shutil
from natsort import natsorted
import shapefile
import pandas as pd


# clear the screen
os.system("cls" if os.name == "nt" else "clear")


def write_paths():
    """ "
    This function creates a JSON file that can be used later for reading the
    paths.
    """
    directories = {
        "dsm_source": "/Users/jari/DATA/Projects/3D_House_DSM/",
        "dsm_path": "/Users/jari/DATA/Projects/DSM/",
        "dtm_source": "/Users/jari/DATA/Projects/3D_House_DTM/",
        "dtm_path": "/Users/jari/DATA/Projects/DTM/",
    }
    json_string = json.dumps(directories)
    with open("./data/dsm_and_dtm_directories", "w", encoding="UTF-8") as outfile:
        outfile.write(json_string)


def read_path(filename: str) -> str:
    """
    Reads correct paths from JSON file
    :filename : a string containing the filename for example: dsm_source, dtm_source, dsm_path or
    dtm_path.
    :returns : the path to the file
    """
    with open("./data/dsm_and_dtm_directories", encoding="UTF-8") as json_file:
        paths = dict(json.load(json_file))
        path_to_file = paths.get(filename)
        return path_to_file


def copy_files(dsm: bool):
    """copies files to DSM or DTM folder.
    :dsm : a boolean value, if True DSM files are copied. Otherwise DTM files will be copied"""
    dsm_path = read_path("dsm_path")
    dtm_path = read_path("dtm_path")
    dsm_source = read_path("dsm_source")
    dtm_source = read_path("dtm_source")
    if dsm:
        source_path = dsm_source
        dest_path = dsm_path
    else:
        source_path = dtm_source
        dest_path = dtm_path

    counter = 0
    for path, dirs, files in os.walk(source_path):
        for filename in files:
            #if filename.endswith(
            #    (".dbf", ".prj", ".sbn", ".sbx", ".shp", ".shx", ".tif")
            #):
            if filename.endswith((".tif", ".shp")):
                file_from = os.path.join(path, filename)
                file_to = dest_path + filename
                print("FILE FROM: ", file_from)
                print("FILE TO:", file_to)
                shutil.copy2(file_from, file_to)
                counter += 1
    print("Total count of files:", counter)


def create_list_of_shp_files() -> Tuple[list, list]:
    """
    Searches all the files ending with .shp and adds those filenames to a list.
    Creates a sexond list that has tif-names.
    :return : two lists. First one is containing all the .shp filenames and second
    one generated .tif files.
    """
    dsm_path = read_path("dsm_path")
    dtm_path = read_path("dtm_path")
    # Creating a list of .shp files and sorting the list
    all_files = os.listdir(dsm_path)
    shp_files = []
    for filename in all_files:
        if filename.endswith(".shp"):
            shp_files.append(filename)
    shp_files = natsorted(shp_files)

    # Creating a list of .tif files in same order as .shp files
    dsm_tif_files, dtm_tif_files = [], []

    pattern = "k[\d]+."
    regex_compiled = re.compile(pattern)
    for shp_file in shp_files:
        result = regex_compiled.findall(shp_file)[0]
        dsm_tif_file = f"DHMVIIDSMRAS1m_{result}tif"
        dsm_tif_files.append(dsm_tif_file)
        dtm_tif_file = f"DHMVIIDTMRAS1m_{result}tif"
        dtm_tif_files.append(dtm_tif_file)

    # Checking that generated .tif filename actually exists
    for dsm_tif_file in dsm_tif_files:
        if not dsm_tif_file in all_files:
            print("FILE DOESN'T EXISTS", dsm_tif_file)
    all_dtm_files = os.listdir(dtm_path)
    for dtm_tif_file in all_dtm_files:
        if not dtm_tif_file in all_dtm_files:
            print("FILE DOESN'T EXISTS", dtm_tif_file)
    return shp_files, dsm_tif_files, dtm_tif_files


def create_lambert_coordinates():
    """
    Creating lambert coordinates and saving it to a file
    """
    dsm_path = read_path("dsm_path")
    shp_files, dsm_tif_files, dtm_tif_files = create_list_of_shp_files()
    left_list, bottom_list, right_list, top_list = [], [], [], []

    # Read the boundaries and add them to lists
    for filename in shp_files:
        shapef = shapefile.Reader(os.path.join(dsm_path, filename))
        left_list.append(round(shapef.bbox[0], -3))
        bottom_list.append(round(shapef.bbox[1], -3))
        right_list.append(round(shapef.bbox[2], -3))
        top_list.append(round(shapef.bbox[3], -3))

    # Create  a dataframe from the lists and save it to a CSV file
    my_dataframe = pd.DataFrame(
        list(
            zip(
                left_list,
                bottom_list,
                right_list,
                top_list,
                dsm_tif_files,
                dtm_tif_files,
            )
        ),
        columns=["Left", "Bottom", "Right", "Top", "DSM_file", "DTM_file"],
    )
    my_dataframe.to_csv("./data/lambert_coordinates.csv")

def main(args):
    """
    Main function
    """
    print(args)
    if 'dsm' in args:
        #copy_files(True)
        print("Copying DSM files")
        copy_files(True)

    if 'dtm' in args:
        #copy_files(True)
        print("Copying DTM files")
        copy_files(False)
    
    if 'lambert' in args:
        print("Creating lambert coordinates")
        create_lambert_coordinates()
    


if __name__ == "__main__":
    main(sys.argv[1:])