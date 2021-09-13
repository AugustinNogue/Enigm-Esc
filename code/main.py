#!/usr/bin/env python3

# Author: AUGUSTIN NOGUE <augustin.nogue@student.unamur.be>
# Repository: https://github.com/UNamurCSFaculty/2021_INFOB318_ENIGM-ESC
#
# Date Created: December 10, 2021
# Last Modified: March 07, 2021
#
# Developed and tested using Python 3.7.3

import tkinter as tk
from raspberry import *
from configuration import *


class MainWindow(tk.Tk):
    def __init__(self):
        """
        Initialisation of the main window
        :author: AUGUSTIN NOGUE
        :version: 1.0
        """
        super().__init__()
        # Name of the window
        self.title("ENIGM-ESC")
        # Size of the window
        self.geometry("1920x1080")
        self.attributes('-fullscreen', True)
        self.resizable(False, False)
        # Reference color of the Unamur University
        self.unamur_green = '#56b04c'

        # Reference Coordinates
        self.x_size = 1920
        self.y_size = 1080
        self.CENTER_COORD = (self.x_size / 2, self.y_size / 2)
        self.TOP_CENTER_COORD = (self.x_size / 2, 50)
        self.RIGHT_COORD = ((self.x_size / 2) / 2, 250)
        self.LEFT_COORD = (self.x_size - (self.x_size / 2) / 2, 250)

        # Task status
        self.tasks_status = [False, False, False, False, False]
        # Boolean to know if we are in selection screen
        self.in_selection_screen = False

        # Main window characteristics
        self.main_window = tk.Canvas(self, bg="black", width=self.x_size, height=self.y_size)
        self.main_window.pack(side=tk.LEFT, anchor=tk.N)
        # Bind escape to the exit function
        self.bind("<Escape>", exit)

        # Display last image of the list while the arduino establish connection.
        self.display_image(pictures_for_frame[len(pictures_for_frame)-1], self.CENTER_COORD, True)
        # First phase of the game display pictures (fake picture frame) while fsr isn't pressed
        self.picture_frame(pictures_for_frame, time_between_images)

        self.once_fsr_passed()

        # Once the fsr is pressed, wait for the load cell weight to be heavy enough
        while not get_arduino_sensor_status("load cell"):
            pass

        # Once the load cell weight is enough
        self.once_load_cell_passed()
        # Bind mouse left click to the mouse_left_click function
        self.bind("<Button-1>", self.mouse_left_click)

    def mouse_left_click(self, event):
        """
        Record the different left mouse click even and react base on their coordinates
        :param event: event
        :author: AUGUSTIN NOGUE
        :version: 1.0
        """
        # Center Left of the screen
        if event.x < 960 and 100 < event.y < 880 and self.in_selection_screen and not self.win_conditions():
            # Load the floppy view
            self.floppy_view()
            self.in_selection_screen = False
        # Center Right of the screen
        if event.x > 960 and 100 < event.y < 880 and self.in_selection_screen and not self.win_conditions():
            # Load the RFID view
            self.rfid_view()
            self.in_selection_screen = False
        # Top left of the screen
        if event.x < 960 and event.y < 100 and not self.win_conditions():
            # Back to the wait screen for player actions
            self.once_load_cell_passed()
        # Top right of the screen
        if event.x > 1800 and event.y < 100:
            deactivate_solenoide()
            # Leave the program
            exit()
        # Bottom of the screen
        if self.win_conditions() and 880 < event.y:
            # End screen
            self.end_screen()

    def exit(self):
        """
        Exit function link to the escape key
        :author: AUGUSTIN NOGUE
        :version: 1.0
        """
        # Leave the program
        self.destroy()

    def win_conditions(self) -> bool:
        """
        Check if the win conditions are met or not
        Return true if they are and false if they aren't.
        :return: bool
        :author: AUGUSTIN NOGUE
        :version: 1.0
        """
        # Check if there is task not completed
        for task in self.tasks_status:
            if not task:
                return False

        return True

    def display_image(self, image: str, coord: tuple, clear: bool):
        """
        Display image based on the coordinates (coord) and the path of the file.
        The image can only be a .png file.
        If the boolean clear is true clear the window.

        :param image: string
        :param coord: tuple
        :param clear: boolean
        :author: AUGUSTIN NOGUE
        :version: 1.0
        """
        assert type(image) == str, 'Wrong file name type, should be string'
        assert image.endswith('.png'), 'Image should be of type .png'
        assert type(coord) == tuple, 'Coordinates should be a tuple'
        assert (all(isinstance(c, int) for c in coord) or all(isinstance(c, float) for c in coord)), \
            'Coordinates should be int or float'
        # Clear window
        if clear:
            self.main_window.delete("all")

        # Display of the image
        self.picture = tk.PhotoImage(file=image)
        self.main_window.create_image(coord, image=self.picture)
        self.update()

    def picture_frame(self, pictures_list: list, time_between_pictures: int):
        """
        Cycle through the picture list displaying them.
        Time in between images are given by the integer time_between_pictures
        :param pictures_list: list
        :param time_between_pictures: int
        :author: AUGUSTIN NOGUE
        :version: 1.0
        """
        assert all(isinstance(picture, str) for picture in pictures_list), 'Picture name should be a string'
        assert all(picture.endswith('.png') for picture in pictures_list), 'Picture should be a .png file'
        assert type(time_between_images) == int, 'time between pictures should be an integer'
        i = 0
        modulo = len(pictures_list)
        # Picture Frame loop waiting for fsr activation
        while not get_arduino_sensor_status("fsr"):
            # Display last image waiting for the serial communication to be established
            self.display_image(pictures_list[(i % modulo)], self.CENTER_COORD, True)
            i += 1
            time_before = time.time()
            # Wait for the specified amount of time between pictures while checking for fsr status.
            while time.time() - time_before < time_between_pictures and not get_arduino_sensor_status("fsr"):
                pass

    def once_fsr_passed(self):
        """
        Display the after fsr is passed window
        :author: AUGUSTIN NOGUE
        :version: 1.0
        """
        # Delete all elements of main window
        self.main_window.delete("all")
        # Create desk error text
        self.main_window.create_text(self.CENTER_COORD, text="Desk Error Detected!", fill="white", font=(None, 100))
        # Update main window
        self.update()
        if not get_arduino_sensor_status("load cell"):
            time_before = time.time()
            # Wait for the specified amount of time between pictures while checking for fsr status.
            while time.time() - time_before < time_before_lc_clue and not get_arduino_sensor_status("load cell"):
                pass
            # Call the function to display clue for the load cell if the load cell wasn't activated in time.
            if not get_arduino_sensor_status("load cell"):
                self.load_cell_clue()

    def load_cell_clue(self):
        """
        Function to display the clue for the load cell.
        :author: AUGUSTIN NOGUE
        :version: 1.0
        """
        self.main_window.delete("all")
        self.display_image(assets_folder + '/clean_desk_clue.png', self.CENTER_COORD, True)
        self.main_window.create_text(self.TOP_CENTER_COORD, text="Here is a clue!", fill="white", font=(None, 50))
        self.update()

    def informative_layout(self, top_page_text: str, separator: bool, back_button: bool):
        """
        Function to display the informative layout.
        It consist of a header, a text in the header, a footer and a middle of a screen.
        If the boolean separator is true then the middle of the screen is divided in two equal parts by a separator.
        If the back button boolean is true then a back button is displayed on the top left corner.
        :param top_page_text: str
        :param separator: boolean
        :param back_button: boolean
        :author: AUGUSTIN NOGUE
        :version: 1.0
        """

        assert type(top_page_text) == str, 'Top page text should be of type string'
        assert type(separator) == bool, 'Separator should be of type bool'
        assert type(back_button) == bool, 'Back button should be of type bool'

        # Header
        self.main_window.create_rectangle(0, 0, self.x_size, 100, fill=self.unamur_green)
        self.main_window.create_text(self.TOP_CENTER_COORD, text=top_page_text, fill="black", font=(None, 65))
        # Footer
        self.main_window.create_rectangle(0, self.y_size - 200, self.x_size, self.y_size, fill=self.unamur_green)
        # Separator
        if separator:
            self.main_window.create_rectangle((self.x_size / 2) - 5, 100, (self.x_size / 2) + 5, self.y_size - 200,
                                              fill=self.unamur_green)
        # Back button
        if back_button and not self.win_conditions():
            self.display_image(assets_folder + '/back_button.png', (50, 50), False)

        # if winning conditions are met display and back button is true the access to end screen
        if back_button and self.win_conditions():
            self.main_window.create_text((950, self.y_size - 100), text="Click here to access win screen",
                                         fill="orange", font=(None, 70))
        else:
            # information of the solving steps of the game
            self.main_window.create_text((200, self.y_size - 170), text="Steps completed: ", fill="black",
                                         font=(None, 30))
            self.main_window.create_text((150, self.y_size - 100), text="1: %s" % str(self.tasks_status[0]),
                                         fill="black", font=(None, 30))
            self.main_window.create_text((550, self.y_size - 100), text="2: %s" % str(self.tasks_status[1]),
                                         fill="black", font=(None, 30))
            self.main_window.create_text((950, self.y_size - 100), text="3: %s" % str(self.tasks_status[2]),
                                         fill="black", font=(None, 30))
            self.main_window.create_text((1350, self.y_size - 100), text="4: %s" % str(self.tasks_status[3]),
                                         fill="black", font=(None, 30))
            self.main_window.create_text((1750, self.y_size - 100), text="5: %s" % str(self.tasks_status[4]),
                                         fill="black", font=(None, 30))

        self.update()

    def once_load_cell_passed(self):
        """
        Display the after load cell is passed window
        :author: AUGUSTIN NOGUE
        :version: 1.0
        """
        # Delete all elements of main window
        self.main_window.delete("all")
        # Floppy Logo
        self.picture1 = tk.PhotoImage(file=assets_folder + '/save.png')
        self.main_window.create_image(self.RIGHT_COORD, image=self.picture1)
        self.main_window.create_text(((self.x_size / 2) / 2, 550), text="Insert Floppy Disk", fill="orange",
                                     font=(None, 70))
        # Rfid Logo
        self.picture2 = tk.PhotoImage(file=assets_folder + '/rfid_logo.png')
        self.main_window.create_image(self.LEFT_COORD, image=self.picture2)
        self.main_window.create_text((self.x_size - (self.x_size / 2) / 2, 550), text="Scan RFID card",
                                     fill="orange", font=(None, 70))

        # Load the layout
        self.informative_layout("Tap your choice: ", True, False)
        self.in_selection_screen = True

    def floppy_view(self):
        """
        Display the floppy view after the floppy read was chosen by the player
        :author: AUGUSTIN NOGUE
        :version: 1.0
        """
        # Delete all elements of main window
        self.main_window.delete("all")
        # Waiting text to display
        self.main_window.create_text(self.CENTER_COORD, text="Wait a minute will you \nIt's old tech !", fill="orange",
                                     font=(None, 100))
        # Load informative layout
        self.informative_layout("Reading data from Floppy Disk: ", False, True)
        # Load text from floppy disk
        text = text_from_floppy(floppy_path + "/clue.txt")
        
        # Smaller font for bigger clues
        if len(text) > 300:
            font_size = 20
        else:
            font_size = 30

        # Delete all elements of main window
        self.main_window.delete("all")
        # Text from floppy disk
        self.main_window.create_text(self.CENTER_COORD, text=text, fill="orange",
                                     font=(None, font_size))
        # Load informative layout
        self.informative_layout("Reading data from Floppy Disk: ", False, True)

    def rfid_view(self):
        """
        Display the RFID view after the RFID scan was chosen by the player.
        The information will change base on the card scanned.
        :author: AUGUSTIN NOGUE
        :version: 1.0
        """
        # Delete all elements of main window
        self.main_window.delete("all")
        # Scanning badge text
        self.main_window.create_text(self.CENTER_COORD, text="Scanning Badge...", fill="orange",
                                     font=(None, 100))
        # Load informative layout
        self.informative_layout("RFID SCAN: ", False, True)
        # Scan RFID card
        scan = rfid_scan()
        # Delete all elements of main window
        self.main_window.delete("all")
        # if scan was done
        if scan:
            self.main_window.create_text((self.x_size / 2, (self.y_size / 2) - 100), text="Badge Scanned successfully",
                                         fill=self.unamur_green, font=(None, 70))
            i = 0
            # Run through the task and UIDS list to check if the card link to them is in it
            while i < 5:
                # If the card is the right one and the task linked to it is not completed
                if scan == rfid_uids[i] and self.tasks_status[i] is False:
                    # If the task number is strictly bigger than 0 and the task before it is false
                    if i > 0 and not self.tasks_status[i-1]:
                        self.main_window.create_text((self.x_size / 2, (self.y_size / 2) + 70),
                                                     text="Wrong order", fill="orange", font=(None, 100))
                        self.main_window.create_text((self.x_size / 2, (self.y_size / 2) + 200),
                                                     text="One less chance available, careful now !", fill="orange",
                                                     font=(None, 70))
                    # If the task is the first one or the task before it is completed
                    else:
                        self.tasks_status[i] = True
                        self.main_window.create_text((self.x_size / 2, (self.y_size / 2) + 70),
                                                     text="Task %s has been completed" % str(i + 1), fill="orange",
                                                     font=(None, 100))
                    break

                # If the card is the right one and the task linked to it is completed
                elif scan == rfid_uids[i] and self.tasks_status[i] is True:
                    self.main_window.create_text((self.x_size / 2, (self.y_size / 2) + 70),
                                                 text="Task %s has already been completed" % str(i + 1),
                                                 fill="orange",
                                                 font=(None, 70))
                    break
                # If the card is a wrong card
                else:
                    i += 1
                    if i == 5:
                        self.main_window.create_text((self.x_size / 2, (self.y_size / 2) + 70),
                                                     text="Wrong Card", fill="orange", font=(None, 100))
                        self.main_window.create_text((self.x_size / 2, (self.y_size / 2) + 200),
                                                     text="One less chance available, careful now !", fill="orange",
                                                     font=(None, 70))
        # If there is a scan error
        else:
            self.main_window.create_text((self.x_size / 2, (self.y_size / 2) - 100), text="Error scan badge",
                                         fill=self.unamur_green, font=(None, 70))
        # Load informative layout
        self.informative_layout("RFID SCAN: ", False, True)

    def end_screen(self):
        """
        Display the end screen view after the player has completed all the tasks and tapes the go to end screen area.
        :author: AUGUSTIN NOGUE
        :version: 1.0
        """
        # Delete all elements of main window
        # deactivate_solenoide()
        self.main_window.delete("all")
        # Load the victory image
        self.win_image = tk.PhotoImage(file=assets_folder + '/congrats.png')
        self.main_window.create_image(self.CENTER_COORD, image=self.win_image)
        # Load informative layout
        deactivate_solenoide()
        self.informative_layout("Well Done: Desk is now open", False, False)


if __name__ == "__main__":
    # Setup arduino
    setup_arduino()
    # Automatically list of pictures to display in picture frame
    pictures_for_frame = get_files_in_directory(picture_frame_folder, ".png")
    w = MainWindow()
    w.mainloop()
    # Cleanup arduino
    cleanup_arduino()


