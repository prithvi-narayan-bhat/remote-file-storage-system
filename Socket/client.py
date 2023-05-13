##################################################################
# Project:  CSE-5306 Multi-Threaded Server
# Date:     Friday 9 September 2022
# Authors:  Prithvi Bhat (pnb3598@mavs.uta.edu)
##################################################################

import socket
import os

PORT                = 8000                      # Port to bind socket to
DELIMITER           = "<DELIMITER>"             # to decode path and filenames
BUFFER_SIZE         = 5120                      # 5MB buffer size
CLIENT_HOST         = "0.0.0.0"
CLIENT_FILES        = "./client_files/"

def Main():
    socket_instance = socket.socket()                           # Get instance of socket
    socket_instance.connect((CLIENT_HOST, PORT))                # Bind hostname and port number to socket

    print(f"Server[{socket_instance}] connected")               # Provide feedback to user

    operation = input("Select operation (DOWNLOAD | UPLOAD | DELETE | RENAME):---: ")
    file_name = input("Enter file name (DOWNLOAD/UPLOAD/DELETE/RENAME):----------: ")
    file_path = input("Enter file path (UPLOAD source/DOWNLOAD destination):-----: ")
    new_name =  input("Enter new file name (RENAME):-----------------------------: ")
    destination = file_path + "/" + file_name

    if operation == "RENAME":
        if new_name:
            print("Requesting rename of " + file_name + " to " + new_name + " with server")
            socket_instance.send(f"{file_path}{DELIMITER}{file_name}{DELIMITER}{new_name}{DELIMITER}RENAME".encode())        # Send request to server
            print("File renamed")

        socket_instance.close()                                                                             # Close socket connection

    elif operation == "DELETE":
        print("Requesting deletion of file " + file_name + " from server")
        socket_instance.send(f"{file_path}{DELIMITER}{file_name}{DELIMITER}{new_name}{DELIMITER}DELETE".encode())            # Send request to server

        print("File Deleted")
        socket_instance.close()

    elif operation == "UPLOAD":
        print("Requesting upload of " + file_name + " to server")

        while True:
            file_exists = os.path.exists(destination)                                                       # Check if the file exists at given location

            if not file_exists:
                print("ERROR: File does not appear to exist. Closing Connection")

            else:
                socket_instance.send(f"{file_path}{DELIMITER}{file_name}{DELIMITER}{new_name}{DELIMITER}UPLOAD".encode())    # Send request to server
                file = open(destination, 'rb')                                                              # If file actually exists, send it to client
                data = file.read(BUFFER_SIZE)

                while data:
                    socket_instance.sendall(data)                                                           # Send file as stream of binary data
                    data = file.read(BUFFER_SIZE)                                                           # Continue reading next character until NULL is encountered

                    if not data:
                        break
                break

        file.close()                                                                                        # Close file descriptor
        print("File Uploaded. Closing Connection")
        socket_instance.close()

    elif operation == "DOWNLOAD":
        print("Requesting download of " + file_name + " from server")
        socket_instance.send(f"{file_path}{DELIMITER}{file_name}{DELIMITER}{new_name}{DELIMITER}DOWNLOAD".encode())          # Send request to server

        with open(destination, "wb") as file:                                                               # Store the received data into a file at the user specified location

            while True:
                file_data = socket_instance.recv(BUFFER_SIZE)                                               # Accept the data stream sent by the server

                if not file_data:
                    break
                else:
                    file.write(file_data)

            print("File Downloaded. Closing Connection")
            socket_instance.close()                                                                         # Close file descriptor

    else:
        print("ERROR: Invalid operation")

if __name__ == '__main__':
    Main()