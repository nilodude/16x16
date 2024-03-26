from machine import Pin, Timer
from neopixel import Neopixel

led = Pin("LED", Pin.OUT)
tim = Timer()
gradient = Timer()

pixels = Neopixel(16*16, 0, 2, "GRB") 

val = 0

def tick(timer):
    global led
    led.toggle()

def grad(gradient):
    global val
    val = val + 50
    
    val = 0 if val > 4000 else val
    val = 4000 if val < 0  else val
    print(val)

tim.init(freq=1, mode=Timer.PERIODIC, callback=tick)
gradient.init(freq=10, mode=Timer.PERIODIC, callback=grad)

while(True):
    
    r=int(val/100)
    color = (3, 4+r, 30-r)
    
    rgbw1 = color
    rgbw2 = (56,20+0.1*r, 8-0.1*r)
    pixels.set_pixel_line_gradient(0, 255, rgbw1, rgbw2) # display parpadea cuando hay que llegar a muchos pixeles, se nota latencia

#     hay que investigar porqué el color (aprox) blanco se consigue con (r,g,b)=(94,60,255) en la matriz 16x16
#     con el r=94, g=60, y bajando el azul de 255 se consigue blanco más cálido, pero al bajar el azul el verde hay que bajarlo un poco tambien
#     pixels.fill((94,50,100))
    
    pixels.show()    