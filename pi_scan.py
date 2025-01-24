# pi_scan.py
import asyncio
from bleak import BleakScanner
import csv
import os
import time

# Define the target BLE device names or MAC addresses
TARGET_DEVICES = {
    "RaspberryPi_Beacon": "YOUR_PI_MAC_ADDRESS",  # Optional: Replace with Pi's MAC if needed
    "FlipperZero_Beacon": "FF:EE:DD:CC:BB:AA"    # <-- Update with your Flipper Zero's MAC address
}

CSV_FILE = "rssi_dual_device_data.csv"

def log_data(timestamp, scanner_device, target_device, rssi):
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, scanner_device, target_device, rssi])

async def scan():
    devices = await BleakScanner.discover(timeout=5.0)
    timestamp = time.time()
    for device in devices:
        for target_name, target_mac in TARGET_DEVICES.items():
            if device.address.lower() == target_mac.lower() or device.name == target_name:
                print(f"[{timestamp}] Detected {target_name} ({device.address}) with RSSI {device.rssi} dBm")
                log_data(timestamp, "Pi", target_name, device.rssi)

def setup_csv():
    if not os.path.isfile(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "scanner", "target_device", "rssi"])
        print(f"Created {CSV_FILE} with headers.")

def main():
    setup_csv()
    print("Starting BLE scanning. Press Ctrl+C to stop.")
    try:
        while True:
            asyncio.run(scan())
            # Wait before the next scan
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nBLE scanning stopped.")

if __name__ == "__main__":
    main()
