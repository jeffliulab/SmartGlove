from machine import I2C, Pin

# 扫描 I2C0（默认端口）
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
devices = i2c.scan()

print("I2C address: ", devices)  # 期待 [104] (0x68)
