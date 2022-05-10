import telebot
from telebot import types
import parse
import maly_parser



bot = telebot.TeleBot('5210663817:AAHMMgXqfQYdGA-34lJgn4sg3J_8irqZD2U')

@bot.message_handler(commands=['start'])
def start(message):
   kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
   btn1 = types.KeyboardButton(text='Большой театр')
   btn2 = types.KeyboardButton(text='Малый театр')
   kb.add(btn1, btn2)
   bot.send_message(message.chat.id, 'Выберите театр:', reply_markup=kb)

@bot.message_handler(func=lambda message:message.text=='Большой театр')
def bolshoi(message):
   sent = bot.send_message(message.chat.id,'Введите дату в формате - 02/05/2022 (число,месяц,год)\nОбратите внимание, что вводить надо текущий год',reply_markup=types.ReplyKeyboardRemove())
   bot.register_next_step_handler(sent, review_bolshoi)

@bot.message_handler(func=lambda message:message.text=='Малый театр')
def malyi(message):
   sent = bot.send_message(message.chat.id,'Введите дату в формате - 26 апреля(число,месяц)\nАфиша будет дана на текущий год')
   bot.register_next_step_handler(sent,review_malyi)

def review_bolshoi(message):
   data = message.text.split('/')
   day,month,ye = data[0],data[1],data[2]
   year = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
   if int(month)>12 or int(month)<1:
      bot.send_message(message.chat.id,f'{month} месяца нет, нажмите /start и введите снова верную дату')
   elif int(day)>year[int(month)] or int(day)<1:
         bot.send_message(message.chat.id,f'В {month} месяце всего {year[int(month)]} дней, нажмите /start и введите верную дату')
   else:
      user_date = f'{day}.{month}.{ye}'
      timetable = parse.parse()
      items_to_user = []
      for data in timetable:
         if user_date in data:
            items_to_user = data[user_date]
      if not items_to_user: #examination for empty collection
         answer = f'В ваш день представлений нет'
         bot.send_message(message.chat.id,answer)
      else:
         answer = f'Афиша на  {user_date}'
         bot.send_message(message.chat.id, answer)
         for i, element in enumerate(items_to_user,1):
            info = f'{i}.Представление: {element[0]}\nВремя начала: {element[1]}\nСцена: {element[2]}\nДополнительная информация: {element[3]}'
            bot.send_message(message.chat.id,info)

def review_malyi(message):
   data = message.text.split()
   day, month = data[0], data[1]
   year = {'января': 31, 'февраля': 29, 'марта': 31, 'апреля': 30, 'мая': 31, 'июня': 30, 'июля': 31, 'августа': 31, 'сентября': 30, 'октября': 31, 'ноября': 30, 'декабря': 31}
   if month not in year:
      bot.send_message(message.chat.id, f'{month} месяца нет, нажмите /start и введите снова верную дату')
   elif int(day) > year[month] or int(day) < 1:
      bot.send_message(message.chat.id, f'В {month} месяце всего {year[month]} дней, нажмите /start и введите верную дату')
   else:
      user_date = f'{day} {month}'
      timetable = maly_parser.timetable_maly
      items_to_user = []
      for data in timetable:
         if user_date in data:
            items_to_user = data[user_date]
      if not items_to_user:
         answer = f'В ваш день представлений нет'
         bot.send_message(message.chat.id, answer)
      else:
         answer = f'Афиша на {user_date}'
         bot.send_message(message.chat.id, answer)
         for i,element in enumerate(items_to_user,1):
            info = f'{i}.Представление: {element[0]}\nВремя начала: {element[1]}\nСцена: {element[2]}'
            bot.send_message(message.chat.id, info)

@bot.message_handler(func = lambda message:True)
def theatre(message):
   bot.send_message(message.chat.id,'Если вы хотите увидеть список постановок,нажмите /start')

bot.polling()
