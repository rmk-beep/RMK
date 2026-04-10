import RPi.GPIO as GPIO
import time

TRIG = 20
ECHO = 21

OBSTACLE_DISTANCE_CM = 25   # trigger avoidance below this distance


def setup():
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)
    time.sleep(0.5)   # let sensor settle


def get_distance_cm():
    """Return distance in cm. Returns 999 on timeout."""
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start = time.time()
    timeout = start + 0.04   # 40 ms timeout

    while GPIO.input(ECHO) == 0:
        start = time.time()
        if start > timeout:
            return 999

    while GPIO.input(ECHO) == 1:
        end = time.time()
        if end > timeout:
            return 999

    duration = end - start
    distance = (duration * 34300) / 2   # speed of sound: 343 m/s
    return round(distance, 1)


def obstacle_detected():
    return get_distance_cm() < OBSTACLE_DISTANCE_CM
