from machine import Pin, Timer
from neopixel import Neopixel

led = Pin("LED", Pin.OUT)
tim = Timer()

adc = machine.ADC(28)
adcvalue = 0
pixels = Neopixel(16*16, 0, 2, "GRB") 

val = 0
lastBr = 0
dir = True

def tick(timer):
    global led
    led.toggle()

tim.init(freq=1, mode=Timer.PERIODIC, callback=tick)
brDecay = 50

while(True):
    adcvalue = adc.read_u16()
    
    adcc = int(3000*(adcvalue/65000))
    
    print(adcc)
    
    val = val + (40*(1 if dir else -1))
    
    if val >= 2000:
        dir = False
    elif val <= 0:
        dir = True
    
#     follow ADC
    br = 255 if adcc > 255 else int(adcc)
    br = 1 if adcc < 1 else int(adcc)
    
    if(br < lastBr):
        br = br - brDecay
        
    pixels.brightnessvalue = br if br > 5 else 5  
    
#     up and down
    r=int(val/80)

    color = (3, 4+r, 30-r)
    rgbw1 = color
    rgbw2 = (56,20+0.1*r, 8-0.1*r)
    
#     pixels.set_pixel_line_gradient(0, 255, rgbw1, rgbw2) # display parpadea cuando hay que llegar a muchos pixeles, se nota latencia
    
    color = pixels.colorHSV(br, 100, 100)
    pixels.fill(color)
    
#     hay que investigar porqué el color (aprox) blanco se consigue con (r,g,b)=(94,60,255) en la matriz 16x16
#     con el r=94, g=60, y bajando el azul de 255 se consigue blanco más cálido, pero al bajar el azul el verde hay que bajarlo un poco tambien
#     pixels.fill((94,50,100))
#     pixels.fill((94,60,255))
    pixels.show()
    lastBr = br