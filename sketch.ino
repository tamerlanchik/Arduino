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
        
        temp=char( Serial.read() ) ;
        if(temp!='$')
        {
          
          ans=ans*10+int(temp-'0');
        }
        delay(2);
        
      }
    }
    
    lcd.clear();
    lcd.print(long(ans));
    ans=0;
    temp='a';
 

}
