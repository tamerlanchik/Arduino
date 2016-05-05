#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);
void refresh(LiquidCrystal_I2C lcd, int startS, int startL, int count)
{
  lcd.setCursor(startS, startL);
  for (int i=0; i<count; i++)
    lcd.print(" ");
  lcd.setCursor(startS, startL);
}
int t=0;
const char stoppers[2]={'%', '$'};
void setup() {
  lcd.init();
  lcd.backlight();
  Serial.begin(9600);
  lcd.print("R: P1:  P2:")
}
int readSerial(char stopper)
{
  int val=0;
  char temp='j';
  while (1)
  {
    if (Serial.available()>0)
    {        
        temp=char( Serial.read() ) ;
        if(temp!=stopper)
        {
          if (temp>='0' && temp<='9')
          {
            val=val*10+int(temp-'0');
            delay(2);
          }          
        }          
        else 
          return (val);                
    }
  }
}
void loop() {
    t=readSerial('$');
    refresh(lcd, 0, 0, 3);
    lcd.print(t);
}
