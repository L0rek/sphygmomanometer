#include "config.h"
#include "veml7700.h"
#include "pressure.h"



Veml7700 veml = Veml7700();
Pressure pres = Pressure(F_READ,ONCLOCK);

volatile bool send = false;
int val = 40555;
unsigned time = 0;

void setup() {
  veml.Init();
  pres.Init();
  pinMode(VALVE, OUTPUT);
  pinMode(MOTOR, PWM);
  pwmWrite(MOTOR, val);
  Timer3.pause();
  Timer3.setCount(0);
  Timer3.setMode(TIMER_CH1, TIMER_OUTPUTCOMPARE);
  Timer3.setPeriod(DATA_RATE); // in microseconds
  Timer3.setCompare(TIMER_CH1, 1);      // overflow might be small
  Timer3.attachInterrupt(TIMER_CH1, handler_data);


}


void loop() {

  if (Serial.available() > 0)
  {
    switch (Serial.read())
    {
      case 'C':
        digitalWrite(VALVE, HIGH);
        pres.Calibrate();
        Timer3.resume();
        Serial.println("OK");
        break;
      case 'O':
        digitalWrite(VALVE, LOW);
        Timer3.pause();
        Timer3.setCount(0);
        time = 0;
        Serial.println("OK");
        break;
      case 'M':
        //val = 
        pwmWrite(MOTOR, val);
        Serial.println("OK");
        break;
      default:
        break;
    }
  }
  if (send == true)
  {
    time += 50;
    Serial.print(time);
    Serial.print("\t");
    Serial.print(pres.Get());
    Serial.print("\t");
    Serial.println(veml.ReadData(0x04));
    send = false;
  }

}

void handler_data()
{
  send = true;
}
