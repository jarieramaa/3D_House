"""This module contains methods to create dataframes 
that are used when reading the 'surface of the plot' and 
'living area' information
bpncapa.shp, bpncapa_1.shp, BpnRebu.shp, BpnRebu_1.shp and BpnCabu.shp
"""

from concurrent.futures.process import _SafeQueue
import fiona #https://gis.stackexchange.com/questions/113799/how-to-read-a-shapefile-in-python
import pandas as pd
import pickle
import os

os.system('cls' if os.name == 'nt' else 'clear')
# Example data
# 24115B0357-00R000

path_BnpCapa_0 = "/Users/jari/DATA/Projects/GIS/CadGIS_fiscaal_20210101_GewVLA_Shapefile/Shapefile/BpnCapa.shp"
path_BnpCapa_1 = "/Users/jari/DATA/Projects/GIS/CadGIS_fiscaal_20210101_GewVLA_Shapefile/Shapefile/BpnCapa_1.shp"

path_BpnCabu = "/Users/jari/DATA/Projects/GIS/CadGIS_fiscaal_20210101_GewVLA_Shapefile/Shapefile/BpnCabu.shp"
path_BpnRebu_0 = "/Users/jari/DATA/Projects/GIS/CadGIS_fiscaal_20210101_GewVLA_Shapefile/Shapefile/BpnRebu.shp"
path_BpnRebu_1 = "/Users/jari/DATA/Projects/GIS/CadGIS_fiscaal_20210101_GewVLA_Shapefile/Shapefile/BpnRebu_1.shp"



def read_shapefile_property_to_dataframe(shapefile_path:str)->pd.DataFrame:
    """
    Reads a shapefile and returns a pandas dataframe
    :param shapefile_path: path to the shapefile
    :return: pandas dataframe
    """
    with fiona.open(shapefile_path) as shapefile:
        return pd.DataFrame([feature['properties'] for feature in shapefile])

def save_df_to_pickle(df:pd.DataFrame, file_path:str):
    """
    Saves a pandas dataframe to a pickle file
    :return: None
    """
    with open(file_path, 'wb') as f:
        pickle.dump(df, f)

def read_and_write_files():
    """
    Reads and writes the files
    :return: None
    """
    # Read files
    #df_BnpCapa_0 = read_shapefile_property_to_dataframe(path_BnpCapa_0)
    #df_BnpCapa_1 = read_shapefile_property_to_dataframe(path_BnpCapa_1)
    #df_BpnRebu_0 = read_shapefile_property_to_dataframe(path_BpnRebu_0)
    #df_BpnRebu_1 = read_shapefile_property_to_dataframe(path_BpnRebu_1)
    df_BpnCabu = read_shapefile_property_to_dataframe(path_BpnCabu)

    # Save files
    #save_df_to_pickle(df_BnpCapa_0, "./data/df_BpnCapa_0.pkl")
    #save_df_to_pickle(df_BnpCapa_1, "./data/df_BpnCapa_1.pkl")
    #save_df_to_pickle(df_BpnRebu_0, "./data/df_BpnRebu_0.pkl")
    #save_df_to_pickle(df_BpnRebu_1, "./data/df_BpnRebu_1.pkl")
    save_df_to_pickle(df_BpnCabu, "./data/df_BpnCabu.pkl")

#read_and_write_files()

def read_df_from_pickle(file_path:str)->pd.DataFrame:
    """
    Reads a pandas dataframe from a pickle file
    :param file_path: path to the pickle file
    :return: pandas dataframe
    """
    with open(file_path, 'rb') as f:
        return pickle.load(f)



#BnpCapa_0 = read_df_from_pickle("./data/df_BnpCapa_0.pkl")
#print(BnpCapa_0.head())


#my_df = read_shapefile_property_to_dataframe(path_to_shpfile_1)
#save_df_fo_file(my_df, "./data/bpncapa_1.csv")


"""my_df_0 = read_csv("./data/bpncapa.csv")
my_df_1 = read_csv("./data/bpncapa_1.csv")

print(my_df_0.shape)
print(my_df_1.shape)

my_df_result = my_df_0.append(my_df_1)

print(my_df_result.shape)

save_df_fo_file(my_df_result, "./data/bpncapa_all.csv")
"""
def append_two_dfs(df_0:pd.DataFrame, df_1:pd.DataFrame, name)->pd.DataFrame:
    """
    Appends two dataframes
    :param df_0: pandas dataframe
    :param df_1: pandas dataframe
    :return: pandas dataframe
    """
    merged_df = df_0.append(df_1)
    save_df_to_pickle(merged_df, f"./data/{name}.pkl")
    return merged_df


capakey = "24115B0357/00R000"
#capakey = "12038A0016/00C002"


""" find the row with the capakey """
def find_row_with_capakey(df:pd.DataFrame, capakey:str)->pd.DataFrame:
    """
    Finds a row with the capakey in the dataframe
    :param df: pandas dataframe
    :param capakey: capakey
    :return: pandas dataframe
    """
    return df[df['CAPAKEY'] == capakey]

#my_row = find_row_with_capakey(df_rebu1, capakey)

def clean_unnecessary_columns():
    df_BpnCapa_all = read_df_from_pickle("./data/df_BpnCapa_all.pkl")
    df_BpnCapa_all = df_BpnCapa_all[['OIDN', 'UIDN', 'CAPAKEY', 'OPPERVL']]
    save_df_to_pickle(df_BpnCapa_all, "./data/df_BpnCapa_all_light.pkl")

def clean_unnecessary_columns_rebu(file_path:str, name):
    df_light = read_df_from_pickle(file_path)
    df_light = df_light[['OIDN', 'UIDN', 'OPPERVL']]
    df_light= df_light.rename(columns={'OPPERVL': 'SURFACE_OF_PLOT'}, inplace=True)
    save_df_to_pickle(df_light, f"./data/{name}.pkl")

def clean_merge_and_save_rebu_files():
    """ Reads and merges the files """
    df_BpnCapu= read_df_from_pickle("./data/df_BpnCabu.pkl")
    df_BpnCapu = df_BpnCapu[['OIDN', 'UIDN', 'OPPERVL']]
    df_BpnCapu.rename(columns={'OPPERVL': 'SURFACE_OF_PLOT'}, inplace=True)
    print("df_BpnCapu",df_BpnCapu.shape)
    print(df_BpnCapu.columns)

    df_BpnRebu_0 = read_df_from_pickle("./data/df_BpnRebu_0.pkl")
    df_BpnRebu_0 = df_BpnRebu_0[['OIDN', 'UIDN', 'OPPERVL']]
    df_BpnRebu_0.rename(columns={'OPPERVL': 'SURFACE_OF_PLOT'}, inplace=True)
    print("df_BpnRebu_0",df_BpnRebu_0.shape)
    print(df_BpnRebu_0.columns)

    df_BpnRebu_1 = read_df_from_pickle("./data/df_BpnRebu_1.pkl")
    df_BpnRebu_1 = df_BpnRebu_1[['OIDN', 'UIDN', 'OPPERVL']]
    df_BpnRebu_1.rename(columns={'OPPERVL': 'SURFACE_OF_PLOT'}, inplace=True)
    print("df_BpnRebu_1", df_BpnRebu_1.shape)
    print(df_BpnRebu_1.columns)

    merged_df = df_BpnRebu_1.append(df_BpnRebu_0)
    print("after first merger", merged_df.shape)
    merged_df = merged_df.append(df_BpnCapu)
    print("after second merger:",merged_df.shape)
    uniq_list = merged_df['OIDN'].unique()
    print("UNIQUE:", len(uniq_list))
    save_df_to_pickle(merged_df, "./data/df_BpnRebu_all_light.pkl")

df_recu_light = read_df_from_pickle("./data/df_BpnRebu_all_light.pkl")
print(df_recu_light.shape)
uniq_list = pd.unique(df_recu_light[['OIDN', 'UIDN']])
print(len(uniq_list))

#clean_merge_and_save_rebu_files()




#append_two_dfs(df_BpnCaba_0, df_BpnCaba_1, "df_BpnCapa_all")


#my_df = read_df_from_pickle("./data/df_BpnCapa_all_light.pkl")
#print(my_df.head())


#dublicates = find_duplicates(my_df)
#print(dublicates.head())
#print(dublicates.shape)



#print(df_BpnCapu.columns == df_BpnRebu_1.columns)


"""print("-"*100)
print(df_BpnCapu.shape)
uniq_list = df_BpnCapu['OIDN'].unique()
print(len(uniq_list))"""



