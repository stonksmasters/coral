# convert_to_tflite_flipper.py
import tensorflow as tf

MODEL_FILE = "rssi_model_flipper.h5"
TFLITE_FILE = "rssi_model_flipper.tflite"

def main():
    # Load the Keras model
    model = tf.keras.models.load_model(MODEL_FILE)
    model.summary()
    
    # Convert to TensorFlow Lite
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    
    # Optimize the model for size and latency
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    
    # Set the supported types to float16 for better compatibility with Edge TPU
    converter.target_spec.supported_types = [tf.float16]
    
    tflite_model = converter.convert()
    
    # Save the TFLite model
    with open(TFLITE_FILE, "wb") as f:
        f.write(tflite_model)
    
    print(f"TensorFlow Lite model saved as {TFLITE_FILE}")

if __name__ == "__main__":
    main()
