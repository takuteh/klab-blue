#include "motor.h"
#include "blue_control.h"
#include<unistd.h>
blue::Motor motor;

namespace blue{
void Blue_control::forward(int i){
    motor.rotate("drv1","forward");
    motor.rotate("drv2","forward");
    sleep(i);
    motor.rotate("drv1","neutral");
    motor.rotate("drv2","neutral");

}
void Blue_control::backward(int i){
    motor.rotate("drv1","backward");
    motor.rotate("drv2","backward");
    sleep(i);
    motor.rotate("drv1","neutral");
    motor.rotate("drv2","neutral");

}

void Blue_control::right(int i){
    motor.rotate("drv1","backward");
    motor.rotate("drv2","forward");
    sleep(i);
    motor.rotate("drv1","neutral");
    motor.rotate("drv2","neutral");

}
void Blue_control::left(int i){
    motor.rotate("drv1","forward");
    motor.rotate("drv2","backward");
    sleep(i);
    motor.rotate("drv1","neutral");
    motor.rotate("drv1","neutral");

}
}//namespace blue
