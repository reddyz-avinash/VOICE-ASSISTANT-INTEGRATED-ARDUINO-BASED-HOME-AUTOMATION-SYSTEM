#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "Your Wifi Name";
const char* password = "Your Wifi password";

WebServer server(80);

#define RELAY1 26
#define RELAY2 27

bool bulb = false;
bool fan = false;

HardwareSerial ArduinoSerial(2);

void sendStatus()
{
  ArduinoSerial.print("B:");
  ArduinoSerial.print(bulb ? "ON" : "OFF");
  ArduinoSerial.print(",F:");
  ArduinoSerial.println(fan ? "ON" : "OFF");
}

String webpage()
{
  String page="";

  page+="<html>";
  page+="<head>";
  page+="<title>Home Automation</title>";
  page+="<style>";
  page+="body{font-family:Arial;text-align:center;background:#f2f2f2;}";
  page+="button{width:180px;height:50px;font-size:20px;margin:10px;}";
  page+="</style>";
  page+="</head>";

  page+="<body>";

  page+="<h1>HOME AUTOMATION</h1>";

  page+="<h2>Bulb : ";
  page+=bulb?"ON":"OFF";
  page+="</h2>";

  page+="<a href='/bulbon'><button>Bulb ON</button></a>";
  page+="<a href='/bulboff'><button>Bulb OFF</button></a>";

  page+="<br><br>";

  page+="<h2>Fan : ";
  page+=fan?"ON":"OFF";
  page+="</h2>";

  page+="<a href='/fanon'><button>Fan ON</button></a>";
  page+="<a href='/fanoff'><button>Fan OFF</button></a>";

  page+="</body></html>";

  return page;
}

void home()
{
  server.send(200,"text/html",webpage());
}

void bulbOn()
{
  digitalWrite(RELAY1,LOW);
  bulb=true;
  sendStatus();
  home();
}

void bulbOff()
{
  digitalWrite(RELAY1,HIGH);
  bulb=false;
  sendStatus();
  home();
}

void fanOn()
{
  digitalWrite(RELAY2,LOW);
  fan=true;
  sendStatus();
  home();
}

void fanOff()
{
  digitalWrite(RELAY2,HIGH);
  fan=false;
  sendStatus();
  home();
}

void setup()
{
  Serial.begin(115200);

  ArduinoSerial.begin(9600,SERIAL_8N1,16,17);

  pinMode(RELAY1,OUTPUT);
  pinMode(RELAY2,OUTPUT);

  digitalWrite(RELAY1,HIGH);
  digitalWrite(RELAY2,HIGH);

  WiFi.begin(ssid,password);

  while(WiFi.status()!=WL_CONNECTED)
  {
    delay(500);
  }

  Serial.println(WiFi.localIP());

  server.on("/",home);

  server.on("/bulbon",bulbOn);
  server.on("/bulboff",bulbOff);

  server.on("/fanon",fanOn);
  server.on("/fanoff",fanOff);

  server.begin();

  sendStatus();
}

void loop()
{
  server.handleClient();

  if(Serial.available())
  {
    String cmd=Serial.readStringUntil('\n');
    cmd.trim();

    if(cmd=="BULB_ON")
    {
      bulbOn();
    }

    else if(cmd=="BULB_OFF")
    {
      bulbOff();
    }

    else if(cmd=="FAN_ON")
    {
      fanOn();
    }

    else if(cmd=="FAN_OFF")
    {
      fanOff();
    }
  }
}