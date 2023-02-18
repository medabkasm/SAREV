
from connection import *
from datetime import datetime
from time import sleep
import saving
import ActuatorsCmd
import os




# function to handle client connection , created by control_unit.py as a thread method.
'''
    arguments for client_handler are :
        serverSocket : socket used to handle clients connections .
        clientConnection : client connection object returned by serverSocket.accept() .
        clientAddress : client IP address.
        actuators : dictionary holds actuators pins for command.
        driveObj : google drive api object.
        driveAuthStatus : google drive api authentication status ( true , false ).
'''
def client_handler(serverSocket,clientConnection,clientAddress,actuators,driveObj,driveAuthStatus):
    conn = Connection(clientAddress[0],clientAddress[1]) # return Connection instance with client info.
    print("-------------------------------------------------------")
    print("connection accepted at : {}".format(datetime.now()))
    print("IP : {}".format(clientAddress[0]))
    print("PORT : {}".format(clientAddress[1]))
    # conn._hand_shake(*) returns -1 for handshake faillure , or socket Object ( client connection ) in case of succefull handshake.
    if isinstance(conn._hand_shake(clientConnection),socket.socket):
        try:
            data = clientConnection.recv(1024) # start receiving data from client.
        except Exception as err:
            print(CRED+"Error :: error with receving data from client : {}".format(str(err))+CEND)
            return
        if data:
            try:
                # data received from client in json format eg: {'temp' : 20 , 'hum' : 40 ....}
                # id , TEMPERATURE , AIR MOISTURE , SOIL MOISTURE .
                jsonData = json.loads(data.decode("ascii").strip("\r\n"))
                jsonData["time"] = str(datetime.now())
                print("\nTIME : {}".format(jsonData["time"]))
                print("NODE ID : {}".format(jsonData["id"]))
                print("TEMPERATURE : {} C".format(jsonData["temp"]))
                print("AIR MOISTURE : {} %".format(jsonData["hum"]))
                print("SOIL MOISTURE : {} %".format(jsonData["sm"]))

                # check data , in order to make decision wether the client should execute an action or not.

                '''
                    jsonData : json object with all data sent by client.
                    actuators : dictionary holds actuators pins for command.
                '''
                
                commandStatus = ActuatorsCmd.relay_command(jsonData,actuators)
                # set system_status data for records.
                jsonData["system_status"] = {
                    "extr_temp" : actuators["extr_temp"].value ,
                    "extr_hum" : actuators["extr_hum"].value ,
                    "elect_valve" : actuators["elect_valve"].value,
                    "commandStatus" : commandStatus[0],
                    "commandStatusText" : commandStatus[1],
                    }

                # create system_status json file and upload it to google drive.
                fileName = "node_data_"+str(datetime.now())+".json"
                fileObj = saving.Saving("./data/"+fileName) # file name should be ended with extension , .txt , .csv , .js or .sjon.
                if fileObj:
                    if fileObj.create_file():
                        if fileObj.add_data(jsonData):
                            fileObj.close_file()
                            '''
                            if driveAuthStatus: # check authentication status
                                if driveObj.set_data("./data/"+fileName,fileName): # create the file for google drive
                                    driveObj.upload_file() # upload file to google drive
                            '''
            except Exception as err:
                print(CRED+"Error :: error with creating data in json file : {}".format(str(err))+CEND)

        else:
            print(CRED+"Error :: no data received : {}".format(data)+CEND)

    clientConnection.close()
    print(CYELLOW+"connection with node closed"+CEND)
    print("-------------------------------------------------------")
    return
