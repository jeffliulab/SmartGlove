import utime
from machine import I2C, Pin
from mpu9250 import MPU9250

# **确保使用 I2C(0) 或 I2C(1)，并正确匹配 SDA/SCL**
i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=400000)

print("正在扫描 I2C 设备...")
devices = i2c.scan()

if len(devices) == 0:
    print("❌ 没有找到 I2C 设备，请检查接线！")
else:
    print(f"✅ 找到 I2C 设备: {devices}")

    # 继续初始化 MPU9250
    sensor = MPU9250(i2c)

    print("MPU9250 id: " + hex(sensor.whoami))

    while True:
        print("加速度:", sensor.acceleration)
        print("陀螺仪:", sensor.gyro)
        print("磁场:", sensor.magnetic)
        print("温度:", sensor.temperature)

        utime.sleep_ms(1000)
