# pi_scan_flipper_only.py
import asyncio
from bleak import BleakScanner
import csv
import os
import time

# Define the Flipper Zero's BLE MAC address
FLIPPER_MAC_ADDRESS = "FF:EE:DD:CC:BB:AA"  # <-- Update with your Flipper Zero's MAC address

CSV_FILE = "rssi_flipper_data.csv"

def log_data(timestamp, scanner_device, target_device, rssi):
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, scanner_device, target_device, rssi])

async def scan():
    devices = await BleakScanner.discover(timeout=5.0)
    timestamp = time.time()
    for device in devices:
        if device.address.lower() == FLIPPER_MAC_ADDRESS.lower():
            print(f"[{timestamp}] Detected Flipper Zero ({device.address}) with RSSI {device.rssi} dBm")
            log_data(timestamp, "Pi", "FlipperZero", device.rssi)

def setup_csv():
    if not os.path.isfile(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "scanner", "target_device", "rssi"])
        print(f"Created {CSV_FILE} with headers.")

def main():
    setup_csv()
    print("Starting BLE scanning for Flipper Zero. Press Ctrl+C to stop.")
    try:
        while True:
            asyncio.run(scan())
            # Wait before the next scan
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nBLE scanning stopped.")

if __name__ == "__main__":
    main()
