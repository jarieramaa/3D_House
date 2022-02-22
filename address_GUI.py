
""" simple dialog with a text input fields for user to enter a city, postcode, street and street number
    and a button to submit the data.
"""

import PySimpleGUI as sg

import address
 
sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
txt_size = (16, 1)

def get_address(test = False):
    """
    Open a dialog window to get the user input
    """
    font=("Arial", 14)

    layout = [  [sg.Text('')],
        [sg.Text('Please enter the address information:', font=font)], 
                [sg.Text('City/town', size=(txt_size), font=font), sg.InputText('karijoki', size=20, font=font)],
                [sg.Text('Post code', size=(txt_size), font=font), sg.InputText(size= 4, font = font)],
                [sg.Text('Street', size=(txt_size), font=font), sg.InputText(size = 20, font = font)],
                [sg.Text('Street number', size=(txt_size), font=font), sg.InputText(size = 4, font = font)],
                   [sg.Text('')] , 
                [sg.Button('Ok', font=font), sg.Button('Cancel', font=font)]
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
        json_coordinates  = address.get_address(values, test)
        print("json_info", json_coordinates)
        if json_coordinates == (None, None) or json_coordinates is None:
            print("opening dialog")
            sg.popup_ok("Address not found!",font=font)
            #error_message("The address is not valid", font)
            continue
        else:
            print("close window")
            whole_address = f"{values[2]} {values[3]}, {values[1]}, {values[0]}".upper()
            window.close()
            return json_coordinates, whole_address
    

    
