/*
 * 
 *    Co2 -  A0-|--------------|-D0  - Temp i Hum
 *              |              |-D1  - Kontaktron furtka
 *              |              |-D2  - przekaznik furtka
 *              |              |-D3  - syrena
 *              |    NODEMCU   |-D4  - przekaznik brama
 *              |              |-D5  - kontaktron brama
 *              |              |-D6  -
 *              |              |-D7  -
 *              |______________|-D8  - LED
 *            
 * 
 */
#include "DHTesp.h"

#include <EEPROM.h>
#include <DallasTemperature.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>

// #define DHTPIN 4     // what digital pin the DHT22 is conected to
// #define DHTTYPE DHT22   // there are multiple kinds of DHT sensors

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


//const char* Version = "{\"Version\":\"low_prio_wifi_v2\"}";
//const char* Status = "{\"Message\":\"up and running\"}";



DHTesp dht;

//deklaracja pinów
#define pin_co2              A0                        //analog feed from MQ135
#define co2Zero              55                        //calibrated CO2 0 level
#define pin_dht              D0
#define pin_gateway_rswitch  D1
#define pin_gate             D2
#define pin_syren            D3
#define pin_gateway          D4
#define pin_gate_rswitch     D5
#define pin_led              D8

//ustaienie zegara
unsigned long sensorCo2Status  = 0;
unsigned long sensorTempStatus = 0;
unsigned long kontaktronStatus = 0;

// Connect to the WiFi
const char* ssid        = "UPC5A95ED7";
const char* password    = "fh5rjQksw2Wr";
const char* mqtt_server = "108.59.81.89";

//tematy mqtt
char* MQTT_client       = "climate_log1";
char* temper_topic      = "temperature_out";
char* hum_topic         = "humidity_out";
char* co2_topic         = "co2_out";
char* gateway_rswitch   = "gateway_rswitch";
char* gate_rswitch      = "gate_rswitch";
char* gate_switch       = "gate_switch";
char* gateway_switch    = "gateway_switch";
char* syren_topic       = "ALARM";

WiFiClient espClient;
PubSubClient client(espClient);

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
   client.subscribe(gate_switch);
   client.subscribe(gateway_switch);
   client.subscribe(syren_topic);
 }
}

void publish_data(char* topic, String measure)
{
  client.publish(topic, (char*) measure.c_str());
}

void setup(){
  Serial.begin(9600);
  Serial.setTimeout(2000);
  WiFi.mode(WIFI_STA);
  //ustawienie trybów wyjść
  dht.setup(pin_dht, DHTesp::DHT22); // Connect DHT sensor to GPIO 17
  pinMode(pin_gate,OUTPUT);
  pinMode(pin_syren,OUTPUT);
  pinMode(pin_gateway,OUTPUT);
  pinMode(pin_gateway_rswitch, INPUT_PULLUP);
  pinMode(pin_gate_rswitch, INPUT_PULLUP);
  pinMode(pin_co2,INPUT);                     //MQ135 analog feed set for input

  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  
  digitalWrite(pin_gate, HIGH);
  digitalWrite(pin_gateway, HIGH);
  
  // Wait for serial to initialize.
  
  while(!Serial) { }
}
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.println("topic"+ String(topic));
  String mess;
  for (int i=0;i<length;i++) {
    char receivedChar = (char)payload[i];
    mess+=receivedChar;
    }Serial.println(mess);
  if(String(topic)==gate_switch){
    if (mess=="1"){
    digitalWrite(pin_gate, HIGH);
   }
   else if (mess=="0"){
    digitalWrite(pin_gate, LOW);
   }
  }
  if(String(topic)==gateway_switch){
    if (mess=="1"){
    digitalWrite(pin_gateway, HIGH);
   }
   else if (mess=="0"){
    digitalWrite(pin_gateway, LOW);
   }
  }
  if(String(topic)==syren_topic){
    if (mess=="1"){
    tone(pin_syren, 4300); //Wygeneruj sygnał o częstotliwości 4300Hz na pinie A5  
    delay(150);  
    tone(pin_syren, 3500); //Wygeneruj sygnał o częstotliwości 3500Hz na pinie A5  
    delay(150);
   }
   else if (mess=="0"){
    digitalWrite(pin_syren, LOW);
   }
  }
  tone(D0, 4300); //Wygeneruj sygnał o częstotliwości 4300Hz na pinie A5  
  delay(150);  
  tone(D0, 3500); //Wygeneruj sygnał o częstotliwości 3500Hz na pinie A5  
  delay(150);
   
   
  }
void log_temperature(){

  
  float h = dht.getHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.getTemperature();
  Serial.print("Temperatura:");
  Serial.println(t);
  Serial.print("Wilgotność:");
  Serial.println(h);
  // Check if any reads failed and exit early (to try again).
  if (isnan(t) ) {
    Serial.println("Failed to read from DHT sensor!");
    
    return;
  }



    publish_data(temper_topic, String(t) );
    publish_data(hum_topic, String(h));

  delay(100);
  // wait 100ms for next reading
  
}

void loop(){

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
                     if(millis() - sensorTempStatus > 1000){
                                              log_temperature();
                                              sensorTempStatus=millis();
                                                    
                                             }
                                            
                    if(millis() - sensorCo2Status > 1000){
                                              co2Detect();
                                              sensorCo2Status=millis();
                                                    
                                             }
                                            
                     if(millis() - kontaktronStatus > 1000){
                                              detect_gateway_rswitch();
                                              kontaktronStatus=millis();
                                                    
                                             }                 
    client.loop();                                             
  } 
}












void co2Detect(){
  
  int co2now;                                   //int array for co2 readings
  int co2raw = 0;                               //int for raw value of co2
  int co2ppm = 0;                               //int for calculated ppm
  int zzz = 0;                                  //int for averaging

  if(millis() - sensorCo2Status > 1000){
  co2now=analogRead(A0);
  co2ppm = co2now - co2Zero;      //get calculated ppm
  }
                  
  Serial.print("AirQuality=");
  Serial.print(co2ppm);  // prints the value read
  Serial.println(" PPM");
  publish_data(co2_topic,String(co2ppm));
  delay(50);             

}

void detect_gateway_rswitch(){
  if (digitalRead(pin_gateway_rswitch) == LOW) { //Jeśli czujnik zwarty
    //digitalWrite(pin_gate ,HIGH);
    publish_data(gateway_rswitch,String(1));
    Serial.println("Zamknięte");
  } else {
    publish_data(gateway_rswitch,String(0));
    //digitalWrite(pin_gate ,LOW);
    Serial.println("Otwarte");
  }

  if (digitalRead(pin_gate_rswitch) == LOW) { //Jeśli czujnik zwarty
    //digitalWrite(pin_gate ,HIGH);
    publish_data(gate_rswitch,String(1));
    Serial.println("Zamknięte");
  } else {
    publish_data(gate_rswitch,String(0));
    //digitalWrite(pin_gate ,LOW);
    Serial.println("Otwarte");
  }
}