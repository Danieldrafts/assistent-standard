from gtts import gTTS
import os, platform
from subprocess import call #necessario para usar em linux e MAC
from playsound import playsound

def create_audio(message, language, file_name):
    tts = gTTS(message, lang=language)
    tts.save(file_name)

def play_audio(audio_name):
    oparation_system = platform.system()

    if(oparation_system == "Windows"):
        playsound(audio_name) #OSX
    elif(oparation_system == "Linux"):
        call(['aplay', audio_name]) #lINUX
    else:
        call(['afplay', audio_name]) #OSX

"""
create_audio('Olá! Eu sou a Mari!', 'pt-br', 'audios/hello.mp3')
create_audio('Oi', 'pt-br', 'audios/feedback.mp3')
create_audio('Vou muito bem e você?', 'pt-br', 'audios/vou-bem-e-voce.mp3')
create_audio('Vai trabalhar!', 'pt-br', 'audios/vai-trabalhar.mp3')
create_audio('Não sou paga para isto!', 'pt-br', 'audios/nao-sou-paga-para-isto.mp3')
create_audio('Desculpe, não entendi', 'pt-br', 'audios/nao-entendi.mp3')
"""

"""
play_audio('audios/hello.mp3')
play_audio('audios/feedback.mp3')
play_audio('audios/vou-bem-e-voce.mp3')
play_audio('audios/vai-trabalhar.mp3')
play_audio('audios/nao-sou-paga-para-isto.mp3')
play_audio('audios/nao-entendi.mp3')
"""

