from machine import I2C, Pin

# 初始化 I2C 设备
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# 扫描 I2C 设备
devices = i2c.scan()

if devices:
    print("找到 I2C 设备地址:", [hex(device) for device in devices])
else:
    print("没有找到 I2C 设备，请检查连接！")
