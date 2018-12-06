#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
 
const char* SSID = "***";
const char* PSK = "***";
const char* MQTT_BROKER = "***";

#define DHTPIN D4 //DHT-Pin
#define DHTTYPE DHT22 //DHT 22 (AM2302)

 
WiFiClient espClient;
PubSubClient client(espClient);
DHT dht(DHTPIN, DHTTYPE);
long lastMsg = 0;
char msg[50];
char msgT[50];
int value = 0;

void sendSensor(){
  float h = dht.readHumidity();
  float t = dht.readTemperature(); // or dht.readTemperature(true) for Fahrenheit
  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  Serial.println(h);
  Serial.println(t);

}


void setup() {
    Serial.begin(115200);
    setup_wifi();
    client.setServer(MQTT_BROKER, 1883);
}
 
void setup_wifi() {
    delay(10);
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(SSID);
 
    WiFi.begin(SSID, PSK);
 
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
 
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
}
 
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
void loop() {
 
    if (!client.connected()) {
        reconnect();
    }
    client.loop();
 
    snprintf (msg, 50, "Alive since %ld milliseconds", millis());
    Serial.print("Publish message: ");
    Serial.println(msg);
    client.publish("/home/data", msg);
    
    sendSensor();
    
    float tPub = dht.readTemperature();
    snprintf (msgT, 50, "Temperature is at %.1f", tPub);
    Serial.println(msgT);
    client.publish("/home/data", msgT);
    
    delay(5000);
}
