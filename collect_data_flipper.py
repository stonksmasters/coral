# collect_data_flipper.py
import asyncio
from bleak import BleakScanner
import csv
import os
import time

# Flipper Zero's MAC address
FLIPPER_MAC_ADDRESS = "80:E1:27:B5:B6:D0".lower()

CSV_FILE = "rssi_flipper_data.csv"

def log_data(timestamp, rssi, source_x, source_y):
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, rssi, source_x, source_y])

async def scan_flipper():
    devices = await BleakScanner.discover(timeout=3.0)
    for device in devices:
        if device.address.lower() == FLIPPER_MAC_ADDRESS:
            return device.rssi
    return None

def setup_csv():
    if not os.path.isfile(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "rssi", "source_x", "source_y"])
        print(f"Created {CSV_FILE} with headers.")

def main():
    setup_csv()
    print("Starting data collection. Press Ctrl+C to stop.")
    try:
        while True:
            rssi = asyncio.run(scan_flipper())
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            if rssi is not None:
                print(f"Detected Flipper Zero: RSSI={rssi} dBm")
                try:
                    source_x = float(input("Enter signal source X position (meters): "))
                    source_y = float(input("Enter signal source Y position (meters): "))
                    log_data(timestamp, rssi, source_x, source_y)
                    print(f"Logged position ({source_x}, {source_y}) with RSSI={rssi} dBm")
                except ValueError:
                    print("Invalid input. Please enter numerical values for positions.")
            else:
                print(f"[{timestamp}] Flipper Zero not found.")
                log_data(timestamp, None, None, None)
            
            # Wait before the next scan
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nData collection stopped.")

if __name__ == "__main__":
    main()
