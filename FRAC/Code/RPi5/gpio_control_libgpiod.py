#!/usr/bin/env python3
import gpiod
import json

# Specify the GPIO pins to monitor (using Broadcom numbering)
pins = [24, 25, 26]

# Open the GPIO chip (typically 'gpiochip0' on Raspberry Pi)
chip = gpiod.Chip('gpiochip0')

# Request the specified lines as inputs
lines = chip.get_lines(pins)
lines.request(consumer="gpio_read", type=gpiod.LINE_REQ_DIR_IN)

# Read the values and build a JSON-ready dictionary
values = lines.get_values()
gpio_data = {}
for pin, value in zip(pins, values):
    gpio_data[f"GPIO {pin}"] = value

print(json.dumps(gpio_data))
