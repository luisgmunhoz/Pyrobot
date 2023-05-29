from machine import PWM
from machine import Pin
from machine import time_pulse_us
from time import sleep_us, sleep
import random
import utime
M=100


# Define the GPIO pin numbers for the trigger and echo pins
ECHO_PIN = 2
ECHO1 = 3
ECHO2 = 4
TRIGGER_PIN =1 

# Initialize trigger and echo pins
trigger = Pin(TRIGGER_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

led = Pin(25, Pin.OUT)

# motor_a (esquerda) ports
ina1 = Pin(11, Pin.OUT) # Verde
ina2 = Pin(10, Pin.OUT) # Marrom
#pwm_a = PWM(Pin(12)) 

# motor_b (direita) ports
inb1 = Pin(15, Pin.OUT) # Lilás
inb2 = Pin(14, Pin.OUT) # Branco
#pwm_b = PWM(Pin(13))

#pwm_a.freq(10000)
#pwm_b.freq(10000)

def right_motor_forward(duty):
    inb1.value(0)
    inb2.value(1)
    #duty_16 = int((duty * 65536) / 100)
    #print("motor esquerdo", duty_16)
    #pwm_b.duty_u16(duty_16)
    
def right_motor_backward(duty):
    inb1.value(1)
    inb2.value(0)
    led.value(1)
    #duty_16 = int((duty * 65536) / 100)
    #pwm_b.duty_u16(duty_16)

def stop_right_motor():
    inb2.value(0)
    inb1.value(0)
    #pwm_b.duty_u16(0)

def left_motor_forward(duty):
    ina1.value(0)
    ina2.value(1)
    led.value(0)
    #duty_16 = int((duty * 65536) / 100)
    #print("motor direito", duty_16)
    #pwm_a.duty_u16(duty_16)

def left_motor_backward(duty):
    ina1.value(1)
    ina2.value(0)
    #duty_16 = int((duty * 65536) / 100)
    #pwm_a.duty_u16(duty_16)

def stop_left_motor():
    ina1.value(0)
    ina2.value(0)
    #pwm_a.duty_u16(0)
    
# Forward
def move_forward(duty):    
    right_motor_forward(duty)
    left_motor_forward(duty)
    
# Backward
def move_backward(duty):
    right_motor_backward(duty)
    left_motor_backward(duty)
    
#Turn Left
def turn_right(duty):
    right_motor_backward(duty)
    left_motor_forward(duty)
    
#Turn Right
def turn_left(duty):
    left_motor_backward(duty)
    right_motor_forward(duty)
   
#Stop
def stop():
    stop_right_motor()
    stop_left_motor()

def test_left(duty):
    left_motor_forward(duty)
    sleep(1)
    left_motor_backward(duty)
    sleep(1)
    
def test_right(duty):
    right_motor_forward(duty)
    sleep(1)
    right_motor_backward(duty)
    sleep(1)

def getDistance(echo_pin,trigger_pin):
    
    trigger = Pin(trigger_pin, Pin.OUT)
    echo = Pin(echo_pin, Pin.IN)
    # Ensure trigger is low initially
    trigger.low()
    sleep_us(200)

    # Send a 10 microsecond pulse to the trigger pin
    trigger.high()
    sleep_us(100)
    trigger.low()

    # Measure the duration of the echo pulse (in microseconds)
    pulse_duration = time_pulse_us(echo, Pin.high)

    # Calculate the distance (in centimeters) using the speed of sound (343 m/s)
    distance = pulse_duration * 0.0343 / 2
    return distance

stopDistance=50

# sleep(10)
def test(M):
    move_forward(M)
    sleep(1)
    stop()
    sleep(1)
    move_backward(M)
    sleep(1)
    stop()
    sleep(1)
    turn_left(M)
    sleep(1)
    stop()
    sleep(1)
    turn_right(M)
    
if True:
    test(M)
    
stopDist=50    
while True:
    distance_mid = getDistance(2,1)
    distance_left = getDistance(3,1)
    distance_right = getDistance(4,1)
    print(f"2     {distance_mid}")
    print(f"3     {distance_left}")
    print(f"4     {distance_right}")