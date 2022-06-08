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
        return f'Представление: {self.name}\nВремя начала: {self.time}\nСцена: {self.stage}\nДополнительная информация: {self.descr}'


def get_content(html):
    soup = BeautifulSoup(html,'html.parser')
    items = soup.find_all('div',class_='DATE timetable_content') #Separate of datas
    collection_by_datas = []
    for item in items:
        data = '.'.join(((item['id']).split('.'))[:2])
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
            timetable.append(actual_perf)
        collection_by_datas.append({data:timetable})
    return collection_by_datas

def parse(date):
    html = get_html(URL)
    perfomances = []
    items_to_user = []
    if html.status_code == 200:
        perfomances.extend(get_content(html.text))
        for element in perfomances:
            if date in element:
                items_to_user = element[date]
        return items_to_user
    else:
        print('Error')






