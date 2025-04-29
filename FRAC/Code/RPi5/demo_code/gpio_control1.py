from gpiozero import LED
import argparse
import time

# Define GPIO pin mappings
GPIO_PINS = {
    "alarm": LED(24),
    "doorcontact": LED(25),
    "strike": LED(26)
}

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Control Raspberry Pi GPIO outputs.")
    parser.add_argument("pin", choices=GPIO_PINS.keys(), help="Pin to control (alarm, doorcontact, strike)")
    parser.add_argument("action", choices=["on", "off"], help="Turn the pin on or off")
    parser.add_argument("--duration", type=int, help="Optional: Duration in seconds before turning off (only for 'on' action)")
    
    args = parser.parse_args()
    control_gpio(args.pin, args.action, args.duration)
