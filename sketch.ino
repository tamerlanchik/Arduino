#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);
void refresh(LiquidCrystal_I2C lcd, unsigned int startS, unsigned int startL, unsigned int count)
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
  //lcd.print("R:  1:  2:");
}
void serialEvent()
{
  unsigned int port=readSerial();
  unsigned int val=readSerial();
  lcd.clear();
  lcd.print(port);
  lcd.print(" ");
  lcd.print(val);
}
int readSerial()
{
  char temp='l';
  int val=0;
  
        if (Serial.available()>0)
        {        
            temp=char( Serial.read() ) ;
            val=int(temp);
            /*if(temp!=stopper)
            {
              if (temp>='0' && temp<='9')
              {
                val=val*10+int(temp-'0');
                //delay(2);
              }      
              val=int(temp);    
            }          
            else
              return (val);*/
         }
                              
       
       return (val);
    
  
  
  
}
void loop() {
    
}
