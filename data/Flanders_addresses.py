

import pandas as pd


def read_post_add(file_name):
    """
    Read the post address data from the csv file
    """
    df = pd.read_csv(file_name, sep=',', encoding='utf-8')
    #df.columns = ['street', 'street_nbr', 'post_code', 'city']
    return df

my_df = read_post_add('post_add.csv')
