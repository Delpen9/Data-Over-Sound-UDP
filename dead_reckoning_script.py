import numpy as np
import RPi.GPIO as GPIO
from time import sleep

# turn_or_move: "turn" or "move"
# angle_or_distance: (e.g. -90/90 or -10/10)
# Negative values correspond to reverse direction
def basic_movement(turn_or_move, angle_or_distance):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # Left motor
    GPIO.setup(22, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
    
    # Right motor
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)
    
    if (turn_or_move == "turn"):
        if (angle_or_distance < 0):
            # Determines direction of left motor
            GPIO.output(22, True)
            # Determines direction of the right motor
            GPIO.output(23, False)
        else:
            # Determines direction of left motor
            GPIO.output(22, False)
            # Determines direction of the right motor
            GPIO.output(23, True)  

        # Turns on left motor
        GPIO.output(27, True)
        # Turns on right motor
        GPIO.output(24, True)

        # TODO: this will require some testing
        time = np.abs(angle_or_distance)/45
        sleep(time)  
        
    elif (turn_or_move == "move"):
        if (angle_or_distance < 0):
            # Determines direction of left motor
            GPIO.output(22, False)
            # Determines direction of the right motor
            GPIO.output(23, False)
        else:
            # Determines direction of left motor
            GPIO.output(22, True)
            # Determines direction of the right motor
            GPIO.output(23, True)          

        # Turns on left motor
        GPIO.output(27, True)
        # Turns on right motor
        GPIO.output(24, True)
        
        # TODO: this will require some testing
        time = np.abs(angle_or_distance)/2
        sleep(time)
        
    # Turns motors off
    GPIO.output(27, False)
    GPIO.output(24, False)

    GPIO.cleanup()

