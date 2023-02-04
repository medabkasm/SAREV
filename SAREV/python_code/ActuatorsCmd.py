from colors import *



def relay_command(jsonData,actuators):
    try:
        # references.json file holds reference data used for comparaison between it and real time data sent by client , for actions decision.
        '''
            eg : if the real temperature value sent from client is 27c degree , and reference temperature
            values in references.json file is 29c as minimum and 35c degree as maximum , broker gives order
            to actuator ( heater ) to take action and start working till the client sends a 29c value or above
            next time.
        '''

        with open("./config_files/references.json","r") as referencesFile:
            references = json.load(referencesFile)
            print(CGREEN+"references file loaded succefully"+CEND)
    except Exception as err:
        print(CRED+"Error :: during opening references file :: {}".format(str(err))+CEND)
        return ( False , "Error :: during opening references file :: " + str(err) )

    try:
        # comparaison between real values and reference values.
        if jsonData["hum"] >= references["MAX_HUM"]:
            if actuators["extr_hum"].value == 1:
                print(CYELLOW+"EXCTRACTOR_HUM IS TURNED ON"+CEND)
            else:
                actuators["extr_hum"].on()
                print(CYELLOW+"EXCTRACTOR_HUM TURNED ON"+CEND)
        elif jsonData["hum"] <= references["MIN_HUM"]:
            if actuators["extr_hum"].value == 0:
                print(CYELLOW+"EXCTRACTOR_HUM IS TURNED OFF"+CEND)
            else:
                actuators["extr_hum"].off()
                print(CYELLOW+"EXCTRACTOR_HUM TURNED OFF"+CEND)
        else:
            if actuators["extr_hum"].value == 0:
                print(CYELLOW+"EXCTRACTOR_HUM IS TURNED OFF"+CEND)
            else:
                print(CYELLOW+"EXCTRACTOR_HUM TURNED ON"+CEND)


        if jsonData["temp"] >= references["MAX_TEMP"]:
            if actuators["extr_temp"].value == 1:
                print(CYELLOW+"EXCTRACTOR_TEMP IS TURNED ON"+CEND)
            else:
                actuators["extr_temp"].on()
                print(CYELLOW+"EXCTRACTOR_TEMP TURNED ON"+CEND)
        elif jsonData["temp"] <= references["MIN_TEMP"]:
            if actuators["extr_temp"].value == 0:
                print(CYELLOW+"EXCTRACTOR_TEMP IS TURNED OFF"+CEND)
            else:
                actuators["extr_temp"].off()
                print(CYELLOW+"EXCTRACTOR_TEMP TURNED OFF"+CEND)
        else:
            if actuators["extr_temp"].value == 0:
                print(CYELLOW+"EXCTRACTOR_TEMP IS TURNED OFF"+CEND)
            else:
                print(CYELLOW+"EXCTRACTOR_TEMP TURNED ON"+CEND)


    except Exception as err:
        print(CRED+"Error :: during executing commands :: {}".format(str(err))+CEND)
        return ( False , "Error :: during executing commands :: " + str(err) )

    try:
        # update actuators states file (actuators_statuses.json).
        with open("./config_files/actuators_statuses.json","w") as actStates:
            statuses = {
                "elect_valve" : actuators["elect_valve"].value,
                "extr_temp" : actuators["extr_temp"].value,
                "extr_hum" : actuators["extr_hum"].value,
            }
            json.dump(statuses,actStates)
            print(CGREEN+"actuators_statuses.json file setted succefully"+CEND)
    except Exception as err:
        print(CYELLOW+"# WARNING: actuators_statuses.json file : {}".format(str(err))+CEND)
        return (True ,"# WARNING: actuators_statuses.json file : "+str(err) )

    return (True , "command operation done successfully")
