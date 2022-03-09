""" This module contains the methods that are needed for modifying the tif files
and their coordinates."""

import os
from typing import Tuple
import pandas as pd
from shapely.geometry import Polygon
import geopandas as gpd
import rasterio
from rasterio.mask import mask
import matplotlib.pyplot as plt

import setup


def _convert_coordinates(coordinates: list) -> Tuple[list, list]:
    """This method converts the coordinates to two separate lists of x and y coordinates.
    :param: list of coordinates [[x1,y1], [x2,y2]...[xn, yn]]
    :return: two lists of x and y coordinates"""
    x_coord, y_coord = [], []
    for xy_coord in coordinates[0]:
        x_coord.append(xy_coord[0])
        y_coord.append(xy_coord[1])
    return x_coord, y_coord


def get_tif(coordinates) -> Tuple[str, str]:
    """
    A method that returns a correct tif file based on the coordinates given as a parameter.
    Param:
    :coordinates : A list of coordinates that
    :return raster_files, two strings that contains the correct tif files (dsm and dtm).
    """
    x_coord, y_coord = _convert_coordinates(coordinates)
    my_df = pd.read_csv("./data/lambert_coordinates.csv")  # Load the csv file
    my_df = my_df[
        (my_df["Left"] < min(x_coord))
        & (my_df["Right"] > max(x_coord))
        & (my_df["Bottom"] < min(y_coord))
        & (my_df["Top"] > max(y_coord))
    ]
    dsm_file = my_df.iloc[0]["DSM_file"]
    dtm_file = my_df.iloc[0]["DTM_file"]
    dsm_path = setup.read_path("dsm_path")
    dtm_path = setup.read_path("dtm_path")
    dsm_filename = os.path.join(dsm_path, dsm_file)
    dtm_filename = os.path.join(dtm_path, dtm_file)
    dsm_tif = rasterio.open(dsm_filename)
    dtm_tif = rasterio.open(dtm_filename)
    return dsm_tif, dtm_tif


def mask_tif_files(
    dsm_tif, dtm_tif, polygon: Polygon
) -> Tuple[rasterio.io.DatasetReader, rasterio.io.DatasetReader]:
    """This method masks the tif files with the polygon given as a parameter.
    :dsm_tif: DSM tif file
    :dtm_tif: DTM tif file
    :polygon: Shapely polygon
    :return: masked DSM and DTM tif files
    """
    # create a mask from the polygon
    masked_dsm = mask(dataset=dsm_tif, shapes=polygon.geometry, crop=True, pad=True)[0]
    masked_dtm = mask(dataset=dtm_tif, shapes=polygon.geometry, crop=True, pad=True)[0]
    raster_chm = masked_dsm - masked_dtm  # calculate the CHM
    return raster_chm


def get_polygon(coordinates: list, draw_polygon: bool) -> Polygon:
    """This polygon is needed for masking the .tif files
    :param: list of coordinates [[x1,y1], [x2,y2]...[xn, yn]]"""
    x_coord, y_coord = _convert_coordinates(coordinates)
    polygon = Polygon(zip(x_coord, y_coord))
    polygon = gpd.GeoDataFrame(index=[0], crs="epsg:31370", geometry=[polygon])
    if draw_polygon:
        polygon.plot()
        plt.title("Floor plan area: " + str(int(polygon.area)) + " m2")
        plt.show()
    return polygon
