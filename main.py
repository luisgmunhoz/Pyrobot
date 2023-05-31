from machine import Pin  # type: ignore
from machine import time_pulse_us  # type: ignore
from time import sleep  # type: ignore
from hcsr04 import HCSR04

# Importa a biblioteca utime para usar funções relacionadas ao tempo
import utime  # type: ignore

# Define the GPIO pin numbers for the trigger and echo pins
TRIGGER_PIN = 1
ECHO_LEFT = 4
ECHO_MIDDLE = 3
ECHO_RIGHT = 2
# Initialize trigger and echo pins

# motor_a (esquerda) ports
ina1 = Pin(11, Pin.OUT)  # Marrom
ina2 = Pin(10, Pin.OUT)  # Verde

# motor_b (direita) ports
inb1 = Pin(15, Pin.OUT)  # Branco
inb2 = Pin(14, Pin.OUT)  # Lilás


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


# Turn Left
def turn_right():
    right_motor_backward()
    left_motor_forward()


# Turn Right
def turn_left():
    left_motor_backward()
    right_motor_forward()


# Stop
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


def get_distance(echo_pinL, echo_pinM, echo_pinR, trigger_pin):
    sleep(0.1)
    trigger = Pin(trigger_pin, Pin.OUT)

    echos = (Pin(echo_pinL, Pin.IN), Pin(echo_pinM, Pin.IN), Pin(echo_pinR, Pin.IN))
    # Ensure trigger is low initially
    trigger.low()
    sleep(2 * 10 ** (-6))

    # Send a 10 microsecond pulse to the trigger pin
    trigger.high()
    sleep(10 * 10 ** (-6))
    trigger.low()

    sound_speed = 0.0343

    return (time_pulse_us(echo, 1) * sound_speed / 2 for echo in echos)


def test():
    move_forward()
    sleep(1)
    stop()
    sleep(1)
    move_backward()
    sleep(1)
    stop()
    sleep(1)
    turn_left()
    sleep(1)
    stop()
    sleep(1)
    turn_right()


stop_dist = 5
# Define os pinos do Raspberry Pi Pico conectados ao módulo HC-SR04
hcsr04_trigger_pin = TRIGGER_PIN
hcsr04_echo_pinL = ECHO_LEFT
hcsr04_echo_pinM = ECHO_MIDDLE
hcsr04_echo_pinR = ECHO_RIGHT


# Define o timeout para o módulo HC-SR04 em ms
hcsr04_timeout_ms = 20

hcsr04_sensorL = HCSR04(hcsr04_trigger_pin, hcsr04_echo_pinL, hcsr04_timeout_ms)
hcsr04_sensorM = HCSR04(hcsr04_trigger_pin, hcsr04_echo_pinM, hcsr04_timeout_ms)
hcsr04_sensorR = HCSR04(hcsr04_trigger_pin, hcsr04_echo_pinR, hcsr04_timeout_ms)
while True:
    distance_left = hcsr04_sensorL.get_distance_cm()
    distance_mid = hcsr04_sensorM.get_distance_cm()
    distance_right = hcsr04_sensorR.get_distance_cm()
    utime.sleep(1)

    print(f"{distance_left:.2f} \t {distance_mid:.2f} \t {distance_right:.2f}")

    if distance_mid > stop_dist:
        move_forward()
        sleep(0.2)
    else:
        stop()
        sleep(0.2)

    if (
        distance_left >= stop_dist
        and distance_right >= stop_dist
        and distance_mid < stop_dist
    ):
        turn_left()
        sleep(0.2)
    elif (
        distance_left >= stop_dist
        and distance_right < stop_dist
        or distance_left >= distance_right
        and distance_mid < stop_dist
    ):
        turn_left()
        sleep(0.2)
    elif distance_left < distance_right and distance_mid < stop_dist:
        turn_right()
        sleep(0.2)
