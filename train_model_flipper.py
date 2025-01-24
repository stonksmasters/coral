# train_model_flipper.py
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import os

PREPARED_FILE = "prepared_data_flipper.csv"
MODEL_FILE = "rssi_model_flipper.h5"
PLOTS_DIR = "plots_flipper"

def load_prepared_data(prepared_file):
    df = pd.read_csv(prepared_file)
    return df

def prepare_datasets(df):
    train_df = df[df["set"] == "train"]
    val_df = df[df["set"] == "val"]
    test_df = df[df["set"] == "test"]
    
    X_train = train_df["rssi"].values.reshape(-1, 1).astype(np.float32)
    y_train = train_df[["source_x", "source_y"]].values.astype(np.float32)
    
    X_val = val_df["rssi"].values.reshape(-1, 1).astype(np.float32)
    y_val = val_df[["source_x", "source_y"]].values.astype(np.float32)
    
    X_test = test_df["rssi"].values.reshape(-1, 1).astype(np.float32)
    y_test = test_df[["source_x", "source_y"]].values.astype(np.float32)
    
    return X_train, X_val, X_test, y_train, y_val, y_test

def build_model(input_shape=(1,)):
    model = keras.Sequential([
        layers.Input(shape=input_shape),
        layers.Dense(64, activation='relu'),
        layers.Dense(64, activation='relu'),
        layers.Dense(2)  # Output: source_x, source_y
    ])
    
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    model.summary()
    return model

def plot_history(history, plots_dir):
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)
    
    # Plot loss
    plt.figure(figsize=(10, 5))
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Val Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('MSE Loss')
    plt.legend()
    plt.savefig(f"{plots_dir}/loss.png")
    plt.close()
    
    # Plot MAE
    plt.figure(figsize=(10, 5))
    plt.plot(history.history['mae'], label='Train MAE')
    plt.plot(history.history['val_mae'], label='Val MAE')
    plt.title('Model MAE')
    plt.xlabel('Epoch')
    plt.ylabel('Mean Absolute Error (meters)')
    plt.legend()
    plt.savefig(f"{plots_dir}/mae.png")
    plt.close()
    print(f"Training plots saved in {plots_dir}/")

def main():
    df = load_prepared_data(PREPARED_FILE)
    print(f"Loaded prepared data with {len(df)} samples.")
    
    X_train, X_val, X_test, y_train, y_val, y_test = prepare_datasets(df)
    print(f"Dataset sizes - Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
    
    model = build_model()
    
    # Train the model
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=200,
        batch_size=16,
        callbacks=[
            keras.callbacks.EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True)
        ]
    )
    
    # Plot training history
    plot_history(history, PLOTS_DIR)
    
    # Evaluate on test set
    test_loss, test_mae = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test MSE: {test_loss:.4f}, Test MAE: {test_mae:.4f} meters")
    
    # Save the trained model
    model.save(MODEL_FILE)
    print(f"Trained model saved as {MODEL_FILE}")

if __name__ == "__main__":
    main()
