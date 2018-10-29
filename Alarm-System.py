import requests, datetime
from gpiozero import MotionSensor
from picamera import PiCamera
from signal import pause
from time import sleep
camera = PiCamera()

pir = MotionSensor(17)
print("ALARM Starting")
sleep(10)

def send_msg():
    timestamp = datetime.datetime.now()
    timestamp = str(timestamp.strftime("%Y-%m-%d %H:%M:%S"))
    print("ALARM TRIGGERED: "+timestamp)
    camera.capture("/home/pi/"+str(timestamp)+".jpg")
    r = requests.post("https://api.pushover.net/1/messages.json", data = {
        "token": "API TOKEN",
        "user": "API USER KEY",
        "message": ("Alert: "+timestamp)
    },
    files = {
      "attachment": (timestamp, open("/home/pi/"+timestamp+".jpg", "rb"), "image/jpeg")
    })
    print(r.text)
    sleep(30)

pir.when_motion = send_msg
pause()
