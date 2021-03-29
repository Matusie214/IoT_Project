/*
 * 
 *    Co2 -  A0-|--------------|D0  - Temperatura i wilgotność
 *              |              |D1  - PIR salon
 *              |              |D2  - LED
 *              |              |D3  - przekaźnik okno
 *              |    NODEMCU   |D4  - przekaźnik ogrzewanie
 *              |              |D5  - SCK  Pamięć
 *              |              |D6  - MISO Pamięć
 *              |              |D7  - MOSI Pamięć
 *              |______________|D8  - Pamięć
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
#define pin_co2           A0                        //analog feed from MQ135
#define co2Zero           55                        //calibrated CO2 0 level
#define pin_dht           D0
#define pin_pir           D1
#define pin_LED           D2
#define pin_switch_window D3
#define pin_switch_heat   D4



//ustaienie zegara
unsigned long sensorCo2Status  = 0;
unsigned long sensorPirStatus  = 0;
unsigned long sensorTempStatus = 0;



volatile long temper      = 0;
volatile long lastTemper  = 0;
volatile long hum         = 0;
volatile long lastHum     = 0;
volatile long co2         = 0;
volatile long lastCo2     = 0;
volatile int lastPirState = LOW;
volatile int pirState     = LOW; 
 

// Connect to the WiFi
const char* ssid        = "UPC5A95ED7";
const char* password    = "fh5rjQksw2Wr";
const char* mqtt_server = "34.123.208.229";

//tematy czujników
char* MQTT_client       = "ESP8266_home";
char* temper_topic      = "temperature_in";
char* hum_topic         = "humidity_in";
char* co2_topic         = "co2_in";
char* pir_topic         = "pir_salon";

// tematy aktorów
char* LED_topic         = "led_salon";
char* heating_switch    = "heating_switch";
char* window_switch     = "window_switch";



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
    client.subscribe("heating_switch");
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
  
  dht.setup(pin_dht, DHTesp::DHT22);           // Connect DHT sensor to GPIO 17
  pinMode(pin_pir, INPUT);
  pinMode(pin_co2,INPUT);                     //MQ135 analog feed set for input
  pinMode(pin_LED,OUTPUT);
  pinMode(pin_switch_heat,OUTPUT);
  pinMode(pin_switch_window,OUTPUT);
  
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  
  digitalWrite(pin_LED, LOW);
  // Wait for serial to initialize.
  
  while(!Serial) { }
}
void callback(char* topic, byte* payload, unsigned int length) {
 
  String mess;
  for (int i=0;i<length;i++) {
    char receivedChar = (char)payload[i];
    mess+=receivedChar;
  //  Serial.println(mess);
   if (mess=="1"){
    digitalWrite(pin_LED, HIGH);
   }
   else{
    digitalWrite(pin_LED, LOW);
   }
  }
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
 
      log_temperature();
      log_hum();
      co2Detect();
      notify_pir_salon();
      client.loop();                                             
  } 
}








/*
 * Metoda obsługująca przesyłanie informacji o stanie czujnika pir w salonie
 * Podczas pracy za pomocą wykrywania brzegowego NodeMcu wysyła wiadomość do brokera o stanie czujnika.
 */
void notify_pir_salon(){
  
  pirState = digitalRead(pin_pir);// read input value
  
  if (pirState != lastPirState){            
    
      if(pirState==LOW){
        publish_data(pir_topic, String("1"));
        Serial.println("Pir Status : movement");
      }
      else{
        publish_data(pir_topic, String("0"));
        Serial.println("Pir Status : no movement");
      }
          
      delay(50);
   
  }
  lastPirState=pirState;
  
}





/*
 * Metoda obsługująca pracę czujnika czystosci powietrza
 * 
 * Zwraca liczbę która jest masą powietrza. W zależności od tej masy można określić czystość powietrza otoczenia
 */
void co2Detect(){
  co2=analogRead(A0);
  int co2now;                                   //int array for co2 readings
  int co2raw = 0;                               //int for raw value of co2
  int co2ppm = 0;                               //int for calculated ppm
  int zzz    = 0;                               //int for averaging

  if(co2!= lastCo2){
    
    co2now=analogRead(A0);
    co2ppm = co2now - co2Zero;      //get calculated ppm
    Serial.print("AirQuality=");
    Serial.print(co2ppm);  // prints the value read
    Serial.println(" PPM");
    publish_data(co2_topic,String(co2ppm));
  }
  delay(50);             
  lastCo2=co2;
}





/*
 * Metoda zajmująca sie powiadamianiem o wartościach odczytu z czujnika DHT22. Publikuje wiadomości zawierające odczyt temperatury i wilgotności
 */
void log_temperature(){
  temper =dht.getTemperature();
  if (isnan(temper) ) {
    Serial.println("Failed to read from DHT sensor!");
    
    return;
  }

  if(temper!=lastTemper){
    Serial.print("Temperature:");
    Serial.println(temper);
    publish_data(temper_topic, String(temper) );
  }
  lastTemper=temper;
   

  delay(50);
  // wait 100ms for next reading
  
}

void log_hum(){
  hum=dht.getHumidity();
  if (isnan(hum) ) {
    Serial.println("Failed to read from DHT sensor!");//Check if any reads failed and exit early (to try again).
    
    return;
  }
  if(hum!=lastHum){
  Serial.print("Humidity:");
  Serial.println(hum);
  publish_data(hum_topic, String(hum));
  }
  
  lastHum=hum;
   
}

  