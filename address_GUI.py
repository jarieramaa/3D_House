""" simple dialog with a text input fields for user to enter a city,
postcode, street and street number and a button to submit the data.
"""
import time
import PySimpleGUI as sg


import api_query
import address


class AddressGUI:
    """Graphical user interface for the address input"""

    def __init__(self) -> None:
        """
        Initialize the GUI
        """
        self.window = None
        self.address_data = address.Data(self.window)
        self.time_0 = time.time()

    def get_address(self, test=False):
        """
        Open a dialog window to get the user input
        """
        sg.theme("DarkAmber")  # Add a touch of color
        api_q = api_query.ApiQuery(test)
        font = ("Arial", 14)
        txt_size = (16, 1)
        # my_list =['first item', 'second item', 'third item']

        layout = [
            [sg.Text("")],
            [sg.Text("Please enter the address information:", font=font)],
            [
                sg.Text("Street", size=(txt_size), font=font),
                sg.InputText(size=20, font=font),
            ],
            [
                sg.Text("Street number", size=(txt_size), font=font),
                sg.InputText(size=4, font=font),
            ],
            [
                sg.Text("Post code", size=(txt_size), font=font),
                sg.InputText(size=4, font=font),
            ],
            [
                sg.Text("City/town", size=(txt_size), font=font),
                sg.InputText(size=20, font=font),
            ],
            [sg.Text("")],
            [sg.Checkbox("Show Floor Plan", default=True)],
            [sg.Text("")],
            [sg.Button("Ok", font=font), sg.Button("Cancel", font=font)],
        ]

        # Create the Window
        self.window = sg.Window("Input address", layout)
        self.address_data.window = (
            self.window
        )  # setting the window for the address data class
        # Event Loop to process "events" and get the "values" of the inputs
        is_successful = False
        while is_successful is False:
            event, values = self.window.read()
            print("reading values")
            self.address_data.street = values[0]
            self.address_data.street_nbr = values[1]
            self.address_data.post_code = values[2]
            self.address_data.municipality = values[3]
            draw_polygon = values[4]
            print("self.address_data.street: ", self.address_data.street)
            print("self.address_data.street_nbr: ", self.address_data.street_nbr)
            print("self.address_data.post_code: ", self.address_data.post_code)
            print("self.address_data.municipality: ", self.address_data.municipality)
            print("draw_polygon: ", draw_polygon)

            if event in (
                sg.WIN_CLOSED,
                event == "Cancel",
            ):  # if user closes window or clicks cancel
                break
            if self.address_data.validated is False:
                continue
            print("######## api_q.get_address() ALKAA ######## ")
            self.time_0 = time.time()
            print("time_0: ", self.time_0)
            is_successful = api_q.get_address(self.address_data, test)
            print("######## api_q.get_address() PÄÄTTYY ######## ")
            print("is_successful = ", is_successful)
            print("EVENT:", event, " ---- is_successful", is_successful)
            if event == "Ok" and is_successful:

                the_coordinates, is_successful = api_q.get_coordinates()
                self.address_data.coordinates = the_coordinates
                print(
                    "GUI.get_address: address.coordinates: ",
                    self.address_data.coordinates,
                )
                if is_successful is False or the_coordinates == (None, None):
                    sg.popup_ok(
                        "No address found! Please, make sure that the address is in Flanders.",
                        font=font,
                    )
                else:
                    print(
                        "\n\n>>>>>>> self.address_data", self.address_data.coordinates
                    )
                    return self.address_data, draw_polygon
            else:
                sg.popup_ok(
                    "No address found! \nPlease, make sure that the address is in Flanders.",
                    font=font,
                )

    @property
    def get_start_time(self):
        """
        Get the start time of the program
        """
        return self.time_0

    def close_window(self):
        """
        Close the window"""
        if self.window is not None:
            self.window.close()
