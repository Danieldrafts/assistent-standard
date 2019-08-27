from gtts import gTTS
import os, platform, random
from subprocess import call #necessario para usar em linux e MAC
from playsound import playsound

class Voice():
    def __init__(self, language = 'pt-br'):
        self.language = language

    def create_audio(self, message, file_name):
        textToSound = gTTS(message, lang=self.language)
        textToSound.save(file_name)

    def play_audio(self, audio_name):
        oparation_system = platform.system()
        
        if(oparation_system == "Windows"):
            playsound(audio_name) #OSX
        elif(oparation_system == "Linux"):
            call(['mpg321', audio_name]) #lINUX
        else:
            call(['afplay', audio_name]) #OSX

    def speak(self, message):
        version = random.randint(1,900)
        version = str(version)
        try:
            self.create_audio(message, 'audios/speaking'+version+'.mp3')
            self.play_audio('audios/speaking'+version+'.mp3')
            os.remove('audios/speaking'+version+'.mp3')
        except PermissionError:
            version = random.randint(1,10)
            version = str(version)
            self.create_audio(message, 'audios/speaking-temp'+version+'.mp3')
            self.play_audio('audios/speaking-temp'+version+'.mp3')
            os.remove('audios/speaking-temp'+version+'.mp3')
