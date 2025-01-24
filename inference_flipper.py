# inference_flipper.py
import asyncio
from bleak import BleakScanner
import os
import numpy as np
from pycoral.adapters import common
from pycoral.utils.edgetpu import make_interpreter
import sys
import time

FLIPPER_MAC_ADDRESS = "FF:EE:DD:CC:BB:AA"  # <-- Update with your Flipper Zero's MAC address
MODEL_FILE = "rssi_model_flipper_edgetpu.tflite"

def load_model(model_file):
    interpreter = make_interpreter(model_file)
    interpreter.allocate_tensors()
    return interpreter

async def scan_ble():
    devices = await BleakScanner.discover(timeout=3.0)
    for d in devices:
        if d.address.lower() == FLIPPER_MAC_ADDRESS.lower():
            return d.rssi
    return None

def predict_position(interpreter, rssi):
    if rssi is None:
        return None, None

    # Prepare input data as a numpy array
    input_data = np.array([[rssi]], dtype=np.float32)
    
    # Set input tensor
    common.set_input(interpreter, input_data)
    
    # Run inference
    interpreter.invoke()
    
    # Get output
    output = common.output_tensor(interpreter, 0)
    pred_x, pred_y = output[0]
    return pred_x, pred_y

def main():
    # Check if model file exists
    if not os.path.isfile(MODEL_FILE):
        print(f"Model file {MODEL_FILE} not found. Please convert and compile the model first.")
        sys.exit(1)
    
    # Load the model
    interpreter = load_model(MODEL_FILE)
    print(f"Loaded model {MODEL_FILE} for inference.")

    print("Starting real-time inference. Press Ctrl+C to stop.")
    try:
        while True:
            rssi = asyncio.run(scan_ble())
            if rssi is not None:
                pred_x, pred_y = predict_position(interpreter, rssi)
                if pred_x is not None and pred_y is not None:
                    print(f"RSSI: {rssi} dBm -> Estimated Source Position: ({pred_x:.2f}, {pred_y:.2f}) meters")
                else:
                    print("RSSI detected, but position could not be estimated.")
            else:
                print("Target device not found. RSSI: None")
            
            # Wait a short interval before the next scan
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nInference stopped.")

if __name__ == "__main__":
    main()
