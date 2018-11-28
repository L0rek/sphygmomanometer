#ifndef PRESSURE_H
#define PRESSURE_H

#include "wirish.h"

class Pressure
{
  public:
    Pressure(uint8_t Signal_Pin, uint8_t Enable_Pin);
    bool Init();
    void Calibrate();
    double ReadFrequency();
    double Get();

  private:
    static void handler() {if ( counter == 0) Timer2.setCount(0); counter++;}
    static volatile uint16_t counter;
    uint8_t s_pin;
    uint8_t e_pin;
    double first = 0;
};

#endif
