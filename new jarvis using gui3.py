import customtkinter as ctk
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import threading
import time
from thefuzz import fuzz
import os

class JarvisGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- GUI Configuration ---
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title("JARVIS AI System")
        self.geometry("550x700")

        # --- State Variables ---
        self.is_running = False
        self.is_listening_state = False
        self.is_speaking_state = False
        self.pulse_tick = 0

        self.setup_ui_elements()
        self.animate_reactor()

    def setup_ui_elements(self):
        self.header_label = ctk.CTkLabel(self, text="J.A.R.V.I.S.", font=("Orbitron", 35, "bold"), text_color="#00d2ff")
        self.header_label.pack(pady=(30, 20))

        self.reactor_visual = ctk.CTkButton(
            self, text="SYSTEM\nOFFLINE", width=220, height=220, corner_radius=110,
            fg_color="#00334d", text_color="#80ebff", font=("Arial", 16, "bold"),
            hover=False, border_width=4, border_color="#005f7f"
        )
        self.reactor_visual.pack(pady=10)

        self.start_btn = ctk.CTkButton(self, text="INITIALIZE SYSTEM", command=self.start_thread, fg_color="#00d2ff", text_color="black")
        self.start_btn.pack(pady=20)

        self.output_box = ctk.CTkTextbox(self, width=480, height=200, corner_radius=15, font=("Consolas", 12), fg_color="#1a1a1a", text_color="#00d2ff")
        self.output_box.pack(pady=20)

    def animate_reactor(self):
        if not self.is_running:
             self.reactor_visual.configure(fg_color="#00334d", text="SYSTEM\nOFFLINE")
        elif self.is_speaking_state:
            self.reactor_visual.configure(text="SPEAKING...")
            color = "#e0ffff" if self.pulse_tick % 2 == 0 else "#00d2ff"
            self.reactor_visual.configure(fg_color=color)
            self.pulse_tick += 1
        elif self.is_listening_state:
             self.reactor_visual.configure(fg_color="#00a3cc", text="LISTENING...")
        else:
             self.reactor_visual.configure(fg_color="#005f7f", text="ONLINE\nWAITING")
        
        self.after(150, self.animate_reactor)

    def add_to_log(self, text):
        self.output_box.insert("end", f"{text}\n")
        self.output_box.see("end")

    def speak(self, text):
        """Fresh engine initialization to prevent the 'one-run' bug."""
        self.is_speaking_state = True
        self.add_to_log(f">> Jarvis: {text}")
        try:
            # Initializing inside the function ensures the loop doesn't hang
            engine = pyttsx3.init()
            engine.setProperty('rate', 170)
            engine.say(text)
            engine.runAndWait()
            engine.stop() # Properly shut down the engine after speaking
            del engine    # Clear from memory
        except Exception as e:
            print(f"Speak Error: {e}")
        finally:
            self.is_speaking_state = False
            time.sleep(0.3) # Short pause before Jarvis listens again

    def listen(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.is_listening_state = True
            self.add_to_log("\n[Listening...]")
            recognizer.adjust_for_ambient_noise(source, duration=0.8)
            try:
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=5)
                self.is_listening_state = False
                self.add_to_log("[Recognizing...]")
                query = recognizer.recognize_google(audio, language='en-in')
                self.add_to_log(f"User: {query}")
                return query.lower()
            except Exception:
                self.is_listening_state = False
                return ""

    def is_similar(self, actual_query, target_phrase):
        return fuzz.partial_ratio(target_phrase.lower(), actual_query.lower()) >= 70

    def run_jarvis_logic(self):
        self.is_running = True
        self.start_btn.configure(state="disabled", text="SYSTEM ACTIVE")
        self.speak("Hello Manjit, Greatings from Jarvis.")
        self.speak("I am here to help you, continue with your commands.")

        while True:
            query = self.listen()
            if not query or query == "":
                continue

            # --- Fuzzy Command Logic ---
            if self.is_similar(query, 'hey jarvis') or self.is_similar(query, 'hi'):
                self.speak("Yes sir, I am listening.")
            
            elif self.is_similar(query, 'time'):
                strTime = datetime.datetime.now().strftime("%I:%M %p")
                self.speak(f"Sir, the time is {strTime}")

            elif self.is_similar(query, 'google'):
                self.speak("Opening Google.")
                webbrowser.open("https://www.google.com")

            elif self.is_similar(query, 'search'):
                search_query = query.replace("search", "").strip()
                self.speak(f"Searching for {search_query}")
                webbrowser.open(f"https://www.google.com/search?q={search_query}")

            elif self.is_similar(query, 'whatsapp'):
                self.speak(f"Opening Whatsapp")
                webbrowser.open("https://web.whatsapp.com/")

            elif self.is_similar(query, 'music'):
                self.speak("Opening youtube music.")
                webbrowser.open("https://music.youtube.com")

            elif 'close' in query:
                # You must use the executable name (e.g., 'notepad.exe', 'chrome.exe', 'msedge.exe')
                app_name = query.replace("close", "").strip() 
                self.speak(f"Closing {app_name}, sir.")
                cls_app = app_name+".exe"
                if self.is_similar(app_name, 'dev'):
                    os.system(f"taskkill /f /im devcpp.exe")

                # /f forces it to close, /im specifies the image name
                elif cls_app:
                    os.system(f"taskkill /f /im {cls_app}")
                else:
                    self.speak("No such file to close sir.")
            
            elif self.is_similar(query, 'dev c++') or self.is_similar(query, 'cpp'):
                # Replace the path below with the actual path to your file
                file_path = r"E:\DEV C++\Dev-Cpp\devcpp.exe" 
                
                if os.path.exists(file_path):
                    self.speak("Opening the requested file, sir.")
                    os.startfile(file_path) # Opens file with default system app
                else:
                    self.speak("I am sorry, I could not find that file in the specified location.")
            
            elif self.is_similar(query, 'vs code') or self.is_similar(query, 'visual studio'):
                # Replace the path below with the actual path to your file
                file_path = r"D:\VS code\Microsoft VS Code\Code.exe" 
                
                if os.path.exists(file_path):
                    self.speak("Opening the requested file, sir.")
                    os.startfile(file_path) # Opens file with default system app
                else:
                    self.speak("I am sorry, I could not find that file in the specified location.")
            
            elif self.is_similar(query, 'notepad'):
                # Replace the path below with the actual path to your file
                file_path = r"C:\Windows\System32\notepad.exe" 
                
                if os.path.exists(file_path):
                    self.speak("Opening the requested file, sir.")
                    os.startfile(file_path) # Opens file with default system app
                else:
                    self.speak("I am sorry, I could not find that file in the specified location.")
            
            elif self.is_similar(query, 'media'):
                # Replace the path below with the actual path to your file
                file_path = r"C:\Users\DELL\OneDrive\Desktop\Groove Music.lnk" 
                
                if os.path.exists(file_path):
                    self.speak("Opening the requested file, sir.")
                    os.startfile(file_path) # Opens file with default system app
                else:
                    self.speak("I am sorry, I could not find that file in the specified location.")
    
            elif self.is_similar(query, 'stop') or self.is_similar(query, 'exit') or self.is_similar(query, 'bye'):
                self.speak("Goodbye Manjit.")
                self.quit()
                break
            
            # Optional: Catch-all for unknown commands
            else:
                self.speak("No such command in the library.")
                self.add_to_log("[Command not recognized]")

    def start_thread(self):
        threading.Thread(target=self.run_jarvis_logic, daemon=True).start()

if __name__ == "__main__":
    app = JarvisGUI()
    app.mainloop()