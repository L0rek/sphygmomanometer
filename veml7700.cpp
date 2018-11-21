#include "veml7700.h"
#include "config.h"

Veml7700::Veml7700(uint8_t scl, uint8_t sda)
{
  SWire = new SoftWire(PB9, PB8, SOFT_FAST);
  SWire->begin();
}
bool Veml7700::Init()
{

  const uint16_t  register_cache[4] =
  { (uint16_t(ALS_GAIN) << 11) | (uint16_t(ALS_IT) << 6) | (uint16_t(ALS_PERS) << 4) | (uint16_t(ALS_INT_EN) << 1) | (uint16_t(ALS_SD)),
    ALS_WH,
    ALS_WL,
    (uint16_t(PSM) << 1) | (uint16_t(PSM_EN))
  };
  byte error = 0 ;
  for (uint8_t i = 0; i < 4; i++)
  {
    SWire->beginTransmission(Address);
    SWire->write(i);
    SWire->write(uint8_t(register_cache[i] & 0xff));
    SWire->write(uint8_t(register_cache[i] >> 8));
    if (error = SWire->endTransmission())
    {
      return false;
    }
  }
  delay(3);
  return true;
}
uint16_t Veml7700::ReadData(uint8_t command)
{
  SWire->beginTransmission(Address);
  SWire->write(command);
  byte error = 0 ;
  if (error = SWire->endTransmission(false))  // NB: don't send stop here
  {
    Serial.print("recive_data error ");
    Serial.println(error);
  }
  if (error = SWire->requestFrom(Address, 2) != 2)
  {
    Serial.print("requestFrom error ");
    Serial.println(error);
  }
  uint16_t data = SWire->read();
  data |= uint16_t(SWire->read()) << 8;
  return data;
}
