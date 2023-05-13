##################################################################
# Project:  CSE-5306 Multi-Threaded Server
# Date:     Monday 10 September 2022
# Authors:  Prithvi Bhat (pnb3598@mavs.uta.edu)
##################################################################

import os
import threading
import xmlrpc.client
import sys

PORT                = 8000                      # Port to bind socket to
SERVER_HOST         = "0.0.0.0"                 # Server Host address
CLIENT_FILES        = "./synced_dir_client/"    # Location of files on client

def Main():
    server_endpoint = 'http://{}:{}'.format(SERVER_HOST, PORT)      # Set an endpoint for the client to communicate to

    server_proxy = xmlrpc.client.ServerProxy(server_endpoint)

    operation = input("Select operation (DOWNLOAD | UPLOAD | DELETE | RENAME):---: ")
    # if not operation == 'DOWNLOAD' or not operation == 'UPLOAD' or not operation == 'RENAME' or not operation == 'DELETE':
        # print("ERROR: Invalid operation requested")
        # sys.exit()

    if operation == "UPLOAD":
        file_name = input("Enter name of file to upload:-----------------------------: ")
        if not os.path.exists(os.path.join(CLIENT_FILES, file_name)):
            print("ERROR: File does not exist")
            sys.exit(1)
        else:
            print("Validated file. Uploading to server..")

        with open (os.path.join(CLIENT_FILES, file_name), "rb") as file:
            file_data = xmlrpc.client.Binary(file.read())
            server_proxy.file_upload(file_name, file_data)
            print("Request completed")

    elif operation == "DOWNLOAD":
        file_name = input("Enter name of file to download:---------------------------: ")
        print("Requesting to file download")
        with open(os.path.join(CLIENT_FILES, file_name), "wb") as file:
            try:
                file.write(server_proxy.file_download(file_name).data)
            except:
                print("File Downloaded")

    elif operation == "DELETE":
        file_name = input("Enter name of file to delete:-----------------------------: ")
        print("Requesting to file deletion")
        server_proxy.file_delete(file_name)
        print("Request completed")

    elif operation == "RENAME":
        file_name = input("Enter name of file to rename:-----------------------------: ")
        new_name  = input("Enter new file name:--------------------------------------: ")
        print("Requesting file name change")
        server_proxy.file_rename(file_name, new_name)
        print("Request completed")

    else:
        print("ERROR: Invalid operation. Terminating")

if __name__ == '__main__':
    Main()