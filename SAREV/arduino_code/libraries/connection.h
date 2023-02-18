
#ifndef CONNECTION_H
#define CONNECTION_H

#include "Arduino.h"
#include <ESP8266WiFi.h>


bool init_SAP(String ssid,IPAddress local_IP,IPAddress gateway,IPAddress subnet,unsigned short success,unsigned short failed);
bool init_station(const char* ssid,const char* password,IPAddress staticIp,IPAddress gateway,IPAddress subnet,unsigned short success,unsigned short failed );

class Connection{
  private:
    bool timeout(WiFiClient client,unsigned long maxTime);
  public:
    bool init_connection(WiFiClient client,unsigned long maxTime);
    void read_data(WiFiClient client,unsigned long maxTime,unsigned short analogPin,unsigned short cmdPin[3],int sensorMaxVal,int sensorMinVal);
    void get_command(WiFiClient client ,unsigned long maxTime ,unsigned short orderPin);
};

#endif
