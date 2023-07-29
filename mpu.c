// i2C motor drive using MPU9250
#include <stdio.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <linux/i2c-dev.h>
#include <i2c/smbus.h>

#define MPU9250_ADDRESS 0x69
#define I2C_DevName  "/dev/i2c-1"

int main()
{
	int fd; //i2cのファイルデスクリプタ

	if ((fd = open(I2C_DevName, O_RDWR)) < 0) {
		printf("Faild to open i2c port! ><\n");
		return 1;
	}

	if (ioctl(fd, I2C_SLAVE, MPU9250_ADDRESS) < 0) {
		printf("Faild to open port...\n");
		return 1;
	}

	// 初期化
	i2c_smbus_write_byte_data(fd, 0x6B, 0);
	i2c_smbus_write_byte_data(fd, 0x1C, 0x18);
	i2c_smbus_write_byte_data(fd, 0x1B, 0x18);

	// 値の取得
	unsigned char accelerationData[6];
	i2c_smbus_read_i2c_block_data(fd, 0x3B, 6, accelerationData);

	short rawAx = (accelerationData[0] << 8) | accelerationData[1];
	short rawAy = (accelerationData[2] << 8) | accelerationData[3];
	short rawAz = (accelerationData[4] << 8) | accelerationData[5];
        for(int i = 0;i<6;i++)
        {
            printf("%d\n",accelerationData[i]);
        }

	double ax = rawAx * 16.0 / 32768.0;
	double ay = rawAy * 16.0 / 32768.0;
	double az = rawAz * 16.0 / 32768.0;

	printf("---\n");
	printf("%f\n", ax);
	printf("%f\n", ay);
	printf("%f\n", az);

	return 0; //終了
}


