//#include <ESP8266WiFi.h> already included in connection.h file
#include"connection.h"
#include"sensors.h"
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

using namespace std;

unsigned short success = 14; // success operation D0
unsigned short failed = 12; // failed operation D1
unsigned short waitingConnection = 2; // waitingConnection led ( waiting for station to connect with the AP D2
unsigned short analogPin = A0; // pin to read the sensor data -- analog signal
unsigned short tempSensor = 5 ; // use temperature sensor D5
unsigned short SmSensor = 4; // use soil moisture sensor D6
unsigned short CoSensor = 16 ; // use CO2 sensor D7
unsigned short dhtPin = 0 ; // dht sensor needs digital input D8
unsigned short cmdPins[] =  {SmSensor,tempSensor,CoSensor,dhtPin};

float temp , hum , sm ;
char jsonData[40];
unsigned short nodeId = 1;
DHT_Unified dht(dhtPin, DHT22);

const char* ssid = "redmi";
const char* password = "";

IPAddress local_IP(192,168,43,5);
IPAddress gateway(192,168,43,11);
IPAddress subnet(255,255,255,0);

float sensorMaxVal = 740; // 0% dry
float sensorMinVal = 250; // 100% wet

IPAddress server(192,168,43,246);
unsigned short PORT = 65000;
WiFiClient client;

void setup(void){
  Serial.begin(9600);
  pinMode(success,OUTPUT);
  pinMode(failed,OUTPUT);
  pinMode(waitingConnection,OUTPUT);
  pinMode(SmSensor,OUTPUT);
  pinMode(tempSensor,OUTPUT);
  pinMode(CoSensor,OUTPUT);
  pinMode(analogPin,INPUT);
  pinMode(dhtPin,INPUT);

  while(true){
    if( init_station(ssid,password,local_IP,gateway,subnet,success,failed) ){
      break;
    }
    delay(2000); // wait for 2 seconds befor trying to reconect to the AP
  }
  dht.begin();
  Serial.println(F("DHTxx Unified Sensor Example"));
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);
  dht.humidity().getSensor(&sensor);
}

void loop() {

  digitalWrite(tempSensor,0);
  digitalWrite(CoSensor,0);
  digitalWrite(SmSensor,0);

  Serial.println("waiting for server connection...");
  if(client.connect(server,PORT)){
    digitalWrite(success,1);
    Serial.println("server is alive");
    Connection *node ;
    node = new Connection;
    if(node->init_connection(client,10000)){ // init connection between the client and the server (handshake)
      temp = sensor_data(A0,cmdPins,"GETTM",sensorMaxVal,sensorMinVal);
      hum = sensor_data(A0,cmdPins,"GETHUM",sensorMaxVal,sensorMinVal);
      sm = sensor_data(A0,cmdPins,"GETSM",sensorMaxVal,sensorMinVal);
      sprintf(jsonData,"{ \"id\" : %d , \"temp\" : %f , \"hum\" : %f , \"sm\" : %f }",nodeId,temp,hum,sm);
      Serial.println(jsonData);
      client.print(jsonData);
      delete node;
      digitalWrite(success,0);
    }
  }



}
