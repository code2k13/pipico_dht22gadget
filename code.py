import time
import board
import adafruit_dht
import busio
from adafruit_st7735r import ST7735R
import displayio
import terminalio
from adafruit_display_text import label

dht = adafruit_dht.DHT22(board.GP28)
mosi_pin = board.GP11
clk_pin = board.GP10
reset_pin = board.GP17
cs_pin = board.GP18
dc_pin = board.GP16

displayio.release_displays()
spi = busio.SPI(clock=clk_pin, MOSI=mosi_pin)
display_bus = displayio.FourWire(
    spi, command=dc_pin, chip_select=cs_pin, reset=reset_pin
)
display = ST7735R(display_bus, width=128, height=160, bgr=True)

bmp_group = displayio.Group()
bitmap = displayio.OnDiskBitmap("/thermometer.bmp")
thermometer = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
thermometer.x = 80
thermometer.y = 10
thermometer.flip_x = True
bmp_group.append(thermometer)

bitmap = displayio.OnDiskBitmap("/humidity.bmp")
humidity = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
humidity.x = 15
humidity.y = 10
bmp_group.append(humidity)


old_temp = ''
old_humid = ''

lbl_temp = label.Label(terminalio.FONT, text="", color=0xFFC100, label_direction="DWR", scale=4)
lbl_temp.x = 100
lbl_temp.y = 50
display.show(bmp_group)
bmp_group.append(lbl_temp)

lbl_hum = label.Label(terminalio.FONT, text="", color=0x0000FF, label_direction="DWR", scale=4)
lbl_hum.x = 40
lbl_hum.y = 50
bmp_group.append(lbl_hum)

while True:
    h = dht.humidity
    time.sleep(1)
    t = dht.temperature
    time.sleep(1)
    lbl_temp.text = str(t)
    lbl_hum.text =  str(h)
    time.sleep(1)