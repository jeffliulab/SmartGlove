from machine import I2C, Pin
import time

# 使用 GP26 和 GP27
i2c = I2C(1, sda=Pin(26), scl=Pin(27), freq=100000)

print("Scanning I2C bus...")
try:
    devices = i2c.scan()
    if devices:
        print("Found devices:", [hex(d) for d in devices])
    else:
        print("No devices found")
except Exception as e:
    print("Error:", e)