import unittest
from raspberry import *
from configuration import *


# Testing of the arduino serial communication with the pi
class TestArduinoFunctions(unittest.TestCase):
    # Testing of the status of the fsr after setup
    def test_fsr_status(self):
        setup_arduino()
        self.assertEqual(get_arduino_sensor_status("fsr"), False)

    # Testing of the status of the load cell after setup
    def test_load_cell_status(self):
        setup_arduino()
        self.assertEqual(get_arduino_sensor_status("load cell"), False)


# Testing of the function interacting with the files
class TestFileFunctions(unittest.TestCase):

    def test_text_files_in_directory(self):
        self.assertEqual(get_files_in_directory(os.path.join(os.path.dirname(__file__), 'testing/'), "txt"),
                         ['testing/test2.txt', 'testing/test1.txt'])

    def test_png_files_in_directory(self):
        self.assertEqual(get_files_in_directory(os.path.join(os.path.dirname(__file__), 'testing/'), "png"),
                         ['testing/test2.png'])

    def test_read_txt(self):
        self.assertEqual(read_txt(os.path.join(os.path.dirname(__file__), 'testing/test1.txt')), 'foobar')


# Testing of the RFID
class TestRFIDFunctions(unittest.TestCase):
    def test_rfid(self):
        self.assertEqual(rfid_scan(), [25, 201, 83, 179, 48])


if __name__ == '__main__':
    unittest.main()
