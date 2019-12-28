import speech_recognition as sr
import webbrowser
import time
import playsound
import os
import random
from gtts import gTTS
from time import ctime

class person:
    name = ''
    def setName(self, name):
        self.name = name


def there_exist(terms):
    for term in terms:
        if term in voice_data:
            return True



r = sr.Recognizer()

# listen for audio and convert it to text:
def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            speak('Sorry, I did not get that')
        except sr.RequestError:
            speak('Sorry, the speech recognition service is down')
        print(f">> {voice_data.lower()}")  # print what user said
        return voice_data.lower()

# get string and make a audio file and play it out
def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 10000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(f'kiri: {audio_string}')  # print what app said
    os.remove(audio_file)


def respond(voice_data):
    #tell what it can do
    if there_exist(['hey sarah']):
        talk_statement = 'here are the this i can do, search, time of the day, open web pages'
        speak(talk_statement)

    #open web pages
    if there_exist(['open']):
        page = voice_data.split('open')[-1].strip()
        location = record_audio(f'Do you mean {page}.com')
        if there_exist(['Yes', 'ok']):
            url = f'https://{page}.com'
            webbrowser.get().open(url)
            speak(f'Here is what i found for {page}')
        else:
            url = f'https://google.com/search?q={page}'
            webbrowser.get().open(url)
            speak(f'Here is what I found for {page} on google')


    #greetings
    if there_exist(['hey', 'hi', 'hello']):
        greetings = [f"hey, how can I help you {person_obj.name}", f"hey, what's up? {person_obj.name}",
                      f"I'm listening {person_obj.name}", f"how can I help you? {person_obj.name}", f"hello {person_obj.name}"]
        greet = greetings[random.randint(0, len(greetings)-1)]
        speak(greet)
    
    #name
    if there_exist(['what is your name?', "what's your name?", 'tell me your name']):
        if person_obj.name:
            speak(f'My name is Sarah')
        else:
            speak(f'my name is Sarah. what is your name?')
    
    if there_exist(['my name is']):
        person_name = voice_data.split('is')[-1].strip()
        speak(f"okay, i will remember that {person_name}")
        person_obj.setName(person_name)
    elif there_exist(['i am', 'am']):
        person_name = voice_data.split('am')[-1].strip()
        speak(f"okay, i will remember that {person_name}")
        person_obj.setName(person_name)

    # checking up
    if there_exist(["how are you","how are you doing"]):
        speak(f"I'm very well, thanks for asking {person_obj.name}")



    #time
    if there_exist(["what's the time","tell me the time","what time is it"]):
        time = ctime().split(" ")[3].split(":")[0:2]
        if time[0] == "00":
            hours = '12'
        else:
            hours = time[0]
        minutes = time[1]
        time = f'{hours} {minutes}'
        speak(time)


    #search google
    if there_exist(["search for", "can you search for"]) and 'youtube' not in voice_data:
        search_term = voice_data.split("for")[-1]
        url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on google')
        
    if there_exist(["what is meaning of", "meaning of"]):
        search_term = voice_data.split("of")[-1]
        url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on google')

    #search youtube
    if there_exist(["youtube"]):
        search_term = voice_data.split("for")[-1]
        url = f"https://www.youtube.com/results?search_query={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on youtube')

    #find location
    if there_exist(['find location']):
        location = record_audio('What is the location?')
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        speak(f'Here is the location of  {location}')


    #close app
    if there_exist(['exit', 'ok bye', 'close']):
        speak('Okay, see you next time. Bye')
        exit()


time.sleep(1)

speak('hey, how can i help you?')
person_obj = person()

while 1:
    #get voice input
    voice_data = record_audio()
    respond(voice_data)
