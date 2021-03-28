import pyttsx3
import datetime
import speech_recognition as sr
import os
import webbrowser
import pyjokes
import randfacts
import wikipedia
import weathercom
import json
import requests
import pyautogui
import psutil
from oyt import *
from wiki import *
from word2number import w2n

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[1].id)
engine.setProperty('voice',voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning")
    elif hour>=12 and hour<18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio,language="en-in")
        print(f"User said :{query}\n")

    except Exception as e:
        print("I am sorry, please repeat it again...")
        return "None"
    return query

def weatherReport(city):
    weatherdetails = weathercom.getCityWeatherDetails(city)
    temp = json.loads(weatherdetails)["vt1observation"]["temperature"]
    humidity = json.loads(weatherdetails)["vt1observation"]["humidity"]
    phrase = json.loads(weatherdetails)["vt1observation"]["phrase"]
    return temp,humidity,phrase

if __name__=='__main__':
    wish()
    speak("I am your Personal Assistant. How are you sir?")
    while True:
        text = takeCommand().lower()
        if "what" and "about" and "you" in text:
            speak("I am good sir, what can i do for you?")
        
        elif "date" in text:
            curDate = datetime.datetime.now().strftime("%d:%B:%Y")
            curDay = datetime.datetime.now().strftime("%A")
            speak(f"Today's date is {curDate} and the day is {curDay}")

        elif "time" in text:
            curTime = datetime.datetime.now().strftime("%I:%M:%S %p")
            speak(f"The current time is {curTime}")
        
        elif "open" and "dev" in text:
            speak("Opening Dev Cpp")
            codePath = "C:\\Program Files (x86)\\Dev-Cpp\\Lang"
            os.startfile(codePath)

        elif "open google" in text:
            speak("Opening Google in your browser")
            webbrowser.open(url="https://google.com")

        elif "open youtube" in text:
            speak("Opening YouTube in your browser")
            webbrowser.open(url="https://youtube.com")

        elif "open whatsapp" in text:
            speak("Opening WhatsApp in your browser")
            webbrowser.open(url="https://web.whatsapp.com/")

        elif "joke" in text:
            J = pyjokes.get_joke("en","neutral")
            print(J)
            speak(J)

        elif "facts" in text:
            F = randfacts.getFact()
            print(F)
            speak(F)
        
        elif "cpu stats" in text:
            usage = str(psutil.cpu_percent())
            speak("CPU is at" + usage)

            battery = psutil.sensors_battery()
            speak("battery is at")
            speak(battery.percent)

        elif "take screenshot" in text:
            img = pyautogui.screenshot()
            speak("Done Sir")
            img.save('C://Users//Sachi Kaushik//Pictures')
        
        elif "take notes" in text:
            file = open('notes.txt','w')
            speak("Should I include date and time?")
            ans = takeCommand()
            speak("What should I write sir?")
            notes = takeCommand()
            if "yes" or "sure" in ans:
                curTime = datetime.datetime.now().strftime("%I:%M:%S %p")
                curDate = datetime.datetime.now().strftime("%d:%B:%Y")
                file.write(curTime)
                file.write(curDate)
                file.write(':-\n')
                file.write(notes)
                speak("Done taking notes sir.")
            else:
                file.write(notes)
                speak("Done taking notes sir.")

        elif "show notes" in text:
            speak("Opening notes")
            file = open('notes.txt','r')
            print(file.read())

        elif "according to wikipedia" in text:
            speak("Searching to wikipedia...")
            word = text.replace("wikipedia","")
            results = wikipedia.summary(word,sentences=2)
            speak("According to wikipedia...")
            print(results)
            speak(results)

        elif "play" and "play online" in text:
            speak("Sure sir, what do you want me to play?")
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                r.pause_threshold = 0.8
                audio = r.listen(source)
                print("Recognizing...")
                title = r.recognize_google(audio, language="en-in")
            print("Playing {} in youtube".format(title))
            speak("Playing {} in youtube".format(title))
            bot = music()
            bot.play(title)

        elif "information" in text:
            speak("Please name the topic sir?")
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                r.pause_threshold = 0.8
                audio = r.listen(source)
                print("Recognizing...")
                topic = r.recognize_google(audio, language="en-in")
            print("Searching {} in wikipedia online".format(topic))
            speak("Searching {} in wikipedia online".format(topic))
            assist = info()
            assist.get_info(topic)

        elif "weather" in text:
            print("Sure sir, please tell me the city?")
            speak("Sure sir, please tell me the city?")
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                r.pause_threshold = 0.8
                audio = r.listen(source)
                print("Recognizing...")
                city = r.recognize_google(audio, language="en-in")
            temp , humidity ,phrase = weatherReport(city)
            print("Currently in "+ city + "the temperature is "+str(temp)+" degrees celsius , with humidity of"+str(humidity)+"percent and sky is"+str(phrase))
            speak("Currently in "+ city + "the temperature is "+str(temp)+" degrees celsius , with humidity of"+str(humidity)+"percent and sky is"+str(phrase))

        elif "news" in text:
            api_address = "https://newsapi.org/v2/top-headlines?country=in&apiKey=3975d6e26cf24731ac34815d1945a50e"   
            response = requests.get(api_address)
            news_json = json.loads(response.text)
            speak("How many headlines do you want to know?")
            print("How many headlines do you want to know?")
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")
                r.pause_threshold = 0.8
                audio = r.listen(source)
                print("Recognizing...")
                count_word = r.recognize_google(audio, language="en-in")

            count = w2n.word_to_num(count_word)
            print("Here are todays top {} headlines:".format(count))
            speak("Here are todays top {} headlines".format(count))

            for news in news_json['articles']:
                if count > 0:
                    T = str(news['title'])
                    print(T)
                    speak(T)
                    count -= 1
        
        elif "go offline" in text:
            speak("Going offline sir")
            quit()   