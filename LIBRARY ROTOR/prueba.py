import utime
from machine import I2C,Pin
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from machine import Pin
from time import sleep_ms
from rotary_irq import RotaryIRQ
#Dirección del I2C y tamaño del LCD
I2C_ADDR  =  0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 19
# Raspberry Pi Pico
#i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
#Esp8266
i2c = I2C(sda=Pin(4), scl=Pin(5), freq=100000)
#Configuración LCD
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
battery_0 = [0x1D,
  0x15,
  0x17,
  0x00,
  0x11,
  0x1B,
  0x0A,
  0x04]
battery_15 = [0x1F,
  0x00,
  0x15,
  0x00,
  0x11,
  0x1B,
  0x0A,
  0x04]
battery_30 = [0x00,
  0x0E,
  0x11,
  0x11,
  0x11,
  0x0A,
  0x1B,
  0x00]
battery_45 = [0x1F,
  0x00,
  0x15,
  0x00,
  0x04,
  0x0A,
  0x0E,
  0x0A]
battery_60 = [  0x05,
  0x04,
  0x0D,
  0x1C,
  0x1D,
  0x0C,
  0x04,
  0x05]
battery_75 = [ 0x00,
  0x00,
  0x09,
  0x0D,
  0x1F,
  0x0D,
  0x09,
  0x00]
battery_100 = [ 0x04,
  0x04,
  0x06,
  0x1F,
  0x1F,
  0x06,
  0x04,
  0x04]

def lcd_str(message, col, row):
    lcd.move_to(col, row)
    lcd.putstr(message)
def main():
    lcd.custom_char(0, bytearray(battery_0))
    lcd.custom_char(1, bytearray(battery_15))
    lcd.custom_char(2, bytearray(battery_30))
    lcd.custom_char(3, bytearray(battery_45))
    lcd.custom_char(4, bytearray(battery_60))
    lcd.custom_char(5, bytearray(battery_75))
    lcd.custom_char(6, bytearray(battery_100))


r = RotaryIRQ(pin_num_clk=32, 
              pin_num_dt=33, 
              min_val=0, 
              max_val=19, 
              reverse=True, 
              range_mode=RotaryIRQ.RANGE_WRAP)
sw = Pin(34, Pin.IN)              
val_old = r.value()
isRotaryEncoder = False

while True:
    if sw.value()==1:
        isRotaryEncoder = not isRotaryEncoder
        if isRotaryEncoder==True:
            print('Rotary Encoder is now enabled.')
        else:
            print('Rotary Encoder is now disabled.')
            
    if isRotaryEncoder==True:
        val_new = r.value()
        if val_old != val_new:
            val_old = val_new
            print('result = {}'.format(val_new))

    sleep_ms(200)