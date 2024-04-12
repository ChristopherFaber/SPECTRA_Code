import RPi.GPIO as GPIO
import time
import board
import drivers
import numpy as np
import matplotlib.pyplot as plt
from adafruit_as7341 import AS7341

# Functions -------------------------------------------------------------------------------------------------------------------

def setup():
    global p
    GPIO.setmode(GPIO.BCM)         # use GPIO Numbering
    GPIO.setup(LedPin, GPIO.OUT)   # set LedPin to OUTPUT mode
    GPIO.output(LedPin, GPIO.LOW)  # make ledPin output LOW level to turn off LED 

    p = GPIO.PWM(LedPin, 500)      # set PWM Frequence to 500Hz
    p.start(0)                     # set initial Duty Cycle to 0
    
    #GPIO.setup(26, GPIO.IN)        # Set gpio 26 as input
    #GPIO.setup(6, GPIO.IN)         # Set gpio 6 as input
    GPIO.setup(StartButton, GPIO.IN) # Set GPIO5 as an input for the "start test" button
    GPIO.setup(ContButton, GPIO.IN) # Set GPIO6 as an input for the "continue" button

def wait():
    print("Waiting for experiment")
    display_on_lcd("WAITING FOR", 1)
    display_on_lcd("EXPERIMENT", 2)
    while True:
        if GPIO.input(StartButton) == GPIO.HIGH:
            display.lcd_clear()
            break

def wait2():
    print("Press button to continue")
    display.lcd_clear()
    display_on_lcd("PRESS BUTTON", 1)
    display_on_lcd("TO CONTINUE", 2)
    while True:
        if GPIO.input(ContButton) == GPIO.HIGH:
            display.lcd_clear()
            break

def display_on_lcd(data, line):               # Function for siplaying message on LCD
    #display.lcd_clear()                      # Clear the screen
    display.lcd_display_string(data, line)    # Display the desired message
    
def PWM_calibration():
    global setDutyCycle
    setDutyCycle = 100
    
    display_on_lcd("SARTING PROGRAM",1)
    display_on_lcd("CALIBRATING LED", 2)
    
    # Start with the initial duty cycle
    p.ChangeDutyCycle(setDutyCycle)
    
    # Check if all sensor values are below the threshold (to avoid saturation)
    while True:
        #measure = [sensor.channel_415nm, sensor.channel_445nm, sensor.channel_480nm, sensor.channel_515nm, sensor.channel_555nm, sensor.channel_590nm, sensor.channel_630nm, sensor.channel_680nm]
        measure1 = np.array([sensor.channel_415nm, sensor.channel_445nm, sensor.channel_480nm, sensor.channel_515nm, sensor.channel_555nm, sensor.channel_590nm, sensor.channel_630nm, sensor.channel_680nm])
        measure2 = np.array([sensor.channel_415nm, sensor.channel_445nm, sensor.channel_480nm, sensor.channel_515nm, sensor.channel_555nm, sensor.channel_590nm, sensor.channel_630nm, sensor.channel_680nm])
        measure3 = np.array([sensor.channel_415nm, sensor.channel_445nm, sensor.channel_480nm, sensor.channel_515nm, sensor.channel_555nm, sensor.channel_590nm, sensor.channel_630nm, sensor.channel_680nm])
        #measure4 = np.array([sensor.channel_415nm, sensor.channel_445nm, sensor.channel_480nm, sensor.channel_515nm, sensor.channel_555nm, sensor.channel_590nm, sensor.channel_630nm, sensor.channel_680nm])
        #measure5 = np.array([sensor.channel_415nm, sensor.channel_445nm, sensor.channel_480nm, sensor.channel_515nm, sensor.channel_555nm, sensor.channel_590nm, sensor.channel_630nm, sensor.channel_680nm])
        #measure6 = np.array([sensor.channel_415nm, sensor.channel_445nm, sensor.channel_480nm, sensor.channel_515nm, sensor.channel_555nm, sensor.channel_590nm, sensor.channel_630nm, sensor.channel_680nm])
        
        average = (measure1 + measure2 + measure3)/3 #+ measure4 + measure5 + measure6) / 6
        
        # Check if all sensor values are below 65535
        if all(value < 65000 for value in average):
            print(average)
            print(setDutyCycle)
            break # Exit the loop if all values are below the threshold
        
        # Decrease the duty cycle by 1
        setDutyCycle -= 5
        p.ChangeDutyCycle(setDutyCycle)
        print("Changed duty cycle")
        # Wait for a short time before taking the next measurement
        #time.sleep(0.1)
    display.lcd_clear()
    display_on_lcd("CALIBRATION",1)
    display_on_lcd("COMPLETE",2)
    
    time.sleep(1.5)

def loop():
    #global setDutyCycle
    
    while True:
        
        #p.ChangeDutyCycle(setDutyCycle)  # change the duty cycle based on user input
        print("Input calibration solution")
        display.lcd_clear()
        display_on_lcd("INPUT SOLUTION", 1)
        display_on_lcd("FOR CALIBRATION", 2)
        time.sleep(5)
        
        print()
        wait2() # wait for "continue" button to be pressed
        print()
        
        print("Taking base measurement...")
        display.lcd_clear()
        display_on_lcd("TAKING BASELINE", 1)
        display_on_lcd("MEASUREMENT...", 2)
        #time.sleep(0.5)
        
        measure1 = np.array([sensor.channel_415nm, sensor.channel_445nm, sensor.channel_480nm, sensor.channel_515nm, sensor.channel_555nm, sensor.channel_590nm, sensor.channel_630nm, sensor.channel_680nm])
        measure2 = np.array([sensor.channel_415nm, sensor.channel_445nm, sensor.channel_480nm, sensor.channel_515nm, sensor.channel_555nm, sensor.channel_590nm, sensor.channel_630nm, sensor.channel_680nm])
        measure3 = np.array([sensor.channel_415nm, sensor.channel_445nm, sensor.channel_480nm, sensor.channel_515nm, sensor.channel_555nm, sensor.channel_590nm, sensor.channel_630nm, sensor.channel_680nm])
        measure4 = np.array([sensor.channel_415nm, sensor.channel_445nm, sensor.channel_480nm, sensor.channel_515nm, sensor.channel_555nm, sensor.channel_590nm, sensor.channel_630nm, sensor.channel_680nm])
        measure5 = np.array([sensor.channel_415nm, sensor.channel_445nm, sensor.channel_480nm, sensor.channel_515nm, sensor.channel_555nm, sensor.channel_590nm, sensor.channel_630nm, sensor.channel_680nm])
        measure6 = np.array([sensor.channel_415nm, sensor.channel_445nm, sensor.channel_480nm, sensor.channel_515nm, sensor.channel_555nm, sensor.channel_590nm, sensor.channel_630nm, sensor.channel_680nm])
        
        print(measure1)
        print(measure2)
        print(measure3)
        print(measure4)
        print(measure5)
        print(measure6)
        print()
        
        time.sleep(1)
        
        
        print("Input sample")
        display.lcd_clear()
        display_on_lcd("INPUT SAMPLE", 1)
        time.sleep(5)
        
        print()
        wait2() # wait for "contiue button to be pressed
        print()
        
        print("Starting sample measurement...")
        display_on_lcd("STARTING SAMPLE", 1)
        display_on_lcd("MEASUREMENT...", 2)
        #time.sleep(2)
        measure7 = np.array([sensor.channel_415nm, sensor.channel_445nm, sensor.channel_480nm, sensor.channel_515nm, sensor.channel_555nm, sensor.channel_590nm, sensor.channel_630nm, sensor.channel_680nm])
        measure8 = np.array([sensor.channel_415nm, sensor.channel_445nm, sensor.channel_480nm, sensor.channel_515nm, sensor.channel_555nm, sensor.channel_590nm, sensor.channel_630nm, sensor.channel_680nm])
        measure9 = np.array([sensor.channel_415nm, sensor.channel_445nm, sensor.channel_480nm, sensor.channel_515nm, sensor.channel_555nm, sensor.channel_590nm, sensor.channel_630nm, sensor.channel_680nm])
        measure10 = np.array([sensor.channel_415nm, sensor.channel_445nm, sensor.channel_480nm, sensor.channel_515nm, sensor.channel_555nm, sensor.channel_590nm, sensor.channel_630nm, sensor.channel_680nm])
        measure11 = np.array([sensor.channel_415nm, sensor.channel_445nm, sensor.channel_480nm, sensor.channel_515nm, sensor.channel_555nm, sensor.channel_590nm, sensor.channel_630nm, sensor.channel_680nm])
        measure12 = np.array([sensor.channel_415nm, sensor.channel_445nm, sensor.channel_480nm, sensor.channel_515nm, sensor.channel_555nm, sensor.channel_590nm, sensor.channel_630nm, sensor.channel_680nm])
        
        print(measure7)
        print(measure8)
        print(measure9)
        print(measure10)
        print(measure11)
        print(measure12)
        print()
        
        average1 = (measure1 + measure2 + measure3 + measure4 + measure5 + measure6)/6
        average2 = (measure7 + measure8 + measure9 + measure10 + measure11 + measure12)/6
        absorption = average1 - average2
        
#         print("Average 1: ", average1)
#         print()
#         print("Average 2: ", average2)
#         print()
#         print("Absorption detected: ", absorption)
#         print()
        
        # Convert arrays to strings with fixed width for each element
        average1_str = ["{:<12.3f}".format(num) for num in average1]
        average2_str = ["{:<12.3f}".format(num) for num in average2]
        absorption_str = ["{:0<10.4f}".format(num) for num in absorption]

        # Print the formatted arrays
        print("Average 1:", " ".join(average1_str))
        print()
        print("Average 2:", " ".join(average2_str))
        print()
        print("Absorption detected:", " ".join(absorption_str))
        print()
        
        # Create subplots
        fig, axs = plt.subplots(3,1) # 3 rows, 1 column
        
        wavelengths = np.array([415, 445, 480, 515, 555, 590, 630, 680])
        
        # First Subplot
        axs[0].plot(wavelengths, average1, marker='o', linestyle='-')
        axs[0].set_xlabel('Wavelength (nm)')
        axs[0].set_ylabel('Absorption')
        axs[0].set_title("Base Measurement")
        axs[0].grid(True)
        #axs[0].show()
        
        # Second subplot
        axs[1].plot(wavelengths, average2, marker='o', linestyle='-')
        axs[1].set_xlabel('Wavelength (nm)')
        axs[1].set_ylabel('Absorption')
        axs[1].set_title("Sample Measurement")
        axs[1].grid(True)
        #axs[1].show()
        
        # Third subplot
        axs[2].plot(wavelengths, absorption, marker='o', linestyle='-')
        axs[2].set_xlabel('Wavelength (nm)')
        axs[2].set_ylabel('Absorption')
        axs[2].set_title("Total Absorption")
        axs[2].grid(True)
        #axs[2].show()
        
        plt.tight_layout() # Adjust layout to prevent overlap
        plt.show()#block=False)
        
        if absorption[6] > absorption[7] and absorption[6] > absorption[4] and absorption[6] > absorption[5] and absorption[6] >= 2000:
            print("Malaria Detected")
            display.lcd_clear()
            display_on_lcd("MALARIA DETECTED", 1)
        else:
            print("No Malaria Detected")
            display.lcd_clear()
            display_on_lcd("NO MALARIA", 1)
            display_on_lcd("DETECTED", 2)
        
        break
         

def destroy():
    p.stop() # stop PWM
    GPIO.cleanup() # Release all GPIO

# Main Code ------------------------------------------------------------------------------------------------------------------

# Load the driver and set it to "display" (For LCD)
# If you use something from the driver library use the "display." prefix first
#display = drivers.Lcd(0x27) # set I2C address for LCD screen
display = drivers.Lcd()  #I2C address for LCD is 0x27

i2c = board.I2C()       #I2C Address for sensor is 0x39
sensor = AS7341(i2c)

LedPin = 18     # define the LedPin (GPIO18)
StartButton = 5 # define the "Start Test" button (GPIO5)
ContButton = 6  # define the "Continue" button (GPIO6)

GPIO.setwarnings(False)

setDutyCycle = 0

if __name__ == '__main__':     # Program entrance
    
    setup()  # set up all the GPIO ports
    
    while True:
        wait()   # wait for user to start experiment
    
        print ('Program is starting ... ')
    
    # Get user input for the duty cicle
    #setDutyCycle = int(input("Set the desired duty cycle for the PWM: "))
        print ("Calibrating SPECTRA")
    
        PWM_calibration()    # call function to set the correct duty cycle
    
        print("Calibration complete!")

        time.sleep(2)
    
        try:
            loop()    # take control and sample measurements
        
        except KeyboardInterrupt:  # Press ctrl-c to end the program.
            destroy()
            
        time.sleep(2)

