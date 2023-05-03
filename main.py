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



led = Pin(25, Pin.OUT)

# motor_a ports
ina1 = Pin(11, Pin.OUT)
ina2 = Pin(10, Pin.OUT)
pwm_a = PWM(Pin(12))

# motor_b ports
inb1 = Pin(15, Pin.OUT)
inb2 = Pin(13, Pin.OUT)
pwm_b = PWM(Pin(14))

pwm_a.freq(10000)
pwm_b.freq(10000)

def left_motor_forward(duty):
    inb1.value(0)
    inb2.value(1)
    duty_16 = int((duty * 65536) / 100)
    #print("motor esquerdo", duty_16)
    pwm_b.duty_u16(duty_16)
    
def left_motor_backward(duty):
    inb1.value(1)
    led.value(1)
    inb2.value(0)
    duty_16 = int((duty * 65536) / 100)
    pwm_b.duty_u16(duty_16)

def stop_left_motor():
    pwm_b.duty_u16(0)
    inb2.value(0)
    inb1.value(0)

def right_motor_forward(duty):
    ina1.value(0)
    ina2.value(1)
    led.value(0)
    duty_16 = int((duty * 65536) / 100)
    #print("motor direito", duty_16)
    pwm_a.duty_u16(duty_16)

def right_motor_backward(duty):
    ina1.value(1)
    ina2.value(0)
    duty_16 = int((duty * 65536) // 100)
    pwm_a.duty_u16(duty_16)

def stop_right_motor():
    inb1.value(0)
    inb2.value(0)
    pwm_a.duty_u16(0)
    
# Forward
def move_forward(duty):    
    right_motor_forward(duty)
    left_motor_forward(duty)
    
# Backward
def move_backward(duty):
    left_motor_backward(duty)
    right_motor_backward(duty)
    
#Turn Left
def turn_left(duty):
    right_motor_backward(duty)
    left_motor_forward(duty)
    
#Turn Right
def turn_right(duty):
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

def getDistance(ECHO_PIN,TRIGGER_PIN):
    
    
    trigger = Pin(TRIGGER_PIN, Pin.OUT)
    echo = Pin(ECHO_PIN, Pin.IN)
    # Ensure trigger is low initially
    trigger.low()
    sleep_us(2)

    # Send a 10 microsecond pulse to the trigger pin
    trigger.high()
    sleep_us(10)
    trigger.low()

    # Measure the duration of the echo pulse (in microseconds)
    pulse_duration = time_pulse_us(echo, Pin.high)

    # Calculate the distance (in centimeters) using the speed of sound (343 m/s)
    distance = pulse_duration * 0.0343 / 2
    return distance

stopDistance=50

# sleep(10)
def test(M):
    print(0)
    test_left(M)
    stop()
    sleep(1)
    test_right(M)
    stop()
    sleep(1)
    
    move_forward(M)
    sleep(1)
    move_backward(M)
    sleep(1)
    turn_right(M)
    sleep(1)
    turn_left(M)
    sleep(1)
    stop()
    
if True:
    test(M)
stopDist=50    
while True:

    distance_mid = getDistance(7,6)
    
    if(distance_mid >= stopDist) :
        move_forward()

    while(distance_mid >= stopDist):
        distance_mid = getDistance(7,6)

    stop()

    distance_left = getDistance(9,8)
    distance_right = getDistance(5,4)

    if (distance_left>=200 and distance_right>=200):
        turn_left(M)
        sleep(0.4)
    elif (distance_left<=stopDist and distance_right<=stopDist):
        turn_left(M)
        sleep(0.8)
    elif (distance_left>=distance_right):
        turn_left(M)
        sleep(0.4)
    elif (distance_left<distance_right):
        turn_right(M)
        sleep(0.4)


