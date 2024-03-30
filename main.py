from machine import Pin, Timer
from neopixel import Neopixel
import math

led = Pin("LED", Pin.OUT)
tim = Timer()

adc = machine.ADC(28)
adcvalue = 0
pixels = Neopixel(16*16, 0, 2, "GRB") 

val = 0
dir = True

def tick(timer):
    global led
    led.toggle()

tim.init(freq=1, mode=Timer.PERIODIC, callback=tick)

def measure():
    raw = 0
    numsamples = 700
    rms = 0
    for i in range(numsamples):
        raw = 65535 - adc.read_u16()
        amp = abs(raw - 32767)
        rms = rms + (amp*amp)

    rms = rms/numsamples
    dB = 20.0 * math.log10(math.sqrt(rms) / 32767);
#     print(dB)
    return dB

while(True):
    adcvalue = adc.read_u16()
    
#     print(int(2000*(adcvalue/65000)))
    
#     adcc = int(2000*(adcvalue/65000))
    
    
#     follow ADC
    br= abs(measure() *1000)
    
    
    print(br)
    pixels.brightnessvalue = br 
    
        
    val = val + (40*(1 if dir else -1))
    
    if val >= 2000:
        dir = False
    elif val <= 0:
        dir = True
    
#     up and down
    r=int(val/80)

    color = (3, 4+r, 30-r)
    rgbw1 = color
    rgbw2 = (56,20+0.1*r, 8-0.1*r)
    
#     pixels.set_pixel_line_gradient(0, 255, rgbw1, rgbw2) # display parpadea cuando hay que llegar a muchos pixeles, se nota latencia
    
#     hay que investigar porqué el color (aprox) blanco se consigue con (r,g,b)=(94,60,255) en la matriz 16x16
#     con el r=94, g=60, y bajando el azul de 255 se consigue blanco más cálido, pero al bajar el azul el verde hay que bajarlo un poco tambien
    pixels.fill((94,50,100))
#     pixels.fill((94,60,255))
    pixels.show()    