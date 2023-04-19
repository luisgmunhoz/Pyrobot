from machine import PWM
from machine import Pin
from machine import time_pulse_us
from time import sleep_us, sleep
import random
import utime
M=100


# Define the GPIO pin numbers for the trigger and echo pins
ECHO_PIN = 26
TRIGGER_PIN = 27

# Initialize trigger and echo pins
trigger = Pin(TRIGGER_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)



led = PWM(Pin(25))

# motor_a ports
ina1 = Pin(11, Pin.OUT)
ina2 = Pin(12, Pin.OUT)
pwm_a = PWM(Pin(10))

# motor_b ports
inb1 = Pin(15, Pin.OUT)
inb2 = Pin(14, Pin.OUT)
pwm_b = PWM(Pin(13))



led.freq(10000)
#pwm_a.freq(10000)
pwm_b.freq(10000)

def left_motor_forward(duty):
    inb1.value(0)
    inb2.value(1)
    duty_16 = int((duty * 65536) / 100)
    print("motor esquerdo", duty_16)
    pwm_b.duty_u16(duty_16)
    
def left_motor_backward(duty):
    inb1.value(1)
    inb2.value(0)
    duty_16 = int((duty * 65536) / 100)
    pwm_b.duty_u16(duty_16)

def stop_left_motor():
    pwm_a.value(0)
    ina2.value(0)
    ina1.duty_u16(0)


def right_motor_forward(duty):
    ina1.value(0)
    ina2.value(1)
    duty_16 = int((duty * 65536) / 100)
    print("motor direito", duty_16)
    pwm_a.duty_u16(duty_16)

def right_motor_backward(duty):
    ina1.value(1)
    ina2.value(0)
    duty_16 = int((duty * 65536) // 100)
    pwm_a.duty_u16(duty_16)

def stop_right_motor():
    inb1.value(0)
    inb2.value(0)
    pwm_b.duty_u16(0)


# def sensor_test_with_counter(port):
    # counter = 0
    # input_sensor = Pin(port, Pin.OUT)
    # input_sensor(1)
    # utime.sleep(0.01)
    # input_sensor.init(Pin.IN, Pin.PULL_DOWN)
    # while input_sensor.value() == 1:
        # counter = counter+1
        # print(port, counter)
        # return counter


# def sensor_test_with_utime(port):
    # input_sensor = Pin(port, Pin.OUT)
    # input_sensor(1)
    # pulse_start = utime.utime_ns()
    # input_sensor.init(Pin.IN, Pin.PULL_DOWN)
    # while input_sensor.value() > 0:
        #utime.sleep(0.00001)
        # if input_sensor.value() == 0:
            # pulse_end = utime.utime_ns()
            # pulse_duration = pulse_end - pulse_start
            # return pulse_duration

# Forward
def move_forward(duty):
    left_motor_forward(duty)
    right_motor_forward(duty)
    
# Backward
def move_backward(duty):
    left_motor_backward(duty)
    right_motor_backward(duty)
    
#Turn Right
def turn_right(duty):
    stop_right_motor()
    left_motor_forward(duty)
    
#Turn Left
def turn_left(duty):
    stop_left_motor()
    right_motor_forward(duty)
   
#Stop
def stop():
    stop_right_motor()
    stop_left_motor()
    
    
def test_l(duty):
    stop_left_motor()
    right_motor_backward(duty)

def test_r(duty):
    stop_right_motor()
    left_motor_backward(duty)

import ultrasonic as sonic
import mq2Read as mq2r

# sonic.test(26,27)
#mq2r.calibrate(28,3.3) #calibra os sensores
#mq2r.test
# sleep(10)
while True:
    
    move_forward(M)
    sleep(5)
        
    


   
#     print("right")
#     right_motor_backward(25)
#     left_motor_forward(50)
#     utime.sleep(1)
    
#     print("left")
#     left_motor_backward(25)
#     right_motor_forward(50)
    
    # else:
        # stop_left_motor()
        # stop_right_motor()

