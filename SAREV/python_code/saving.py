import csv # for saving module
from colors import *
import json

class Saving:
    def __init__(self,fileName,separateFiles = False):
        self.fileName = fileName # created file name to store the data
        try:
            self.fileFormat = self.fileName.split(".")[-1].lower()
        except:
            print(CRED+"Error :: file format not exist ( .txt , .csv , .json , .js )".format(str(err))+CEND)
            return None
            
        self.separateFiles = separateFiles # store data in separate files or not (humidty data , temperature data ...ect) , False by default
        self.__csvWriter = None
        self.__dataFile = None

    def create_file(self):

        if self.fileFormat == "csv" or self.fileFormat == "txt" or self.fileFormat == "js" or self.fileFormat == "json":
            try:
                self.__dataFile = open(self.fileName,"w") # didn't use 'with' statement for future use of the open file
                print(CGREEN+"\nfile {} created".format(self.fileName)+CEND)
                return True
            except Exception as err:
                print(CRED+"Error :: file {} cannot be created :: {}".format(str(err))+CEND)
                return False

            if self.fileFormat == "csv":
                try:
                    self.__csvWriter = csv.writer(self.__dataFile,delimiter = ',')
                    return True
                except Exception as err:
                    print(CRED+"Error :: with opening csv writer :: {}".format(str(err))+CEND)
                    return False
            else:
                return True
        else:
            print(CRED+"Error :: unkown file format :: supports only .txt and .csv and .json formats"+CEND)
            return FalseTrue



    def add_data(self,data):

        # data parameter should be list type in case of .csv file , string in case of text file , and dictionary in case of json file.
        if self.fileFormat == "csv":
            if isinstance(data,list):
                try:
                    self.__csvWriter.writerow(data) # use the open writer from the create_file methode
                    print(CGREEN+"data added succefully to the {} file".format(self.fileName)+CEND)
                    return True
                except Exception as err :
                    print(CRED+"Error :: during writing row to {} file :: {}".format(self.fileName,str(err))+CEND)
                    return False
            else:
                print(CRED+"Error :: data for csv file must be a list"+CEND)
                return False

        elif self.fileFormat == "txt":
            if isinstance(data,str):
                try:
                    data = data.rstrip("\n")
                    self.__dataFile.write(data + "\n")
                    print(CGREEN+"data added succefully to the {} file".format(selfileName)+CEND)
                    return True
                except Exception as err:
                    print(CRED+"Error :: during writing data to {} file :: {}".format(self.fileName,str(err))+CEND)
                    return False
            else:
                print(CRED+"Error :: data for txt file must a string"+CEND)
                return False

        elif self.fileFormat == "json" or self.fileFormat == "js":
            if isinstance(data,dict):
                try:
                    json.dump(data,self.__dataFile)
                    print(CGREEN+"data added succefully to the {} file".format(self.fileName)+CEND)
                    return True
                except Exception as err:
                    print(CRED+"Error :: during writing data to {} file :: {}".format(self.fileName,str(err))+CEND)
                    return False
            else:
                print(CRED+"Error :: data for txt file must a dict"+CEND)
                return False




    def close_file(self):
        try:
            self.__dataFile.close()
            self.__csvWriter = None
            print(CGREEN+"file {} closed succefully".format(self.fileName)+CEND)
            return True

        except Exception as err:
            print(CRED+"Error :: cannot close file {} succefully :: {}".format(self.fileName,str(err))+CEND)
            return False
