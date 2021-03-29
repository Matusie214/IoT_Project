/*
 * 
 *            A0|--------------|D0  - Pir
 *              |              |D1  - Przekaźnik
 *              |              |D2  - RST (RFID)
 *              |              |D3  - Kontaktron
 *              |    NODEMCU   |D4  - SDA (RFID)
 *              |              |D5  - SCK (RFID)
 *              |              |D6  - MISO (RFID)
 *              |              |D7  - MOSI (RFID)
 *              |______________|D8  - LED
 *            
 * 
 */






//do mqtt
#include <EEPROM.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
unsigned long waitCount = 0;                 // counter
uint8_t conn_stat = 0;                       // Connection status for WiFi and MQTT:
                                             //
                                             // status |   WiFi   |    MQTT
                                             // -------+----------+------------
                                             //      0 |   down   |    down
                                             //      1 | starting |    down
                                             //      2 |    up    |    down
                                             //      3 |    up    |  starting
                                             //      4 |    up    | finalising
                                             //      5 |    up    |     up
const char* ssid        = "UPC5A95ED7";
const char* password    = "fh5rjQksw2Wr";
const char* mqtt_server = "34.123.208.229";

//tematy mqtt
char* MQTT_client       = "climate_log2";
char* door_rswitch      = "door_rswitch";
char* pir_door          = "pir_door";
char* rfid_topic        = "RFID";

char* door_switch       = "door_switch";
char* LED_topic         = "led_door";

WiFiClient espClient;
PubSubClient client(espClient);



//do czujników
#include <SPI.h>
#include<MFRC522.h>




#define pin_pir          D0
#define pin_switch_door  D1
#define RST_PIN          D2
#define pin_rswitch      D3 
#define SS_PIN           D4
#define pin_led          D8

MFRC522 mfrc522(SS_PIN,RST_PIN);
int conCounter              = 0;   // counter for the number of button presses
volatile int conState       = LOW;         // current state of the button
volatile int lastConState   = LOW; 

int pirCounter              = 0;   // counter for the number of button presses
volatile int pirState       = LOW;         // current state of the button
volatile int lastPirState   = LOW; 

volatile float co2          =0;
volatile float lastCo2State =0;



//mqtt
void setup_wifi() {
    delay(10);
    // We start by connecting to a WiFi network
    //Serial.println();
    //Serial.print("Connecting to ");
    //Serial.println(ssid);

    //WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);

   // Serial.println("");
   // Serial.println("WiFi connected");
   // Serial.println("IP address: ");
   //Serial.println(WiFi.localIP());
}

void reconnect() {
 // Loop until we're reconnected
   // Attempt to connect
 if (client.connect(MQTT_client)) {
   Serial.println("connected");
   // ... and subscribe to topic
    client.subscribe("test_switch");
 }
}

void publish_data(char* topic, String measure)
{
  client.publish(topic, (char*) measure.c_str());
}






void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.setTimeout(2000);
  WiFi.mode(WIFI_STA);
  SPI.begin();
  mfrc522.PCD_Init();
  pinMode(pin_pir, INPUT);
  pinMode(pin_rswitch, INPUT_PULLUP); //Kontaktron jako wejście
  pinMode(pin_switch_door, OUTPUT);
  pinMode(pin_led, OUTPUT);

  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  while(!Serial) { }

  
}


void callback(char* topic, byte* payload, unsigned int length) {
 
  String mess;
  for (int i=0;i<length;i++) {
    char receivedChar = (char)payload[i];
    mess+=receivedChar;
  //  Serial.println(mess);
   if (mess=="1"){
    digitalWrite(pin_switch_door, HIGH);
   }
   else{
    digitalWrite(pin_switch_door, LOW);
   }
   }
  }



void loop() {





  if ((WiFi.status() != WL_CONNECTED) && (conn_stat != 1)) { conn_stat = 0; }
  if ((WiFi.status() == WL_CONNECTED) && !client.connected() && (conn_stat != 3))  { conn_stat = 2; }
  if ((WiFi.status() == WL_CONNECTED) && client.connected() && (conn_stat != 5)) { conn_stat = 4;}
  switch (conn_stat) {
    case 0:                                                       // MQTT and WiFi down: start WiFi
      Serial.println("MQTT and WiFi down: start WiFi");
      setup_wifi();
      conn_stat = 1;
      break;
    case 1:                                                       // WiFi starting, do nothing here
      Serial.println("WiFi starting, wait : "+ String(waitCount));
      waitCount++;
      break;
    case 2:                                                       // WiFi up, MQTT down: start MQTT
      Serial.println("WiFi up, MQTT down: start MQTT");
      reconnect();
      conn_stat = 3;
      waitCount = 0;
      break;
    case 3:                                                       // WiFi up, MQTT starting, do nothing here
      Serial.println("WiFi up, MQTT starting, wait : "+ String(waitCount));
      waitCount++;
      break;
    case 4:                                                       // WiFi up, MQTT up: finish MQTT configuration
      Serial.println("WiFi up, MQTT up: finish MQTT configuration");
      //mqttClient.subscribe(output_topic);
      //mqttClient.publish(input_topic, Version);
      conn_stat = 5;                    
      break;
      
  
 
   
  
  
}
 if (conn_stat == 5) {  
    rfid_read();
    notify_pir();
    notify_kon();              
    client.loop();                                             
  } 
  // put your main code here, to run repeatedly:
  

}



void rfid_read(){
  char str[32] = "";
  byte nuidPICC[4];
  int tablica[4];
  String flaga="0";
  if(mfrc522.PICC_IsNewCardPresent())
  {
    for (byte i = 0; i < 4; i++) {
      nuidPICC[i] = mfrc522.uid.uidByte[i];
    }
    printHex(mfrc522.uid.uidByte, mfrc522.uid.size);
    array_to_string(mfrc522.uid.uidByte, 4, str);
    client.publish("RFID",str );
    for( int i = 0; i < sizeof(str);  ++i ){
        str[i] = (char)0;}
  if(mfrc522.PICC_ReadCardSerial())
  {
    
    Serial.println("UID: ");
    for (byte i=0;i<mfrc522.uid.size;i++){
      Serial.print(mfrc522.uid.uidByte[i]<0x10?"0":" ");
      Serial.print(mfrc522.uid.uidByte[i],HEX);
      tablica[i]=mfrc522.uid.uidByte[i];
    }
    for (byte i=0;i<mfrc522.uid.size;i++){
      if(tablica[i]==mfrc522.uid.uidByte[i]){
        flaga="1";
      }
      else{
        flaga="0";
        break;
      }
    }
    Serial.println();
    if (flaga=="1")
    {
      client.publish("test_switch", "1");
    }
    else{
      client.publish("test_switch", "0");
      
    }
    mfrc522.PICC_HaltA();
    }
  }
 
}


void notify_pir(){
  
  pirState= digitalRead(pin_pir);
  if (pirState != lastPirState) {
    // if the state has changed, increment the counter
    if (pirState == HIGH) {
      // if the current state is HIGH then the button went from off to on:
      pirCounter++;
      Serial.println("on");
      Serial.print("number of counter: ");
      Serial.println(pirCounter);
      client.publish(pir_door,"0" );
    } else {
      // if the current state is LOW then the button went from on to off:
      Serial.println("off");
      client.publish(pir_door,"1" );
    }
    
    // Delay a little bit to avoid bouncing
    delay(50);
  }
  // save the current state as the last state, for next time through the loop
  lastPirState = pirState;
  
}

void notify_kon(){
  
  conState= digitalRead(pin_rswitch);
  if (conState != lastConState) {
    // if the state has changed, increment the counter
    if (conState == HIGH) {
      // if the current state is HIGH then the button went from off to on:
      conCounter++;
      Serial.println("daleko");
      Serial.print("number of counter: ");
      Serial.println(conCounter);
      client.publish(door_rswitch,"0" );
      
    } else {
      // if the current state is LOW then the button went from on to off:
      Serial.println("blisko");
      client.publish(door_rswitch,"1" );
    }
    // Delay a little bit to avoid bouncing
    delay(50);
  }
  // save the current state as the last state, for next time through the loop
  lastConState = conState;
  
}
void printHex(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}

void array_to_string(byte array[], unsigned int len, char buffer[])
{
   for (unsigned int i = 0; i < len; i++)
   {
      byte nib1 = (array[i] >> 4) & 0x0F;
      byte nib2 = (array[i] >> 0) & 0x0F;
      buffer[i*2+0] = nib1  < 0xA ? '0' + nib1  : 'A' + nib1  - 0xA;
      buffer[i*2+1] = nib2  < 0xA ? '0' + nib2  : 'A' + nib2  - 0xA;
   }
   buffer[len*2] = '\0';
}