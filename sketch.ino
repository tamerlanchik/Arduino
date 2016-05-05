#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <String.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);
int sender=0;
int val=0;
char temp='a';
int t=0;
void setup() {
  lcd.init();
  lcd.backlight();
  Serial.begin(9600);
}

void loop() {
  
    while(temp!='%')
    {
      while (Serial.available()>0)
      {        
        temp=char( Serial.read() ) ;
        if(temp!='%')
          sender=sender*10+int(temp-'0');
        else break;
        delay(2);        
      }
    }
    lcd.clear();
    lcd.print("sender done");

    while(temp!='$')
    {
      while (Serial.available()>0)
      {        
        temp=char( Serial.read() ) ;
        if(temp!='$')
          val=val*10+int(temp-'0');
        else break;
        delay(2);        
      }
    }
    
    lcd.clear();
    lcd.print(sender);
    lcd.print(" ");
    lcd.print(val);
    sender=0;
    val=0;
    temp='a';

  /*lcd.print(char('a'+'a'));
  delay(1000);*/
 

}
