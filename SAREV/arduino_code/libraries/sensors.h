
#ifndef SENSORS_H
#define SENSORS_H

#include "Arduino.h"



float sensor_data(unsigned short analogPin,unsigned short cmdPin[4],String response,int sensorMaxVal,int sensorMinVal);

#endif
