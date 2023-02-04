from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime
import time
from colors import *

i = 0
data = ""


class Deployement: # class responsible for google drive api

    def __init__(self):
        self.data = ''
        self.drive = None
        self.dataFile = None

    def drive_auth(self): # authentication with settings.yaml file
        try:
            gauth = GoogleAuth()
            # Create local webserver and auto handles authentication.
            gauth.LocalWebserverAuth()
            self.drive = GoogleDrive(gauth)
            print(CGREEN+"Authentication with api is done successfully"+CEND)
            return self.drive
        except Exception as err:
            print(CRED+"Error :: api authentication failed :: {}".format(str(err))+CEND)
            return False

    def set_data(self,filePath,title=''): # create title under this format : eg: HUM%_date.txt or TEMP_date.csv ..ect

        if filePath:
            self.filePath = filePath
        else:
            print(CRED+"Error :: invalid file path {}".format(filePath)+CEND)
            return False
        try:
            self.dataFile = self.drive.CreateFile()
        except Exception as err:
            print(CRED+"Error :: cannot create file :: {}".format(str(err))+CEND)
            return False

        if title:
            self.dataFile['title'] = title

        try:
            self.dataFile.SetContentFile(self.filePath)
            print(CGREEN+"data file setted successfully for drive uploading"+CEND)
            return True
        except Exception as err:
            print(CRED+"Error :: cannot set data properly :: {}".format(str(err))+CEND)
            return False

    def upload_file(self):
        try:
            print(CYELLOW+"uploading..."+CEND)
            self.dataFile.Upload()
            print(CGREEN+"File {} uploaded successfully".format(self.filePath)+CEND)
            return True
        except Exception as err:
            print(CRED+"Error :: file {} cannot be uploaded :: {}".format(self.filePath,str(err))+CEND)
            return False
