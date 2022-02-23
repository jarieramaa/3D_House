
from multiprocessing.connection import wait
from typing import Tuple
import pandas as pd
from shapely.geometry import Polygon
import geopandas as gpd
import rasterio
import os
from rasterio.mask import mask

import handle_files


#TODO these coordinates are for testing only
coordinates = [[[152063.6619006768, 196432.9290343821], [152064.33991667628, 196435.54989838228], [152058.34490867704, 196436.96609038487], [152055.61902067065, 196425.62989837676], [152061.46964468062, 196424.2372583747], [152061.4747646749, 196424.23623437434], [152063.6619006768, 196432.9290343821]]]


def _convert_coordinates(coordinates:list) -> Tuple[list, list]:
   """This method converts the coordinates to two separate lists of x and y coordinates.
   :param: list of coordinates [[x1,y1], [x2,y2]...[xn, yn]]
   :return: two lists of x and y coordinates"""
   x, y = [], []
   for xy_coord in coordinates[0]:
      x.append(xy_coord[0])
      y.append(xy_coord[1])
   return x, y


def get_tif(coordinates) -> Tuple[str, str]:
    """
    A method that returns a correct tif file based on the coordinates given as a parameter.
    Param:
    :coordinates : A list of coordinates that
    :return raster_files, two strings that contains the correct tif files (dsm and dtm).
    """
    x, y = _convert_coordinates(coordinates)
    my_df = pd.read_csv('./data/lambert_coordinates.csv') # Load the csv file
    x_min, x_max, y_min, y_max  = min(x), max(x), min(y), max(y)
    # TODO what happens if the coordinates are not in one tif file (the house is between files)? Will this return the two tif files or nothing?
    my_df = my_df[(my_df['Left'] < x_min) & (my_df['Right'] > x_max) & (my_df['Bottom'] < y_min) & (my_df['Top'] > y_max)]

    dsm_file = my_df.iloc[0]['DSM_file']
    dtm_file = my_df.iloc[0]['DTM_file']

    dsm_path, dtm_path, dsm_source, dtm_source = handle_files.read_paths()
    dsm_filename = os.path.join(dsm_path, dsm_file)
    dtm_filename = os.path.join(dtm_path, dtm_file)
    dsm_tif = rasterio.open(dsm_filename)
    dtm_tif = rasterio.open(dtm_filename)
    print(type(dsm_file))
    print(dsm_tif)

    return dsm_tif, dtm_tif


def get_polygon(coordinates:list) -> Polygon:
   """This polygon is needed for masking the .tif files
   :param: list of coordinates [[x1,y1], [x2,y2]...[xn, yn]]"""
   x, y = _convert_coordinates(coordinates)
   polygon = Polygon(zip(x, y))
   print(zip(x,y))
   polygon = gpd.GeoDataFrame(index=[0], crs='epsg:31370', geometry=[polygon])
   return polygon


def mask_tif_files(dsm_tif, dtm_tif , polygon: Polygon) -> Tuple[rasterio.io.DatasetReader, rasterio.io.DatasetReader]:
    """This method masks the tif files with the polygon given as a parameter.
    :dsm_tif: DSM tif file
    :dtm_tif: DTM tif file
    :polygon: Shapely polygon
    :return: masked DSM and DTM tif files
    """
    # create a mask from the polygon
    masked_DSM, masked_transform_DSM = mask(dataset=dsm_tif, shapes=polygon.geometry, crop=True, pad=True)
    masked_DTM, masked_transform_DTM = mask(dataset=dtm_tif, shapes=polygon.geometry, crop=True, pad=True)  

    raster_CHM = masked_DSM - masked_DTM # calculate the CHM

    return raster_CHM