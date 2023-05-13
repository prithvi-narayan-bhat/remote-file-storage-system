# remote-file-storage
Application to Download, Upload, Rename and Delete files between a client and remote server

## Authors
Prithvi Bhat

### System Requirements
* Linux OS (tested on Mint 21, but any major distro should work)
* Python 3.10

### Organisation
This project has been implemented using
1. Socket
2. RPC
Each implementation is sperately included in the project with the appropriate name

#### Usage
1. Run server.py and client.py simulatneously in the order 
2. Enter operation to be performed when prompted (Case sensitive) (DOWNLOAD, UPLOAD, RENAME, DELETE)
    * Enter name of file to handle (client or server side)
    * Enter path where to download into
    * Enter new name of file if prompted (RENAME operation only)

