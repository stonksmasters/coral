# pi_broadcast.py
import subprocess
import time

def start_ble_advertising():
    # Start bluetoothctl and send commands
    proc = subprocess.Popen(['bluetoothctl'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    commands = [
        'power on\n',
        'agent on\n',
        'default-agent\n',
        'advertise on\n',
        'discoverable on\n',
        'exit\n'
    ]
    for cmd in commands:
        proc.stdin.write(cmd)
        proc.stdin.flush()
        time.sleep(0.5)  # Wait for the command to take effect

if __name__ == "__main__":
    start_ble_advertising()
    print("BLE advertising started.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("BLE advertising stopped.")
