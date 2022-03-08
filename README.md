# 3D_House

# Description

This program shows 3D model of the house of any given address in Flanders. 

Challenge:
* Solo project: Jari Erämaa
* Must-have: 3D lookup of houses
* Showing the house based on address
* Lidar files were provided

As an input an address is needed. Based to that address the solution selects correct lidar (light detection and ranging) files (surface and terrestial).

# Installation

## Required modules and versions
There are modules that are needed to run this program. Here is a list of them and version that are tested with this program. Python version used is 3.9.10.



| Module        | Version  |
|---------------| ---------|
| geopandas     | 0.9.0    |
| matplotlib.   | 3.5.0    |
| natsort       | 7.1.1	    |
| numpy         | 1.21.2.  |
| pandas        | 1.3.5	   |
| plotly        | 5.6.0    |
| PySimpleGUI   | 4.57.0   |
| python        | 3.9.10   |
| rasterio      | 1.1.0	   |
| requests      | 2.27.1  |
| shapefile     | 2.1.3	   |
| shapely       | 1.7.1   |



## File handling
File locations are defined in a JSON file: './data/dsm_and_dtm_directories'. 
There are four file locations:
- dsm_source, contains all the dsm files (original dsm files)
- dsm_path, contains only the required dsm .tif and .shp files (copied with setup.py program)
- dtm_source, contains all the dtm files (original dtm files)
- dtm_path, contains only the required dtm .tif and .shp files (copied with setup.py program)

setup.py copies the files to correct location and creates lambert_coordinates.csv file. Lambert csv file is needed to optimize the code (only required .tif file is opened). Before using setup.py remember to edit the JSON file that contains the folder locations.

| Operation                  | Command                                 |
|----------------------------| ----------------------------------------|
| Copy DSM files             | python setup dsm                        |
| Copy DTM files             | python setup dtm                        |
| Create lambert coordinates | python setup lambert                    |
| all above at once*         | python setup dsm dtm lambert            |

*as shown above it's possible to combine commands. However, note that files needs to be copied before creating lambert csv-file!




# Usage

Start program by command 'python main.py'. 

A graphical user interface will open. Enter any address in Flanders and press 'Ok'-button. There is a check box 'Floor plan'. If selected the house floor plan will be presented. After closing floor plan, the 3D model will be presented. Area of the floor plan will be shown in the terminal. As well as timing data (how long it took to gather data from terminal). Note that 3D picture is shown after the floor plan is closed. If measuring performance uncheck floor plan check box. 



There is a 'Rotate' button in the 3D model. By pressing this button the 3D model will rotate 360 degrees. 



# Visuals

# Timeline

# Personal situation