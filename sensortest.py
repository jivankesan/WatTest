import RPi.GPIO as GPIO
from motors import Car
import pigpio
import MotorEncoder
import serial
import board
import adafruit_bno055



if __name__ == "__main__":  
    i2c = board.I2C()  
    sensor = adafruit_bno055.BNO055_I2C(i2c) 
    
    Pin1 = 8
    Pin2 = 25
    RUN_TIME = 60.0
    SAMPLE_TIME = 0.01
    
    pi = pigpio.pi()
    p = MotorEncoder.reader(pi, Pin1)
    car = Car()
    
    ser = serial.Serial('/dev/ttyUSB0', 115200)
    
    dist = 20
        
    try:
        init = sensor.euler[0]
        curr = 0
        car.drive(0)
        while True:
            angle = sensor.euler[0]
            curr = angle
            curr_distance = (p.pulse_count/4685)*0.471234
            data = ser.readline().decode().strip()
            print(f"Angle: {angle}, Current Distance: {curr_distance}, Data: {data}")
            
    except KeyboardInterrupt:
        print("stopped")
        print(curr-init)
    finally:
        car.stop()
        GPIO.cleanup()
        