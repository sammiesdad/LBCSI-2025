from gpiozero import LED, Button
import argparse
import time

# Define GPIO pin mappings
GPIO_PINS = {
    "alarm": LED(24, initial_value=False),
    "strike": LED(26, initial_value=False)
}

DOORCONTACT = Button(25, pull_up=True)

def control_gpio(pin_name, action, duration=None):
    """Control GPIO pin by name."""
    pin = GPIO_PINS.get(pin_name)
    if pin is None:
        print(f"Invalid pin name: {pin_name}")
        return
    
    if action == "on":
        pin.on()
        print(f"{pin_name} activated.")
        if duration:
            time.sleep(duration)
            pin.off()
            print(f"{pin_name} deactivated after {duration} seconds.")
    elif action == "off":
        pin.off()
        print(f"{pin_name} deactivated.")
    else:
        print("Invalid action. Use 'on' or 'off'.")

def check_doorcontact():
    """Check the state of the door contact sensor."""
    state = "closed" if DOORCONTACT.is_pressed else "open"
    print(f"Door contact is {state}.")

def check_status():
    """Display the status of all GPIO pins passively without activating outputs."""
    statuses = {}
    for name, pin in GPIO_PINS.items():
        statuses[name] = "ON" if pin.value else "OFF"
    statuses["doorcontact"] = "CLOSED" if DOORCONTACT.is_pressed else "OPEN"
    
    for name, status in statuses.items():
        print(f"{name}: {status}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Control Raspberry Pi GPIO outputs and check inputs.")
    parser.add_argument("pin", choices=[*GPIO_PINS.keys(), "doorcontact", "status"], help="Pin to control (alarm, strike) or check (doorcontact, status)")
    parser.add_argument("action", choices=["on", "off", "check"], help="Turn the pin on, off, or check status (only for 'doorcontact' or 'status')")
    parser.add_argument("--duration", type=int, help="Optional: Duration in seconds before turning off (only for 'on' action)")
    
    args = parser.parse_args()
    
    if args.pin == "doorcontact" and args.action == "check":
        check_doorcontact()
    elif args.pin == "status" and args.action == "check":
        check_status()
    else:
        control_gpio(args.pin, args.action, args.duration)
