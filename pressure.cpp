#include "pressure.h"
#include "config.h"

Pressure::Pressure(uint8_t Signal_Pin, uint8_t Enable_Pin)
{
  s_pin = Signal_Pin;
  e_pin = Enable_Pin;
  counter = 0;
}
bool Pressure::Init()
{
  pinMode(s_pin, INPUT);
  pinMode(e_pin, OUTPUT);
  digitalWrite(e_pin, HIGH);
  attachInterrupt(s_pin, handler, RISING);
  Timer2.pause();
  Timer2.setPrescaleFactor(SOFT_PRESCALE);
  Timer2.refresh();
  Timer2.resume();

}
void Pressure::Calibrate()
{
  first = 0;
  for (int i = 0; i < 100; i++)
    first += ReadFrequency();
  first /= 100;

}
double Pressure::ReadFrequency()
{
  digitalWrite(e_pin, LOW);
  counter = 0;
  while (counter < N_MEAN) {}
  double time = Timer2.getCount();
  digitalWrite(e_pin, HIGH);

  return (72000 / SOFT_PRESCALE / time) * (HARD_PRESCALE * counter) ;
}
double Pressure::Get()
{
  return (first - ReadFrequency()*CALIBRATE);
}
volatile uint16_t Pressure::counter = 0;

