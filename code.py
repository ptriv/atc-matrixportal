import time
import board
import displayio
import adafruit_display_text.label
from adafruit_bitmap_font import bitmap_font
from adafruit_matrixportal.matrix import Matrix
from adafruit_display_text import label
import busio
from digitalio import DigitalInOut
import neopixel
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager
import json
import gc
from microcontroller import watchdog as w
from watchdog import WatchDogMode

# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# If you are using a board with pre-defined ESP32 Pins:
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
"""Use below for Most Boards"""
status_light = neopixel.NeoPixel(
    board.NEOPIXEL, 1, brightness=0.2
)

#Setup Wi-Fi connection manager
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(
    esp, secrets, status_light)

DELAY = 90
M = 64
N = 32

#Initiate bitmap reference variables
i = 0
j = 0

#AREA EXTENT COORDINATE WGS4
lon_min = secrets['lon_min']
lat_min = secrets['lat_min']
lon_max = secrets['lon_max']
lat_max = lat_min+(lon_max-lon_min)/2

lat_height = lat_max - lat_min
lon_width = lon_max - lon_min

home_lon = secrets['home_lon']
home_lat = secrets['home_lat']

#REST API QUERY
user_name = secrets['osky_name']
password = secrets['osky_pwd']
URL = "https://"
URL += "opensky-network.org/api/states/all?"
URL += "lamin={}".format(lat_min)
URL += "&lomin={}".format(lon_min)
URL += "&lamax={}".format(lat_max)
URL += "&lomax={}".format(lon_max)

# Define a custom header as a dict that stores the OpenSky user/pass
my_headers = {user_name: password}

# --- Display setup ---
matrix = Matrix()
display = matrix.display
# --- Drawing setup ---
# Create a Group
group = displayio.Group()
# Create a bitmap object
# width, height, bit depth
# Create a color palette
color = displayio.Palette(4)
color[0] = 0x000000  # black
color[1] = 0x00FFFF
color[2] = 0x000A0A  # light blue (Tail)
color[3] = 0xDD8000  # gold

color_tail = displayio.Palette(4)
color_tail[0] = 0x000000  # black
color_tail[1] = 0x90B9EA  # light blue (Tail)
# Create a TileGrid using the Bitmap and Palette
# Add the TileGrid to the Group

# Initialize Bitmap
bitmap = displayio.Bitmap(64, 32, 2)

tile_grid = displayio.TileGrid(
      bitmap, pixel_shader=color)

group.append(tile_grid)
display.show(group)

font = bitmap_font.load_font("/tom-thumb.bdf")
home_label = label.Label(font, color=color[3], text="+")
home_label.x = int((home_lon - lon_min)/lon_width * M)
home_label.y = int((lat_max - home_lat)/lat_height * N)
group.append(home_label)

#Uncomment to use a watchdog timer. Don't forget to add w.feed()!
#w.mode = WatchDogMode.RESET

def fetch_atc():
    atc_get = wifi.get(URL, headers=my_headers)
    atc_json = atc_get.json()
    atc_json = atc_json["states"]
    print(atc_json)
    print(gc.mem_free())

    long = [sub_list[5] for sub_list in atc_json]
    lat = [sub_list[6] for sub_list in atc_json]

    # Free up some memory
    atc_get.close()
    del atc_json
    del atc_get
    gc.collect()
    bitmap.fill(0)

    for flights in range(len(long)):
        i = lat[flights]
        j = long[flights]
        i = int((- i + lat_max)/lat_height * N)
        j = int((j - lon_min)/lon_width * M)
        bitmap[j, i] = 1

while True:
    try:
        fetch_atc()
    except (ValueError, RuntimeError) as e:
        wifi.reset()
        continue
        print("Failed to get data, retrying\n", e)
    atc_get = None
    time.sleep(DELAY)
