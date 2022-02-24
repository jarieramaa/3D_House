""" Module that contains the Data class """

import PySimpleGUI as sg

class Data:
    """ Data class keeps all the information about all the things that are got via API. The idea is that this data is saved
    to the file and next time the same address is searched, the data is loaded from the file (not via API). That way, the 
    application is a lot faster."""
    def __init__(self, window) -> None:
        self._street = ""
        self._street_nbr = ""
        self._post_code = ""
        self._municipality = ""  # Municipality, this field could be added to the search query
        # TODO https://docs.basisregisters.vlaanderen.be/docs/api-documentation.html#operation/ListAddresses MUNICIPALITY
        self._window = window
        self._validated = True
        self._coordinates = None

    @property 
    def street(self) -> str: 
        """ Getter for street """
        return self._street

    @street.setter
    def street(self, value: str) -> None:
        """ Setter for street """
        self._street = value
    
    @property # STREET NUMBER
    def street_nbr(self) -> str:
        """ Getter for street_nbr """
        return self._street_nbr

    @street_nbr.setter
    def street_nbr(self, value: str) -> None:
        """ Setter for street_nbr """
        self._street_nbr = value

    @property # POST CODE
    def post_code(self) -> str: 
        """ Getter for post_code """
        return self._post_code

    @post_code.setter
    def post_code(self, value: str) -> None:
        """ Setter for post_code """
        if not value.isdigit:
            self._validated = False
            sg.popup_ok("Post code should be 4 digits, \nno characters are allowed.", font=("Arial", 14))
        if len(value) == 4:
            self._post_code = value
            self._validated = True
        else:
            self._validated = False
            sg.popup_ok("Post code must be 4 digits long", font=("Arial", 14))

    @property # CITY
    def municipality(self) -> str:
        """ Getter for city """
        return self._municipality

    @municipality.setter
    def municipality(self, value: str) -> None:
        """ Setter for city """
        self._municipality = value
    
    @property # VALIDATED (if address is ok)
    def validated(self) -> bool:
        """ Getter for validated """
        return self._validated

    @property
    def coordinates(self) -> list:
        """ Getter for coordinates """
        return self._coordinates

    @coordinates.setter
    def coordinates(self, value: list) -> None:
        """ Setter for coordinates """
        self._coordinates = value

    @property
    def window(self) -> sg.Window:
        """ Getter for window """
        return self._window
    
    @window.setter
    def window(self, value: sg.Window) -> None:
        """ Setter for window """
        self._window = value