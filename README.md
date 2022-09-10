# atc-matrixportal
Display local air traffic on a retro 64x32 LED matrix, powered by Adafruit's Matrix Portal M4.

![atc_matrix](https://user-images.githubusercontent.com/16847660/182083309-c92dc9a3-b443-4912-87bd-5bb552238625.png)

## Important: Install the included firmware first!
The Adafruit Matrix Portal M4 appears to have an unresolved bug when calling a URL, which is addressed in the included firmware (UF2). Install this firmware as you normally would on the Matrix Portal M4 -- double tap the reset button on your board for the BOOT drive to show up, and then drag/drop the UF2 file into BOOT, and wait for the board to reset. You should see the CIRCUITPY drive now instead of BOOT.

## Upload files to Matrix Portal M4
Upload the lib, code.py, secrets.py and the included font (tom-thumb.bdf) to the CIRCUITPY drive, and wait for the board to reset. Before uploading these files, you need to follow the usage instructions below.


