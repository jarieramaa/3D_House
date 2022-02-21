
"""
Get the address and coordinates for the house/apartment that you want to see.
"""

import requests
from typing import Tuple
import pandas as pd
import os

os.system('cls' if os.name == 'nt' else 'clear')

#TODO The logic to ask the address from the user. Also could check that the given address is valid. There was a idea for autofill (the database should be loaded first)
# TODO the conversion to coordinates is quite long, maybe it could be a separate module, especially if there is more logic for address (see above)

def _json_to_coordinates(my_dict:dict) -> list:
    """ Once we have a valid address, it's possible to get the coordinates from basisregister.vlaanderen.be service.
    :my_dict : A dictionary that contains address information
    :return : The coordinates in a list of coordinate pairs [[x1,y1], [x2,y2]...[xn, yn]]
    """

    # adresMatches / warnings, let's continue with adresMatches
    addresMatches = my_dict.get('adresMatches')

    # Take the first address from the list (there is only one)
    # and convert it to pandas DataFrame
    my_df = pd.json_normalize(addresMatches[0])

    # the first row of the DataFrame
    row_1 = my_df.iloc[0]

    # address_objects list, get the 'details' from the dictionary. There is a url.
    address_objects = row_1['adresseerbareObjecten']
    detail_url = address_objects[0].get('detail')

    # New reguest to obtain some more detailed information about building block
    address = requests.get(detail_url)
    block_building = address.json()

    # take one building and get details, there is be a url
    building = block_building.get('gebouw')
    url_to_house = building.get('detail')

    # Let's get some details from this house
    house = requests.get(url_to_house)
    house_specs = house.json()

    # convert the house_specs to DataFrame and get polygon coordinates -column
    house_df = pd.json_normalize(house_specs)
    the_coordinates = house_df.loc[0,'geometriePolygoon.polygon.coordinates']

    return the_coordinates


def get_address() -> Tuple[dict, str]:
    """ask a address from the user.
    :return :The coordinates in a list of coordinate pairs [[x1,y1], [x2,y2]...[xn, yn]] and the address as a string
    """
    street = "uitbreidingstraat"
    #street = "jaalaranta"
    street_nbr = 10
    post_code = 2840
    whole_address = f"{street} {street_nbr}, {post_code}".upper()

    address = requests.get(
        "https://api.basisregisters.vlaanderen.be/v1/adresmatch",
        params={
            "postcode": post_code,
            "straatnaam": street,
            "huisnummer": street_nbr,
        },
    )
    print("STATUS CODE:", address.status_code)
    request = address.json()

    print(request)
    my_dict = dict(request)
    print("my_dict_keys", my_dict.keys())
    warnings = my_dict.get('warnings')

    # TODO Check that if there is only one address. If several addresses are found then it's necessary to ask furher details


    if address.status_code != 200 or len(warnings) >0:
        print("Error when reading the address. Pls try again")
        return None
    else:
        return _json_to_coordinates(my_dict), whole_address

print(get_address())


