// i2C motor drive using DRV8830
// ループ内のscanfで印加電圧を読み取り，ドライバが読み取れるHexに変換してi2c経由でドライバに出力
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

int main(int argc, char* argv[])
{

	int fd; //i2cのファイルデスクリプタ
	char* i2cDevName = I2C_DevName;
	int i2cAddr1 = MdrvAdr1;
	int i2cAddr2 = MdrvAdr2;
	int x1;
	int x2;
	int x3;
	int x4;
	int x;
	int y;
	int t;
	double v1;
	double v2;
	unsigned char buf[4];
	double targettemp1;
	double targettemp2;
	double targetabs1 = 0.0;
	double targetabs2 = 0.0;
	int dir1;
	int dir2;


	if ((fd = open(i2cDevName, O_RDWR)) < 0) {
		printf("Faild to open i2c port! ><\n");
		return 1;
	}

	if (ioctl(fd, I2C_SLAVE, i2cAddr1) < 0) {
		printf("Faild to open port...\n");
		return 1;
	}


	v1 = atof(argv[1]);
	if (v1 < 5.06) {

		printf("target1[V] = %f\n", v1);

		targetabs1 = abs(v1);
		if (v1 > 0.1) {
			dir1 = 0x01;
		}
		else if (v1 < -0.1) {
			dir1 = 0x02;
		}
		else {
			dir1 = 0x00;
		}
		targettemp1 = ((targetabs1 - 0.48) / (5.06 - 0.48)) * (0x3F - 0x06);
		x1 = 0x06 + ((int)targettemp1);
		x2 = dir1;

		printf("x1=%02x\n", x1);
		printf("x2=%02x\n", x2);

		x = (x1 << 2) | x2;
		printf("x=%x\n", x);
		buf[0] = 0x00;
		buf[1] = x;

		if (write(fd, buf, 2) != 2) {
			printf("error\n");
		}
		else {
			//
		}
	}

	if (ioctl(fd, I2C_SLAVE, i2cAddr2) < 0) {
		printf("Faild to open port...\n");
		return 1;
	}

	v2 = atof(argv[2]);
	if (v2 < 5.06) {

		printf("target2[V] = %f\n", v2);
		targetabs2 = abs(v2);
		if (v2 > 0.1) {
			dir2 = 0x01;
		}
		else if (v2 < -0.1) {
			dir2 = 0x02;
		}
		else {
			dir2 = 0x00;
		}
		targettemp2 = ((targetabs2 - 0.48) / (5.06 - 0.48)) * (0x3F - 0x06);
		x3 = 0x06 + ((int)targettemp2);
		x4 = dir2;

		//scanf("%x", &x1);
		printf("x1=%02x\n", x3);
		//scanf("%x", &x2);
		printf("x2=%02x\n", x4);

		y = (x3 << 2) | x4;
		printf("y=%x\n", y);
		buf[2] = 0x00;
		buf[3] = y;

		if (write(fd, &buf[2], 2) != 2) {
			printf("error\n");
		}
		else {
			//
		}
	}

	if (ioctl(fd, I2C_SLAVE, i2cAddr1) < 0) {
		printf("Faild to open port...\n");
		return 1;
	}



	t = atof(argv[3]) * 1000000;
	usleep(t);
	printf("%d\n", t);



	x1 = 0x00;
	x2 = 0x00;
	x = (x1 << 2) | x2;
	printf("%x\n", x);
	buf[0] = 0x00;
	buf[1] = x;
	while (1) {

		if (write(fd, buf, 2) == 2) {
			break;
		}
	}

	if (ioctl(fd, I2C_SLAVE, i2cAddr2) < 0) {
		printf("Faild to open port...\n");
		return 1;
	}

	x3 = 0x00;
	x4 = 0x00;
	y = (x3 << 2) | x4;
	printf("%x\n", y);

	buf[2] = 0x00;
	buf[3] = y;

	while (1) {

		if (write(fd, &buf[2], 2) == 2) {
			break;
		}

	}
	printf("finish...\n");
	return 0; //終了

}


