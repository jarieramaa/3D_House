
import pandas as pd
import address

#coordinates = [[[152063.6619006768, 196432.9290343821], [152064.33991667628, 196435.54989838228], [152058.34490867704, 196436.96609038487], [152055.61902067065, 196425.62989837676], [152061.46964468062, 196424.2372583747], [152061.4747646749, 196424.23623437434], [152063.6619006768, 196432.9290343821]]]



def get_tif(coordinates):
    """
    A method that returns a correct tif file based on the coordinates given as a parameter.
    Param:
    :coordinates : A list of coordinates that
    :return : tif file that is in given coordinates
    """
    x = []
    y = []

    for xy_coord in coordinates[0]:
       x.append(xy_coord[0])
       y.append(xy_coord[1])
    
    my_df = pd.read_csv('./data/lambert_coordinates.csv') # Load the csv file
    
    
    x_min, x_max, y_min, y_max  = min(x), max(x), min(y), max(y)

    # TODO what happens if the coordinates are not in one tif file (the house is between files)? Will this return the two tif files or nothing?
    my_df = my_df[(my_df['Left'] < x_min) & (my_df['Right'] > x_max) & (my_df['Bottom'] < y_min) & (my_df['Top'] > y_max)]

    tif_file = my_df.iloc[0]['Tif_file']
    print(tif_file)
    return tif_file


