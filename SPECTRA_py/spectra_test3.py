import RPi.GPIO as GPIO
import time
import board
import drivers
from adafruit_as7341 import AS7341

# Load the driver and set it to "display" (For LCD)
# If you use something from the driver library use the "display." prefix first
#display = drivers.Lcd(0x27) # set I2C address for LCD screen
display = drivers.Lcd()

i2c = board.I2C()       #I2C Address for sensor is 0x39
sensor = AS7341(i2c)

LedPin = 18     # define the LedPin (GPIO18)

GPIO.setwarnings(False)

setDutyCycle = 0

def setup():
    global p
    GPIO.setmode(GPIO.BCM)       # use GPIO Numbering
    GPIO.setup(LedPin, GPIO.OUT)   # set LedPin to OUTPUT mode
    GPIO.output(LedPin, GPIO.LOW)  # make ledPin output LOW level to turn off LED 

    p = GPIO.PWM(LedPin, 500)      # set PWM Frequence to 500Hz
    p.start(0)                     # set initial Duty Cycle to 0
    
    GPIO.setup(26, GPIO.IN)        # Set gpio 26 as input
    GPIO.setup(6, GPIO.IN)         # Set gpio 6 as input

def display_on_lcd(data, line):                    # Function for siplaying message on LCD
    #display.lcd_clear()                      # Clear the screen
    display.lcd_display_string(data, line)      # Display the desired message


def loop():
    global setDutyCycle
    while True:
#         for dc in range(0, 101, 1):   
#             p.ChangeDutyCycle(setDutyCycle)  # change the duty cycle based on user input
#             time.sleep(0.01)
        #time.sleep(1)
        p.ChangeDutyCycle(setDutyCycle)  # change the duty cycle based on user input
        # Print to terminal
        print("F1 - 415nm/Violet  %s" % sensor.channel_415nm)
        print("F2 - 445nm//Indigo %s" % sensor.channel_445nm)
        print("F3 - 480nm//Blue   %s" % sensor.channel_480nm)
        print("F4 - 515nm//Cyan   %s" % sensor.channel_515nm)
        print("F5 - 555nm/Green   %s" % sensor.channel_555nm)
        print("F6 - 590nm/Yellow  %s" % sensor.channel_590nm)
        print("F7 - 630nm/Orange  %s" % sensor.channel_630nm)
        print("F8 - 680nm/Red     %s" % sensor.channel_680nm)
        print('\n')
        
        # Print to LCD screen
        data_630nm = "630nm: {}".format(sensor.channel_630nm)
        display_on_lcd(data_630nm, 1)
        dutyCycle = "Duty Cycle: {}".format(setDutyCycle)
        display_on_lcd(dutyCycle.rjust(3), 2)
        
        # Reading the buttons
        button1 = GPIO.input(26)  # reading button voltage from GPIO 26
        button2 = GPIO.input(6)   # reading button voltage from GPIO 6
        #print("Button1: {}, Button2: {}".format(button1, button2))
        if button1:
            setDutyCycle = setDutyCycle + 1
            if setDutyCycle > 100:
                setDutyCycle = 100
        elif button2:
            setDutyCycle = setDutyCycle - 1
            if setDutyCycle < 0:
                setDutyCycle = 0
        else:
            setDutyCycle = setDutyCycle
        time.sleep(0.1)
#         

def destroy():
    p.stop() # stop PWM
    GPIO.cleanup() # Release all GPIO

if __name__ == '__main__':     # Program entrance
    print ('Program is starting ... ')
    # Get user input for the duty cicle
    setDutyCycle = int(input("Set the desired duty cycle for the PWM: "))

    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        destroy()