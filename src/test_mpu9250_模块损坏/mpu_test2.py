from machine import I2C, Pin

# **尝试 I2C1 (GP22 SCL, GP21 SDA)**
i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=400000)

print("🔍 正在扫描 I2C 设备...")
devices = i2c.scan()

if len(devices) == 0:
    print("❌ 没有找到 I2C 设备，请检查接线！")
else:
    print(f"✅ 找到 I2C 设备: {devices}")
