import RPi.GPIO as GPIO
import time
from pygame import mixer

up = 37
down = 35
left = 33
right = 31
center = 29

GPIO.setmode(GPIO.BOARD)
GPIO.setup(up, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(down, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(left, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(right, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(center, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)	

# pygame mixer sound setup
mixer.init() # pygame mixer setup
playlist = ["playlist/song1.mp3", 
			"playlist/song2.mp3", 
			"playlist/song3.mp3",
			"playlist/song4.mp3"]
index = 0

# action song sounds
action_sound = mixer.Sound("action_sounds/menu_accept.wav")
action_sound.set_volume(1)

vol_sound = mixer.Sound("action_sounds/armsrace_kill_01.wav")
vol_sound.set_volume(1)

max_vol_sound = mixer.Sound("action_sounds/weapon_cant_buy.wav")
max_vol_sound.set_volume(1)

change_song_sound = mixer.Sound("action_sounds/beepclear.wav")
change_song_sound.set_volume(1)


first_song_played = False # this is the intial setup
pause_state = False # toggle between pause and unpause
volume = 0.469 #volume is between 0 and 1
max_volume = 1
min_volume = 0.01
volume_granularity = 0.066

pre_action_delay = 0.4
post_action_delay = 0.4

def play_action_sound():
	mixer.music.pause()
	action_sound.play()
	time.sleep(pre_action_delay)
	mixer.music.unpause()
	
def play_change_sound():
	mixer.music.pause()
	change_song_sound.play()
	time.sleep(pre_action_delay)
	mixer.music.unpause()

while True:
	if GPIO.input(up) == GPIO.HIGH:
		vol_sound.play()
		time.sleep(0.1)
		new_volume = volume + volume_granularity
		if new_volume > max_volume: # check that the new volume is within bounds
			max_vol_sound.play()
			pass
		else:
			volume = new_volume
			mixer.music.set_volume(volume)
		print("UP; Volume: {:.2f}".format(volume))
	elif GPIO.input(down) == GPIO.HIGH:
		vol_sound.play()
		time.sleep(0.1)
		new_volume = volume - volume_granularity
		if new_volume < min_volume: # check that the new volume is within bounds
			max_vol_sound.play()
			pass
		else:
			volume = new_volume
			mixer.music.set_volume(volume)
		print("DOWN; Volume: {:.2f}".format(volume))
	elif GPIO.input(left) == GPIO.HIGH:
		play_change_sound()
		index = (index-1)%4 #go back 1 song
		mixer.music.load(playlist[index])
		mixer.music.play()
		pause_state = False
		print("LEFT; ", playlist[index])
	elif GPIO.input(right) == GPIO.HIGH:
		play_change_sound()
		index = (index+1)%4 #go forward 1 song
		mixer.music.load(playlist[index])
		mixer.music.play()
		pause_state = False
		print("RIGHT; ", playlist[index])
	elif GPIO.input(center) == GPIO.HIGH:
		play_action_sound()
		if first_song_played == False:
			mixer.music.load(playlist[index])
			mixer.music.play()
			first_song_played = True
			print("CENTER; play")
		elif first_song_played == True:
			if pause_state == False:
				mixer.music.pause()
				pause_state = True
				print("CENTER; paused")
			elif pause_state == True:
				mixer.music.unpause()
				pause_state = False
				print("CENTER; unpaused")
	# set delay after all events
	time.sleep(post_action_delay)
