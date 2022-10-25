from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pan = 22
GPIO.setup(pan, GPIO.OUT) # gray ==> PAN

def setServoAngle(servo, angle):
	assert angle >=0 and angle <= 180
	pwm = GPIO.PWM(servo, 44)
	pwm.start(8)
	dutyCycle = angle / 18. + 1.
	pwm.ChangeDutyCycle(dutyCycle)
	sleep(0.3)
	pwm.stop()
if __name__ == '__main__':  
    #for i in range (0, 180, 15):
    #    setServoAngle(pan, i)
    
    for i in range (180, 0, -9):
        setServoAngle(pan, i)
        
    setServoAngle(pan, 0)  
    GPIO.cleanup()