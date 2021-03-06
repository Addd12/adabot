# Adabot: line-following robot that detects objects on the way
Adabot is a Raspberry Pi project with the following functionalities: 
  - line-following
  - object detection
  - object sensing  

Raspberry Pi (also referred to as "the board") 4 model B with 4GB, a sufficient memory amount to successfully finish this project. It has its own operating system named Raspberry Pi OS, which is Linux based. Considering that, the project can be developed directly from Raspberry Pi and this project was developed in Visual Studio Code IDE.  
# Set up
The set up of the Raspberry Pi OS can be completed by following the instructions of [their official page](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up).  
# Line-following
The code for this task can be found on the robot.py file. It can be run using `python3 robot.py`. For this task I have used 2 IR sensors that are connected to the board through the GPIO pins using jumper wires.  
# Object detection 
After the successful installation of the Raspberry Pi OS you can get the code by running 
> git clone https://github.com/Addd12/adabot.git  

Then install the requitements through 

> pip install -r requirements.txt    

After these steps are completed, make sure your teminal is on the correct directory and run the commands from command.txt.  

# Sensing objects 
An UDS of type HC-SR04 is used. This type of UDS requires 5V in order to work and considering the maximum voltage input that the Raspberry Pi can handle, two resistors are used to separate the voltage.  
The object-sensing and line-following instructions are integrated together, so while following the line, if the robot faces an object at a distance of 20 cm or less, it stops.

# Youtube video
https://www.youtube.com/watch?v=62L8LD1m0m4
