import utime
from machine import I2C, Pin, ADC
from time import sleep_ms
from pico_i2c_lcd import I2cLcd

#import pcf8574

#Direccion del I2C y tamaño del LCD
I2C_ADDR = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 19
#ESP32 Configuracion
i2c = I2C(sda=Pin(4), scl=Pin(5), freq=100000)
#Definir objeto LCD
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
#Definir objeto pcf
"""
pcf = pcf8574.PCF8574(i2c, 0x20)
ON = 1
OFF = 0
"""
#sensor de para voltaje  ( Vadc -- VGadc) = MV 
Vadc = ADC(Pin(32))          # crear objeto ADC en el pin ADC
#Vadc.read()                  # valor de lectura, 0-4095 en el rango de voltaje 0.0v - 1.0v
#Vadc.atten(ADC.ATTN_6DB)    # establecer la atenuación de entrada de 6dB (rango de voltaje aproximadamente 0.0v - 2.00V)
Vadc.atten(ADC.ATTN_11DB)    # Atenuación de 11dB, proporciona un voltaje de entrada máximo de aproximadamente 3.6v
Vadc.width(ADC.WIDTH_12BIT)   # establecer valores de retorno de 11 bits (rango devuelto 0-2047)


VGadc = ADC(Pin(33))          # crear objeto ADC en el pin ADC
#VGadc.read()                  # valor de lectura, 0-4095 en el rango de voltaje 0.0v - 1.0v
VGadc.atten(ADC.ATTN_6DB)    # establecer la atenuación de entrada de 6dB (rango de voltaje aproximadamente 0.0v - 2.00V)
Vadc.width(ADC.WIDTH_11BIT)   # establecer valores de retorno de 11 bits (rango devuelto 0-2047)


#ADC.WIDTH_9BIT: 9 bits.  29=512 ⇒ valores entre 0 y 511.
#ADC.WIDTH_10BIT: 10 bits. 210=1.024 ⇒ valores entre 0 y 1023.
#ADC.WIDTH_11BIT: 11 bits. 211=2.048 ⇒ valores entre 0 y 2047.
#ADC.WIDTH_12BIT: 12 bits. 212=4.096 ⇒ valores entre 0 y 4095 -es la configuración por defecto-.
#https://www.esploradores.com/micropython_adc/
#https://controlautomaticoeducacion.com/micropython/adc-pico-esp/

#ADC.ATTN_0DB: 0 dB de atenuación. Permite un rango de lectura entre 0.0 V y 1.0 V  -es la configuración por defecto-.
#ADC.ATTN_2_5DB: 2.5 dB de atenuación. Permite un rango de lectura entre 0.0 V y 1.34 V.
#ADC.ATTN_6DB: 6 dB de atenuación. Permite un rango de lectura entre 0.0 V y 2.0 V.
#ADC.ATTN_11DB: 11 dB de atenuación. Permite un rango de lectura entre 0.0 V y 3.6 V.


#sensor de para ohmetro
hadc = ADC(Pin(35))          # crear objeto ADC en el pin ADC
#hadc.read()                  # valor de lectura, 0-4095 en el rango de voltaje 0.0v - 1.0v
hadc.atten(ADC.ATTN_11DB)    # establecer la atenuación de entrada de 6dB (rango de voltaje aproximadamente 0.0v - 2.00V)
hadc.width(ADC.WIDTH_12BIT)   # establecer valores de retorno de 9 bits (rango devuelto 0-4096)
# hadc.read()    


analogInputPin = ADC(Pin(34)) # solo un argumento posicional
                              # que es la identificación del pin

#botones 
escala = Pin(18, Pin.IN)
selec = Pin(15, Pin.IN)

lista_V = []
lista_R = []
lista_A = []

MILLIVOLT_PER_AMPERE = 100   #mV por amperio para sensor de 20 amperios
AREF = 3.3 # volt
DEFAULT_OUTPUT_VOLTAGE = 3.3/2  #sensor vcc = 5 V, pero se usa un divisor de voltaje para obtener 1,65 V de 2,5 V para el pin de salida del sensor
ERROR = 0.12 # amperio

VF = 3.0

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
    suma = 0
    lcd.clear()
    lcd_str("voltimetro",5,0)
    lcd_str("200mV",1,1)
    lcd_str("2V",8,1)
    lcd_str("20V",12,1)
    lcd_str("200V",2,2)
    lcd_str("1000V",9,2)
    
    if escala.value()==1:
        while escala.value()==1:
            suma +=1
            print(suma)
            sleep_ms(100)
            if suma==1:
                lcd_str("",0,1)
                lcd.putchar(chr(4))
                utime.sleep(1)
            elif suma==2:
                lcd_str(" ",0,1)
                lcd_str("",7,1)
                lcd.putchar(chr(4))
                utime.sleep(1)
            elif suma==3:    
                lcd_str(" ",7,1)
                lcd_str("",11,1)
                lcd.putchar(chr(4))
                utime.sleep(1)
            elif suma==4:
                lcd_str(" ",11,1)
                lcd_str("",1,2)
                lcd.putchar(chr(4))
                utime.sleep(1)
            elif suma==5:
                lcd_str(" ",1,2)
                lcd_str("",8,2)
                lcd.putchar(chr(4))
                utime.sleep(1)
            else:
                lcd_str(" ",8,2)
                suma=0
        lcd_str(str(suma),16,1)
        
    if selec.value()==1 and suma==1:
        lista_V.clear()
        lista_V.insert(0,'200mV')
        print(lista_V)
    if selec.value()==1 and suma==2:
        lista_V.clear()
        lista_V.insert(1,'2V')
        print(lista_V)
    if selec.value()==1 and suma==3:
        lista_V.clear()
        lista_V.insert(2,'20V')
        print(lista_V)
    if selec.value()==1 and suma==4:
        lista_V.clear()
        lista_V.insert(3,'200V')
        print(lista_V)
    if selec.value()==1 and suma==5:
        lista_V.clear()
        lista_V.insert(4,'1000V')
        print(lista_V)
        
    utime.sleep(3)
    
def ohm():
    lcd.clear()
    suma = 0
    lcd_str("Ohmetro",5,0)
    lcd_str("",1,1)
    lcd.putchar(chr(2))
    lcd_str("-K",2,1)
    lcd.putchar(chr(2))
    lcd_str("M",9,1)
    lcd.putchar(chr(2))
    
    """
    lcd_str("200K",13,1)
    lcd.putchar(chr(2))
    lcd_str("2M",2,2)
    lcd.putchar(chr(2))
    lcd_str("20M",9,2)
    lcd.putchar(chr(2))
    """
    
    if escala.value()==1:
        while escala.value()==1:
            suma +=1
            print(suma)
            sleep_ms(100)
            if suma==1:
                lcd_str("",0,1)
                lcd.putchar(chr(4))
                lcd_str(" ",7,1)
                utime.sleep(1)
            elif suma==2:
                lcd_str(" ",0,1)
                lcd_str("",7,1)
                lcd.putchar(chr(4))
                utime.sleep(1)                
            else:
                lcd_str(" ",8,2)
                suma=0
        lcd_str(str(suma),16,2)
        """
            elif suma==3:    
                lcd_str(" ",7,1)
                lcd_str("",12,1)
                lcd.putchar(chr(4))
                utime.sleep(1)
            elif suma==4:
                lcd_str(" ",12,1)
                lcd_str("",1,2)
                lcd.putchar(chr(4))
                utime.sleep(1)
            elif suma==5:
                lcd_str(" ",1,2)
                lcd_str("",8,2)
                lcd.putchar(chr(4))
                utime.sleep(1)
            """    
    if selec.value()==1 and suma==1:
        lista_R.clear()
        lista_R.insert(0,'K')
        #lista_R.insert(0,'200h')
        print(lista_R)
    if selec.value()==1 and suma==2:
        lista_R.clear()
        lista_R.insert(1,'M')
        #lista_R.insert(1,'2Kh')
        print(lista_R)
    """
    if selec.value()==1 and suma==3:
        lista_R.clear()
        lista_R.insert(2,'200Kh')
        print(lista_R)
    if selec.value()==1 and suma==4:
        lista_R.clear()
        lista_R.insert(3,'2Mh')
        print(lista_R)
    if selec.value()==1 and suma==5:
        lista_R.clear()
        lista_R.insert(4,'20Mh')
        print(lista_R)
    """
    
    utime.sleep(3)

def Amp():    
    lcd.clear()
    suma = 0
    lcd_str("amperimetro",5,0)
    lcd_str("activar",1,1)
    lcd_str("desativar",10,1)
    
    if escala.value()==1:
        while escala.value()==1:
            suma +=1
            sleep_ms(100)
            if suma==1:
                lcd_str("",4,2)
                lcd.putchar(chr(5))
                utime.sleep(1)
            elif suma==2:
                lcd_str(" ",4,2)
                lcd_str("",14,2)
                lcd.putchar(chr(5))
                utime.sleep(1)
            else:
                lcd_str(" ",14,2)
                suma=0
        lcd_str(str(suma),6,2)
        
    if selec.value()==1 and suma==1:
        lista_A.clear()
        lista_A.insert(0,'Aon')
        print(lista_A)
        
    if selec.value()==1 and suma==2:
        lista_A.clear()
        lista_A.insert(1,'Aoff')
        print(lista_A)  
                   
    utime.sleep(3)

    
def lcd_str(message, col, row):
    lcd.move_to(col, row)
    lcd.putstr(message)

def main():
    config = Pin(2, Pin.IN)
    hM = Pin(23, Pin.OUT)
    hMM = Pin(13, Pin.OUT)
    Vs = Pin(19, Pin.IN)
    Rs = Pin(21, Pin.IN)
    As = Pin(22, Pin.IN)
    
    lcd.custom_char(1, bytearray(VDC_1)) #V
    lcd.custom_char(2, bytearray(R))   #R
    lcd.custom_char(3, bytearray(A_0))  #A
    lcd.custom_char(4, bytearray(fle_0)) #>
    lcd.custom_char(5, bytearray(fle_1)) #^
    lcd.custom_char(6, bytearray(fle_2)) #<
  
    while True: 
        lcd.clear()
        lcd_str("multimetro digital",1,0)
        lcd_str("odd one out ",3,1)
        
        #lcd_str("",1,3)
        #lcd.putchar(chr(3))
        lcd_str("",5,3)
        lcd.putchar(chr(2))
        lcd_str("",9,3)
        lcd.putchar(chr(1))
        lcd_str("escala",13,2)
        utime.sleep(1)
            
        if config.value()==1:
            while config.value()==1:
                lcd_str("      ",13,2)
                lcd_str("CONFIG",13,2)
                lista_V.clear()
                lista_R.clear()
                lista_A.clear()
            utime.sleep(1)
        
        if Vs.value()==1:
            while Vs.value()==1:
                volt()
                
        if Rs.value()==1:
            while Rs.value()==1:
                ohm()
        
        if As.value()==1:
            while As.value()==1:
                Amp()
 
# muestra principal voltimetro
        if '200mV' in lista_V:
            lcd_str("200mV",14,3)
            """
            pcf.pin (0, ON)
            pcf.pin (1, OFF)
            pcf.pin (2, OFF)
            pcf.pin (3, OFF)
            pcf.pin (4, OFF)
            print('0 on')
            """
            voltaje = Vadc.read()
            VL = ((1/20480)*voltaje)
            N = round(VL, 3)
            VLmn = str(N)
            lcd_str(VLmn,1,2)
            utime.sleep(1)
            
        if '2V' in lista_V:
            lcd_str("2V",14,3)
            """
            pcf.pin (0, OFF)
            pcf.pin (1, ON)
            pcf.pin (2, OFF)
            pcf.pin (3, OFF)
            pcf.pin (4, OFF)
            print('1 on')
            """
            voltaje = Vadc.read()
            VL = (((1/2275)*voltaje)*10)
            #N = round(VL, 3)
            VLmn = str(VL)
            lcd_str(VLmn,1,2)
            utime.sleep(1)
            
        
        if '20V' in lista_V:
            lcd_str("20V",14,3)
            """
            pcf.pin (0, OFF)
            pcf.pin (1, OFF)
            pcf.pin (2, ON)
            pcf.pin (3, OFF)
            pcf.pin (4, OFF)
            print('2 on')
            """
            voltaje = Vadc.read()
            VL = ((9/2048)*voltaje)
            #N = round(VL, -3)
            VLmn = str(VL)
            print(VL)
            lcd_str(VLmn,1,2)
            utime.sleep(1)
        
        if '200V' in lista_V:
            lcd_str("200V",14,3)
            """
            pcf.pin (0, OFF)
            pcf.pin (1, OFF)
            pcf.pin (2, OFF)
            pcf.pin (3, ON)
            pcf.pin (4, OFF)
            print('3 on')
            """
            voltaje = Vadc.read()
            VL = ((25/512)*voltaje)
            N = round(VL, -3)
            VLmn = str(N)
            lcd_str(VLmn,1,2)
            utime.sleep(1)
            
            
        if '1000V' in lista_V:
            lcd_str("1000V",14,3)
            """"
            pcf.pin (0, OFF)
            pcf.pin (1, OFF)
            pcf.pin (2, OFF)
            pcf.pin (3, OFF)
            pcf.pin (4, ON)
            print('4 on')
            """
            voltaje = Vadc.read()
            VL = ((125/512)*voltaje)
            N = round(VL, -3)
            VLmn = str(N)
            lcd_str(VLmn,1,2)
            utime.sleep(1)

#muestra pirncipal ohmetro
        if 'K' in lista_R:
            lcd_str("K-M",14,3)
            lcd.putchar(chr(2))
            #pcf.pin (5, ON)
            #pcf.pin (6, OFF)
           
            RT = 973
            Ventrada = hadc.read()
            RV= ((1/2048)*Ventrada)
            RX = (Ventrada*RT/(VF-RV))
            n = round(RX, -3)
            RXx = str(n)
            lcd_str(RXx,1,2)
            """
            if RX > 1000:
                lcd_str("K",10,2)
                lcd_str("",11,2)
                lcd.putchar(chr(2))
           """
            print(n)
            print(Ventrada)
            #print(RXx)
            utime.sleep(1)
            # 77.3K - 0.0V
            
        if 'M' in lista_R:
            lcd_str("M",14,3)
            lcd.putchar(chr(2))
            """
            pcf.pin (5, OFF)
            pcf.pin (6, ON)  
            """
            RT = 974
            Ventrada = hadc.read()
            RV= ((1/2048)*Ventrada)
            RX = (Ventrada*RT/(VF-RV))
            n = round(RX, -2)
            RXx = str(n)
            lcd_str(RXx,1,2)
            if RX > 1000000:
                lcd_str("M",10,2)
                lcd_str("",11,2)
                lcd.putchar(chr(2))
            utime.sleep(1)
        """
        if '200Kh' in lista_R:
            lcd_str("200",14,3)
            lcd.putchar(chr(2))
            pcf.pin (5, OFF)
            pcf.pin (6, OFF)
            pcf.pin (7, ON)
            utime.sleep(1)
        
        
        if '2Mh' in lista_R:
            lcd_str("2M",14,3)
            lcd.putchar(chr(2))
            pcf.pin (5, OFF)
            pcf.pin (6, OFF)
            pcf.pin (7, OFF)
            hM.value(ON)
            utime.sleep(1)
            
        if '20Mh' in lista_R:
            lcd_str("20M",14,3)
            lcd.putchar(chr(2))
            pcf.pin (5, OFF)
            pcf.pin (6, OFF)
            pcf.pin (7, OFF)
            hM.value(OFF)
            hMM.value(ON)
            utime.sleep(1)
         """
         
#muestra de principal amperimetro
        if 'Aon' in lista_A:
            lcd_str("",14,3)
            lcd.putchar(chr(3))
            lcd_str("on",15,3)
            analogValue = ADC.read_u16(analogInputPin)    #leer el valor de la señal analógica sin procesar
            sensor_voltage = (analogValue / 65535) * AREF   # calcular el voltaje de salida del sensor a partir del valor analógico sin procesar
            sensor_voltage = (sensor_voltage - DEFAULT_OUTPUT_VOLTAGE ) * 1000   #convertidor a  milli voltios
            dc_current = (sensor_voltage/ MILLIVOLT_PER_AMPERE) - ERROR # amper
            tt = str(dc_current)
            lcd_str(tt,1,2)
            utime.sleep(1)
       
        if 'Aoff' in lista_A:
            lcd_str("",14,3)
            lcd.putchar(chr(3))
            lcd_str("off",15,3)
            utime.sleep(1)
# leer el valor usando la atenuación y el ancho recién configurados

        """
        voltaje = Vadc.read()
        
        VL = ((1/2048)*voltaje)
        print(voltaje)
        print(VL)
        lcd_str(VLmn,1,2)
        utime.sleep(1)
        #sleep_ms(380)       
        """
    
    
    
if __name__ == '__main__' :
    main()
    
    

    