#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);
long long ans=0;
char temp='a';
int t=0;
void setup() {
  lcd.init();
  lcd.backlight();
  Serial.begin(9600);
}

void loop() {
  
    while(temp!='$')
    {
      while (Serial.available()>0)
      {
        lcd.setCursor(0, 1);
        lcd.print("   ");
        lcd.setCursor(0, 1);
        lcd.print(Serial.available());
        delay(100);
        temp=char( Serial.read() ) ;
        if(temp!='$')
        {
          
          ans=ans*10+int(temp-'0');
        }
        delay(3);
        
      }
    }
    
    lcd.clear();
    //lcd.print(char(Serial.read()));
    lcd.print(char(ans));
    ans=0;
    temp='a';

  /*lcd.print(char('a'+'a'));
  delay(1000);*/
 

}
