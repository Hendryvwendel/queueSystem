import time

def blink_red_led(is_red_blinking, red_led):
    while is_red_blinking:
        red_led.write(1)
        time.sleep(0.5)
        red_led.write(0)
        time.sleep(0.5)

def blink_yellow_led(is_yellow_blinking, yellow_led):
    while is_yellow_blinking:
        yellow_led.write(1)
        time.sleep(0.5)
        yellow_led.write(0)
        time.sleep(0.5)

def blink_green_led(is_green_blinking, green_led):
    while is_green_blinking:
        green_led.write(1)
        time.sleep(0.5)
        green_led.write(0)
        time.sleep(0.5)