#include "motor.h"
#include "blue_control.h"
#include<unistd.h>
blue::Motor motor;

namespace blue{
void forward(float voltage,int time){
    motor.rotate("drv1","forward",voltage);
    motor.rotate("drv2","forward",voltage);
    sleep(time);
    motor.rotate("drv1","neutral",voltage);
    motor.rotate("drv1","neutral",voltage);

}
void backward(float voltage,int time){
    motor.rotate("drv1","backward",voltage);
    motor.rotate("drv2","backward",voltage);
    sleep(time);
    motor.rotate("drv1","neutral",voltage);
    motor.rotate("drv1","neutral",voltage);

}

void right(float voltage,int time){
    motor.rotate("drv1","backward",voltage);
    motor.rotate("drv2","forward",voltage);
    sleep(time);
    motor.rotate("drv1","neutral",voltage);
    motor.rotate("drv1","neutral",voltage);

}
void left(float voltage,int time){
    motor.rotate("drv1","forward",voltage);
    motor.rotate("drv2","backward",voltage);
    sleep(time);
    motor.rotate("drv1","neutral",voltage);
    motor.rotate("drv1","neutral",voltage);

}
}//namespace blue

