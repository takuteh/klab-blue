#ifndef MOTOR_H
#define MOTOR_H

#include<iostream>
#define Mdrv_addr1 0x60
#define Mdrv_addr2 0x64
using std::string;
namespace blue{
class Motor{
    public:
        int voltage_addr;
        char buf[2];
        Motor();
	float voltage;
        void drv1_slave();
        void drv2_slave();
        void rotate(string drv,string direction,float v);
	void convert_v_to_addr();
    private:
        int fd;
        const int i2cAddr1=Mdrv_addr1;
        const int i2cAddr2=Mdrv_addr2;

        const int forward_addr=0x01;
        const int backward_addr=0x02;
        const int stop_addr=0x03;
        const int neutral_addr=0x00;
};
}//namespace blue
#endif
