##################################################################
# Project:  CSE-5306 Multi-Threaded Server
# Date:     Friday 9 September 2022
# Authors:  Prithvi Bhat (pnb3598@mavs.uta.edu)
##################################################################

import threading
import socket
import os

PORT                = 8000                      # Port to bind socket to
DELIMITER           = "<DELIMITER>"             # to decode path and filenames
BUFFER_SIZE         = 5120                      # 5MB buffer size
SERVER_HOST         = "0.0.0.0"                 # Server Host address
SERVER_FILES        = "./server_files/"         # Location of files on server

def download(client_instance, file_name):
    file_path = os.path.join(SERVER_FILES, file_name)
    while True:
        file_exists = os.path.exists(file_path)                                 # Check if the file exists at given location

        if not file_exists:
            print("ERROR: File does not appear to exist")
            break

        else:
            file = open(file_path, 'rb')                                        # If file actually exists, send it to client
            data = file.read(BUFFER_SIZE)

            while data:
                client_instance.sendall(data)                                   # Send file as stream of binary data
                data = file.read(BUFFER_SIZE)                                   # Continue reading next character until NULL is encountered
                if not data:
                    break
            file.close()                                                        # Close file descriptor
            break


    print("Closing Connection")
    client_instance.close()                                                     # Close connection at the end of transaction

def upload(client_instance, file_name):
    destination = os.path.join(SERVER_FILES, file_name)                         # Set the destination for upload operation
    # No need to check if file with same name exists already at the location since one will be uploaded / created anyway
    # Server will store all its files at a default location and will not accept any user input in this regard
    file = open(destination, "wb")                                              # Open an existing file the same name or create a new one

    while True:
        file_data = client_instance.recv(BUFFER_SIZE)

        if not file_data:
            break
        else:
            file.write(file_data)                                               # Store the received data into a file at the default location

    print("File Uploaded")
    client_instance.close()                                                     # Close socket connection and file descriptor
    file.close()

def rename(client_instance, file_name, new_name):
    original = os.path.join(SERVER_FILES, file_name)
    renamed = os.path.join(SERVER_FILES, new_name)

    while True:
        file_exists = os.path.exists(original)                                  # Check if the original file exists at given location

        if not file_exists:
            print("ERROR: File does not appear to exist on server")
            break
        else:
            os.rename(original, renamed)
            break
    client_instance.close()

def delete(client_instance, file_name):
    file_path = os.path.join(SERVER_FILES, file_name)

    while True:
        file_exists = os.path.exists(file_path)

        if file_exists:                                                         # Verify if file exists
            os.remove(file_path)                                                # Delete
            print("File Deleted")

        else:
            print("ERROR: File does not appear to exist on server")
            break

    client_instance.close()


def Main():
    socket_instance = socket.socket()                                           # Get instance of socket
    socket_instance.bind((SERVER_HOST, PORT))                                   # Bind hostname and PORT number to socket

    print(f"Listening for connection request on PORT {PORT}")

    socket_instance.listen(5)                                                   # Number of requests that can be made

    while True:
        client_instance, address = socket_instance.accept()                     # Accept an incoming Client request
        print(f"Client[{client_instance}] connected")                           # Provide feedback to user

        received = client_instance.recv(BUFFER_SIZE).decode()                   # Receive file from client

        if not received:                                                        # No data received
            break

        else:
            print("Received String: " + str(received))
            file_path, file_name, new_name, operation = received.split(DELIMITER)         # Extract the file name, path and operation
            print("Operation: " + str(operation))
            print("File_path: " + str(file_path))
            print("File_name: " + str(file_name))
            print("New_name: " + str(new_name))

            if operation == "DOWNLOAD":
                download_thread = threading.Thread(target = download, args = (client_instance, file_name, ))            # Create new thread for download operation
                download_thread.start()                                                                                 # Spawn new thread

            elif operation == "UPLOAD":
                upload_thread = threading.Thread(target = upload, args = (client_instance, file_name, ))                # Create new thread for upload operation
                upload_thread.start()                                                                                   # Spawn new thread

            elif operation == "RENAME":
                rename_thread = threading.Thread(target = rename, args = (client_instance, file_name, new_name))        # Create new thread for rename operation
                rename_thread.start()                                                                                   # Spawn new thread

            elif operation == "DELETE":
                delete_thread = threading.Thread(target = delete, args = (client_instance, file_name))                  # Create new thread for delete operation
                delete_thread.start()                                                                                   # Spawn new thread

if __name__ == '__main__':
    Main()