import utime
from machine import I2C, Pin
from mpu9250 import MPU9250

# 修改 I2C 端口和引脚（改为 I2C0）
i2c = I2C(0, scl=Pin(1), sda=Pin(0))

# 尝试初始化传感器
sensor = MPU9250(i2c)

print("MPU9250 id: " + hex(sensor.whoami))

while True:
    print(sensor.acceleration)
    print(sensor.gyro)
    print(sensor.magnetic)
    print(sensor.temperature)
    utime.sleep_ms(1000)
