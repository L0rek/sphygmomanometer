#ifndef MOTOR_H
#define MOTOR_H

#include "wirish.h"

class Motor
{
  public:
    Motor(uint8_t pin, volatile unsigned long int *time, uint32_t max_value = 65535, uint32_t min_value = 10000);
    bool Init();
    void UpPid(double val);
    uint32_t Pid(double error);
    void PWMwrite(uint16_t val);
    void SetK(float Kp, float Ki, float Kd);
    void Reset();
    void SetFunction(uint32_t t0,uint32_t ts,uint32_t tk);
    double Function();
    void Store();
  private:
    uint8_t pin;
    uint32_t max;
    uint32_t min;
    uint32_t t0;
    uint32_t ts;
    uint32_t tk;
    volatile unsigned long *time;
    double last_e = 0.0;
    double sum_e = 0.0;
    float kp;
    float ki;
    float kd;
    float step;

};




#endif
