import time
import rp2
import random  
import usb.device
from usb.device.mouse import MouseInterface
from machine import Pin

# 1. Setup the onboard LED
try:
    led = Pin("LED", Pin.OUT)
except TypeError:
    led = Pin(25, Pin.OUT)

print("Starting in 5 seconds... Press STOP in Thonny to cancel.")
time.sleep(5)

# 2. Initialize the mouse interface
mouse = MouseInterface()
usb.device.get().init(mouse, builtin_driver=True)

while not mouse.is_open():
    time.sleep_ms(100)
    
print("Mouse connected! Doing a startup twitch...")
mouse.move_by(50, 0)
time.sleep_ms(300)
mouse.move_by(-50, 0)

# 3. Jiggler configuration
jiggler_active = True
jiggle_interval_ms = 5000  # Set to 5 seconds!
last_jiggle_time = time.ticks_ms()

led.value(1)
print("Jiggler running! Press BOOTSEL to toggle.")

# 4. Main loop
try:
    while True:
        # --- BUTTON CHECK ---
        if rp2.bootsel_button() == 1:
            jiggler_active = not jiggler_active
            led.value(1 if jiggler_active else 0)
            last_jiggle_time = time.ticks_ms()
            
            while rp2.bootsel_button() == 1:
                time.sleep_ms(50)
            time.sleep_ms(100)

        # --- RANDOM JIGGLE CHECK ---
        if jiggler_active:
            current_time = time.ticks_ms()
            
            if time.ticks_diff(current_time, last_jiggle_time) >= jiggle_interval_ms:
                
                x_move = random.randint(-50, 50)
                y_move = random.randint(-50, 50)
                pause = random.randint(200, 800)
                
                led.value(0)
                
                mouse.move_by(x_move, y_move) 
                time.sleep_ms(pause) 
                mouse.move_by(-x_move, -y_move)
                
                led.value(1)
                
                last_jiggle_time = time.ticks_ms()
                
        time.sleep_ms(20)
        
except KeyboardInterrupt:
    print("Jiggler stopped by user.")
