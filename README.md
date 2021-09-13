# 2021_INFOB318_ENIGM-ESC
## In order to use the ENIGM-ESC code

You need to install the [pi-rc522 module](https://github.com/ondryaso/pi-rc522).

All the following information are coming from the page of the module:

Based on [MFRC522-python](https://github.com/mxgxw/MFRC522-python/blob/master/README.md).

Install using pip:
```
pip install pi-rc522
```

Or get source code from Github:
```
git clone https://github.com/ondryaso/pi-rc522.git
cd pi-rc522
python setup.py install
```
You'll also need to install the [**spidev**](https://pypi.python.org/pypi/spidev) and [**RPi.GPIO**](https://pypi.python.org/pypi/RPi.GPIO) libraries on Raspberry PI, and [**Adafruit_BBIO**](https://github.com/adafruit/adafruit-beaglebone-io-python) on Beaglebone Black (which should be installed by default).

[MIFARE datasheet](https://www.nxp.com/docs/en/data-sheet/MF1S50YYX_V1.pdf) can be useful.

## To run the code

In the code directory:
```
python3 main.py
```
## More information will follow with the documentation roll out
