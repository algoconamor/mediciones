# More details can be found in TechToTinker.blogspot.com 
# George Bantique | tech.to.tinker@gmail.com
import utime
from machine import I2C,Pin,ADC
from time import sleep_ms
from rotary_irq import RotaryIRQ  #encoder rotatorio
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
import pcf8574

#Direccion del I2C y tamaño del LCD
I2C_ADDR = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 19

#ESP32 Configuracion
i2c = I2C(sda=Pin(4), scl=Pin(5), freq=100000)

#Definir objeto LCD
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

#Definir objeto pcf
pcf = pcf8574.PCF8574(i2c, 0x20)
ON = 1
OFF = 0

#graficos
VAC_0 = [0x1D,
  0x15,
  0x17,
  0x00,
  0x11,
  0x1B,
  0x0A,
  0x04]
VDC_1 = [0x1F,
  0x00,
  0x15,
  0x00,
  0x11,
  0x1B,
  0x0A,
  0x04]
R = [0x00,
  0x0E,
  0x11,
  0x11,
  0x11,
  0x0A,
  0x1B,
  0x00]
A_0 = [0x1F,
  0x00,
  0x15,
  0x00,
  0x04,
  0x0A,
  0x0E,
  0x0A]
A_1 = [0x1D,
  0x15,
  0x07,
  0x00,
  0x04,
  0x0A,
  0x0E,
  0x0A]

buz = [  0x05,
  0x04,
  0x0D,
  0x1C,
  0x1D,
  0x0C,
  0x04,
  0x05]
diode = [0x00,
  0x00,
  0x09,
  0x0D,
  0x1F,
  0x0D,
  0x09,
  0x00]
fle_0 = [ 0x04,
  0x04,
  0x06,
  0x1F,
  0x1F,
  0x06,
  0x04,
  0x04]
fle_1 = [ 0x04,
  0x0E,
  0x1F,
  0x1F,
  0x1F,
  0x0E,
  0x0E,
  0x0E]


def lcd_str(message, col, row):
    lcd.move_to(col, row)
    lcd.putstr(message)
    
#encoder
def main():    
    r = RotaryIRQ(pin_num_clk=32, 
                  pin_num_dt=33, 
                  min_val=0, 
                  max_val=19, 
                  reverse=True, 
                  range_mode=RotaryIRQ.RANGE_WRAP)
    sw = Pin(34, Pin.IN)              
    val_old = r.value()
    isRotaryEncoder = False


    lcd.custom_char(0, bytearray(VAC_0)) #V~
    lcd.custom_char(1, bytearray(VDC_1)) #V
    lcd.custom_char(2, bytearray(R))   #R
    lcd.custom_char(3, bytearray(A_0))  #A
    lcd.custom_char(4, bytearray(A_1))  #A~
    lcd.custom_char(5, bytearray(buz))  #{|:
    lcd.custom_char(6, bytearray(diode)) #D
    lcd.custom_char(7, bytearray(fle_0)) #>
    lcd.custom_char(8, bytearray(fle_1)) #^


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

        #sleep_ms(60)
    
        lcd.clear()
        lcd_str(str(val_new),1,2) # la funcion str(val_new) es para convertir a numerico a stregin
       
        lcd_str("Battery:", 0, 0)
        lcd.move_to(0,1)     
        lcd.putchar(chr(4))
        lcd.move_to(3,3)
        lcd.putchar(chr(2))
        utime.sleep_ms(280)
        
        #Prende los 3 leds
        pcf.pin (0, ON)
        print('0 on')
        pcf.pin (1, ON)
        print('1 on')
        pcf.pin (2, ON)
        sleep_ms(100)
        
        #Apaga los 3 leds

        
        #https://www.profetolocka.com.ar/2021/03/09/micropython-ampliando-la-capacidad-de-gpio-del-esp8266-con-el-pcf8574/
        
        

if __name__ == '__main__':
    main()    