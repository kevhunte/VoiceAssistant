import speech_recognition as sr
import playsound
import os, random, json
from gtts import gTTS
from time import ctime

#recording instance
r = sr.Recognizer()

class Assistant:

    def __init__(self, config):
        self.config_file_name = config
        with open(self.config_file_name, 'r') as f:
            self.config_data = json.load(f)
        self.__process_config()
        self.speak(f'Hi, my name is {self.Name}. How may I assist you?')

    '''
    takes stored values and sets members of instance
    '''
    def __process_config(self):
        self.Name = 'Ant' if not self.config_data['name']['value'] else self.config_data['name']['value']

    '''
    writes changes in memory back to file
    '''
    def __save_config(self):
        with open(self.config_file_name, 'w') as f:
            json.dump(self.config_data, f,sort_keys=True, indent=4)

    '''
    Allows user to edit and overwrite the config.json file
    '''
    def __edit_config(self):
        self.speak('What would you like to edit?')
        # provide a list of updateable variables. Have allow_modification == true

    '''
    speech to text
    '''
    def record_command(self):
        #global r
        with sr.Microphone() as source:
            audio = r.listen(source)
            voice_data = ''
            try:
                voice_data = r.recognize_google(audio)
            except sr.UnknownValueError:
                self.speak('Sorry I did not understand that command')
            except sr.RequestError:
                self.speak('Sorry my service is unavailable')
            return voice_data

    '''
    Text to speech
    '''
    def speak(self, audio_string: str):
        print(f'speaking: {audio_string}')
        tts = gTTS(text=audio_string, lang='en')
        rand = random.randint(1,1000000)
        audio_file = f'audio-{rand}.mp3'
        tts.save(audio_file)
        playsound.playsound(audio_file)
        os.remove(audio_file)

    '''
    business logic
    '''
    def process_command(self, voice_data: str):
        if 'change my settings' in voice_data:
            self.speak('Sure. Opening up configs.')
            self.__edit_config()
        if 'what is your name' in voice_data:
            self.speak(f"My name is {self.Name}")
        if 'what time is it' in voice_data:
            self.speak(f"The current time is {ctime()}")
        if 'exit' in voice_data or 'shut down' in voice_data:
            self.speak('Goodbye!')
            return False
            #exit()
        return True