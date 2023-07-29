#pragma once
#include "vl53l0x_api.h"
#include "vl53l0x_platform.h"

class DistanceSensor {
public:
	DistanceSensor();
	~DistanceSensor();
	bool isObstacle();
	int sensorRawValue();
private:
	VL53L0X_Dev_t MyDevice;
	VL53L0X_Dev_t* pMyDevice = &MyDevice;
};