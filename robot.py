# pythyon3
# Code available at https://github.com/Addd12/adabot
"""Line following robot that senses the presence of objects in front"""
import gpiozero
from gpiozero import Robot
from gpiozero import InputDevice, OutputDevice
from time import sleep, time

# create robot object and specify pin numbers (motor connetion)
robot = gpiozero.Robot(left=(7,8), right=(9,10))
# line detecting sensors
left = gpiozero.DigitalInputDevice(17)
right = gpiozero.DigitalInputDevice(27)

speed = 0.3 # motor speed
RUNTIME = 90

# distance sensor
trig = OutputDevice(4)
echo = InputDevice(15)
sleep(2)

def get_pulse_time():
    """Record the time the burst of the sound was sent and received - calculate the time it took"""
    trig.on()
    sleep(0.00001)
    trig.off()
    
    while echo.is_active == False:
        pulse_start = time()
        
    while echo.is_active == True:
        pulse_end = time()
        
    sleep(0.06)
    difference = pulse_end - pulse_start
    
    return difference

def get_distance(duration):
    """Calculate distance using the formula and the known parameters"""
    sound_speed = 343 # the speed of sound in air 
    distance = sound_speed * duration / 2
    return distance


def motor_control(): # if any of the sensors detects the line before running, it gives error
    """Give instructions to the motors based on the sensors' input"""
    while True:
        
        while True:
            duration = get_pulse_time()
            distance = get_distance(duration)
            print(distance)

            if distance > 0.2:
                if (left.is_active == False) and (right.is_active == False):
                    # drive forward
                    left_mot = 1
                    right_mot = 1
                # line detected
                elif (left.is_active == False) and (right.is_active == True):
                    # drive backwards 
                    left_mot = -1
                elif (left.is_active == True) and (right.is_active == False):
                    # drive backwards 
                    right_mot = -1
                else:
                    # stop spinning when the sensors are inactive
                    left_mot = 0
                    right_mot = 0
            else:
                left_mot = 0
                right_mot = 0
            
            yield (right_mot * speed, left_mot * speed)

robot.source = motor_control()

sleep(RUNTIME)
