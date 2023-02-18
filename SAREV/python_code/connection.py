import socket # for main program
from colors import *


# Connection class , with different methods used to handle client connection used by client_handling,client_handler(*),
'''
    HOST : client IP address.
    PORT : client PORT.
'''

class Connection:

    def __init__(self,HOST,PORT):
        self.HOST = HOST
        self.PORT = PORT
        self.get = None # get or order (read data-True / make action-False)
        self.dataType = None # the type of data we want to read (temperature , soil moisture , CO2)

    def _action(self,serverSocket): # private methode

        status = self.dataType.encode("ascii")

        try:
            serverSocket.send(status)
        except Exception as err:
            print(CRED+"Error :: while sending {} flag : {}".format(status,str(err))+CEND)
            return -2

        data = serverSocket.recv(1024).decode().strip("\r\n")
        if data and ("CNF" in data):
            try:
                print(CGREEN+"order executed successfully"+CEND)
                serverSocket.send("RECV".encode("ascii"))
                serverSocket.close()
                return True
            except Exception as err:
                print(CRED+"Error :: while sending RECV flag : {}".format(str(err))+CEND)
                serverSocket.close()
                return False
        elif data and ~("CNF" in data):
            try:
                serverSocket.send("RECV".encode("ascii"))
                serverSocket.close()
                data = float(data)
                return data
            except Exception as err:
                print(CRED+"Error :: while sending RECV flag : {}".format(str(err))+CEND)
                serverSocket.close()
                return float(data)
        else:
            print(CRED+"Error :: no data/order_confirmation received"+CEND)
            serverSocket.close()
            return -2 # no data received

    def test_server_connectivity(self):
        try:
            serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # ensuer reusability of socket connection
            serverSocket.connect((self.HOST,self.PORT))
            print(CGREEN+"server is alive"+CEND)
            return serverSocket
        except Exception as err:
            print(CRED+"Error :: while creating the socket object : {}".format(str(err))+CEND)
            return 0

    # start handshake between broker and client (ESP)
    '''
        serverSocket : client connection socket created by control_unit.py returned by socket.accept()
    '''
    def _hand_shake(self,serverSocket):
        try:
            # begin the handshake between the server and the client to start read/write data.
            data = serverSocket.recv(1024).decode().strip("\r\n") # receive the first flag from the client STR.
            if "STR" in data:
                print(CGREEN+"connection with the client begins"+CEND)
                serverSocket.send("STR".encode("ascii")) # STR flag sent to client to inform that the connection begins.
                data = serverSocket.recv(1024).decode().strip("\r\n") # flag received from client to inform that the connection is establised after it received STR flag from broker.
                if "EST" in data:
                    print(CGREEN+"connection with the client is established"+CEND)
                    return serverSocket
                else:
                    print(CRED+"Error :: bad EST flag"+CEND)
                    return -1
            else:
                print(CRED+"Error :: bad STR flag"+CEND)
                return -1
        except Exception as err:
            print(CRED+"Error :: handshake error : {}".format(str(err))+CEND)
            return -1


    def begin(self,get):

        self.get = get

        if self.get == "cmd":
            self.dataType = "ORD"
        elif self.get == "temp":
            self.dataType = "GETTM"
        elif self.get == "hum":
            self.dataType = "GETHUM"
        elif self.get == "sm":
            self.dataType = "GETSM"
        elif self.get == "co":
            self.dataType = "GETCO"
        else:
            print(CYELLOW+"Error :: invalid data type : {}".format(get)+CEND)
            return False

        serverSocket = self.test_server_connectivity()
        if isinstance(serverSocket,socket.socket):
            if isinstance(self._hand_shake(serverSocket),socket.socket):
                actionStatus = self._action(serverSocket)
                return actionStatus

        return False
