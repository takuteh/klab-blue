#include "motor.h"

blue::Motor motor;

namespace blue{
void forward(float voltage,int mode){
    motor.rotate("drv1","forward",voltage);
    motor.rotate("drv2","forward",voltage);
    sleep(mode);
    motor.rotate("drv1","neutral",voltage);
    motor.rotate("drv1","neutral",voltage);

}
void backward(float voltage,int mode){
    motor.rotate("drv1","backward",voltage);
    motor.rotate("drv2","backward",voltage);
    sleep(mode);
    motor.rotate("drv1","neutral",voltage);
    motor.rotate("drv1","neutral",voltage);

}

void right(float voltage,int mode){
    motor.rotate("drv1","backward",voltage);
    motor.rotate("drv2","forward",voltage);
    sleep(mode);
    motor.rotate("drv1","neutral",voltage);
    motor.rotate("drv1","neutral",voltage);

}
void left(float voltage,int mode){
    motor.rotate("drv1","forward",voltage);
    motor.rotate("drv2","backward",voltage);
    sleep(mode);
    motor.rotate("drv1","neutral",voltage);
    motor.rotate("drv1","neutral",voltage);

}
}//namespace blue