import hashlib

# Function to calculate the MD5 hash of a file
def calculate_md5(file_path):
    try:
        with open(file_path, 'rb') as f:
            hash_md5 = hashlib.md5()
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"Error calculating hash for {file_path}: {e}")
        return None

# Test the function with a specific file
if __name__ == "__main__":
    test_file = "Test.txt"  # Replace with the path to your test file
    hash_value = calculate_md5(test_file)
    if hash_value:
        print(f"MD5 hash of '{test_file}': {hash_value}")
    else:
        print("Failed to calculate hash.")