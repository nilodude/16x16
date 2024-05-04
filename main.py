from machine import Pin, Timer
from neopixel import Neopixel
import math
import random

led = Pin("LED", Pin.OUT)
tim = Timer()

adc = machine.ADC(28)
adcvalue = 0
pixels = Neopixel(16*16 + 180, 0, 2, "GRB") 

val = 0
dVal = 5
dir = True

def tick(timer):
    global led
    led.toggle()

tim.init(freq=1, mode=Timer.PERIODIC, callback=tick)

def measure(mean=500):
    dB=0
    raw = 0
    numsamples = mean
    rms = 0
    for i in range(numsamples):
        raw = 65535 - adc.read_u16()
        amp = abs(raw - 32767)
        rms = rms + (amp*amp)
    rms = rms/numsamples
    dB = 20.0 * math.log10(math.sqrt(rms) / 32767);
    return -dB

randomismo = 0
prev = 0
decay = 60
pixels.brightnessvalue=0
pixels.fill((0,0,0))
pixels.show()
while(True):
#     brightness follows ADC
    br= int(measure(400)*1000 -25)
    
#     if(br < 20):
#     print(br)
   
    if br > 500:
        randomismo = random.randrange(-4, 2)
#         print(randomismo)
    
    pixels.brightnessvalue = 0 if br < 2 else (900 if br > 900 else br)
    
        
#     color oscillates at steps of dVal  
    val = val + (dVal*(1 if dir else -1))
    
    if val >= 2000:
        dir = False
    elif val <= 1:
        dir = True
    
    r=int(val/90) + randomismo
#     print(randomismo)
    r = 15 if r > 15 else (-1 if r < -1 else r)
    color = (3*3+r, 1+r, 30-r)
    rgbw1 = color
    rgbw2 = (56,20+0.3*r, 8-0.3*r)
    
    

#     pixels.set_pixel_line_gradient(0, 255, rgbw1, rgbw2) # display parpadea cuando hay que llegar a muchos pixeles, se nota latencia
    
    pixels.fill(rgbw1)
#     hay que investigar porqué el color (aprox) blanco se consigue con (r,g,b)=(94,60,255) en la matriz 16x16
#     con el r=94, g=60, y bajando el azul de 255 se consigue blanco más cálido, pero al bajar el azul el verde hay que bajarlo un poco tambien
#     pixels.fill((94,50,100))
#     pixels.fill((94,60,255))
    
    pixels.show()    