import telebot
from telebot import types
import parse
import maly_parser
from settings import BOT_TOKEN


bot = telebot.TeleBot(BOT_TOKEN)

user_date = ''

@bot.message_handler(commands=['start'])
def start(message):
    sent = bot.send_message(message.chat.id, 'Введите дату в формате - "02.05" (число,месяц)')
    bot.register_next_step_handler(sent, verify_date)

def verify_date(message):
   try:
      date = (message.text).split('.')
      day,month = date[0],date[1]
      year = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
      if int(month)>12 or int(month)<1:
         sent = bot.send_message(message.chat.id,f'{month} месяца нет, введите корректную дату')
         bot.register_next_step_handler(sent,verify_date)
         return
      elif int(day)>year[int(month)] or int(day)<1:
         sent = bot.send_message(message.chat.id,f'В {month} месяце всего {year[int(month)]} дней, введите корректную дату')
         bot.register_next_step_handler(sent,verify_date)
         return
      elif len(day) == 1 or len(month)==1:
         sent = bot.send_message(message.chat.id,'Ты,возможно, забыл про ведущие нули в дате - 06.05.Попробуй еще раз')
         bot.register_next_step_handler(sent,verify_date)
         return
      bot.send_message(message.chat.id,f'Ваша дата - {day}.{month}')
      global user_date
      user_date = f'{day}.{month}'
   except:
      sent = bot.send_message(message.chat.id,'Упс,ты ввел, наверное, не дату. Попробуй ещё. Обрати внимание на формат - 06.05(через точку)')
      bot.register_next_step_handler(sent,verify_date)
      return

   kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)
   btn1 = types.KeyboardButton(text='Большой театр')
   btn2 = types.KeyboardButton(text='Малый театр')
   kb.add(btn1, btn2)
   bot.send_message(message.chat.id, 'Теперь выберите театр:', reply_markup=kb)

@bot.message_handler(func=lambda message:message.text=='Большой театр')
def bolshoi(message):
   bot.send_message(message.chat.id,f'Вы выбрали Большой театр, на дату - {user_date}\n Гружу афишу, подождите')
   timetable_to_user = parse.parse(user_date)
   if not timetable_to_user:
      answer = f'В ваш день представлений нет'
      bot.send_message(message.chat.id, answer)
   else:
      answer = f'Афиша на {user_date}'
      bot.send_message(message.chat.id,answer)
      for i, element in enumerate(timetable_to_user, 1):
         info = f'{i}.{element.__str__()}'
         bot.send_message(message.chat.id, info)
   bot.send_message(message.chat.id, 'Если хотите афишу на еще какой-то день, нажмите /start, '
                                     'если нет - то всего хорошего!')

@bot.message_handler(func=lambda message:message.text=='Малый театр')
def malyi(message):
   bot.send_message(message.chat.id,f'Вы выбрали Малый театр, на дату - {user_date}\nГружу афишу,подождите')
   timetable_to_user = maly_parser.parse(user_date)
   if not timetable_to_user:
      answer = f'В ваш день представлений нет'
      bot.send_message(message.chat.id, answer)
   else:
      answer = f'Афиша на {user_date}'
      bot.send_message(message.chat.id, answer)
      for i,element in enumerate(timetable_to_user,1):
         info = f'{i}.{element.__str__()}'
         bot.send_message(message.chat.id, info)
   bot.send_message(message.chat.id, 'Если хотите афишу на еще какой-то день, нажмите /start, '
                                              'если нет - то всего хорошего!')


@bot.message_handler(func = lambda message:True)
def theatre(message):
   bot.send_message(message.chat.id,'Если вы хотите увидеть список постановок,нажмите /start')

bot.polling()
