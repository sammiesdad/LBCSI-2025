from gpiozero import LED, Button

# Define GPIO pin mappings
GPIO_PINS = {
    "alarm": LED(25),
    "strike": LED(26)
}

DOORCONTACT = Button(24)

def check_status():
    """Check the status of all GPIO pins."""
    statuses = {}
    for name, pin in GPIO_PINS.items():
        statuses[name] = "ON" if pin.value else "OFF"
    statuses["doorcontact"] = "CLOSED" if DOORCONTACT.is_pressed else "OPEN"
    
    return statuses

if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Control Raspberry Pi GPIO outputs and check inputs.")
    parser.add_argument("pin", choices=[*GPIO_PINS.keys(), "doorcontact", "status"], help="Pin to control or check status")
    parser.add_argument("action", choices=["on", "off", "check"], help="Turn on, off, or check status")

    args = parser.parse_args()

    if args.pin == "status":
        print(json.dumps(check_status()))
    elif args.pin == "doorcontact" and args.action == "check":
        print(f"Door contact is {'CLOSED' if DOORCONTACT.is_pressed else 'OPEN'}")
    else:
        pin = GPIO_PINS.get(args.pin)
        if pin:
            if args.action == "on":
                pin.on()
                print(f"{args.pin} activated.")
            elif args.action == "off":
                pin.off()
                print(f"{args.pin} deactivated.")
