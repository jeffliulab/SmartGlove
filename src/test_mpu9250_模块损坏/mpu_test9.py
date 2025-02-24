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

def scan_i2c():
    """Scan for I2C devices"""
    print("\n=== I2C Device Scan ===")
    try:
        devices = i2c.scan()
        if devices:
            print("Found devices at addresses:", [hex(d) for d in devices])
        else:
            print("No I2C devices found!")
        return devices
    except Exception as e:
        print("Scan failed:", e)
        return []

def check_who_am_i(addr):
    """Check WHO_AM_I register"""
    print(f"\n=== Testing address {hex(addr)} ===")
    try:
        whoami = i2c.readfrom_mem(addr, WHO_AM_I_REG, 1)
        print(f"WHO_AM_I register value: {hex(whoami[0])}")
        if whoami[0] == 0x71 or whoami[0] == 0x73:  # Common MPU9250 WHO_AM_I values
            print("Valid MPU9250 WHO_AM_I response!")
        else:
            print("WARNING: Unexpected WHO_AM_I value")
        return whoami[0]
    except Exception as e:
        print(f"Failed to read WHO_AM_I: {e}")
        return None

def try_wake_up(addr):
    """Try to wake up the device"""
    print("\n=== Attempting wake up ===")
    try:
        # Clear sleep bit
        i2c.writeto_mem(addr, PWR_MGMT_1, bytes([0x00]))
        time.sleep_ms(100)
        # Read power management register
        pwr = i2c.readfrom_mem(addr, PWR_MGMT_1, 1)
        print(f"Power management register: {hex(pwr[0])}")
        return True
    except Exception as e:
        print(f"Wake up failed: {e}")
        return False

def read_sensor_config(addr):
    """Read sensor configuration registers"""
    print("\n=== Reading Configuration ===")
    try:
        config = i2c.readfrom_mem(addr, CONFIG, 1)
        gyro = i2c.readfrom_mem(addr, GYRO_CONFIG, 1)
        accel = i2c.readfrom_mem(addr, ACCEL_CONFIG, 1)
        
        print(f"CONFIG register: {hex(config[0])}")
        print(f"GYRO_CONFIG register: {hex(gyro[0])}")
        print(f"ACCEL_CONFIG register: {hex(accel[0])}")
        return True
    except Exception as e:
        print(f"Failed to read configuration: {e}")
        return False

def read_test_values(addr):
    """Try to read some sensor values"""
    print("\n=== Reading Sensor Data ===")
    try:
        # Read accelerometer data (registers 0x3B-0x40)
        accel_data = i2c.readfrom_mem(addr, 0x3B, 6)
        accel_x = (accel_data[0] << 8) | accel_data[1]
        accel_y = (accel_data[2] << 8) | accel_data[3]
        accel_z = (accel_data[4] << 8) | accel_data[5]
        
        print("Accelerometer raw data:")
        print(f"X: {accel_x}")
        print(f"Y: {accel_y}")
        print(f"Z: {accel_z}")
        return True
    except Exception as e:
        print(f"Failed to read sensor data: {e}")
        return False

# Initialize I2C with lower frequency and pull-up resistors
print("=== MPU9250 Diagnostic Tool ===")
print("Initializing I2C...")

try:
    i2c = I2C(1, scl=Pin(7, pull=Pin.PULL_UP), sda=Pin(6, pull=Pin.PULL_UP), freq=100000)
    print("I2C initialized successfully")
except Exception as e:
    print("I2C initialization failed:", e)
    raise e

# Run diagnostic tests
devices = scan_i2c()

# Test both possible addresses
for addr in [MPU9250_ADDR_1, MPU9250_ADDR_2]:
    if addr in devices:
        print(f"\nTesting device at {hex(addr)}")
        if check_who_am_i(addr):
            if try_wake_up(addr):
                read_sensor_config(addr)
                read_test_values(addr)
    else:
        print(f"\nNo device found at {hex(addr)}")

print("\n=== Diagnostic Complete ===")