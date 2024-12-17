import os
import hashlib
import time

# Directory to monitor
monitor_dir = 'admin'

# Path to store the baseline hash file
baseline_file = 'file_integrity_baseline.txt'

# Function to calculate the MD5 hash of a file
def calculate_md5(file_path):
    try:
        hash_md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"Error calculating hash for {file_path}: {e}")
        return None

# Function to create a baseline of file hashes
def create_baseline():
    baseline = {}
    for root, dirs, files in os.walk(monitor_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_md5(file_path)
            if file_hash:
                baseline[file_path] = file_hash
    with open(baseline_file, 'w') as f:
        for file_path, file_hash in baseline.items():
            f.write(f"{file_path},{file_hash}\n")
    print("Baseline created.")

# Function to load the baseline from file
def load_baseline():
    baseline = {}
    if not os.path.exists(baseline_file):
        print("Baseline file not found. Creating new baseline.")
        create_baseline()
    else:
        with open(baseline_file, 'r') as f:
            for line in f:
                file_path, file_hash = line.strip().split(',')
                baseline[file_path] = file_hash
    return baseline

# Function to update the baseline
def update_baseline(current_files):
    with open(baseline_file, 'w') as f:
        for file_path, file_hash in current_files.items():
            f.write(f"{file_path},{file_hash}\n")
    print("Baseline updated.")

# Function to check for changes in the monitored directory
def check_integrity(baseline):
    current_files = {}
    for root, dirs, files in os.walk(monitor_dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = calculate_md5(file_path)
            if file_hash:
                current_files[file_path] = file_hash
    print(current_files)
    # Compare current state with baseline
    for file_path, file_hash in current_files.items():
        if file_path not in baseline:
            print(f"New file detected: {file_path}")
            update_baseline(current_files)
        elif baseline[file_path] != file_hash:
            print(f"File modified: {file_path}")

    for file_path in baseline.keys():
        if file_path not in current_files:
            print(f"File deleted: {file_path}")

    

# Monitor directory for changes
if __name__ == "__main__":
    while True:
        baseline = load_baseline()
        print("Checking file integrity...")
        check_integrity(baseline)
        print("Monitoring...")
        time.sleep(60)  # Check every 60 seconds