//#include <ESP8266WiFi.h> already included in connection.h file
#include"connection.h"

unsigned short success = 16; // success operation D0
unsigned short failed = 5; // failed operation D1
unsigned short waitingConnection = 4; // waitingConnection led ( waiting for station to connect with the AP D2
unsigned short cmdPin = 14 ; // command the pompe , valve ..ect  D5
float data ;
String response;

const char* ssid = "redmi";
const char* password = "";

IPAddress local_IP(192,168,43,6);
IPAddress gateway(192,168,43,11);
IPAddress subnet(255,255,255,0);

float sensorMaxVal = 1024; // 0% dry
float sensorMinVal = 250; // 100% wet

WiFiServer server(25);


void setup(void){
  Serial.begin(9600);
  pinMode(success,OUTPUT);
  pinMode(failed,OUTPUT);
  pinMode(waitingConnection,OUTPUT);
  pinMode(cmdPin,OUTPUT);

  while(true){
    if( init_station(ssid,password,local_IP,gateway,subnet,success,failed) ){
      server.begin();
      break;
    }
    delay(5000); // wait for 5sec befor trying to reconect to AP
  }
}

void loop() {

  WiFiClient client = server.available(); // wait for a new client
  delay(1000);

  if(client.connected()){

    Connection *node ;
    node = new Connection;

    if(node->init_connection(client,10000)){ // init connection between the client and the server (handshake)
      node->get_command(client,10000,cmdPin); // send data and close connection
      delete node;
    }
  }

}
