
#include "Arduino.h"
#include <MQ135.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>




float sensor_data(unsigned short analogPin,unsigned short cmdPin[4],String response,int sensorMaxVal,int sensorMinVal){
  float data;

  if(response.substring(3) == "SM"){
    digitalWrite(cmdPin[0],1);
    delay(2000);
    data = analogRead(analogPin);
    Serial.print("sm readed\t");
    Serial.println(data);
    digitalWrite(cmdPin[0],0);
    return map(data,sensorMaxVal,sensorMinVal,0,100);
  }
  else if(response.substring(3) == "TM"){
    extern DHT_Unified dht;
    digitalWrite(cmdPin[1],1);
    delay(2000);
    Serial.println(F("DHTxx Unified Sensor reading temperature begins..."));
    // Print temperature sensor details.
    sensors_event_t event;
    dht.temperature().getEvent(&event);
    digitalWrite(cmdPin[1],0);
    if (isnan(event.temperature)) {
      Serial.println(F("Error reading temperature!"));
      return -100;
    }
    else {
      Serial.print(F("Temperature: "));
      Serial.print(event.temperature);
      Serial.println(F("°C"));
      return event.temperature;
    }
  }
  else if (response.substring(3) == "HUM"){
    extern DHT_Unified dht;
    digitalWrite(cmdPin[1],1);
    delay(2000);
    Serial.println(F("DHTxx Unified Sensor reading humidity begins..."));
    // Get humidity event and print its value.
    sensors_event_t event;
    dht.humidity().getEvent(&event);
    digitalWrite(cmdPin[1],0);
    if (isnan(event.relative_humidity)) {
      Serial.println(F("Error reading humidity!"));
      return -1;
    }
    else {
      Serial.print(F("Humidity: "));
      Serial.print(event.relative_humidity);
      Serial.println(F("%"));
      return event.relative_humidity;
    }

  }
  else if(response.substring(3) == "CO"){
    float data;
    #define RZERO 76.63;
    MQ135 gasSensor = MQ135(analogPin);
    digitalWrite(cmdPin[2],1);
    delay(30000);
    data = gasSensor.getPPM();
    Serial.println("co readed");
    digitalWrite(cmdPin[2],0);
    return data;
  }

}
