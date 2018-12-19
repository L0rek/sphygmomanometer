#include "config.h"
#include "veml7700.h"
#include "pressure.h"
#include "motor.h"

volatile bool send = false;
volatile unsigned long time = 0;
unsigned long last = 0;

Veml7700 veml = Veml7700(SCL, SDA);
Pressure pres = Pressure(F_READ, ONCLOCK);
Motor motor = Motor(MOTOR, &time);

void Menu()
{
  Serial.println("OK");
  bool on = true;

  while (on)
  {
    if (Serial.available() > 0)
    {
      char buff[5] = {0};
      char par1[10] = {0}, par2[10] = {0}, par3[10] = {0};
      Serial.readBytesUntil(' ', buff, 5);
      Serial.readBytesUntil(' ', par1, 10);
      Serial.readBytesUntil(' ', par2, 10);
      Serial.readBytesUntil('\n', par3, 10);
      switch (buff[0])
      {
        case 'P':
          if (par3[0] != 0)
          {
            motor.SetK(atof(par1), atof(par2), atof(par3));
            Serial.println("OK");
          }
          else
            Serial.println("Error");
          break;
        case 'V':
          if (par2[0] != 0)
          {
            Serial.print("Gain = ");
            Serial.print(par1);
            Serial.print(" integration time = ");
            Serial.println(par2);
            Serial.println("OK");

          }
          else
            Serial.println("Error");
          break;
        case 'F':
          if (par3[0] != 0)
          {
            motor.SetFunction(atoi(par1), atoi(par2), atoi(par3));
            Serial.println("OK");
          }
          else
            Serial.println("Error");
          break;
        case 'S':
          Serial.println("OK");
          break;
        case 'Q':
          on = false;
          Serial.println("exit");
          break;
        default:
          break;
      }
    }
  }
}



void setup() {
  veml.Init();
  pres.Init();
  motor.Init();
  Serial.setTimeout(10);
  pinMode(VALVE, OUTPUT);


}


void loop() {

  if (Serial.available() > 0)
  {
    switch (Serial.read())
    {
      case 'C':
        digitalWrite(VALVE, HIGH);
        send=true;
        pres.Calibrate();
        Serial.println("OK");
        last = micros();
        break;
      case 'O':
        digitalWrite(VALVE, LOW);
        send=false;
        motor.PWMwrite(0);
        time =0;
        Serial.println("OK");
        break;
      case 'M':
        Menu();
        break;
      default:
        break;
    }
  }
  if (( micros()-last >= DATA_RATE*1000) && send)
  {
    
    Serial.print((time+=(micros()-last)/1000)-DATA_RATE, DEC);
    last = micros();
    Serial.print("\t");
    double pressure = pres.Get();
    double lux = veml.ReadData(0x04);
    motor.UpPid(pressure);
    Serial.print(pressure, 1);
    Serial.print("\t");
    Serial.println(lux, 4);



  }

}
