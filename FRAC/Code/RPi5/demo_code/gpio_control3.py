from gpiozero import LED, Button
import argparse
import time

# Define GPIO pin mappings
GPIO_PINS = {
    "alarm": LED(25),
    "strike": LED(26)
}

DOORCONTACT = Button(25)

def check_status():
    """Check the status of all GPIO pins."""
    statuses = {}
    for name, pin in GPIO_PINS.items():
        statuses[name] = "ON" if pin.value else "OFF"
    statuses["doorcontact"] = "CLOSED" if DOORCONTACT.is_pressed else "OPEN"
    
    return statuses

def control_gpio(pin_name, action):
    """Control GPIO pin by name."""
    pin = GPIO_PINS.get(pin_name)
    if pin is None:
        print(f"Invalid pin name: {pin_name}")
        return
    
    if action == "on":
        pin.on()
        print(f"{pin_name} activated and will remain on until deactivated.")
    elif action == "off":
        pin.off()
        print(f"{pin_name} deactivated.")
    else:
        print("Invalid action. Use 'on' or 'off'.")

def check_doorcontact():
    """Check the state of the door contact sensor."""
    state = "closed" if DOORCONTACT.is_pressed else "open"
    print(f"Door contact is {state}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Control Raspberry Pi GPIO outputs and check inputs.")
    parser.add_argument("pin", choices=[*GPIO_PINS.keys(), "doorcontact"], help="Pin to control (alarm, strike) or check (doorcontact)")
    parser.add_argument("action", choices=["on", "off", "check"], help="Turn the pin on, off, or check status (only for 'doorcontact')")
    
    args = parser.parse_args()
     if args.pin == "status":
        print(json.dumps(check_status()))
    elif args.pin == "doorcontact" and args.action == "check":
        check_doorcontact()
    else:
        control_gpio(args.pin, args.action)
