/*
 * 
 *    Co2 -  A0-+--------------+-D0  - Temp i Hum
 *              |              |-D1  - Kontaktron furtka
 *              |              |-D2  - przekaznik furtka
 *              |              |-D3  - syrena
 *              |    NODEMCU   |-D4  - przekaznik brama
 *              |              |-D5  - kontaktron brama
 *              |              |-D6  -
 *              |              |-D7  -
 *              +--------------+-D8  - LED
 *            
 * 
 */
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

unsigned long waitCount = 0;                 // counter
uint8_t conn_stat = 0;                       // Connection status for WiFi and MQTT:
                                             
 /*                                           
                                              status |   WiFi   |    MQTT
                                              -------+----------+------------
                                                   0 |   down   |    down
                                                   1 | starting |    down
                                                   2 |    up    |    down
                                                   3 |    up    |  starting
                                                   4 |    up    | finalising
                                                   5 |    up    |     up


*/

// Connect to the WiFi
const char* ssid        = "UPC5A95ED7";
const char* password    = "fh5rjQksw2Wr";
const char* mqtt_server = "108.59.81.89";
#define PIN_led            D4
#define NUMPIXELS          16
//tematy mqtt
char* MQTT_client       = "climate_log1";
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN_led, NEO_GRB + NEO_KHZ800);
WiFiClient espClient;
PubSubClient client(espClient);

int n_r = 255;
int n_g = 255;
int n_b = 255;
int n_i = 122;

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
   client.subscribe("Blind_switch");
   client.subscribe("r");
   client.subscribe("g");
   client.subscribe("b");
   client.subscribe("i");
 }
}

void publish_data(char* topic, String measure)
{
  client.publish(topic, (char*) measure.c_str());
}


void setup() {
  Serial.begin(9600);
  Serial.setTimeout(2000);
  WiFi.mode(WIFI_STA);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  pinMode(D0,OUTPUT);
  pinMode(D1,OUTPUT);
  pinMode(PIN_led,OUTPUT);
  digitalWrite(D1, HIGH);
  digitalWrite(D0, HIGH);

  #if defined (__AVR_ATtiny85__)
  if (F_CPU == 16000000) clock_prescale_set(clock_div_1);
  #endif
  // End of trinket special code

  pixels.begin(); // This initializes the NeoPixel library.
  
  while(!Serial) { }
}

int flag=0;
int flag2=0;
void callback(char* topic, byte* payload, unsigned int length) {
  
  Serial.println("topic"+ String(topic));
  String mess;
  for (int i=0;i<length;i++) {
    char receivedChar = (char)payload[i];
    mess+=receivedChar;
    
    
  if((String(topic)=="Blind_switch")&&flag2==0){
    
    if (mess=="1"){
    digitalWrite(D1, HIGH);
    digitalWrite(D0, LOW);
    flag=1;
   }
   else if (mess=="2"){
    digitalWrite(D0, HIGH);
    digitalWrite(D1, LOW);
    flag=0;
   }
   else if (mess=="0"){
    digitalWrite(D0, HIGH);
    digitalWrite(D1, HIGH);
   }
   
  }
  
//  if ((String(topic)=="test_switch2")&&flag==0){
//    if (mess=="1"){
//    digitalWrite(D0, HIGH);
//    digitalWrite(D1, LOW);
//    
//    flag2=1;
//   }
//   else{
//    digitalWrite(D1, HIGH);
//    flag2=0;
//   }
//  }
  
  
   
   }
   int number;
   Serial.println(mess);
  number=mess.toInt();
  if(String(topic) == "r"){
    n_r =number;
  }
  if(String(topic) == "g"){
    n_g =number;
  }
  if(String(topic) == "b"){
    n_b = number;
  }
  if(String(topic) == "i"){
    n_i = number;
  }

  pixels.setBrightness(n_i);
  for (int i = 0; i <= NUMPIXELS; i++){
    // Fix note: r swipped with g. This is grb diode.
    pixels.setPixelColor(i, pixels.Color(n_g, n_r, n_b)); // Moderately bright green color.
    pixels.show(); // This sends the updated pixel color to the hardware.
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
  client.loop();
//  analogWriteRange(1023);
//  analogWriteFreq(1000);//Padrão é 1Khz
// analogWrite(D2,0);
// delay(500);
// analogWrite(D2,100);
// delay(500);
// analogWrite(D2,300);
// delay(500);
// analogWrite(D2,500);
// delay(500);
// analogWrite(D2,700);
// delay(500);
// analogWrite(D2,900);
// delay(500);
// analogWrite(D2,1023);
// delay(1500);
// 
//
// analogWriteRange(2047);
//
//  analogWrite(D2,1023);
// delay(1000);
//
// analogWrite(D2,2047);
// delay(1000);
//
// analogWriteFreq(2000);//Padrão é 1Khz
//
//   analogWrite(D2,1023);
// delay(1000);
//
// analogWrite(D2,2047);
// delay(1000);
    pixels.setBrightness(n_i);
//    for (int i = 0; i <= NUMPIXELS; i++){
//      pixels.setPixelColor(i, pixels.Color(n_r, n_g, n_b)); // Moderately bright green color.
//      pixels.show(); // This sends the updated pixel color to the hardware.
// }
}
}