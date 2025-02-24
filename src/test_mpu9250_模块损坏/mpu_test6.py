from machine import I2C, Pin

# 使用 I2C1（SDA=GP6, SCL=GP7）
i2c = I2C(1, scl=Pin(7), sda=Pin(6))

MPU9250_ADDR = 0x68  # MPU9250 默认 I2C 地址
WHO_AM_I_REG = 0x75  # 设备 ID 寄存器

try:
    whoami = i2c.readfrom_mem(MPU9250_ADDR, WHO_AM_I_REG, 1)
    print("MPU9250 WHO_AM_I:", whoami)
except Exception as e:
    print("FAILED:", e)
