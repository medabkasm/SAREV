//#include <ESP8266WiFi.h> already included in connection.h file
#include"connection.h"
//#include"sensors.h"
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

const char* ssid = "redmi";
const char* password = "";
unsigned short nodeId = 1;

IPAddress local_IP(192,168,43,5);
IPAddress gateway(192,168,43,11);
IPAddress subnet(255,255,255,0);

float sensorAirVal = 1024; // 0% dry
float sensorWaterVal = 250; // 100% wet

IPAddress server(192,168,43,246);
unsigned short PORT = 65000;
WiFiClient client;

DHT_Unified dht(dhtPin, DHT22);

void setup(void){
  Serial.begin(9600);
  pinMode(success,OUTPUT);
  pinMode(failed,OUTPUT);
  pinMode(waitingConnection,OUTPUT);
  pinMode(SmSensor,OUTPUT);
  pinMode(tempSensor,OUTPUT);
  pinMode(CoSensor,OUTPUT);
  pinMode(analogPin,INPUT);
  //pinMode(dhtPin,INPUT);

  while(true){
    if( init_station(ssid,password,local_IP,gateway,subnet,success,failed) ){
      break;
    }
    delay(2000); // wait for 2 seconds befor trying to reconnect to the AP.
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

  if(client.connect(server,PORT)){ // start connection with the server via given AP.
    Serial.println("server is alive");
    digitalWrite(failed,1);
    Connection *node ;
    node = new Connection;
    if(node->init_connection(client,10000)){ // init connection between the client and the server (handshake)
      digitalWrite(failed,0);
      digitalWrite(success,1);
      float data;
      digitalWrite(SmSensor,1);
      delay(2000);
      data = analogRead(A0);
      data = map(data,sensorAirVal,sensorWaterVal,0,100);
      Serial.print(F("Soil moisture: "));
      Serial.print(data);
      Serial.println(F("%"));
      sm = data;
      digitalWrite(SmSensor,0);
      digitalWrite(tempSensor,1);
      delay(2000);

      sensors_event_t event;
      dht.temperature().getEvent(&event);

      if (isnan(event.temperature)) {
        Serial.println(F("Error reading temperature!"));
        temp = NULL;
      }
      else {
        Serial.print(F("Temperature: "));
        Serial.print(event.temperature);
        Serial.println(F("°C"));
        temp = event.temperature;
      }
      dht.humidity().getEvent(&event);
      if (isnan(event.relative_humidity)) {
        Serial.println(F("Error reading humidity!"));
        hum = NULL;
      }
      else {
        Serial.print(F("Humidity: "));
        Serial.print(event.relative_humidity);
        Serial.println(F("%"));
        hum = event.relative_humidity;
      }
        digitalWrite(tempSensor,0);
        sprintf(jsonData,"{ \"id\" : \%d , \"temp\" : %f , \"hum\" : %f , \"sm\" : %f }",nodeId,temp,hum,sm);
        Serial.println(jsonData);
        client.print(jsonData);

        delete node;
        digitalWrite(success,0);
      }
    }
  delay(5000);


}
