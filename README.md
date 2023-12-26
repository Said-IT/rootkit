# Rootkit

## Prerequisites:

- Install the necessary modules or packages like socket, os, subprocess, etc.
- Launch in order (server first, then client).

## Operation:

This demonstration is intended solely for educational purposes, promoting ethical understanding of how certain functionalities work. It is not meant for malicious intent.

- When the server is launched, it listens, waiting for the client to connect.
- When the client is launched, it connects to the server's port and IP.
- Once the connection is established, you have 4 options:

  - **Shell:** Take control of the victim's terminal and execute commands.
  - **Help:** Understand the commands to use.
  - **File Transfer:** Note that paths must be specified correctly. 
    To perform file transfers, you need to create the file(s) first in /client/client_folder/files/.
    Transferred files will be in /server/server_folder/files.

    - The transfer of a file is carried out in three steps. 
      The first is to send the file name, the second is to send the data, 
      and the last is to end the transfer. 
      Before these steps, the consideration of a directory path is put in place 
      to avoid sending loaded and unrelated files. 
      You can customize it, for example, send all files from the current directory.

    - The reception takes place reciprocally. 
      Before reception, a directory is created to place 
      the files transmitted by the client.

  - **Exit:** To exit the program and terminate the connection.

## Issues Encountered:

To avoid encountered issues, please note:

- Lack of precision in the path.
- Create the file you want to transfer in a different directory 
  than the one mentioned, provided that you adapt it to your needs.
- Use of an identical and specific port.


