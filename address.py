
import PySimpleGUI as sg

class Data:
    def __init__(self, window) -> None:
        self._street = ""
        self._street_nbr = ""
        self._post_code = ""
        self._city = ""
        self._window = window
        self._validated = True

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

    @street_nbr.setter
    def post_code(self, value: str) -> None:
        """ Setter for post_code """
        if len(value) == 4:
            self._post_code = value
            self._validated = True
        else:
            self._validated = False
            sg.popup_ok("Post code must be 4 characters long", font=("Arial", 14))

    @property # CITY
    def city(self) -> str:
        """ Getter for city """
        return self._city

    @street_nbr.setter
    def city(self, value: str) -> None:
        """ Setter for city """
        self._city = value
    
    @property # VALIDATED
    def validated(self) -> bool:
        """ Getter for validated """
        return self._validated

    @property
    def window(self) -> sg.Window:
        """ Getter for window """
        return self._window
    
    @window.setter
    def window(self, value: sg.Window) -> None:
        """ Setter for window """
        self._window = value