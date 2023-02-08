//#include <ESP8266WiFi.h> already included in connection.h file
#include"connection.h"


using namespace std;

unsigned short success = 14; // success operation D0
unsigned short failed = 12; // failed operation D1


const char* ssid = "redmi";
const char* password = "";
unsigned short nodeId = 1;

IPAddress local_IP(192,168,43,5);
IPAddress gateway(192,168,43,11);
IPAddress subnet(255,255,255,0);


IPAddress server(192,168,43,246);
unsigned short PORT = 65000;
WiFiClient client;



void setup(void){
  Serial.begin(9600);
  pinMode(success,OUTPUT);
  pinMode(failed,OUTPUT);

  while(true){
    if( init_station(ssid,password,local_IP,gateway,subnet,success,failed) ){
      break;
    }
    delay(2000); // wait for 2 seconds befor trying to reconnect to the AP.
  }

}

void loop() {


  Serial.println("waiting for server connection...");

  if(client.connect(server,PORT)){ // start connection with the server via given AP.
    Serial.println("server is alive");
    digitalWrite(failed,1);
    Connection *node ;
    node = new Connection;
    if(node->init_connection(client,10000)){ // init connection between the client and the server (handshake)
      digitalWrite(failed,0);
      digitalWrite(success,1);

        delete node;
        digitalWrite(success,0);
      }
    }
  delay(5000);


}
