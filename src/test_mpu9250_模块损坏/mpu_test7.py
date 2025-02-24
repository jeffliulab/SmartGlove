from machine import I2C, Pin

i2c = I2C(1, scl=Pin(7), sda=Pin(6))  # 使用 I2C1

devices = i2c.scan()  # 扫描 I2C 设备
print("I2C:", devices)  # 期待输出 [104]（0x68）或者 [105]（0x69）
