import csv
from datetime import date
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd


class WeatherParsing:

    raw_html = ''
    html = ''
    place_w = 'Брест'
    results = [ ]

    def __init__(self):
        self.url = 'https://yandex.by/pogoda/month/june?lat=52.093566&lon=23.685708&via=ms'
        self.path = 'weather.csv'


    def get_html(self):
        req= urllib.request.urlopen(self.url)
        self.raw_html = req.read()
        self.html = BeautifulSoup(self.raw_html, 'html.parser')

    def parsing_w(self):
        weather = self.html.find_all('div', class_ ='climate-calendar-day__detailed-container-center')


        for item in weather:
            w_date = item.find ( 'h6', class_='climate-calendar-day__detailed-day').get_text(strip=True)
            day_degrees = item.find('div','span', class_='temp climate-calendar-day__detailed-basic-temp-day').get_text(strip=True)
            night_degrees = item.find ('div','span', class_='temp climate-calendar-day__detailed-basic-temp-night').get_text(strip=True )
            wind_speed = item.find('div', class_='wind-speed').get_text(strip=True)
            self.results.append({
                'w_date': w_date,
                'w_place': self.place_w,
                'day_degrees' : day_degrees,
                'night_degrees' : night_degrees,
                'wind_speed' : wind_speed

            })

    def save(self):
        with open (self.path, 'w', encoding='utf-8' ) as csv_f :
            file_writer = csv.writer ( csv_f, dialect='excel' )
            file_writer.writerow ( [ 'Дата(Число,день/нед.)', 'Место', 'Температура днем','Температура ночью', 'Скорость ветра м/с' ] )
            i = 1
            for item in self.results :
                file_writer.writerow (
                    [f'{item[ "w_date" ]}, {item[ "w_place" ]},{item[ "day_degrees" ]},{item[ "night_degrees" ]}, {item[ "wind_speed" ]}'])
                i += 1

    def get_average_weather(self):
        aver_day_temp = []
        aver_night_temp = []
        for i in self.results:
            for key, value in i.items():
                if key == 'day_degrees':
                    aver_day_temp.append(int(value.strip('+')))
                elif key == 'night_degrees':
                    aver_night_temp.append(int(value.strip('+')))




        with open (self.path, 'a', encoding='UTF-8') as csv_f:
            file_writer = csv.writer ( csv_f, dialect='excel' )

            file_writer.writerow ([f'\n\n****************** \n Средняя дневная температура {sum(aver_day_temp)//len(aver_day_temp)} градусов Цельсия \n\n Средняя ночная температура {sum(aver_night_temp)//len(aver_night_temp)} градусов Цельсия \n\n********************'])


    def run(self):
        self.get_html()
        self.parsing_w()
        self.save()
        self.get_average_weather()







from dzkurs import WeatherParsing
parser = WeatherParsing()
parser.run()