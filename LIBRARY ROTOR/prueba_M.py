import utime
from machine import I2C,Pin,ADC
from time import sleep_ms
from rotary_irq import RotaryIRQ  #encoder rotatorio
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

#Direccion del I2C y tamaño del LCD
I2C_ADDR = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 19
#ESP32 Configuracion
i2c = I2C(sda=Pin(4), scl=Pin(5), freq=100000)
#Definir objeto LCD
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

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
fle_2 = [  0x00,
  0x04,
  0x0C,
  0x1F,
  0x1F,
  0x0C,
  0x04,
  0x00]

def volt():
    lcd.clear() 
    lcd_str("voltimetro",5,0)
    lcd_str("200mV",1,1)
    lcd_str("2V",8,1)
    lcd_str("20V",12,1)
    lcd_str("200V",2,2)
    lcd_str("2V",9,2)
    lcd_str("1000V",13,2)
    
    utime.sleep(8)
    
def ohm():
    lcd.clear()
    lcd_str("ohmetro",5,0)

def A():    
    lcd.clear()
    lcd_str("amperimetro",5,0)

def lcd_str(message, col, row):
    lcd.move_to(col, row)
    lcd.putstr(message)
  

def main(): 
    
#encoder
    r = RotaryIRQ(pin_num_clk=18, 
                  pin_num_dt=33, 
                  min_val=0, 
                  max_val=19, 
                  reverse=True, 
                  range_mode=RotaryIRQ.RANGE_WRAP)
    sw = Pin(34, Pin.IN)              
    val_old = r.value()
    isRotaryEncoder = False
  
    
    lcd.custom_char(1, bytearray(VDC_1)) #V
    lcd.custom_char(2, bytearray(R))   #R
    lcd.custom_char(3, bytearray(A_0))  #A
    lcd.custom_char(4, bytearray(fle_0)) #>
    lcd.custom_char(5, bytearray(fle_1)) #^
    lcd.custom_char(6, bytearray(fle_2)) #<
    
    while True:
        #if sw.value()==1:
        isRotaryEncoder = not isRotaryEncoder
         #   if isRotaryEncoder==True:
          #      print('Rotary Encoder is now enabled.')     
          #  else:
          #      print('Rotary Encoder is now disabled.')
                
        if isRotaryEncoder==True:
            val_new = r.value()
            if val_old != val_new:
                val_old = val_new
                print('result = {}'.format(val_new))
        #sleep_ms(60)
        lcd.clear()
        utime.sleep(1)
        lcd_str("multimetro digital",1,0)
        #lcd_str("ESP32",1,1)
        lcd_str(str(val_new),17,3) # la funcion str(val_new) es para convertir a numerico a stregin
        lcd_str(" ",1,2)
        lcd.putchar(chr(1))
        lcd_str(" ",5,2)
        lcd.putchar(chr(2))
        lcd_str(" ",9,2)
        lcd.putchar(chr(3))
        lcd_str("atras",14,2)
        utime.sleep(1)
        #if sw.value()==1:
        #    lcd_str("data",8,1)
        
        
        if val_new ==4:
           lcd_str("",19,2)
           lcd.putchar(chr(6))
        
        if val_new ==1 and sw.value() ==1 :
            lcd_str(" ",1,3)
            lcd.putchar(chr(5))
            utime.sleep(1)
            volt()
            sleep_ms(100)  

        elif val_new ==2 and sw.value() ==0:
            lcd_str(" ",5,3)
            lcd.putchar(chr(5))
            utime.sleep(1)
            ohm()
            sleep_ms(100)
            
        elif val_new ==3 and sw.value() ==1:
            lcd_str(" ",9,3)
            lcd.putchar(chr(5))
            utime.sleep(1)
            A()
            sleep_ms(100)
            
        else:
            lcd_str("No selec medida",1,3)
        
        sleep_ms(380)       
        
    
    
    
if __name__ == '__main__':
    main() 