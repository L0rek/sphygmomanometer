#include "config.h"
#include "veml7700.h"
#include "pressure.h"



Veml7700 veml = Veml7700();
Pressure pres = Pressure(F_READ,ONCLOCK);

volatile bool send = false;
int val = 40555;
volatile unsigned long time = 0;
unsigned long last = 0;

void setup() {
  veml.Init();
  pres.Init();
  pinMode(VALVE, OUTPUT);
  pinMode(MOTOR, PWM);
  pwmWrite(MOTOR, val);
  Timer3.pause();
  Timer3.setCount(0);
  Timer3.setMode(TIMER_CH1, TIMER_OUTPUTCOMPARE);
  Timer3.setPeriod(1000);
  Timer3.setCompare(TIMER_CH1, 1);
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
        Timer3.pause();
        Timer3.setCount(0);
        digitalWrite(VALVE, LOW);
        time = 0;
        last=0;
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
  if (time-last>=DATA_RATE)
  {
    last = time;
    Serial.print(time,DEC);
    Serial.print("\t");
    Timer3.pause();
    double pressure = pres.Get();
    double lux = veml.ReadData(0x04);
    Timer3.resume();
    Serial.print(pressure,4);
    Serial.print("\t");
    Serial.println(lux,4);
    
    
  }

}

void handler_data()
{
  time++;
}
