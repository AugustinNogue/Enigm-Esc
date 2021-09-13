#!/usr/bin/env python3

# Author: AUGUSTIN NOGUE <augustin.nogue@student.unamur.be>
# Repository: https://github.com/UNamurCSFaculty/2021_INFOB318_ENIGM-ESC
#
# Date Created: December 10, 2021
# Last Modified: March 07, 2021
#
# Developed and tested using Python 3.7.3

import os
import time
import serial  # Module for communication between the arduino and the Raspberry Pi
from pirc522 import RFID  # Module for RFID
from configuration import *


def setup_arduino():
    """
    Function asking the arduino to reset the FSR pressed and load cell pressed data.
    Activate the solenoide
    :author: AUGUSTIN NOGUE
    :version: 1.0
    """
    ser.write(b"setup\n")


def cleanup_arduino():
    """
    Function asking the arduino to reset the FSR pressed and load cell pressed data.
    Deactivate the solenoide.
    Close the serial communication
    :author: AUGUSTIN NOGUE
    :version: 1.0
    """
    ser.write(b"cleanup\n")
    ser.close()


def deactivate_solenoide():
    """
    Function asking the arduino to deactivate the solenoide.
    :author: AUGUSTIN NOGUE
    :version: 1.0
    """
    ser.write(b"deactivate solenoide\n")


def get_files_in_directory(path: str, file_type: str) -> list:
    """
    Return a list of files of the mentioned type in the path given.
    :param path: string
    :param file_type: string
    :return: files_list: list
    :author: AUGUSTIN NOGUE
    :version: 1.0
    """
    assert type(path) == str, "Path name should be a string"
    assert type(file_type) == str, "File type should be a string"

    files_list = []

    for file in os.listdir(path):
        # Check if the type of the file match the one in parameters
        # If it does append the file path to the list
        if file.endswith(file_type):
            files_list.append(os.path.join(path, file))

    return files_list


def get_arduino_sensor_status(sensor: str) -> bool:
    """
    Get arduino sensor status. Pass the sensor name as an argument.
    It can be a fsr or load cell.
    If the sensor was activated the function returns True.
    Else it will return False.
    There is a function corresponding to the other side
    of the communication in the arduino file.
    :param sensor: string
    :return: bool
    :author: AUGUSTIN NOGUE
    :version: 1.0
    """
    assert type(sensor) == str, "Sensor should be a string"
    assert (sensor == "fsr" or sensor == "load cell"), "Sensor should be FSR or Load cell"

    # Encode sensor name as bytes
    sensor_name_as_byte = sensor.encode("utf-8")
    # Request the FSR status
    ser.write((b"status update %s\n" % sensor_name_as_byte))
    # Read answer and decodes it
    input_str = ser.readline().decode("utf-8").strip()
    # If the FSR was pressed
    if input_str == ("%s activated: true" % sensor):
        return True
    else:
        return False


def read_txt(text_file_path: str) -> str:
    """
    Read and return the text inside of a .txt file.
    :param text_file_path: string
    :return: text: string
    :author: AUGUSTIN NOGUE
    :version: 1.0
    """
    assert type(text_file_path) == str, "text_file_path should be a string"
    assert text_file_path.endswith(".txt"), "File should be of type .txt"

    file = open(text_file_path, encoding="utf8")
    text = file.read()
    file.close()

    return text


def text_from_floppy(floppy_text_path: str) -> str:
    """
    Mount the floppy drive.
    Call the read_txt function to read text from floppy disk.
    Return the text inside the file in the floppy disk.
    Unmount the floppy drive
    :param floppy_text_path: string
    :return: text: string
    :author: AUGUSTIN NOGUE
    :version: 1.0
    """
    assert type(floppy_text_path) == str, "Floppy_Path should be a string"

    try:
        # Try to mount the floppy drive
        os.system(mount_command)
        # Call the read_text function to path of the floppy disk
        text = read_txt(floppy_text_path)
        time.sleep(1)
        # Unmount the floppy drive
        os.system(unmount_command)
    # Catch os errors
    except OSError:
        text = "An error occurred"
    # Cautionary unmounting
    os.system("sudo umount -t msdos /dev/sda")

    return text


def rfid_scan() -> list:
    """
    Scan RFID cards or badges.
    Return the scanned UID

    Based on the code of Ondryaso : https://github.com/ondryaso
    from the pi-rc522 module
    from https://github.com/ondryaso/pi-rc522

    :return: scan: list of integers
    :author: AUGUSTIN NOGUE
    :version: 1.0
    """
    rdr = RFID()
    util = rdr.util()
    scan = []
    rdr.wait_for_tag()
    (error, data) = rdr.request()
    (error, uid) = rdr.anticoll()
    if not error:
        i = 0
        while i < 5:
            scan.append(uid[i])
            i += 1
        util.deauth()

    rdr.cleanup()
    return scan
