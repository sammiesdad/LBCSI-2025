#!/usr/bin/env python3

import gpiod
import time
import json

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

chip = gpiod.Chip('gpiochip4')

input_lines = {}
for name, pin in PIN_INPUTS.items():
    line = chip.get_line(pin)
    line.request(consumer=name, type=gpiod.LINE_REQ_DIR_IN)
    input_lines[name] = line

output_lines = {}
for name, pin in PIN_OUTPUTS.items():
    line = chip.get_line(pin)
    line.request(consumer=name, type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
    output_lines[name] = line

status_file = '/var/www/html/sensor_status.json'

try:
    print("Monitoring sensors...")
    while True:
        sensor_status = {name: line.get_value() for name, line in input_lines.items()}
        
        with open(status_file, 'w') as file:
            json.dump(sensor_status, file)
        
        time.sleep(1)

except KeyboardInterrupt:
    print("Terminating...")

finally:
    for line in input_lines.values():
        line.release()
    for line in output_lines.values():
        line.set_value(0)
        line.release()
    chip.close()
