#include "motor.h"
#include "config.h"

Motor::Motor(uint8_t Pin, volatile unsigned long int *Time, uint32_t Max, uint32_t Min)
{
  pin = Pin;
  step = STEP;
  max = Max;
  min = Min;
  time = Time;
}

void Motor::UpPid(double val)
{
  double error = Function() - val;
  val = Pid(error);
  PWMwrite(val);
}

bool Motor::Init()
{
  pinMode(pin, PWM);
  pwmWrite(pin, 0);
  SetK(KP,KI,KD);
  SetFunction(5000,35000,5000);
  return true;
}

uint32_t Motor::Pid(double e)
{
  double up = 0, ui = 0, ud = 0;
  sum_e += e;

  up = e * kp;
  ui = sum_e * step * ki;
  ud = ((e - last_e) / step) * kd;

  uint32_t val = uint32_t(up + ui + ud);
  last_e = e;
  if (val > max) {
    val = max;
    sum_e -= e;
  } else if (val < min) {
    val = 0;
    sum_e += e;
  }

  return val;
}

void Motor::PWMwrite(uint16_t val)
{
  pwmWrite(MOTOR, val);
}
void Motor::SetK(float Kp, float Ki, float Kd)
{
  kp = Kp;
  ki = Ki;
  kd = Kd;
}
void Motor::Reset()
{
  last_e = 0.0;
  sum_e = 0.0;
}
void Motor::SetFunction(uint32_t T0, uint32_t Ts, uint32_t Tk)
{
  t0 = T0;
  ts = t0 + Ts;
  tk = ts + Tk;

}

double Motor::Function()
{
  if (*time < t0)
    return 0;
  else if (*time < ts)
    return 150/double(ts-t0) * double(*time - t0);
  else if (*time < tk)
    return 150;
  else
    return 0;
}
void Motor::Store()
{
  
}
