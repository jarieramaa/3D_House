
"""
Get the address and coordinates for the house/apartment that you want to see.
"""

from audioop import add
from anyio import CapacityLimiter
import requests
from typing import Tuple
import pandas as pd
import os
from shapely.geometry import Polygon
import geopandas as gpd

import address

os.system('cls' if os.name == 'nt' else 'clear')

#TODO The logic to ask the address from the user. Also could check that the given address is valid. There was a idea for autofill (the database should be loaded first)
# TODO the conversion to coordinates is quite long, maybe it could be a separate module, especially if there is more logic for address (see above)

class API_query:
    """
    This class contains all methods that are needed for the API interaction.
    """

    def __init__(self, test = False):
        """Constructor"""
        self.test = test
        self.address =  requests.models.Response
        self.address_dict = dict
        self.house_specs = dict

    def get_coordinates(self) -> Tuple[list, bool]:
        """ Once we have a valid address, it's possible to get the coordinates from basisregister.vlaanderen.be service.
        :my_dict : A dictionary that contains address information
        :return : The coordinates in a list of coordinate pairs [[x1,y1], [x2,y2]...[xn, yn]]
        :return : True if the coordinates are found, False if not
        """

        # adresMatches / warnings, let's continue with adresMatches
        addresMatches = self.address_dict.get('adresMatches')
        print("addresMatches", addresMatches)

        # Take the first address from the list (there is only one)
        # and convert it to pandas DataFrame
        if len(addresMatches) == 0:
            return None, False
        my_df = pd.json_normalize(addresMatches[0])

        # the first row of the DataFrame
        if my_df is None or len(my_df) == 0:
            return None, False
        row_1 = my_df.iloc[0]

        # address_objects list, get the 'details' from the dictionary. There is an url.
        address_objects = row_1['adresseerbareObjecten']
        print(len(address_objects))
        print("address_objects: ", address_objects)
        print("=="*20)
        if address_objects is None or len(address_objects) == 0:
            return None, False
        detail_url = address_objects[0].get('detail')

        # New reguest to obtain some more detailed information about building block
        address = requests.get(detail_url)
        block_building = address.json()

        # take one building and get details, there is be an url
        building = block_building.get('gebouw')
        url_to_house = building.get('detail')


        # Let's get some details from this house
        house = requests.get(url_to_house)
        house_specs = house.json()

        # convert the house_specs to DataFrame and get polygon coordinates -column
        house_df = pd.json_normalize(house_specs)
        the_coordinates = house_df.loc[0,'geometriePolygoon.polygon.coordinates']
        return the_coordinates, True

    def get_capakey(self) -> str:
        """
        :return : The capakey of the address
        """
        if self.house_specs is None:
            return None
        house_list = self.house_specs.get('percelen')
        my_dict2 = dict(house_list[0])
        my_url2 = my_dict2.get('detail')
        #take the rest of the url address after /percelen and get the CAPAKEY
        capakey = my_url2.split('/')[-1]
        return capakey


    def get_address(self, address : address, test = False) -> Tuple[list, str]:
        """ask a address from the user.
        :return : The coordinates in a list of coordinate pairs [[x1,y1], [x2,y2]...[xn, yn]] 
        :return : The address as a string
        """

        #TODO city is not yet used in the query. Should it be added to the query
        street, street_nbr, post_code  = address.street, address.street_nbr, address.post_code

        if test :
            street = "Tildonksesteenweg"
            street_nbr = 71
            post_code = 3020
            # uitbreidingstraat 3 2840 haren - original
            # Tildonksesteenweg 71 3020 Herent - horisontal split - nice house!!
            # Regentschapsstraat 44 , Brussel 1000 -- does not work
            # Klipgaardestraat 9 3473 Kortenaken - 4 ways split

        self.address = requests.get(
            "https://api.basisregisters.vlaanderen.be/v1/adresmatch",
            params={
                "postcode": post_code,
                "straatnaam": street,
                "huisnummer": street_nbr,
            },
        )

        request = self.address.json()
        self.address_dict = dict(request)
        warnings = self.address_dict.get('warnings')

        if self.address.status_code != 200 or len(warnings) > 0:
            print("Error when reading the address. Pls try again")
            return False
        else:
            return True




    #coordinates = []
    #address = ""
    #coordinates, address = get_address()
    #
    #print("COORDINATES (get_address): ", coordinates)

    #get_address("akffj", True)

