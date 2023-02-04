#include <GSM.h>


GSM gsmAccess;

GSM_SMS sms;

char phoneNumber[12]= "213656935000";


// char array of the message
char messageText[200]="MSG:V220I1P2000F0.8:END";

void setup()
{

  // initialize serial communications

  Serial.begin(9600);

  Serial.println("SMS Messages Sender/Receiver");
  Serial.println("Connecting...");
  // connection state

  boolean notConnected = true;

  // Start GSM shield

  while(!(gsmAccess.begin()==GSM_READY)){
    Serial.println("Not connected yet...");
    delay(1000);
  }

  Serial.println("GSM initialized");
  sendSMS(sms,phoneNumber,messageText);

}

void loop()
{
  receiveSMS(sms);

}


void sendSMS(GSM_SMS sms,char phoneNumber[12],char messageText[20]){

  Serial.print("Sending Message to mobile number: ");
  Serial.println(phoneNumber);
  Serial.println("Seding...");
  Serial.println();
  Serial.println("Message: ");
  Serial.println(messageText);
  // send the message
  sms.beginSMS(phoneNumber);
  sms.print(messageText);
  sms.endSMS();
  Serial.println("\nSending is done.\n");
}

void receiveSMS(GSM_SMS sms){
  char msgChar;
  char messageText[20];
  char senderNumber[12];
  short int i = 0;
  // If there are any SMSs available()
  Serial.println("Wait for message...");

  if (sms.available()) {

    Serial.println("\nMessage received from :");

    // Get remote number

    sms.remoteNumber(senderNumber, 12);

    Serial.println(senderNumber);

    while (msgChar = sms.read()) {
      Serial.print(msgChar);
      messageText[i] = msgChar;
      i = i + 1;
    }

    Serial.println("\nMessage receiving Done.");
    sms.flush();

}
delay(1000);
}
