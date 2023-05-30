from machine import PWM
from machine import Pin
from machine import time_pulse_us
from time import sleep_us, sleep
import random
import utime

# Define the GPIO pin numbers for the trigger and echo pins
TRIGGER_PIN = 1 
ECHO_LEFT = 4
ECHO_MIDDLE = 3
ECHO_RIGHT = 2
# Initialize trigger and echo pins

# motor_a (esquerda) ports
ina1 = Pin(11, Pin.OUT) # Verde
ina2 = Pin(10, Pin.OUT) # Marrom

# motor_b (direita) ports
inb1 = Pin(15, Pin.OUT) # Lilás
inb2 = Pin(14, Pin.OUT) # Branco

def right_motor_forward():
    inb1.value(0)
    inb2.value(1)
    
def right_motor_backward():
    inb1.value(1)
    inb2.value(0)

def stop_right_motor():
    inb2.value(0)
    inb1.value(0)

def left_motor_forward():
    ina1.value(0)
    ina2.value(1)

def left_motor_backward():
    ina1.value(1)
    ina2.value(0)

def stop_left_motor():
    ina1.value(0)
    ina2.value(0)
    
# Forward
def move_forward():    
    right_motor_forward()
    left_motor_forward()
    
# Backward
def move_backward():
    right_motor_backward()
    left_motor_backward()
    
#Turn Left
def turn_right():
    right_motor_backward()
    left_motor_forward()
    
#Turn Right
def turn_left():
    left_motor_backward()
    right_motor_forward()
   
#Stop
def stop():
    stop_right_motor()
    stop_left_motor()

def test_left():
    left_motor_forward()
    sleep(1)
    left_motor_backward()
    sleep(1)
    
def test_right():
    right_motor_forward()
    sleep(1)
    right_motor_backward()
    sleep(1)

def getDistance(echo_pinL, echo_pinM, echo_pinR,trigger_pin):
    
    trigger = Pin(trigger_pin, Pin.OUT)
    
    echos = (Pin(echo_pinL, Pin.IN), Pin(echo_pinM, Pin.IN), Pin(echo_pinR, Pin.IN))
    # Ensure trigger is low initially
    trigger.low()
    sleep_us(200)

    # Send a 10 microsecond pulse to the trigger pin
    trigger.high()
    sleep_us(10)
    trigger.low()
    
    sound_speed = 0.0343
    distances = (time_pulse_us(echo, Pin.high) for echo in echos)
    
    return (dist * sound_speed / 2 for dist in distances)

stopDistance=50

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
    
stopDist=50
while True:
    sleep(0.1)
    distance_left, distance_mid, distance_right = getDistance(ECHO_LEFT, ECHO_MIDDLE, ECHO_RIGHT, TRIGGER_PIN)

    print("%.2f \t %.2f \t %.2f" %(distance_left, distance_mid, distance_right))
    