import RPi.GPIO as GPIO
import time
import board
from adafruit_as7341 import AS7341

i2c = board.I2C()       #I2C Address for sensor is 0x39
sensor = AS7341(i2c)

LedPin = 18     # define the LedPin (GPIO18)

GPIO.setwarnings(False)

# Get user input for the duty cicle
setDutyCycle = int(input("Set the desired duty cycle for the PWM: "))

def setup():
    global p
    GPIO.setmode(GPIO.BCM)       # use GPIO Numbering
    GPIO.setup(LedPin, GPIO.OUT)   # set LedPin to OUTPUT mode
    GPIO.output(LedPin, GPIO.LOW)  # make ledPin output LOW level to turn off LED 

    p = GPIO.PWM(LedPin, 500)      # set PWM Frequence to 500Hz
    p.start(0)                     # set initial Duty Cycle to 0

def loop():
    while True:
        for dc in range(0, 101, 1):   # make the led brighter
            p.ChangeDutyCycle(setDutyCycle)     # set dc value as the duty cycle
            time.sleep(0.01)
        time.sleep(1)
        print("F1 - 415nm/Violet  %s" % sensor.channel_415nm)
        print("F2 - 445nm//Indigo %s" % sensor.channel_445nm)
        print("F3 - 480nm//Blue   %s" % sensor.channel_480nm)
        print("F4 - 515nm//Cyan   %s" % sensor.channel_515nm)
        print("F5 - 555nm/Green   %s" % sensor.channel_555nm)
        print("F6 - 590nm/Yellow  %s" % sensor.channel_590nm)
        print("F7 - 630nm/Orange  %s" % sensor.channel_630nm)
        print("F8 - 680nm/Red     %s" % sensor.channel_680nm)
        print('\n')
#         for dc in range(100, -1, -1): # make the led darker
#             p.ChangeDutyCycle(dc)     # set dc value as the duty cycle
# #             print("second for loop")
#             time.sleep(0.01)
#         time.sleep(1)

def destroy():
    p.stop() # stop PWM
    GPIO.cleanup() # Release all GPIO

if __name__ == '__main__':     # Program entrance
    print ('Program is starting ... ')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()