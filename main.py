import network
import time

print("Connecting to WiFi", end="")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("SSID", "password")
while not wlan.isconnected():
    print(".", end="")
    time.sleep(0.1)
print(" Connected!")

from machine import Pin

button = Pin(3, Pin.IN, Pin.PULL_UP)

from bell import Bell
from bell import Note
from messenger import Messenger
# from keypad import Keypad
# from display import Display

row_pins = [23, 0, 4, 19]
col_pins = [18, 5, 17, 16]

# Send messages to doorbell owner
# keypad = Keypad(row_pins, col_pins)
# display = Display()

# motion_sensor = Pin(15, Pin.IN)

ringer = Bell(15)

# Whatever SMTP email you want to use, I recommend Gmail (Hotmail was blocked by Verizon for some reason)
email = "email@gmail.com"
# The password to the email, if this is a Gmail, you need to generate an App Password (https://support.google.com/accounts/answer/185833?hl=en)
password = ""
# Replace this with your email or phone number email (https://www.makeuseof.com/tag/email-to-sms/)
recipients = ["1234567890@vtext.com"]
communicator = Messenger(email, password, recipients)


def ring_bell():
    ringer.play()
    communicator.send_message("The doorbell was rung.")


previous_value = 1
button_gap_time = 3
motion_gap_time = 60
last_button_press = int(time.time()) - button_gap_time
last_motion_sense = int(time.time()) - motion_gap_time
display_text = []

while True:
    # Rings the doorbell when pressed, if enough time has elapsed
    if not button.value() and last_button_press < int(time.time()) - button_gap_time:
        last_button_press = int(time.time())
        ring_bell()
    # key, change = keypad.get_key()
    # # Type using the keypad; it works similar to a phone dialing thing; more in keypad.py
    # if key:
    #     if key == "#":
    #         display.draw_text("")
    #         communicator.send_message("".join(display_text))
    #         display_text = []
    #     elif key == "\b":
    #         if len(display_text) > 0:
    #             display_text.pop()
    #     elif change:
    #         display_text[-1] = key
    #     else:
    #         display_text.append(key)
    #     display.draw_text("".join(display_text))
    # # Send a message to the owner if motion is detected but don't spam them if its too close together
    # if motion_sensor.value() and last_motion_sense < int(time.time()) - motion_gap_time:
    #     communicator.send_message("Motion Detected")
