#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <SoftwareSerial.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

// RX, TX
SoftwareSerial espSerial(10, 11);

String bulbStatus = "OFF";
String fanStatus = "OFF";

void updateLCD()
{
  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("Bulb:");
  lcd.print(bulbStatus);

  lcd.setCursor(0, 1);
  lcd.print("Fan :");
  lcd.print(fanStatus);
}

void setup()
{
  lcd.init();
  lcd.backlight();

  espSerial.begin(9600);

  lcd.setCursor(0,0);
  lcd.print("Home Automation");

  lcd.setCursor(0,1);
  lcd.print("Starting...");

  delay(2000);

  updateLCD();
}

void loop()
{
  if(espSerial.available())
  {
    String data = espSerial.readStringUntil('\n');
    data.trim();

    // Example:
    // B:ON,F:OFF

    int bIndex = data.indexOf("B:");
    int fIndex = data.indexOf("F:");

    if(bIndex >= 0)
    {
      bulbStatus = data.substring(bIndex + 2, data.indexOf(",", bIndex));
    }

    if(fIndex >= 0)
    {
      fanStatus = data.substring(fIndex + 2);
    }

    updateLCD();
  }
}