# atc-matrixportal
Display local air traffic on a retro 64x32 LED matrix, powered by Adafruit's Matrix Portal M4.

![atc_matrix](https://user-images.githubusercontent.com/16847660/182083309-c92dc9a3-b443-4912-87bd-5bb552238625.png)

## Important: Install the included firmware first!
The Adafruit Matrix Portal M4 appears to have an unresolved bug when calling a URL multiple times, which is addressed in the included firmware (UF2). Install this firmware as you normally would on the Matrix Portal M4 -- double tap the reset button on your board for the BOOT drive to show up, and then drag/drop the UF2 file into BOOT, and wait for the board to reset. You should see the CIRCUITPY drive now instead of BOOT.

## Upload files to Matrix Portal M4
Upload the *lib, code.py, secrets.py* and the included font (*tom-thumb.bdf*) to the CIRCUITPY drive, and wait for the board to reset. Before uploading these files, you need to follow the usage instructions below.

## Usage -- *secrets.py*
First, we need to tell the LED matrix the latitude/longitude coordinate extents for the air traffic you'd like to show on the display, and what you want your home point to be. Additionally, we need to set up Wi-Fi settings. All settings are conveniently located in *secrets.py*. No need to touch *code.py*!

Open *secrets.py* in your text editor, and you'll find:
- ssid -- your Wi-Fi SSID
- password -- your Wi-Fi password
- timezone -- your time zone (Country/City: http://worldtimeapi.org/timezones)
- lon_min -- In WGS84 coordinates (decimals), the Western extent of your desired longitude  
- lat_min -- In WGS84 coordinates (decimals), the Southern extent of your desired latitude  
- lon_max In WGS84 coordinates (decimals), the Eastern extent of your desired latitude  
Note: The Northern extent (lat_max) is automatically calculated such that the geographic extents conform to the same aspect ratio as the 64x32 LED matrix. From here onwards, *code.py* automatically 'downscales' the air traffic data to the 64x32 LEd matrix and converts the lat/long coordinates of air traffic from OpenSky to x, y pixel coordinates.
- osky_name -- This is your OpenSky username, if you are a registered user. Leave empty if you're non-registered, but please beware that the refresh rate (configurable in the DELAY variable in *code.py*) can't exceed 100/day for non-registered users. Read more on [OpenSky](https://openskynetwork.github.io/opensky-api/rest.html).
- osky_pwd : Your OpenSky password
- home_lon : In WGS84 coordinates (decimals), the longitude of your home point. Your home point shows up as a yellow 'plus' sign on the display
- home_lat : In WGS84 coordinates (decimals), the latitude of your home point.

## Known issues
1. OpenSky registered user API access appears to not be working at this time. Credentials don't appear to be passed throuh the GET request.
2. Board may crash from time-to-time if there is an error in fetching the data. Haven't been able to address this with a watchdog timer either due to the DELAY interval, so just tap the manual RESET button if this happens.
