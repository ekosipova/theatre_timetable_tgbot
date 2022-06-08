import requests
from bs4 import BeautifulSoup


URL = 'http://www.maly.ru/afisha'
HEADERS = {'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
           'accept':'*/*'}

def get_html(url,params = None):
    r = requests.get(url,headers=HEADERS,params=params)
    return r

def count_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = [x.text for x in soup.find(id="affichesearchform-date").find_all('option')]
    year = {'Янв':1,'Фев':2,'Мар':3,'Апр':4,'Май':5,'Июн':6,'Июл':7,'Авг':8,'Сен':9,'Окт':10,'Ноя':11,'Дек':12}
    our_year = []
    for page in pagination:
        date = page.split()
        our_year.append((str(year[date[0]]),date[1]))
    return our_year

class Perfomance:
    def __init__(self,name,time,stage):
        self.name = name
        self.time = time
        self.stage = stage

    def __str__(self):
        return f'Представление: {self.name}\nВремя начала: {self.time}\nСцена: {self.stage}'

def convert_date(data):
    year = {'января': '01', 'февраля': '02', 'марта':'03', 'апреля':'04', 'мая':'05', 'июня':'06', 'июля':'07', 'августа':'08', 'сентября':'09', 'октября':'10', 'ноября':'11', 'декабря':'12'}
    day = (data.split())[0]
    month = year[(data.split())[1]]
    if len(day) == 1:
        return f'0{day}.{month}'
    return f'{day}.{month}'

def get_content(html):
    soup = BeautifulSoup(html,'html.parser')
    items = soup.find_all('div',class_='affiche-day-block')
    collection_by_days = []
    for item in items:
        key = item.find('div',class_='dayname').text
        date = convert_date(key)
        perfomances = item.find_all('a',class_='l_title')
        day_timetable = []
        for perf in perfomances:
            place_time = ((perf.find_next('div',class_="affiche-item__block-right primary-flex").get_text()).split())[:-2]
            time = place_time[-1]
            stage = ' '.join(place_time[:len(place_time)-1])
            name = (perf.text).capitalize()
            perfomance = Perfomance(name,time,stage)
            day_timetable.append(perfomance)
        collection_by_days.append({date:day_timetable})
    return collection_by_days



def parse(date):
    html = get_html(URL)
    perfomances = []
    items_to_user = []
    if html.status_code == 200:
        pages_count = count_pages(html.text)
        for p in range(2):
            month_year = pages_count[p]
            htm = get_html(URL,params={'month':month_year[0],'year':month_year[1]})
            perfomances.extend(get_content(htm.text))
        for element in perfomances:
            if date in element:
                items_to_user = element[date]
        return items_to_user
    else:
        print('Error')



