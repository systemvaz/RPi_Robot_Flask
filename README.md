# RPi_Robot #
Robotics project utilising Rasberry Pi 4B, motor controllers and various sensors.
Making it up as I go, so it's a work in progresss....

## Current Hardware: ##
* Rasberry Pi 4b 8GB ram - Overclocked to 2Ghz - Heatsink and dual fans
* Logitec HD 720p webcam
* max7219 8x8 Red LED Matrix
* L298N Dual Motor Controller
* 4 x Geard Motors
* Ultrasonic Distance Sensor
* Onboard batteries for power to motors and RPi
* USB hub to route power to the RPi. Going to replace with a USB power bank to supply more power, eg. 5v 3A

## Current Software & Functionality ##
* Raspberry Pi OS Lite
* Basic motor control
* Multi object detection and recognition via webcam
* Face detection and recognition + expression recognition via webcam
* LED matrix displays different faces mimicking the humans expression (I don't know, it just seemed fun / a good test lol)
* Flask web application for remote viewing via network
* Python 3.7.3, Tensorflow lite runtime, OpenCV

![Robo](https://github.com/systemvaz/RPi_Robot/blob/master/Robot/lib/img/robo.jpg)
![Robo](https://github.com/systemvaz/RPi_Robot/blob/master/Robot/lib/img/robo2.jpg)
![Robo](https://github.com/systemvaz/RPi_Robot/blob/master/Robot/lib/img/vision-test.jpg)
