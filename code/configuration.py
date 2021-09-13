#!/usr/bin/env python3

# Author: AUGUSTIN NOGUE <augustin.nogue@student.unamur.be>
# Repository: https://github.com/UNamurCSFaculty/2021_INFOB318_ENIGM-ESC
#
# Date Created: December 10, 2021
# Last Modified: March 07, 2021
#
# Developed and tested using Python 3.7.3

import os
from raspberry import *

# UIDS of the RFID cards composing the solution of the escape game
rfid_uids = [[25, 201, 83, 179, 48], [105, 26, 84, 179, 148], [249, 138, 83, 179, 147], [137, 225, 73, 178, 147],
             [217, 194, 99, 178, 202]]
# Folder locations of assets necessary to run the program
assets_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Assets/'))
# Folder with picture to display in the picture frame
picture_frame_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'PictureFrame/'))

# Path of the floppy mount
floppy_path = os.path.abspath("/media/pi")
# Time between pictures in picture frame
time_between_images = 20
# Time before clue leading to load cell
time_before_lc_clue = 30
# Mount command
mount_command = "sudo mount -t msdos /dev/sda /media/pi"
# Unmount command
unmount_command = "sudo umount -t msdos /dev/sda"

# Arduino
# Characteristic of the serial communication
# First the port then the data rate and then the timout option
ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=10)
