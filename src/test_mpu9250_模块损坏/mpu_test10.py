from machine import I2C, Pin
import time

# I2C addresses and registers
MPU9250_ADDR_1 = 0x68  # AD0 low
MPU9250_ADDR_2 = 0x69  # AD0 high
WHO_AM_I_REG = 0x75
PWR_MGMT_1 = 0x6B
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
ACCEL_CONFIG = 0x1C

# Pico W specific pin definitions
# Default I2C pins for Pico:
# I2C0: SDA = GP0 (pin 1), SCL = GP1 (pin 2)
# I2C1: SDA = GP2 (pin 4), SCL = GP3 (pin 5)
I2C_SDA_PIN = 6  # GP6
I2C_SCL_PIN = 7  # GP7

def init_i2c():
    """Initialize I2C with proper pin configuration for Pico W"""
    print("\n=== Initializing I2C ===")
    try:
        # Try different frequencies if 100KHz doesn't work
        i2c = I2C(1,
                  sda=Pin(I2C_SDA_PIN),
                  scl=Pin(I2C_SCL_PIN),
                  freq=100000)
        print(f"I2C initialized on SDA=GP{I2C_SDA_PIN}, SCL=GP{I2C_SCL_PIN}")
        return i2c
    except Exception as e:
        print(f"I2C initialization failed: {e}")
        return None

def scan_i2c(i2c):
    """Scan for I2C devices"""
    print("\n=== I2C Device Scan ===")
    try:
        devices = i2c.scan()
        if devices:
            print(f"Found {len(devices)} devices:")
            for device in devices:
                print(f"  - Address: {hex(device)}")
        else:
            print("No I2C devices found! Check connections:")
            print("  - SDA connection (GP6)")
            print("  - SCL connection (GP7)")
            print("  - Power (3.3V)")
            print("  - Ground")
        return devices
    except Exception as e:
        print(f"Scan failed: {e}")
        return []

def check_who_am_i(i2c, addr):
    """Check WHO_AM_I register"""
    print(f"\n=== Testing MPU9250 at {hex(addr)} ===")
    try:
        whoami = i2c.readfrom_mem(addr, WHO_AM_I_REG, 1)
        val = whoami[0]
        print(f"WHO_AM_I register value: {hex(val)}")
        if val == 0x71 or val == 0x73:
            print("SUCCESS: Valid MPU9250 WHO_AM_I response!")
        else:
            print("WARNING: Unexpected WHO_AM_I value!")
        return val
    except Exception as e:
        print(f"Failed to read WHO_AM_I: {e}")
        print("Check if the sensor is properly powered and connected")
        return None

def try_wake_up(i2c, addr):
    """Try to wake up the device"""
    print("\n=== Attempting wake up ===")
    try:
        # Reset device first
        i2c.writeto_mem(addr, PWR_MGMT_1, bytes([0x80]))
        time.sleep_ms(100)
        # Clear sleep bit and set clock source
        i2c.writeto_mem(addr, PWR_MGMT_1, bytes([0x01]))
        time.sleep_ms(100)
        # Read power management register
        pwr = i2c.readfrom_mem(addr, PWR_MGMT_1, 1)
        print(f"Power management register: {hex(pwr[0])}")
        return True
    except Exception as e:
        print(f"Wake up failed: {e}")
        return False

def read_sensor_data(i2c, addr):
    """Read accelerometer and gyroscope data"""
    print("\n=== Reading Sensor Data ===")
    try:
        # Read accelerometer data (registers 0x3B-0x40)
        accel_data = i2c.readfrom_mem(addr, 0x3B, 6)
        accel_x = (accel_data[0] << 8) | accel_data[1]
        accel_y = (accel_data[2] << 8) | accel_data[3]
        accel_z = (accel_data[4] << 8) | accel_data[5]
        
        # Convert to signed integers
        accel_x = accel_x - 65536 if accel_x > 32767 else accel_x
        accel_y = accel_y - 65536 if accel_y > 32767 else accel_y
        accel_z = accel_z - 65536 if accel_z > 32767 else accel_z
        
        print("Accelerometer readings:")
        print(f"  X: {accel_x:6d}")
        print(f"  Y: {accel_y:6d}")
        print(f"  Z: {accel_z:6d}")
        
        if abs(accel_x) == 0 and abs(accel_y) == 0 and abs(accel_z) == 0:
            print("WARNING: All accelerometer values are 0!")
            print("This might indicate a sensor problem")
        
        return True
    except Exception as e:
        print(f"Failed to read sensor data: {e}")
        return False

def run_diagnostics():
    """Run complete diagnostic sequence"""
    print("============================")
    print("MPU9250 Diagnostic Tool")
    print("For Raspberry Pi Pico W")
    print("============================")
    
    # Initialize I2C
    i2c = init_i2c()
    if not i2c:
        return
    
    # Scan for devices
    devices = scan_i2c(i2c)
    
    # Test both possible addresses
    for addr in [MPU9250_ADDR_1, MPU9250_ADDR_2]:
        if addr in devices:
            who_am_i_val = check_who_am_i(i2c, addr)
            if who_am_i_val:
                if try_wake_up(i2c, addr):
                    read_sensor_data(i2c, addr)
        else:
            print(f"\nNo device found at {hex(addr)}")
    
    print("\n=== Diagnostic Complete ===")
    if not devices:
        print("\nTroubleshooting steps:")
        print("1. Check all connections")
        print("2. Verify 3.3V power supply")
        print("3. Try different I2C pins")
        print("4. Check for shorts or breaks in wires")
        print("5. Try a different MPU9250 module if available")

# Run the diagnostics
run_diagnostics()