#include "motor.h"
#include "blue_control.h"
#include<unistd.h>
blue::Motor motor;

namespace blue{
void Blue_control::forward(float voltage,float time){
    motor.rotate("drv1","forward",voltage);
    motor.rotate("drv2","forward",voltage);
    usleep(time*1000*1000);
    motor.rotate("drv1","neutral",voltage);
    motor.rotate("drv2","neutral",voltage);

}
void Blue_control::backward(float voltage,float time){
    motor.rotate("drv1","backward",voltage);
    motor.rotate("drv2","backward",voltage);
    usleep(time*1000*1000);
    motor.rotate("drv1","neutral",voltage);
    motor.rotate("drv2","neutral",voltage);

}

void Blue_control::right(float voltage,float time){
    motor.rotate("drv1","backward",voltage);
    motor.rotate("drv2","forward",voltage);
    usleep(time*1000*1000);
    motor.rotate("drv1","neutral",voltage);
    motor.rotate("drv2","neutral",voltage);

}
void Blue_control::left(float voltage,float time){
    motor.rotate("drv1","forward",voltage);
    motor.rotate("drv2","backward",voltage);
    usleep(time*1000*1000);
    motor.rotate("drv1","neutral",voltage);
    motor.rotate("drv2","neutral",voltage);

}
}//namespace blue

