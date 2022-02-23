
""" simple dialog with a text input fields for user to enter a city, postcode, street and street number
    and a button to submit the data.
"""

import PySimpleGUI as sg

import API_query
 
class Address_GUI:
    """Graphical user interface for the address input"""

    def __init__(self) -> None:
        """
        Initialize the GUI
        """
        self.window = None
        
    def get_address(self, test = False ):
        """
        Open a dialog window to get the user input
        """
        sg.theme('DarkAmber')   # Add a touch of color
        api_query = API_query.API_query(test)
        font=("Arial", 14)
        txt_size = (16, 1)

        layout = [  [sg.Text('')],
            [sg.Text('Please enter the address information:', font=font)], 
                    [sg.Text('City/town', size=(txt_size), font=font), sg.InputText(size=20, font=font)],
                    [sg.Text('Post code', size=(txt_size), font=font), sg.InputText(size= 4, font = font)],
                    [sg.Text('Street', size=(txt_size), font=font), sg.InputText(size = 20, font = font)],
                    [sg.Text('Street number', size=(txt_size), font=font), sg.InputText(size = 4, font = font)],
                       [sg.Text('')] , 
                    [sg.Button('Ok', font=font), sg.Button('Cancel', font=font)]
                 ]

        # Create the Window
        self.window = sg.Window('Input address', layout)
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                break
            print('You entered ', values[0])
            print('You entered ', values[1])
            print('You entered ', values[2])
            print('You entered ', values[3])
            #TÄHÄN chekkaus, jos osoite on oikea
            is_successful  = api_query.get_address(values, test)
            if is_successful:
                the_coordinates, is_successful = api_query.get_coordinates()
                if is_successful == False or the_coordinates == (None, None):
                    sg.popup_ok("No address found! Please, make sure that the address is in Wallonia.",font=font)
                    continue
                else:
                    whole_address = f"{values[2]} {values[3]}, {values[1]}, {values[0]}".upper()
                    return the_coordinates, whole_address
        
    def close_window(self):
        if self.window is not None:
            self.window.close()





            
    

    
