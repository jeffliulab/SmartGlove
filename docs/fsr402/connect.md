
## Conncect

FSR402 第 1 根线 → Pico W 的 Pin 36 (3V3(OUT))

这会给 FSR402 提供 3.3V 电压。

FSR402 第 2 根线 → Pico W 的 Pin 31 (GPIO26 / ADC0)

这个节点就是我们要读取电压的地方。

10kΩ 固定电阻

一端 → 同样连接到 Pin 31 (GPIO26 / ADC0)

另一端 → 连接到 Pico W 的 GND（例如 Pin 38 或任何一个标有 GND 的引脚）

## 代码
`main.py`
```python
import machine
import time

# 初始化 ADC，GPIO26（对应 Pico W 的 Pin 31，ADC0）
adc = machine.ADC(26)

while True:
    # 读取 ADC 数值（范围 0～65535，虽然实际 ADC 为 12 位，但 MicroPython 会进行缩放）
    sensor_value = adc.read_u16()
    print("Force Sensor: ", sensor_value)
    time.sleep(0.1)
```

该程序会自动运行

## 通过串口读取信息

在4b上安装`pip install pyserial`
```python
import serial

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
while True:
    line = ser.readline().decode('utf-8').strip()
    if line:
        print(line)
```