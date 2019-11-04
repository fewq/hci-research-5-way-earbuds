import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # left
GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # center
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # up
GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # right
GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)	# down

while True:
	time.sleep(0.1) # set a delay between commands
	if GPIO.input(40) == GPIO.HIGH:
		print("LEFT")
	elif GPIO.input(38) == GPIO.HIGH:
		print("CENTER")
	elif GPIO.input(37) == GPIO.HIGH:
		print("UP")
	elif GPIO.input(35) == GPIO.HIGH:
		print("RIGHT")		
	elif GPIO.input(33) == GPIO.HIGH:
		print("DOWN")
