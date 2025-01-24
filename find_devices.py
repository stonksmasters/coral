import asyncio
from bleak import BleakScanner

async def find_devices():
    devices = await BleakScanner.discover(timeout=5.0)
    for d in devices:
        print(f"Device: {d.name}, MAC: {d.address}, RSSI: {d.rssi} dBm")

asyncio.run(find_devices())
