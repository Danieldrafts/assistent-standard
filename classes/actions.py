#-*- coding: utf-8 -*-
from datetime import datetime
import sys, os, platform, time
import requests
from bs4 import BeautifulSoup

base_dir_name = os.path.dirname(os.path.abspath(__file__))
base_dir_name = base_dir_name.replace ( "classes", "" ) 

class Actions():

    def __init__(self, assistent):
        self.assistent = assistent

    def verify_command(self, command):
        if (command in ['vou te ensinar algo novo']):
            self.assistent.play_sound('denied.mp3')
            print('- '+self.assistent.name+': Você ainda não me programou para isto!')
            self.assistent.anwser('Você ainda não me programou para isto!')

        elif command in ['vá dormir', 'vai dormir', 'fechar assistente']:
            self.assistent.play_sound('accepted.mp3')
            self.assistent.anwser('Ok, até mais!')
            exit()
            return True

        elif command =='pode deixar' or command == 'cancelar':
            self.assistent.anwser('Como quiser!')
            return True
			
        elif 'que dia é hoje' in command:
            today = datetime.now()
            today_date = today.strftime('%d/%m/%Y')
            self.assistent.anwser('Hoje é dia: '+today_date)
            return True

        elif 'quantas horas' in command or 'que horas são' in command:
            today = datetime.now()
            today_date = today.strftime('%H:%M')
            self.assistent.anwser('São: '+today_date)
            return True

        elif command =='repita' or command == 'repita o que eu disser':
            self.assistent.play_sound('accepted.mp3')
            self.repeat()
            return True

        elif 'reiniciar sistema' in command:
            self.assistent.anwser('Reiniciando!')
            os.system('sudo reboot')
            return True

        elif command in ['quais são as últimas notícias', 'me dê as últimas notícias', 'me atualize das noticias', 'últimas notícias']:
            return self.last_news()

        elif 'onde fica' in command or 'pesquise' in command:
            self.google_search(command)
            return True

        elif 'status da captação' in command:
            self.show_energy_threshold()
            return True

        elif 'atualizar' in command or 'atualize' in command:
            return self.update_asistent()

        else:
            return False
    
    def repeat(self):
        self.assistent.anwser('Pode falar')
        youSaid = self.assistent.voice_capture(message = "Escutando", phrase_time_limit = self.assistent.phrase_time_limit)
        self.assistent.writeMessage('Acho que você disse: "'+youSaid+'"')
        self.assistent.anwser('Acho que você disse: "'+youSaid)

    def last_news(self):
        site_news = requests.get("https://news.google.com/news/rss?ned=pt_br&gl=BR&hl=pt")
        noticias =  BeautifulSoup(site_news.text, 'html.parser')
        for noticia in noticias.findAll('item')[:5]:
            message = noticia.title.text
            self.assistent.anwser(message)
        return True

    def google_search(self, keywords):
        keywords = keywords.replace(self.assistent.hotword, "")
        keywords = keywords.replace(" ", "+")
        search = requests.get("https://www.google.com/search?q={}&cr=brazil%20&lr=pt_br".format(keywords))
        search = BeautifulSoup(search.text, 'html.parser')
        for result in search.findAll("div", {"class": "g"})[:5]:
            self.assistent.anwser(result)
    
    def update_asistent(self):   
        self.assistent.anwser('Recebendo atualizações!') 
        os.system('git pull https://danieldrafts:dantesm21@github.com/Danieldrafts/assistent-standard.git')
        os.system('sleep 10 | bash /home/pi/assistent.sh')
        exit()
    
    def show_energy_threshold(self):
        i = 0
        for i in range(0 < 7):
            print("Current ambient caption: "+str(self.assistent.recognizer.energy_threshold))
            i = i+1
            time.sleep(2)