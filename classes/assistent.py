#-*- coding: utf-8 -*-
import speech_recognition as sr
from playsound import playsound
from termcolor import colored
import sys, os, platform
from subprocess import call #necessario para usar em linux e MAC

import requests
from bs4 import BeautifulSoup
from classes.voice import Voice
from classes.actions import Actions
from classes.settings import Settings

base_dir_name = os.path.dirname(os.path.abspath(__file__))
base_dir_name = base_dir_name.replace ( "classes", "" ) 


settings = Settings(base_dir_name+"/settings.ini")
general = settings.get_section_settings('GENERAL')
voice_capture = settings.get_section_settings('VOICE_CAPTURE')
speech_api = settings.get_section_settings('SPEECH_API')
other_settings = settings.get_section_settings('OTHERS')

class Assistent():
    def __init__(self):
        #Configurações
        self.hotword = general['keyword']
        self.name = general['assistent_name']
        self.full_name = general['assistent_full_name']     
        self.recognizer = sr.Recognizer()
        self.set_configurations()
        self.voice = Voice(self.language)

    def set_configurations(self):
        self.__you_said_color = general['human_text_color']
        self.__color_output = general['assistent_text_color']
        self.timeout_capture = int(voice_capture['timeout_capture'])
        self.phrase_time_limit = int(voice_capture['phrase_time_limit'])
        self.threshold = int(voice_capture['threshold'])
        self.language = general['language']
        self.__voiceToTextAPI = speech_api['voice_to_text_api']
        self.__apiKey = speech_api['api_key'] 
        self.silence_limit = int(other_settings['silence_limit'])

    def awake(self):
        self.writeMessage('************* Iniciando {} *************'.format(self.name))
        self.play_sound('start.mp3')

    def start(self):
        while True:
            self.make_sure_you_were_called()

    def make_sure_you_were_called(self):
        you_said = self.voice_capture(message = "Escutando", phrase_time_limit = self.phrase_time_limit)
        if you_said is not None:
            if self.hotword.lower() in you_said:                  
                self.anwser('Oi!')
                is_command = self.search_command(you_said)
                if is_command is True:
                    return True
                while True:
                    you_said = self.voice_capture(message = "Fale...", phrase_time_limit = self.phrase_time_limit)
                    if you_said is not None:
                        is_command = self.search_command(you_said)
                        if is_command is True:
                            return True

    def anwser(self, message):
        print('- Processando...')
        self.writeMessage(message)
        self.voice.speak(message) 
    
    def play_sound(self, soundName):
        try:
            soundName = 'audios/'+soundName
            self.voice.play_audio(soundName)
        except Exception:
            pass
        
    def writeMessage(self, message, who = "self"):
        if(platform.system() != "Windows"):
            if who == "self":
                print(colored('- '+self.name+': '+message, self.__color_output))
            else:
                print(colored('- '+who+': '+message, self.__you_said_color))
        else:
            if who == "self":
                print('- '+self.name+': '+message)
            else:
                print('- '+who+': '+message)

####################################### Recognition ##########################################
    def voice_capture(self, message = "", timeout = None, phrase_time_limit = None):
        with sr.Microphone() as microphone:
            print("\n"+message)
            audio = self.recognizer.listen(microphone, timeout= timeout, phrase_time_limit=phrase_time_limit)
            if audio is not None:
                voice_command = ""
                if self.__voiceToTextAPI == 'wit.ai':
                    return self.__wit_caption(audio)
                else:
                    return self.__google_caption(audio)

    def __google_caption(self, audio):
        try:
            audio_recognized = self.recognizer.recognize_google(audio, language='pt-BR')
            
            audio_recognized = audio_recognized.lower()
            self.writeMessage(audio_recognized, "Você")
            return audio_recognized                
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            return None

    def __wit_caption(self, audio):
        try:
            audio_recognized = self.recognizer.recognize_wit(audio, key=self.__apiKey)
            
            audio_recognized = audio_recognized.lower()
            self.writeMessage(audio_recognized, "Você")
            return audio_recognized
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            return None

#################################### Commands #######################################

    def search_command(self, voice_command, fast_command = False):
        
        if self.conversation(voice_command):
            return True
        else:
            actions = Actions()
            return actions.verify_command(self, voice_command)
        
#################################### ACTIONS ######################################

    def conversation(self, your_question):
        answers = {'como você está': 'muito bem, obrigado!', 'como vai você':'vou muito bem, obrigado!', 'faça café':'Não sou paga para isto!',
        'faz um café pra mim':'Não sou paga para isto!', 'me dê dinheiro': 'vai trabalhar!', 'me dá dinheiro': 'vai trabalhar!', 
        'quem é você': 'eu sou '+self.name+' assistente virtual!','qual é o seu nome': 'meu nome é '+self.name,
        }
        for question in answers:
            if your_question in question:
                self.play_sound('accepted.mp3')
                self.anwser(answers[question])
                return True
            elif your_question =='pode deixar' or your_question == 'cancelar':
                self.anwser('Como quiser!')
                return True
                
    def repeat(self):
        self.anwser('Pode falar')
        youSaid = self.voice_capture(message = "Escutando", phrase_time_limit = self.phrase_time_limit)
        self.writeMessage('Acho que você disse: "'+youSaid+'"')
        self.anwser('Acho que você disse: "'+youSaid)

    def google_search(self, keywords):
        search = requests.get("https://www.google.com/search?q={}&cr=brazil%20&lr=pt_br".format(keywords))
        search = BeautifulSoup(search.text, 'html.parser')
        for result in search.findAll("div", {"class": "g"})[:5]:
            self.anwser(result)



