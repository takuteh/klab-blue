#include<iostream>
#include<stdlib.h>
#include<strings.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <termios.h>
#include <unistd.h>
#include <linux/i2c-dev.h>
#include "motor.h"

using std::cout;
using std::endl;
using std::string;
using std::cin;

#define I2C_DevName  "/dev/i2c-1"

namespace blue{
Motor::Motor(){
    	if ((this->fd = open(I2C_DevName, O_RDWR)) < 0) {
		printf("Faild to open i2c port! ><\n");
         }
        buf[0]=0x00;
       }

void Motor::drv1_slave(){
	if (ioctl(this->fd, I2C_SLAVE, i2cAddr1) < 0) {
		printf("Faild to open port...\n");
	}
}

void Motor::drv2_slave(){
    	if (ioctl(this->fd, I2C_SLAVE, i2cAddr2) < 0) {
		printf("Faild to open port...\n");
	}
}
void Motor::convert_v_to_addr(){
this->voltage_addr=(voltage-0.48)/(5.06-0.48)*(0x3F-0x06);
}

void Motor::rotate(string drv,string direction){
convert_v_to_addr();
if(drv=="drv1"){
this->drv1_slave();
}else if(drv=="drv2"){
this->drv2_slave();
}else{
cout<<drv<<" is invalid string!!"<<endl;
}
    if(direction=="forward"){
        buf[1]=this->voltage_addr<<2|this->forward_addr;
    }else if(direction=="backward"){
        buf[1]=this->voltage_addr<<2|this->backward_addr;
    }else if(direction=="stop"){
        buf[1]=this->voltage_addr<<2|this->stop_addr;
    }else if(direction=="neutral"){
        buf[1]=this->neutral_addr;
    }else{
	cout<<"invalid string!"<<endl;
   }

    if(write(this->fd,buf,2)!=2){
    cout<<"error"<<endl;
    }
}
}//namespace blue

// int main(){
// while(1){
//     Motor motor;
//    cout<<"input voltage:";
//     cin>>motor.voltage;
//     motor.rotate("drv1","forward");
//     motor.rotate("drv2","backward");
//     sleep(1);
//     motor.rotate("drv1","neutral");
//     motor.rotate("drv2","neutral");
// sleep(1);
//     motor.rotate("drv1","backward");
//     motor.rotate("drv2","forward");
// sleep(1);
//     motor.rotate("drv1","neutral");
//     motor.rotate("drv2","neutral");
// }
// return 0;
// }
