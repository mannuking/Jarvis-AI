import time
import threading
import keyboard
import numpy as np
import sounddevice as sd
import speech_recognition as sr
import os
import pyautogui
import subprocess as sp
import webbrowser
import imdb
from kivy.uix import widget,image,label,boxlayout,textinput
from kivy import clock
from constants import SCREEN_HEIGHT,SCREEN_WIDTH,GEMINI_API_KEY
from utils import speak,youtube,search_on_google,search_on_wikipedia,send_email,get_news,weather_forecast,find_my_ip
from jarvis_button import JarvisButton
import google.generativeai as genai
from system_controller import SystemController
import re
import json


genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

class Jarvis(widget.Widget):
    def __init__(self, **kwargs):
        super(Jarvis, self).__init__(**kwargs)
        # Load app paths from json
        try:
            with open("GUI/app_paths.json", 'r') as f:
                self.app_paths = json.load(f)
                # Expand environment variables in paths
                self.app_paths = {k: os.path.expandvars(v) for k, v in self.app_paths.items()}
        except FileNotFoundError:
            print("Warning: app_paths.json not found. Application launching by name might not work.")
            self.app_paths = {}

        # Add new controllers
        self.system_controller = SystemController()
        self.volume = 0
        self.volume_history = [0,0,0,0,0,0,0]
        self.volume_history_size = 140

        self.app_paths = {
            "edge": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Edge.lnk",
            "forza": "C:\\Users\\jk422\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\ForzaHorizon5.lnk",
            "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
            "contra": "C:\\Users\\jk422\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\ContraOG.lnk",
            "file explorer": "C:\\Users\\jk422\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\File Explorer.lnk",
            "mk11": "C:\\Users\\jk422\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\MK11.lnk",
            "brave": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Brave.lnk",
            "drawio": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\draw.io.lnk",
            "sticky notes": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Sticky Notes (new).lnk",
            "onenote": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\OneNote.lnk",
            "epic games launcher": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Epic Games Launcher.lnk",
            "onedrive": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\OneDrive.lnk",
            "google chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "android studio": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Android Studio\\Android Studio.lnk",
            "anydesk": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\AnyDesk\\AnyDesk.lnk",
            "nvidia": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\NVIDIA Corporation\\NVIDIA.lnk",
            "nvidia broadcast": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\NVIDIA Corporation\\NVIDIA Broadcast.lnk",
            "obs studio": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\OBS Studio\\OBS Studio (64bit).lnk",
            "valorant": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Riot Games\\VALORANT.lnk",
            "task manager": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\System Tools\\Task Manager.lnk",
            "gpuview help": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Windows Kits\\Windows Performance Toolkit\\GPUView Help.lnk",
            "gpuview": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Windows Kits\\Windows Performance Toolkit\\GPUView.lnk",
            "windows performance analyzer": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Windows Kits\\Windows Performance Toolkit\\Windows Performance Analyzer.lnk",
            "windows performance recorder": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Windows Kits\\Windows Performance Toolkit\\Windows Performance Recorder.lnk",
            "hyper v manager": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Administrative Tools\\Hyper-V Manager.lnk",
            "vmcreate": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Administrative Tools\\VMCreate.lnk",
            "iscsi initiator": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Administrative Tools\\iSCSI Initiator.lnk",
            "security configuration management": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Administrative Tools\\Security Configuration Management.lnk",
            "odbc data sources 32 bit": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Administrative Tools\\ODBC Data Sources (32-bit).lnk",
            "odbc data sources 64 bit": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Administrative Tools\\ODBC Data Sources (64-bit).lnk",
            "performance monitor": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Administrative Tools\\Performance Monitor.lnk",
            "print management": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Administrative Tools\\Print Management.lnk",
            "recovery drive": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Administrative Tools\\RecoveryDrive.lnk",
            "registry editor": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Administrative Tools\\Registry Editor.lnk",
            "resource monitor": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Administrative Tools\\Resource Monitor.lnk",
            "services": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Administrative Tools\\services.lnk",
            "system configuration": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Administrative Tools\\System Configuration.lnk",
            "system information": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Administrative Tools\\System Information.lnk",
            "task scheduler": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Administrative Tools\\Task Scheduler.lnk",
            "windows defender firewall": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Administrative Tools\\Windows Defender Firewall with Advanced Security.lnk",
            "memory diagnostics tool": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Administrative Tools\\Memory Diagnostics Tool.lnk",
            "component services": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Administrative Tools\\Component Services.lnk",
            "computer management": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Administrative Tools\\Computer Management.lnk",
            "dfrgui": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Administrative Tools\\dfrgui.lnk",
            "disk cleanup": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Administrative Tools\\Disk Cleanup.lnk",
            "event viewer": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Administrative Tools\\Event Viewer.lnk",
            "docker desktop": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Docker Desktop.lnk",
            "hidhide configuration client": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\HidHide Configuration Client.lnk",
            "quick share": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Quick Share.lnk",
            "code": "C:\\Users\\jk422\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        }

        self.min_size = .2 * SCREEN_WIDTH
        self.max_size = .7 * SCREEN_WIDTH
        
        self.add_widget(image.Image(source='static/border.eps.png',size=(1920,1080)))
        self.circle = JarvisButton(size=(284.0,284.0),background_normal='static/circle.png')
        self.circle.bind(on_press=self.start_recording)
        self.start_recording()
        self.add_widget(image.Image(source='static/jarvis.gif', size=(self.min_size, self.min_size), pos=(SCREEN_WIDTH / 2 - self.min_size / 2, SCREEN_HEIGHT / 2 - self.min_size / 2)))
        
        time_layout = boxlayout.BoxLayout(orientation='vertical',pos=(150,900))
        self.time_label = label.Label(text='', font_size=24, markup=True,font_name='static/mw.ttf')
        time_layout.add_widget(self.time_label)
        self.add_widget(time_layout)
        
        clock.Clock.schedule_interval(self.update_time, 1)
        
        self.title = label.Label(text='[b][color=3333ff]ERROR BY NIGHT[/color][/b]',font_size = 42,markup=True,font_name='static/dusri.ttf',pos=(920,900))
        self.add_widget(self.title)
        
        self.subtitles_input = textinput.TextInput(
            text='Hey Dhruv! I am your personal assistant',
            font_size=24,
            readonly=False,
            background_color=(0, 0, 0, 0),
            foreground_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=80,
            pos=(720, 100),
            width=1200,
            font_name='static/teesri.otf',
        )
        self.add_widget(self.subtitles_input)
        
        self.vrh=label.Label(text='',font_size=30,markup=True,font_name='static/mw.ttf',pos=(1500,500))
        self.add_widget(self.vrh)
        
        self.vlh=label.Label(text='',font_size=30,markup=True,font_name='static/mw.ttf',pos=(400,500))
        self.add_widget(self.vlh)
        self.add_widget(self.circle)
        keyboard.add_hotkey('`',self.start_recording)
        
    def take_command(self):
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                r.pause_threshold = 1
                audio = r.listen(source)

            try:
                print("Recognizing....")
                queri = r.recognize_google(audio, language='en-in')
                return queri.lower()

            except Exception:
                speak("Sorry I couldn't understand. Can you please repeat that?")
                queri = 'None'
                
    def start_recording(self, *args):
            print("recording started") 
            threading.Thread(target=self.run_speech_recognition).start()
            print("recording ended") 
            
            
    def run_speech_recognition(self):
        print('before speech rec obj')
        r = sr.Recognizer()
        query = "None"  # Initialize query with a default value
        
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source) 
            print("audio recorded")
                
        print("after speech rec obj") 
        
        try:
            query = r.recognize_google(audio, language="en-in") 
            print(f'Recognised: {query}')
            clock.Clock.schedule_once(lambda dt: setattr(self.subtitles_input, 'text', query))
            self.handle_jarvis_commands(query.lower())
                            
        except sr.UnknownValueError:
            print("Google speech recognition could not understand audio")
            clock.Clock.schedule_once(lambda dt: setattr(self.subtitles_input, 'text', "Could not understand audio"))
            
        except sr.RequestError as e:
            print(f"Could not request results from speech recognition service; {e}")
            clock.Clock.schedule_once(lambda dt: setattr(self.subtitles_input, 'text', "Speech service error"))
        
        return query.lower()
        
    def update_time(self,dt):
            current_time = time.strftime('TIME\n\t%H:%M:%S')
            self.time_label.text = f'[b][color=3333ff]{current_time}[/color][/b]'
              
    def update_circle(self, dt):
            try:
                self.size_value = int(np.mean(self.volume_history))
                
            except Exception as e:
                self.size_value = self.min_size
                print('Warning:',e)
                
            if self.size_value <= self.min_size:
                self.size_value = self.min_size
            elif self.size_value >= self.max_size:
                self.size_value = self.max_size                                     
            self.circle.size = (self.size_value,self.size_value)
            self.circle.pos = (SCREEN_WIDTH / 2 - self.circle.width / 2, SCREEN_HEIGHT / 2 - self.circle.height / 2)
            
            
    def update_volume(self,indata,frames,time,status):
            volume_norm = np.linalg.norm(indata) * 200
            self.volume = volume_norm
            self.volume_history.append(volume_norm)
            self.vrh.text = f'[b][color=3333ff]{np.mean(self.volume_history)}[/color][/b]'
            self.vlh.text = f'[b][color=3333ff]{np.mean(self.volume_history)}[/color][/b]'
            self.vlh.text = f'''[b][color=3344ff]
                {round(self.volume_history[0],7)}\n
                {round(self.volume_history[1],7)}\n
                {round(self.volume_history[2],7)}\n
                {round(self.volume_history[3],7)}\n
                {round(self.volume_history[4],7)}\n
                {round(self.volume_history[5],7)}\n
                {round(self.volume_history[6],7)}\n
                [/color][/b]'''
                
            self.vrh.text = f'''[b][color=3344ff]
                {round(self.volume_history[0],7)}\n
                {round(self.volume_history[1],7)}\n
                {round(self.volume_history[2],7)}\n
                {round(self.volume_history[3],7)}\n
                {round(self.volume_history[4],7)}\n
                {round(self.volume_history[5],7)}\n
                {round(self.volume_history[6],7)}\n
                [/color][/b]'''  
                
            if len(self.volume_history) > self.volume_history_size:
                self.volume_history.pop(0)  
                
    def start_listening(self):
            self.stream = sd.InputStream(callback=self.update_volume) 
            self.stream.start()
    
    def get_gemini_response(self,query):
        try:
            response = model.generate_content(query)
            return response.text
        except Exception as e:
            print(f"Error getting Gemini response: {e}")
            return "I'm sorry, I couldn't process that request."
            
    def handle_jarvis_commands(self, query):
        try:
            # Application launching - handle this first
            if any(keyword in query for keyword in ['open', 'launch', 'start', 'run']):
                # Extract app name by removing command words
                app_name = query.lower()
                for word in ['open', 'launch', 'start', 'run', 'please', 'can you', 'could you']:
                    app_name = app_name.replace(word, '')
                app_name = app_name.strip()
                
                print(f"Attempting to launch: {app_name}")
                speak(f"Attempting to launch: {app_name}")

                # Try to launch the app
                app_name = app_name.strip()
                if app_name in self.app_paths:
                    try:
                        os.startfile(self.app_paths[app_name])
                        speak(f"Opening {app_name}")
                    except Exception as e:
                        print(f"Error launching {app_name}: {e}")
                        speak(f"Sorry, I couldn't open {app_name}.")
                else:
                    speak(f"Sorry, I don't know how to open {app_name}.")
                return

            # System controls - volume and brightness adjustments
            elif "set volume" in query:
                match = re.search(r'set volume (?:to )?(\d+)', query)
                if match:
                    level = int(match.group(1))
                    if self.system_controller.set_volume(level):
                        speak(f"Volume set to {level} percent")
                    else:
                        speak("Sorry, I couldn't change the volume")
                
            elif "set brightness" in query:
                match = re.search(r'set brightness (?:to )?(\d+)', query) # Adjusted regex for flexibility
                if match:
                    level = int(match.group(1))
                    if self.system_controller.set_brightness(level):
                        speak(f"Brightness set to {level} percent")
                    else:
                        speak("Sorry, I couldn't change the brightness")

            # Handling other commands like IP address, YouTube, Google search, etc.
            elif "how are you" in query:
                speak("I am absolutely fine sir. What about you")

            elif "ip address" in query:
                ip_address = find_my_ip()
                speak(
                    f'Your IP Address is {ip_address}.\nFor your convenience, I am printing it on the screen sir.')
                print(f'Your IP Address is {ip_address}')

            # YouTube functionality

            elif "youtube" in query:
                speak("What do you want to play on youtube sir?")
                video = self.take_command().lower()
                youtube(video)

            elif "search on google" in query:
                speak("What do you want to search on google")
                search_query = self.take_command().lower()
                search_on_google(search_query)

            elif "search on wikipedia" in query:
                speak("what do you want to search on wikipedia sir?")
                search = self.take_command().lower()
                results = search_on_wikipedia(search)
                speak(f"According to wikipedia,{results}")

            elif "send an email" in query:
                speak("On what email address do you want to send sir?. Please enter in the terminal")
                receiver_add = input("Email address:")
                speak("What should be the subject sir?")
                subject = self.take_command().capitalize()
                speak("What is the message ?")
                message = self.take_command().capitalize()
                if send_email(receiver_add, subject, message):
                    speak("I have sent the email sir")
                    print("I have sent the email sir")
                else:
                    speak("something went wrong Please check the error log")

            elif "tell me news" in query:
                speak("I am reading out the latest headline of today,sir")
                speak(get_news())

            elif 'weather' in query:
                try:
                    # Extract city name from query
                    city_match = re.search(r'weather (?:in|at|for)? (.+)', query)
                    if city_match:
                        city = city_match.group(1).strip()
                        weather_data = weather_forecast(city)
                        
                        if weather_data:
                            temp = weather_data['temp']
                            feels_like = weather_data['feels_like']
                            weather = weather_data['weather']
                            
                            def update_ui(dt):
                                weather_text = f"Weather in {city}:\n{weather}\nTemp: {temp}°C\nFeels like: {feels_like}°C"
                                self.subtitles_input.text = weather_text
                            
                            # Use schedule_once for UI update
                            clock.Clock.schedule_once(update_ui)
                            
                            # Speak the weather information
                            speak(f"The current temperature in {city} is {temp}, but it feels like {feels_like}. The weather is {weather}")
                        else:
                            print("No city match found in query:", query)
                            speak("Please specify a city name when asking about weather")
                    else:
                        speak("Please specify a city name when asking about weather")
                except Exception as e:
                    print(f"Weather error in handle_jarvis_commands: {str(e)}")
                    speak(f"Sorry, I couldn't get the weather information. {str(e)}")

            elif "movie" in query:
                movies_db = imdb.IMDb()
                speak("Please tell me the movie name:")
                text = self.take_command()
                movies = movies_db.search_movie(text)
                
                if movies:
                    speak(f"Searching for {text}")
                    speak("I found these:")
                    for movie in movies[:3]:  # Show top 3 results
                        title = movie['title']
                        year = movie.get('year', 'Year not available')
                        speak(f"{title} ({year})")
                        print(f"{title} ({year})")
                else:
                    speak("No movies found with that name")

            elif 'subscribe' in query:
                speak(
                    "Everyone who are watching this video, Please subscribe for more amazing content from error by "
                    "night. I will show you how to do this")
                speak("Firstly Go to youtube")
                webbrowser.open("https://www.youtube.com/")
                speak("click on the search bar")
                pyautogui.moveTo(806, 125, 1)
                pyautogui.click(x=806, y=125, clicks=1, interval=0, button='left')
                speak("type error by night")
                pyautogui.typewrite("error by night")
                speak("press enter")
                pyautogui.press('enter')
                time.sleep(2)
                speak("click on channel")
                pyautogui.moveTo(490, 314, 1)
                pyautogui.click(x=490, y=314, clicks=1, interval=0, button='left')
                speak("click on subscribe button")
                pyautogui.moveTo(1688, 314, 1)
                speak("click here to subscribe our channel")
                pyautogui.click(x=1688, y=314, clicks=1, interval=0, button='left')
                speak("And also Don't forget to press the bell icon")
                pyautogui.moveTo(1750, 314, 1)
                pyautogui.click(x=1750, y=314, clicks=1, interval=0, button='left')
                speak("turn on all notifications")
                pyautogui.click(x=1750, y=320, clicks=1, interval=0, button='left')

            else:
                # If no specific command matches, use Gemini for general conversation
                gemini_response = self.get_gemini_response(query)
                gemini_response = gemini_response.replace("*","")
                if gemini_response and gemini_response != "I'm sorry, I couldn't process that request.":
                    speak(gemini_response)
                    print(gemini_response)

        except Exception as e:
            print(f"Error in handle_jarvis_commands: {str(e)}")
            speak("Sorry, I encountered an error while processing that command")
                
    def show_city_input(self):
        # Remove old input widgets if they exist
        if hasattr(self, 'city_input'):
            self.remove_widget(self.city_input)
        if hasattr(self, 'get_weather_button'):
            self.remove_widget(self.get_weather_button)
        
        # Create new input widgets
        self.city_input = textinput.TextInput(
            hint_text='Enter city name',
            font_size=20,
            background_color=(0.8, 0.8, 0.8, 1),
            foreground_color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(300, 40),
            pos=(SCREEN_WIDTH / 2 - 150, SCREEN_HEIGHT / 2 - 20),
            multiline=False  # Prevent enter key from adding newlines
        )
        
        self.get_weather_button = JarvisButton(
            text='Get Weather',
            size_hint=(None, None),
            size=(150, 40),
            pos=(SCREEN_WIDTH / 2 + 160, SCREEN_HEIGHT / 2 - 20)
        )
        
        # Bind enter key to submit
        self.city_input.bind(on_text_validate=self.get_weather_info)
        self.get_weather_button.bind(on_press=self.get_weather_info)
        
        self.add_widget(self.city_input)
        self.add_widget(self.get_weather_button)
        
        # Focus the input using a separate method
        clock.Clock.schedule_once(self._set_city_input_focus)

    def _set_city_input_focus(self, dt):
        """Helper method to set focus on city input"""
        if hasattr(self, 'city_input'):
            self.city_input.focus = True

    def get_weather_info(self, instance):
        try:
            city = self.city_input.text.strip()
            if not city:
                speak("Please enter a city name")
                return
                
            weather, temp, feels_like = weather_forecast(city)
            
            # Update UI with weather information
            weather_text = f"Weather in {city}:\n{weather}\nTemp: {temp}°C\nFeels like: {feels_like}°C"
            self.subtitles_input.text = weather_text
            
            # Speak the weather information
            speak(f"The current temperature in {city} is {temp} degrees, but it feels like {feels_like} degrees. The weather is {weather}")
            
        except Exception as e:
            speak(f"Sorry, I couldn't get the weather information. {str(e)}")
            print(f"Weather error: {e}")
        finally:
            # Clean up input widgets
            self.remove_widget(self.city_input)
            self.remove_widget(self.get_weather_button)

    def update_weather_ui(self, weather_text):
        """Update weather information in the UI"""
        if hasattr(self, 'subtitles_input'):
            self.subtitles_input.text = weather_text
