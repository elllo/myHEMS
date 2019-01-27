// Jolt! / myHEMS
// Microcontroller ESP8266, two BME280 sensors, publish on MQTT protocol
// placement: bathroom

// This is the code for an ESP8266 board that connects two BME280 sensors via SPI.
// The measurements of both sensors for temperature, humidity and air pressure are published 
// to the MQTT broker on maxPi.
// The WiFi connection is established automatically using the WiFiManager. It tries the last
// known WiFi credentials. If there is no known Wifi available it establish a Wifi network which
// can be used for setting up the Wifi connection.

//----------Header------------

// libraries
#include <ESP8266WebServer.h>
#include <DNSServer.h>
#include <WiFiManager.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

// constants
unsigned long delayTime = 10000;
const char* MQTT_BROKER = "192.168.178.64";
//#define SEALEVELPRESSURE_HPA (998.3)

// assign the ESP8266 pins to arduino pins
#define D1 5
#define D2 4
#define D3 0
#define D4 2
#define D5 14

// assign the SPI bus to pins
#define BME_SCK D1
#define BME_MISO D5
#define BME_MOSI D2
#define BME1_CS D3
#define BME2_CS D4

//initialize bme280 sensors
Adafruit_BME280 bme1(BME1_CS, BME_MOSI, BME_MISO, BME_SCK);
Adafruit_BME280 bme2(BME2_CS, BME_MOSI, BME_MISO, BME_SCK);

//initialize Wifi / MQTT clients
WiFiClient espClient;
PubSubClient client(espClient);



//----------Body------------

void setup() {
// startup Wifi
    Serial.begin(115200);
//    setup_wifi();
    WiFiManager wifiManager;
    wifiManager.autoConnect("AutoConnectAP");
    Serial.println("Wifi connection established... yeah! :)");

// startup MQTT connection
    client.setServer(MQTT_BROKER, 1883);

    bool status;
    
// startup and test sensors
    status = bme1.begin();
    if (!status) {
        Serial.println("Could not find a valid BME280 sensor 1, check wiring!");
    }

    status = bme2.begin();
    if (!status) {
        Serial.println("Could not find a valid BME280 sensor 2, check wiring!");
    }
}

// Reconnect to MQTT broker
void reconnect() {
    while (!client.connected()) {
        Serial.print("Reconnecting...");
        if (!client.connect("ESP8266Client")) {
            Serial.print("failed, rc=");
            Serial.print(client.state());
            Serial.println(" retrying in 5 seconds");
            delay(5000);
        }
    }
}

// This is only needed for testing purposes
void printValues() {

// Sensor 1 measurements
    Serial.println("---Air sensor---");

    Serial.print("Temperature = ");
    Serial.print(bme1.readTemperature());
    Serial.println(" °C");

    Serial.print("Pressure = ");
    Serial.print(bme1.readPressure() / 100.0F);
    Serial.println(" hPa");

//    Serial.print("Approx. Altitude = ");
//    Serial.print(bme.readAltitude(SEALEVELPRESSURE_HPA));
//    Serial.println(" m");

    Serial.print("Humidity = ");
    Serial.print(bme1.readHumidity());
    Serial.println(" %");

    Serial.println();

// Sensor 2 measurements
    Serial.println("---Radiator sensor---");
    Serial.print("Temperature = ");
    Serial.print(bme2.readTemperature());
    Serial.println(" °C");

    Serial.print("Pressure = ");
    Serial.print(bme2.readPressure() / 100.0F);
    Serial.println(" hPa");

//    Serial.print("Approx. Altitude = ");
//    Serial.print(bme.readAltitude(SEALEVELPRESSURE_HPA));
//    Serial.println(" m");

    Serial.print("Humidity = ");
    Serial.print(bme2.readHumidity());
    Serial.println(" %");

    Serial.println();
}

void sendReadingsMQTT() {

    char* msgTemp1;
    char* msgHumid1;
    char* msgAirP1;

    float temp1 = bme1.readTemperature();   
    float humid1 = bme1.readHumidity();
    float airpres1 = (bme1.readPressure() / 100.0F);

    char bufferT[8];
    msgTemp1 = dtostrf(temp1, 3, 1, bufferT);
    char bufferH[8];
    msgHumid1 = dtostrf(humid1, 3, 1, bufferH);
    char bufferA[8];
    msgAirP1 = dtostrf(airpres1, 3, 1, bufferA);

    client.publish("/sensors/bathroom/bme280-1/temperature", msgTemp1);
    client.publish("/sensors/bathroom/bme280-1/humidity", msgHumid1);
    client.publish("/sensors/bathroom/bme280-1/airpressure", msgAirP1);
    printValues();

    char* msgTemp2;
    char* msgHumid2;
    char* msgAirP2;

    float temp2 = bme2.readTemperature();   
    float humid2 = bme2.readHumidity();
    float airpres2 = (bme2.readPressure() / 100.0F);

    msgTemp2 = dtostrf(temp2, 3, 1, bufferT);
    msgHumid2 = dtostrf(humid2, 3, 1, bufferH);
    msgAirP2 = dtostrf(airpres2, 3, 1, bufferA);

    client.publish("/sensors/bathroom/bme280-2/temperature", msgTemp2);
    client.publish("/sensors/bathroom/bme280-2/humidity", msgHumid2);
    client.publish("/sensors/bathroom/bme280-2/airpressure", msgAirP2);
    printValues();
    
}

void loop() { 
    printValues();
    if (!client.connected()) {
        reconnect();
    }
    client.loop();
    sendReadingsMQTT();

    delay(delayTime);
}
