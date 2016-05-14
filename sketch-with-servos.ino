#include <Servo.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

int lastValues[3]={90, 90, 90};
const char stoppers[2]={'%', '$'};
const int countServos=3;
const char powerKey=7;

Servo servoMap[countServos];
const char servoPin[3]={9, 10, 11};
const int minValueServo[3]={0, 10, 20};
const int maxValueServo[3]={180, 165, 165}; 

void setup() {
  pinMode(powerKey, OUTPUT);
  digitalWrite(powerKey, HIGH);
  
  lcd.init();
  lcd.backlight();

  for(int i=0; i<countServos; i++)
    servoMap[i].attach(servoPin[i]);
    
  Serial.begin(9600);
  
  lcd.print("1:  2:  R:");
  lcd.setCursor(0, 1);
  lcd.print("90  90  90");
  
}
void updateServosPosition(float [3]);

void serialEvent()
{
  int angles[countServos];
  angles[0]=readSerial('%');
  angles[1]=readSerial('&');
  angles[2]=readSerial('$');
  


    
    

    lcd.setCursor(0, 1);
    lcd.print(F("              "));
    
    for(int i=0; i<countServos; i++)
    {
      if (angles[i]>180)
        angles[i]=lastValues[i];

      lastValues[i]=angles[i];
      angles[i]=constrain(angles[i], minValueServo[i], maxValueServo[i]);

      lcd.setCursor(i*4, 1);
      lcd.print(angles[i]);

    }
      
    updateServosPosition(angles);
  
    
}
int readSerial(char stopper)
{
  unsigned char temp='l';
  float val=0;
  while(1)
    {
        if (Serial.available())
        {        
              temp=char( Serial.read() ) ;
              if(temp!=stopper)
              {
                if (temp>='0' && temp<='9')
                {
                  val=val*10+int(temp-'0');
                }
              }
              else return (val);
        }
     } 
}

void updateServosPosition(int angles[])
{
  for(int i=0; i<countServos; i++)
    servoMap[i].write(angles[i]);  
}

void loop() {
    
}
