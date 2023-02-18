
import threading
from client_handling import *
#from gpiozero import LED
import json
#from drive_deployement import Deployement
from userGUI import *
import sys
from PyQt5.QtWidgets import QDialog, QApplication



class MyForm(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.ps2.clicked.connect(self.dispmessage)
        self.ui.ps1.clicked.connect(self.dispmessage)
        self.show()

    def dispmessage(self):
        print('button clicked')


def usergui():
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())

clientThread1 = threading.Thread(target = usergui )
clientThread1.start()

'''
electroValve = LED("GPIO18") # GPIO17 for the electroValve
extractor_temp = LED("GPIO23") # GPIO16 for the air extractor 1
extractor_hum = LED("GPIO24") # GPIO15 for the air extractor 2
'''
electroValve = 1
extractor_temp = 2
extractor_hum = 3
actuators = { "elect_valve" : electroValve , "extr_temp" : extractor_temp , "extr_hum" : extractor_hum }

HOST = '0.0.0.0'
PORT = 65000

print(CRED+"---------------------------------------------"+CEND)
print(CGREEN+"SAREV1.0 , The Art of Modern Agriculture"+CEND)
print(CYELLOW+"Created by medabkasm"+CEND)
print("github : https://github.com/medabkasm")
print("email : medabkasm@gmail.com")
print(CRED+"---------------------------------------------"+CEND)

# actuators_statuses.json : json file with the last status of all actuators , used in every start on of the broker ,
# it is also an emergency file after power loss.
print("trying to access actuators_statuses.json file...")
try:
    with open("./config_files/actuators_statuses.json","r") as actStates:
        statuses = json.load(actStates)
        actuators["elect_valve"].value = statuses["elect_valve"]
        actuators["extr_temp"].value = statuses["extr_temp"]
        actuators["extr_hum"].value = statuses["extr_hum"]
        print("ELECT VALVE : {}".format(actuators["elect_valve"].value))
        print("EXTRACTOR TEMP: {}".format(actuators["extr_temp"].value))
        print("EXTRACTOR HUM : {}".format(actuators["extr_hum"].value))

        print(CGREEN+"actuators setted succefully"+CEND)
except Exception as err:
    print(CYELLOW+"# WARNING: actuators_statuses.json file : {}".format(str(err))+CEND)

'''
# this part of code use google drive api to create deployement object and setup the authentication phase ,
# this flag driveAuthStatus used in one part of code to communicate with google drive server , and store data to it with the help of google drive api.
driveObj = Deployement() # create object for deployement
if driveObj.drive_auth(): # authentication with google drive api
    driveAuthStatus = True
else:
    driveAuthStatus = False
'''
# start server node to handle clients connection , each client has its own thread to handle it.

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as serverSocket:
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # ensuer reusability of socket connection
        serverSocket.bind((HOST,PORT)) # bind the socket to the specified host,port
        serverSocket.listen(5) # listen to the clients(ESP)
        serverSocket.settimeout(360) # timeout for 6 minutes

        while True:
            try:
                clientConnection , clientAddress = serverSocket.accept() # accepting the ESP connection ( client connection )
                # handle the client by creating a new thread for it using client_handler function in client_handling .
                '''
                    arguments for client_handler are :
                        serverSocket : socket used to handle clients connections .
                        clientConnection : client connection object returned by serverSocket.accept() .
                        clientAddress : list with client IP address and PORT.
                        actuators : dictionary holds actuators pins for command.
                        driveObj : google drive api object.
                        driveAuthStatus : google drive api authentication status ( true , false ).
                '''
                driveObj = None
                driveAuthStatus = True
                clientThread = threading.Thread(target = client_handler , args = (serverSocket,clientConnection,clientAddress,actuators,driveObj,driveAuthStatus) )
                clientThread.start()

            except Exception as err:
                print(CRED+"Error :: during handling threads / clients :: {}".format(str(err))+CEND)
                clientConnection.close()
