
#include <LiquidCrystal_I2C.h>
#include <Wire.h>
#include <math.h>

int Vo;
float R1 = 10000;
float logR2, R2, T, Tc1, Tc2, Tc3, Tc4, Tc5, Tc6, Tf;
float c1 = 1.009249522e-03, c2 = 2.378405444e-04, c3 = 2.019202697e-07;

LiquidCrystal_I2C lcd(0x27, 20, 4);

byte customChar[] = {
  B00100,
  B01010,
  B01010,
  B01010,
  B01010,
  B10001,
  B10001,
  B01110
};

void setup() {
  lcd.init();
  lcd.createChar(0, customChar);
  //lcd.createChar(1, customChar);
  lcd.home();
  
  lcd.backlight();
 
  Serial.begin(9600);
}

void loop() {
  
  Vo = analogRead(A0);
  R2 = R1 * (1023.0 / (float)Vo - 1.0);
  logR2 = log(R2);
  T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2));
  Tc1 = T - 273.15;
  Tf = (Tc1 * 9.0)/ 5.0 + 32.0; 
  lcd.setCursor(0,0);
  lcd.write(0);
  lcd.print("1:");
  
  lcd.print(Tc1);
  lcd.print(" ");
    
  Serial.println(Tc1);
 
  delay(1000);
}
