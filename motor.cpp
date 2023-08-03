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

using std::cout;
using std::endl;
using std::string;

#define MdrvAddr1 0x60
#define MdrvAddr2 0x64
#define I2C_DevName  "/dev/i2c-1"

class Motor{
    public:
        int voltage_addr;
        char buf[2];
        Motor();
        void drv1_slave();
        void drv2_slave();
        void rotate(string drv,string direction);
    private:
        int fd;
        const int i2cAddr1=MdrvAddr1;
        const int i2cAddr2=MdrvAddr2;

        const int forward_addr=0x01;
        const int backward_addr=0x10;
        const int stop_addr=0x11;
        const int neutral_addr=0x00;
};

Motor::Motor(){
    	if ((this->fd = open(I2C_DevName, O_RDWR)) < 0) {
		printf("Faild to open i2c port! ><\n");
         }
        buf[]=0x00;

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

void Motor::rotate(string drv,string direction){
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
    }

    if(write(fd,buf,2)!=2){
    cout<<"error"<<endl;
    }
}

int main(){
char buf[2];
int fd;
    Motor motor;
    motor.voltage_addr=0x15;
    motor.rotate("drv1","forward");
    motor.rotate("drv2","forward");
    sleep(2);
    motor.rotate("drv1","neutral");
    motor.rotate("drv2","neutral");
return 0;
}