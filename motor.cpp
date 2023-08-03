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
        int fd;
        char buf[2];
        Motor();
        void drv1_slave();
        void drv2_slave();
        void rotate(string drv,string direction);
    private:
        const int i2cAddr1=MdrvAddr1;
        const int i2cAddr2=MdrvAddr2;

        const int forward=0x01;
        const int backward=0x10;
        const int stop=0x11;
        const int neutral=0x00;
};

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
//		return 1;
	}
}

void Motor::rotate(string drv,string direction){
buf[1]=0;
if(drv=="drv1"){
this->drv1_slave();
}else if(drv=="drv2"){
this->drv2_slave();
}else{
cout<<drv<<" is invalid string!!"<<endl;
}
    if(direction=="forward"){
        buf[1]=0x09<<2|this->forward;
    }else if(direction=="backward"){
        buf[1]=0x09<<2|this->backward;
    }else if(direction=="stop"){
        buf[1]=0x09<<2|this->stop;
    }else if(direction=="neutral"){
        buf[1]=0x00;
    }

    if(write(fd,buf,2)!=2){
    cout<<"error"<<endl;
    }
}

int main(){
char buf[2];
int fd;
    Motor motor;
    motor.rotate("drv1","forward");
    motor.rotate("drv2","forward");
    sleep(2);
    motor.rotate("drv1","neutral");
    motor.rotate("drv2","neutral");
return 0;
}