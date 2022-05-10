import requests
from bs4 import BeautifulSoup

URL = 'https://2011.bolshoi.ru/timetable/'
HEADERS = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
           'accept':'*/*'}

def get_html(url,params = None):
    r = requests.get(url,headers=HEADERS,params=params)
    return r

class Perfomanses:
    def __init__(self,name,time,stage,descr):
        self.name = name
        self.time = time
        self.stage = stage
        self.descr = descr

    def __str__(self):
        return (f'{self.name}${self.time}${self.stage}${self.descr}').split('$')


def get_content(html):
    soup = BeautifulSoup(html,'html.parser')
    items = soup.find_all('div',class_='DATE timetable_content') #Separate of datas
    collection_by_data = []
    for item in items:
        data = item['id']
        info_of_data = item.find_all('div',class_='HALL')
        timetable = []
        for one_spect in info_of_data:
            perfomance = one_spect.find_next(class_= 'timetable_content__performance_title')
            description = one_spect.find_next('p',class_='timetable_content__performance_description')
            content_place = one_spect.find_next('td',class_='timetable_content__place').get_text()
            place_time = (''.join(filter(bool, content_place.split('\n'))))
            place = (' '.join(filter(bool, place_time.split('\t')))).split()
            stage = ' '.join(place[:len(place)-1])
            time = place[-1]
            descrip = " ".join((description.text).split())
            actual_perf = Perfomanses(perfomance.text,time,stage,descrip)
            timetable.append(actual_perf.__str__())
        collection_by_data.append({data:timetable})
    return collection_by_data

def parse():
    html = get_html(URL)
    perfomances = []
    if html.status_code == 200:
        perfomances.extend(get_content(html.text))
        return perfomances
    else:
        print('Error')

parse()
timetable = parse()
print(timetable)
