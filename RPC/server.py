##################################################################
# Project:  CSE-5306 Multi-Threaded Server
# Date:     Monday 10 September 2022
# Authors:  Prithvi Bhat (pnb3598@mavs.uta.edu)
##################################################################

import os
import threading
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client

PORT                = 8000                      # Port to bind socket to
SERVER_HOST         = "0.0.0.0"                 # Server Host address
SERVER_FILES        = "./synced_dir_server/"    # Location of files on server

"""
    Constructor to override default limitation of threading.Thread of not returning file values
    Inherits all properties from threading.Thread
"""
class custom_thread(threading.Thread):
    def __init__(self, *argv, **keyword_argv):
        super().__init__(*argv, **keyword_argv)
        self.file_data = None

    def run(self):                                                                                  # Override the run method
        if self._target is None:
            print("ERROR: Something went wrong")
            return
        try:
            self.file_data = self._target(*self._args, **self._kwargs)
        except Exception as exc:
            print(f'{type(exc).__name__}: {exc}', file=sys.stderr)                                  # properly handle the exception

    def join(self, *argv, **keyword_argv):                                                          # Override join method
        super().join(*argv, **keyword_argv)
        return self.file_data

def _file_upload(file_name, file_data):                                                             # Method to handle file upload to server
    destination = os.path.join(SERVER_FILES, file_name)                                             # Set the upload destination

    with open(destination, "wb") as file:                                                           # Create a new file with the same name as received from client
        file.write(file_data.data)                                                                  # Write data into it

    print("File [" + str(file_name) + "] uploaded successfully")

def _file_download(file_name):
    if not os.path.exists(os.path.join(SERVER_FILES, file_name)):
        print("ERROR: File does not exist")
    else:
        print("File found. Initiating download")
        with open(os.path.join(SERVER_FILES, file_name), "rb") as file:
            data = xmlrpc.client.Binary(file.read())
            print("File [" + str(file_name) + "] loaded to buffer")
            return data
    return True

def _file_delete(file_name):
    if not os.path.exists(os.path.join(SERVER_FILES, file_name)):
        print("ERROR: File does not exist")
    else:
        os.remove(os.path.join(SERVER_FILES, file_name))
        print("File [" + str(file_name) + "] deleted")

def _file_rename(file_name, new_name):                                                              # Method to handle file renaming on server
    old_path = os.path.join(SERVER_FILES, file_name)                                                # Variable to store old file name
    new_path = os.path.join(SERVER_FILES, new_name)                                                 # Variable to store new file name
    if not os.path.exists(old_path):                                                                # Validate the existence of file before renaming
        print("ERROR: Requested file does not exist")
    else:
        os.rename(old_path, new_path)                                                               # Rename if file exists
        print("File [" + str(file_name) + "] renamed to [" + str(new_name) + "]")

def file_upload(file_name, file_data):
    upload_thread = threading.Thread(target = _file_upload, args = (file_name, file_data, ))        # Create new thread for upload operation
    upload_thread.start()                                                                           # Spawn a new thread
    return True

def file_download(file_name):                                                                       # Method to handle file download
    download_thread = custom_thread(target = _file_download, args = (file_name,))               # Create a new thread (custom) to return a value on 
    download_thread.start()
    data = download_thread.join(timeout=200)
    if not download_thread.is_alive():
        return data


def file_delete(file_name):
    delete_thread = threading.Thread(target = _file_delete, args = (file_name, ))
    delete_thread.start()
    return True

def file_rename(file_name, new_name):
    rename_thread = threading.Thread(target = _file_rename, args = (file_name, new_name,))          # Create new thread for rename operation
    rename_thread.start()                                                                           # Spawn a new thread
    return True

def Main():
    server = SimpleXMLRPCServer((SERVER_HOST, PORT))
    print("Server online\nListening on port [" + str(PORT) + "]")
    server.register_function(file_upload, 'file_upload')
    server.register_function(file_download, 'file_download')
    server.register_function(file_delete, 'file_delete')
    server.register_function(file_rename, 'file_rename')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Killing Server")

if __name__ == '__main__':
    Main()