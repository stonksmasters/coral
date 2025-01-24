# pi_broadcast.py
import asyncio
from bleak import BleakServer

# Define the BLE advertisement parameters
DEVICE_NAME = "RaspberryPi_Beacon"

async def run():
    server = BleakServer()
    await server.start_advertising(name=DEVICE_NAME)
    print(f"BLE beacon '{DEVICE_NAME}' is now advertising.")
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        await server.stop_advertising()
        print("BLE advertising stopped.")

if __name__ == "__main__":
    asyncio.run(run())
