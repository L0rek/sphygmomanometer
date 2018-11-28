#ifndef VEML7700_H
#define VEML7700_H

#include "wirish.h"
#include <SoftWire.h>

class Veml7700
{
  public:
    Veml7700(uint8_t scl = PB9, uint8_t sda = PB8);
    bool Init();
    double ReadData(uint8_t command);

  private:
    SoftWire *SWire;
    const uint16_t Address = 0x10;
};

#endif
