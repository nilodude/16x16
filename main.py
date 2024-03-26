from machine import Pin, Timer
from neopixel import Neopixel

led = Pin("LED", Pin.OUT)
tim = Timer()

pixels = Neopixel(16*16, 0, 2, "GRB") 

val = 0
dir = True
def tick(timer):
    global led
    led.toggle()

tim.init(freq=1, mode=Timer.PERIODIC, callback=tick)

while(True):
    val = val + (40*(1 if dir else -1))
    if val >= 3000:
        dir = False
    elif val < 0:
        dir = True
    
    r=int(val/100)
    color = (3, 4+r, 30-r)
    
    rgbw1 = color
    rgbw2 = (56,20+0.1*r, 8-0.1*r)
    pixels.set_pixel_line_gradient(0, 255, rgbw1, rgbw2) # display parpadea cuando hay que llegar a muchos pixeles, se nota latencia

#     hay que investigar porqué el color (aprox) blanco se consigue con (r,g,b)=(94,60,255) en la matriz 16x16
#     con el r=94, g=60, y bajando el azul de 255 se consigue blanco más cálido, pero al bajar el azul el verde hay que bajarlo un poco tambien
#     pixels.fill((94,50,100))
    
    pixels.show()    