"""
Get the address and coordinates for the house/apartment that you want to see.
"""

from typing import Tuple
import os
import requests
import pandas as pd

import address

os.system("cls" if os.name == "nt" else "clear")

class ApiQuery:
    """
    This class contains all methods that are needed for the API interaction.
    """

    def __init__(self, test=False):
        """Constructor"""
        self._test = test
        self._address_reguest = requests.models.Response
        self._address_dict = dict
        self._house_specs = dict

    def get_coordinates(self) -> Tuple[list, bool]:
        """Once we have a valid address, it's possible to get the coordinates
        from basisregister.vlaanderen.be service.
        :my_dict : A dictionary that contains address information
        :return : The coordinates in a list of coordinate pairs [[x1,y1], [x2,y2]...[xn, yn]]
        :return : True if the coordinates are found, False if not
        """

        # adresMatches / warnings, let's continue with adresMatches
        addres_matches = self._address_dict.get("adresMatches")

        # Take the first address from the list (there is only one)
        # and convert it to pandas DataFrame
        if len(addres_matches) == 0:
            return None, False
        my_df = pd.json_normalize(addres_matches[0])

        # the first row of the DataFrame
        if my_df is None or len(my_df) == 0:
            return None, False
        row_1 = my_df.iloc[0]

        # address_objects list, get the 'details' from the dictionary. There is an url.
        address_objects = row_1["adresseerbareObjecten"]
        if address_objects is None or len(address_objects) == 0:
            return None, False
        detail_url = address_objects[0].get("detail")

        # New reguest to obtain some more detailed information about building block
        address_req = requests.get(detail_url)
        block_building = address_req.json()

        # take one building and get details, there is be an url
        building = block_building.get("gebouw")
        url_to_house = building.get("detail")

        # Let's get some details from this house
        house = requests.get(url_to_house)
        self._house_specs = house.json()

        # convert the self._house_specs to DataFrame and get polygon coordinates -column
        house_df = pd.json_normalize(self._house_specs)
        the_coordinates = house_df.loc[0, "geometriePolygoon.polygon.coordinates"]
        # self.address.coordinates = the_coordinates
        return the_coordinates, True

    def get_capakey(self) -> str:
        """
        :return : The capakey of the address
        """
        if self._house_specs is None:
            return None
        house_list = self._house_specs.get("percelen")
        my_dict2 = dict(house_list[0])
        my_url2 = my_dict2.get("detail")
        # take the rest of the url address after /percelen and get the CAPAKEY
        capakey = my_url2.split("/")[-1]
        return capakey

    def get_address(self, address_data: address, test=False) -> Tuple[list, str]:
        """ask a address from the user.
        :return : The coordinates in a list of coordinate pairs [[x1,y1], [x2,y2]...[xn, yn]]
        :return : The address as a string
        """
        street, street_nbr, post_code, municipality = (
            address_data.street,
            address_data.street_nbr,
            address_data.post_code,
            address_data.municipality,
        )

        if test:
            street = "Tildonksesteenweg"
            street_nbr = 71
            post_code = 3020

        self._address_reguest = requests.get(
            "https://api.basisregisters.vlaanderen.be/v1/adresmatch",
            params={
                "postcode": post_code,
                "straatnaam": street,
                "huisnummer": street_nbr,
                "gemeentenaam": municipality,
            },
        )

        request = self._address_reguest.json()
        self._address_dict = dict(request)
        warnings = self._address_dict.get("warnings")
        if self._address_reguest.status_code != 200 or len(warnings) > 0:
            return False
        return True
