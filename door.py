import HD44780 as LCD
import time
import RPi.GPIO as GPIO
import requests
import argparse

#使用するGPIOポートを指定する
switch = 17
servo = 4

#設定を読み込む
lcd = LCD.HD44780('lcdsample.conf')
lcd.init()

#初期化
GPIO.setmode(GPIO.BCM)

#ポートの使用用途の選択
GPIO.setup(switch,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(servo,GPIO.OUT)
Servo = GPIO.PWM(servo,50)
Servo.start(0)

def lineNotify(message, *args):
    #APIとトークンを入力
    line_notify_api = ''
    line_notify_token = ''
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}
    if len(args) == 0:
        requests.post(line_notify_api, data=payload, headers=headers)
    else:
        files={'image'}
        requests.post(line_notify_api, data=payload, headers=headers,files=files)
    image_url = r"picture_data.jpg"


def servo_angle(angle):
    duty = 2.5+(12.0-2.5)*(angle+90)/180
    Servo.ChangeDutyCycle(duty)
    time.sleep(0.3)
    
try:
    while True:
        lcd.message('　　 ボタンヲオシテクダサイ',2)
        if GPIO.input(switch) == GPIO.HIGH:
            lineNotify("ロックが解除されました。",image_url)
            camera.camera()
            lcd.message('        OPEN  ',3)
            lcd.message('　　　                   ',2)
            servo_angle(-90)
            second = 10
            for num in range(10):
                second -= 1
                lcd.message(f'    シマルマデ {second}ビョウ',4)
                time.sleep(1)
            lineNotify("再度ロックされました。")
        else:
            lcd.message('       CLOSE ',3)
            lcd.message('                           ',4)
            servo_angle(90)
        
except keyboardInterrupt:
    Sarvo.stop()
    pass

GPIO.cleanup()

