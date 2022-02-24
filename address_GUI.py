
""" simple dialog with a text input fields for user to enter a city, postcode, street and street number
    and a button to submit the data.
"""

from email.errors import InvalidMultipartContentTransferEncodingDefect
import PySimpleGUI as sg

import API_query
import address

class Address_GUI:
    """Graphical user interface for the address input"""

    def __init__(self) -> None:
        """
        Initialize the GUI
        """
        self.window = None
        self.address_data = address.Data(self.window)
        
    def get_address(self, test = False ):
        """
        Open a dialog window to get the user input
        """
        sg.theme('DarkAmber')   # Add a touch of color
        api_query = API_query.API_query(test)
        font=("Arial", 14)
        txt_size = (16, 1)
        l =[] 

        layout = [  [sg.Text('')],
            [sg.Text('Please enter the address information:', font=font)], 
                    [sg.Text('Street', size=(txt_size), font=font), sg.InputText(size = 20, font = font)],
                    [sg.Text('Street number', size=(txt_size), font=font), sg.InputText(size = 4, font = font)],
                    [sg.Text('Post code', size=(txt_size), font=font), sg.InputText(size= 4, font = font)],
                    [sg.Text('City/town', size=(txt_size), font=font), sg.InputText(size=20, font=font)],
                    [sg.Text('')] , 
                    [sg.Button('Show', font= font)],
                    [sg.Listbox(l, size=(70, 20))],

                    [sg.Button('Ok', font= font), sg.Button('Cancel', font= font)]
                 ]

        # Create the Window
        self.window = sg.Window('Input address', layout)
        self.address_data.window = self.window  #setting the window for the address data class
        # Event Loop to process "events" and get the "values" of the inputs
        is_successful = False
        while is_successful == False:
            event, values = self.window.read()
            print("reading values")
            self.address_data.street = values[0]
            self.address_data.street_nbr = values[1]
            self.address_data.post_code = values[2]
            self.address_data.city = values[3]
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                break
            if self.address_data.validated == False:
                continue
            if event == 'Show':
                print("nyt tehdään haku!!")
                continue
            if event == 'Street':
                print("Street vaihdettu!")
                continue
            is_successful  = api_query.get_address(self.address_data, test)
            if event =='Ok' and is_successful:
                the_coordinates, is_successful = api_query.get_coordinates()
                if is_successful == False or the_coordinates == (None, None):
                    sg.popup_ok("No address found! Please, make sure that the address is in Flanders.",font=font)
                    continue
                else:
                    whole_address = f"{self.address_data.street} {self.address_data.street_nbr}, {self.address_data.post_code}, {self.address_data.city}".upper()
                    return the_coordinates, whole_address
            else:
                sg.popup_ok("No address found! \nPlease, make sure that the address is in Flanders.",font=font)
                continue


        
    def close_window(self):
        """
        Close the window"""
        if self.window is not None:
            self.window.close()





            
    

    
