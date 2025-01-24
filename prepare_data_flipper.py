# prepare_data_flipper.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

CSV_FILE = "rssi_flipper_data.csv"
PREPARED_FILE = "prepared_data_flipper.csv"

def load_and_clean_data(csv_file):
    df = pd.read_csv(csv_file)
    
    # Drop rows where RSSI is None or missing
    df = df.dropna(subset=["rssi"])
    
    # Convert RSSI to float
    df["rssi"] = df["rssi"].astype(float)
    
    # Optional: Remove outliers
    # Define RSSI range, e.g., -100 dBm to 0 dBm
    df = df[(df["rssi"] >= -100) & (df["rssi"] <= 0)]
    
    return df

def split_data(df):
    X = df["rssi"].values.reshape(-1, 1).astype(np.float32)
    y = df[["source_x", "source_y"]].values.astype(np.float32)
    
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.30, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.50, random_state=42)
    
    return X_train, X_val, X_test, y_train, y_val, y_test

def save_prepared_data(X_train, X_val, X_test, y_train, y_val, y_test):
    # Save as separate CSVs or combined with a 'set' label
    train_df = pd.DataFrame(X_train, columns=["rssi"])
    train_df[["source_x", "source_y"]] = y_train
    train_df["set"] = "train"
    
    val_df = pd.DataFrame(X_val, columns=["rssi"])
    val_df[["source_x", "source_y"]] = y_val
    val_df["set"] = "val"
    
    test_df = pd.DataFrame(X_test, columns=["rssi"])
    test_df[["source_x", "source_y"]] = y_test
    test_df["set"] = "test"
    
    combined_df = pd.concat([train_df, val_df, test_df], ignore_index=True)
    combined_df.to_csv(PREPARED_FILE, index=False)
    print(f"Prepared data saved to {PREPARED_FILE}")

def main():
    df = load_and_clean_data(CSV_FILE)
    print(f"Loaded data with {len(df)} valid samples.")
    
    X_train, X_val, X_test, y_train, y_val, y_test = split_data(df)
    print(f"Dataset sizes - Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
    
    save_prepared_data(X_train, X_val, X_test, y_train, y_val, y_test)

if __name__ == "__main__":
    main()
