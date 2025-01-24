# collect_data_fixed_pi.py
import asyncio
from bleak import BleakScanner
import csv
import os

# Replace with your target device's MAC address
TARGET_MAC_ADDRESS = "AA:BB:CC:DD:EE:FF"  # <-- Update this
CSV_FILE = "rssi_data_fixed_pi.csv"

def log_data(rssi, source_x, source_y):
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([rssi, source_x, source_y])

async def scan_ble(source_x, source_y):
    devices = await BleakScanner.discover(timeout=5.0)
    for d in devices:
        if d.address.lower() == TARGET_MAC_ADDRESS.lower():
            print(f"Found target device: RSSI={d.rssi} dBm at source position=({source_x}, {source_y})")
            log_data(d.rssi, source_x, source_y)
            return
    print(f"Target device not found at source position=({source_x}, {source_y})")
    log_data(None, source_x, source_y)

def main():
    # Create CSV file with headers if it doesn't exist
    if not os.path.isfile(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["rssi", "source_x", "source_y"])
        print(f"Created {CSV_FILE} with headers.")

    print("Starting data collection. Press Ctrl+C to stop.")
    try:
        while True:
            try:
                source_x = float(input("Enter signal source X position (meters): "))
                source_y = float(input("Enter signal source Y position (meters): "))
                asyncio.run(scan_ble(source_x, source_y))
            except ValueError:
                print("Invalid input. Please enter numerical values for positions.")
    except KeyboardInterrupt:
        print("\nData collection stopped.")

if __name__ == "__main__":
    main()
