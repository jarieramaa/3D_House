
""" simple dialog with a text input fields for user to enter a city, postcode, street and street number
    and a button to submit the data.
"""

import PySimpleGUI as sg

import address
 
sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
txt_size = (16, 1)

def open_dialog():
    """
    Open a dialog window to get the user input
    """
    font=("Arial", 14)

    layout = [  [sg.Text('')],
        [sg.Text('Please enter the address information:')], 
                [sg.Text('City/town', size=(txt_size)), sg.InputText('karijoki', size=20, font=font)],
                [sg.Text('Post code', size=(txt_size)), sg.InputText(size= 4)],
                [sg.Text('Street', size=(txt_size)), sg.InputText(size = 20)],
                [sg.Text('Street number', size=(txt_size)), sg.InputText(size = 4)],
                   [sg.Text('')] , 
                [sg.Button('Ok'), sg.Button('Cancel')]
             ]

    # Create the Window
    window = sg.Window('Input address', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        print("jsdfjksd")
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        print('You entered ', values[0])
        print('You entered ', values[1])
        print('You entered ', values[2])
        print('You entered ', values[3])
        #TÄHÄN chekkaus, jos osoite on oikea
        json_info  = address.get_address()

        if json_info is None:
            error_message("Address not found")
            continue
        else:
            whole_address = f"{values[2]} {values[3]}, {values[1]}, {values[0]}".upper()
            window.close()
            return json_info, whole_address
    

def error_message(message : str):
    """
    Open a dialog window with an error message
    """
    layout = [  [sg.Text('')],
                [sg.Text(message)],
                [sg.Button('Ok')]
             ]

    # Create the Window
    window = sg.Window('Error', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Ok': # if user closes window or clicks ok
            break
    
open_dialog()
