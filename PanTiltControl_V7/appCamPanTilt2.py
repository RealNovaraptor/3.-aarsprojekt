import os
import datetime
import time
from flask import Flask, render_template, request, Response
from picamera import PiCamera
import subprocess

# (requires picamera package from Miguel Grinberg)
from camera_pi import Camera

app = Flask(__name__)

# Global variables definition and initialization
global panServoAngle
global tiltServoAngle
panServoAngle = 90
tiltServoAngle = 90


panPin = 27
tiltPin = 17

@app.route("/")
def home():
	return render_template("video.html")

@app.route('/index')
def photo():
    """photo page."""
    return render_template('photo.html')


@app.route('/photo/')
def Capture():
	time.sleep(0.4)
	timestamp = datetime.datetime.now()
	#date and time format: dd/mm/YYYY H:M:S
	format = "%d-%m-%Y-%H-%M-%S"
	#format datetime using strftime() 
	timestamp = timestamp.strftime(format)
	cmd = f'raspistill --width 1920 --height 1080 -vf -o /home/gruppe6/Pictures/{timestamp}.jpeg'
	subprocess.call(cmd, shell=True)
	print(cmd)
	return render_template('photo.html', timestamp = timestamp)

@app.route("/video")
def video():
    """Video streaming home page."""
    return render_template('video.html')

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    else: 
        print("paused")

@app.route('/video_feed')
def video_feed():
	"""Video streaming route. Put this in the src attribute of an img tag."""
	return Response(gen(Camera()),
					mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/<servo>/<angle>")
def move(servo, angle):
	global panServoAngle
	global tiltServoAngle
	if servo == 'pan':
		if angle == '+':
			panServoAngle = panServoAngle + 10
		else:
			panServoAngle = panServoAngle - 10
		os.system("python3 angleServoCtrl.py " + str(panPin) + " " + str(panServoAngle))
	if servo == 'tilt':
		if angle == '+':
			tiltServoAngle = tiltServoAngle + 10
		else:
			tiltServoAngle = tiltServoAngle - 10
		os.system("python3 angleServoCtrl.py " + str(tiltPin) + " " + str(tiltServoAngle))
	
	templateData = {
      'panServoAngle'	: panServoAngle,
      'tiltServoAngle'	: tiltServoAngle
	}
	return render_template('video.html', **templateData)


if __name__ == '__main__':
    app.run(host='192.168.137.81', port =80, debug=True, threaded=True)
