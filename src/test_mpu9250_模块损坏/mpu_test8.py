from machine import I2C, Pin
import time

# 尝试两个可能的地址
MPU9250_ADDR_1 = 0x68
MPU9250_ADDR_2 = 0x69
WHO_AM_I_REG = 0x75

# 降低频率，使用上拉电阻
i2c = I2C(1, scl=Pin(7, pull=Pin.PULL_UP), sda=Pin(6, pull=Pin.PULL_UP), freq=100000)

print("扫描 I2C 设备...")
devices = i2c.scan()
print("发现的设备地址:", [hex(device) for device in devices])

# 尝试两个地址
for addr in [MPU9250_ADDR_1, MPU9250_ADDR_2]:
    print(f"\n尝试地址 {hex(addr)}:")
    try:
        whoami = i2c.readfrom_mem(addr, WHO_AM_I_REG, 1)
        print(f"WHO_AM_I 寄存器值: {hex(whoami[0])}")
    except Exception as e:
        print(f"读取失败: {e}")