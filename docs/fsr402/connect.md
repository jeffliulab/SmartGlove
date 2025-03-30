请按照下列步骤连接：

FSR402 第 1 根线 → Pico W 的 Pin 36 (3V3(OUT))

这会给 FSR402 提供 3.3V 电压。

FSR402 第 2 根线 → Pico W 的 Pin 31 (GPIO26 / ADC0)

这个节点就是我们要读取电压的地方。

10kΩ 固定电阻

一端 → 同样连接到 Pin 31 (GPIO26 / ADC0)

另一端 → 连接到 Pico W 的 GND（例如 Pin 38 或任何一个标有 GND 的引脚）