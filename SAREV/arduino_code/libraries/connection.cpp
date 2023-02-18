#include "Arduino.h"
#include"connection.h"
#include"sensors.h"

/*
bool init_SAP(const char* ssid,IPAddress local_IP,IPAddress gateway,IPAddress subnet,unsigned short success,unsigned short failed){

 digitalWrite(success,0);
 digitalWrite(failed,0);

  Serial.print("Setting soft-AP configuration ... ");
  if(WiFi.softAPConfig(local_IP,gateway,subnet)){
    Serial.println("Ready");
    digitalWrite(success,1);
    delay(2000);
    digitalWrite(success,0);
    delay(2000);
    Serial.println("Setting soft-AP ... ");

    if(WiFi.softAP(ssid,false)){
      Serial.println("Ready");
      digitalWrite(success,1);
      delay(2000);
      digitalWrite(success,0);
      Serial.print("Soft-AP IP address : ");
      Serial.println(WiFi.softAPIP());
      return true;
    }
    else{
      Serial.println("Failed setting UP AP");
      digitalWrite(failed,1);
      delay(2000);
      return false;
    }
  }

  else{
    Serial.println("Failed configuring AP");
    digitalWrite(failed,1);
    delay(2000);
    return false;
  }

}

*/


// init_station function used to initialize connection of the client (ESP) with the router (modem - access point).
/*
  char * ssid : string with the id of the AP.
  char * password : string with the password of the AP.
  IPAddress staticIp : static IP address for our client given by the AP.
  IPAddress gateway : IP address of the gateway of the AP.
  IPAddress subnet : subnet mask for AP network.
  unsigned short success : PIN for a GREEN LED used for connection success indication.
  unsigned short failed : PIN for a RED LED used for connection failed indication.

  returns true if the connection is established correctly , false otherwise.
*/
bool init_station(const char* ssid,const char* password,IPAddress staticIp,IPAddress gateway,IPAddress subnet,unsigned short success,unsigned short failed ){
  Serial.printf("Connecting to %s\n", ssid);
  if(WiFi.config(staticIp, gateway, subnet)){ // wifi configuration for ESP ( client ).
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED){ // status of wifi connection.
      digitalWrite(failed,1); // RED LED blinking waiting for connection in PIN with the variable failed.
      delay(500);
      digitalWrite(failed,0);
      delay(500);
    }
    digitalWrite(success,1); // GREEN LED on , means wifi connection is established.
    Serial.print("Connected, IP address : ");
    Serial.println(WiFi.localIP()); // prints local ip address for ESP given by AP.
    delay(2000);
    digitalWrite(success,0);
    return true;
  }

  return false;
}

// timeout function , private use inside Connection class.
/*
  WiFiClient client : server object(broker).
  unsigned long : timout value.

  returns true in case of connection timeout , false otherwise.
*/

bool Connection::timeout(WiFiClient client,unsigned long maxTime){
  unsigned long startTime = millis();
  while(!client.available()){ // check server availabality ( connection ).
    if(millis() - startTime > maxTime ){
      Serial.println("connection timeout , connection with the server will be closed");
      return true ;
    }
  }
  return false;
}

// init_connection function , public use inside Connection class , used to establish handshake with the server(broker).
/*
  WiFiClient client : server object ( broker).
  unsigned long : timeout value in micro seconds , used inside timeout function.

  returns false in case of timeout connection or flag error after closing connection with the server , true otherwise.

*/

bool Connection::init_connection(WiFiClient client,unsigned long maxTime){

  Serial.println("client connected"); // start connection with the server
  client.print("STR"); // send STR flag to server in order to start connection , waiting for a returning STR flag.

  if(timeout(client,maxTime)){
    client.stop();
    return false;
  }
  String response  = client.readStringUntil('\r'); // start reading data from server ( handshake ).
  if(response == "STR"){
    Serial.println("start handshake...");
    client.print("EST"); // connection is established , confirmed to the server with EST (established) flag
    Serial.println("Connection with the server is established");
    return true;
    }
    else{
      Serial.println("FLAG :: "+response+" :: bad flag , connection with the server will be closed");
      client.stop();
      return false;
    }

}


void Connection::read_data(WiFiClient client,unsigned long maxTime,unsigned short analogPin,unsigned short cmdPin[4],int sensorMaxVal=100,int sensorMinVal=0){

  if(timeout(client,maxTime)){
    client.stop();
    return;
  }

  String response = client.readStringUntil('\r');
  if (response.substring(0,3)=="GET" && (response.substring(3) == "TM" || response.substring(3) == "SM" || response.substring(3) == "CO" || response.substring(3) == "HUM")){
    Serial.println("reading data...");
    float data = sensor_data(analogPin,cmdPin,response,sensorMaxVal,sensorMinVal);
    Serial.println("data readed successfully");
    Serial.println("sending data...");
    client.print(data);
    Serial.println("data sent successfully");

    if(timeout(client,maxTime)){
      Serial.println("receiving not confirmed");
      client.stop();
      return;
    }
    response = client.readStringUntil('\r');
    if (response == "RECV"){
      Serial.println("receiving confirmed");
    }
    else{
      Serial.println("FLAG :: "+response+" :: bad flag , connection with the server will be closed");
    }
    delay(2000);
    client.stop();
  }
  else{
    Serial.println("FLAG :: "+response+" :: bad flag , connection with the server will be closed");
    client.stop();
  }
}


void Connection::get_command(WiFiClient client , unsigned long maxTime , unsigned short orderPin){

  if(timeout(client,maxTime)){
    client.stop();
    return;
  }

  String response = client.readStringUntil('\r');
  if (response == "ORD"){ // order flag
    Serial.println("action begins");
  //  executes the function that is responsible for command (pompe , electro valve)
    Serial.println("order executed");
    client.print("CNF"); // confirm flag
    Serial.println("confirming order to the server...");

    if(timeout(server,maxTime)){
      Serial.println("order not confirmed");
      client.stop();
      return;
    }
    response = client.readStringUntil('\r');
    if (response == "RECV"){
      Serial.println("order confirmed");
    }
    else{
      Serial.println("FLAG :: "+response+" :: bad flag , connection with the server will be closed");
    }
    delay(2000);
    client.stop();
  }
  else{
    Serial.println("FLAG :: "+response+" :: bad flag , connection with the server will be closed");
    client.stop();
  }

}
