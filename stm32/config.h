//General config
#define ONCLOCK PB3
#define F_READ PB4
#define VALVE PB5
#define MOTOR PB6
#define SDA PB8
#define SCL PB9
#define DATA_RATE 25 // in ms



//VEML7700 config
     //ALS Configuration Register
#define ALS_GAIN 0b01   //Gain selection; 00 = gain x1; 01 = gain x2; 10 = gain x(1/8); 11 = gain x(1/4);
#define ALS_IT 0b1100   //ALS integration time setting; 1100 = 25ms; 1000 = 50ms; 0000 = 100ms; 0001 = 200ms; 0010 = 400ms; 0011 = 800ms;
#define ALS_PERS 0b00   //ALS persistence protect number setting; 00 = 1; 01 = 2; 10 = 4; 11 = 8;
#define ALS_INT_EN 0b0  //ALS interrupt enable setting; 0 = disable; 1 = enable;
#define ALS_SD 0b0      //ALS shut down setting; 0 = power on; 1 = shut down;

  //Power Saving Mode
#define PSM 0b00 //refresh time; 00 = mode1; 01 = mode2; 10 = mode3; 11 = mode4;
#define PSM_EN 0b0 //power saving; 0 disabe; 1 enable;

  // High Threshold Windows Setting
#define ALS_WH 0xff00 //??

  // Low Threshold Windows Setting
#define ALS_WL 0x00ff //??


//Pressure config
#define N_MEAN 1000
#define SOFT_PRESCALE 16
#define HARD_PRESCALE 4
#define CALIBRATE 2.26

//PID
#define KP 60000
#define KI 0
#define KD 0
#define STEP 0.025
