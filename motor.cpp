#include<stdio.h>
#include<stdlib.h>
#include<strings.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <termios.h>
#include <unistd.h>
#include <linux/i2c-dev.h>

#define MdrvAdr1 0x60
#define MdrvAdr2 0x64
#define I2C_DevName  "/dev/i2c-1"

int main(){
    int fd;

    	if ((fd = open(i2cDevName, O_RDWR)) < 0) {
		printf("Faild to open i2c port! ><\n");
		return 1;
	}

	if (ioctl(fd, I2C_SLAVE, i2cAddr1) < 0) {
		printf("Faild to open port...\n");
		return 1;
	}
while(1){
    write(fd,0x02,2);
}
return 0;
}