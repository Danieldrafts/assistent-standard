#-*- coding: utf-8 -*-
from datetime import datetime
import sys, os, platform
import requests
from bs4 import BeautifulSoup

class Actions():

    def verify_command(self, assistent, command):
        if (command in ['vou te ensinar algo novo']):
            assistent.play_sound('denied.mp3')
            print('- '+assistent.name+': Você ainda não me programou para isto!')
            assistent.anwser('Você ainda não me programou para isto!')

        elif command in ['vá dormir', 'vai dormir', 'fechar']:
            assistent.play_sound('accepted.mp3')
            assistent.anwser('Ok, até mais!')
            exit()
            return True

        elif command =='pode deixar' or command == 'cancelar':
            assistent.anwser('Como quiser!')
            return True
			
        elif 'que dia é hoje' in command:
            today = datetime.now()
            today_date = today.strftime('%d/%m/%Y')
            assistent.anwser('Hoje é dia: '+today_date)
            return True

        elif 'quantas horas' in command or 'que horas são' in command:
            today = datetime.now()
            today_date = today.strftime('%H:%M')
            assistent.anwser('São: '+today_date)
            return True

        elif command =='repita' or command == 'repita o que eu disser':
            assistent.play_sound('accepted.mp3')
            assistent.repeat()
            return True

        elif 'reiniciar sistema' in command:
            os.system('sudo reboot')
            assistent.anwser('Reiniciando!')
            return True

        elif command in ['quais são as últimas notícias', 'me dê as últimas notícias', 'me atualize das noticias', 'últimas notícias']:
            site_news = requests.get("https://news.google.com/news/rss?ned=pt_br&gl=BR&hl=pt")
            noticias =  BeautifulSoup(site_news.text, 'html.parser')
            for noticia in noticias.findAll('item')[:5]:
                message = noticia.title.text
                assistent.anwser(message)
            return True

        elif 'onde fica' in command or 'pesquise' in command:
            command = command.replace(assistent.hotword, "")
            command = command.replace(" ", "+")
            assistent.google_search(command)
            return True
            
        else:
            return False