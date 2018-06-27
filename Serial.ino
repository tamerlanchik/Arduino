unsigned int lenght = 0, temp = 0;
  if(Serial.available()){
    do{
      delayMicroseconds(80);    //для скорости 115200 бод
      lenght = temp;
      temp = Serial.available();
    }while(temp-lenght > 0);    //ждем, пока не перестанут приходить байты либо не кончится буфер (63 байт)
    t = new char[lenght];
    for(int i=0; i<lenght; i++){
      t[i] = Serial.read();
    }
    //handling the data
    delete [] t;
