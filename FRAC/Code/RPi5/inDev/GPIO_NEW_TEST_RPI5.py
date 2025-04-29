#!/usr/bin/env python3

import gpiod
import time

# Define GPIO pins (adjust according to your wiring)
PIN_INPUTS = {
    "doorswitch": 17,
    "duress": 27,
    "PIR": 22
}

PIN_OUTPUTS = {
    "doorstrike": 23,
    "siren": 24,
    "spare": 25
}

# Setup GPIO chip
chip = gpiod.Chip('gpiochip4')

# Setup inputs
input_lines = {}
for name, pin in PIN_INPUTS.items():
    line = chip.get_line(pin)
    line.request(consumer=name, type=gpiod.LINE_REQ_DIR_IN)
    input_lines[name] = line

# Setup outputs
output_lines = {}
for name, pin in PIN_OUTPUTS.items():
    line = chip.get_line(pin)
    line.request(consumer=name, type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
    output_lines[name] = line

# Helper functions
def activate_output(name, duration=5):
    print(f"Activating {name}")
    output_lines[name].set_value(1)
    time.sleep(duration)
    output_lines[name].set_value(0)
    print(f"Deactivated {name}")

# Main loop
try:
    print("Monitoring sensors...")
    while True:
        if input_lines["doorswitch"].get_value() == 0:  # assuming active low
            print("Door opened! Activating doorstrike.")
            activate_output("doorstrike", duration=3)

        if input_lines["duress"].get_value() == 0:  # assuming active low
            print("Duress signal received! Activating siren.")
            activate_output("siren", duration=10)

        if input_lines["PIR"].get_value() == 1:  # assuming active high
            print("Motion detected! Activating spare output.")
            activate_output("spare", duration=2)

        time.sleep(0.5)

except KeyboardInterrupt:
    print("Shutting down GPIO control...")
finally:
    for line in input_lines.values():
        line.release()
    for line in output_lines.values():
        line.set_value(0)
        line.release()
    chip.close()
    print("GPIO cleanup complete.")
