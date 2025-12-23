import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import sys
import time

def speak(text):
    """
    Initializes a fresh engine every time to prevent 
    the 'silent after first run' bug.
    """
    print(f"Jarvis: {text}")
    
    # Initialize engine locally inside the function
    # Use 'sapi5' for Windows, 'nsss' for Mac, or leave empty for Linux
    try:
        engine = pyttsx3.init() 
        
        # Set properties
        engine.setProperty('rate', 170)
        engine.setProperty('volume', 1.0)
        
        engine.say(text)
        engine.runAndWait()
        
        # Clean up the engine after speaking
        engine.stop() 
    except Exception as e:
        print(f"Error in speaking: {e}")

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.pause_threshold = 0.8 # Faster response
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query.lower()
    except Exception:
        return "none"

# --- Main Program ---
if __name__ == "__main__":
    speak("Hello Manjit, Moi Jarvis. Ki koribo paru moi?")

    while True:
        query = listen()

        if query == "none":
            continue

        # --- LOGIC COMMANDS ---
        if 'hey jarvis' in query:
            speak(f"Yes sir I am listening.")
        
        elif 'hey jarvis' in query:
            speak(f"Oi Sutmarana khuni asu moi.")
        
        elif 'hey bihari' in query:
            speak(f"Oi Sutmarana, xunni asu moi.")
        
        elif 'sing mayabini' in query:
            speak(f"Mayabini, ratir, bukut, dekha, palu, tumar, sobi")

        elif 'what is the time' in query:
            strTime = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"Sir, the time is {strTime}")
        
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"Sir, the time is {strTime}")

        elif 'good morning' in query:
            speak(f"good morning Sir")

        elif 'open google' in query:
            speak("Opening Google.")
            webbrowser.open("https://www.google.com")
        
        elif 'play music' in query:
            speak("Opening youtube music.")
            webbrowser.open("https://music.youtube.com")

        elif 'play zubeen garg' in query:
            speak("playing legendary mayabini.")
            webbrowser.open("https://music.youtube.com/watch?v=AqUonMjxaog")
        
        elif 'search' in query:
            search_query = query.replace("search", "").strip()
            speak(f"Searching for {search_query}")
            webbrowser.open(f"https://www.google.com/search?q={search_query}")

        elif 'open whatsapp' in query:
            search_query = query.replace("search", "").strip()
            speak(f"Opening Whatsapp")
            webbrowser.open("https://web.whatsapp.com/")

        elif 'stop' in query or 'exit' in query:
            speak("Goodbye Manjit.")
            break