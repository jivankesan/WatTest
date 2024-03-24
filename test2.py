import RPi.GPIO as GPIO
from motors import Car
import pigpio
import MotorEncoder
import serial
import board
import adafruit_bno055
import time



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
        
        car.drive(2)
        angle = sensor.euler[0]
        while(angle < 90):
            angle = sensor.euler[0]
        
        car.stop()
        time.sleep(2)
            
    except KeyboardInterrupt:
        print("stopped")
        print(curr-init)
    finally:
        car.stop()
        GPIO.cleanup()