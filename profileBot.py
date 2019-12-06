# encoding=utf8
import telebot
import types
bot = telebot.TeleBot('1024136960:AAFt2cCEF1zWlaTMe3lymbzqk-mmvJWxlQ0')
name = ''
sex = ''
choiceToChange = ''


@bot.message_handler(commands=['start'])

def start_message(message):
	bot.send_message(message.chat.id, 'Привет, как вас зовут?')
	bot.register_next_step_handler(message, get_name)

def get_name(message):
	global name

	name = message.text
	keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
	keyboard.row('Мужской', 'Женский')
	
	bot.send_message(message.chat.id, 'Выберите пол', reply_markup=keyboard)
	bot.register_next_step_handler(message, get_sex)

def get_sex(message):
	global sex
	
	sex = message.text

	bot.send_message(message.chat.id, "Укажите возраст", reply_markup=telebot.types.ReplyKeyboardRemove())
	bot.register_next_step_handler(message, get_age)

def get_age(message):
	global age
	global keyboard1
	
	age = message.text
	
	try:
		age = int(message.text)
	except Exception:
		bot.send_message(message.chat.id, 'Некоректное значение, попробуйте ещё раз')
		return bot.register_next_step_handler(message, get_age)
	
	keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
	keyboard1.row('Изменить имя', 'Изменить пол')
	keyboard1.row('Изменить возраст')
	
	bot.send_message(message.chat.id, u'Ваше имя: {}\nПол: {} \nВозраст: {}'
		.format(name, sex, age), reply_markup=keyboard1)
	bot.register_next_step_handler(message, get_menu)


def get_menu(message):
	global keyboard1
	global choiceToChange
	global status
	
	status = True
	choiceToChange = message.text
	output = u'Вы выбрали "{}", введите новое значение'.format(choiceToChange)
	
	if choiceToChange == u'Изменить пол':
		keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
		keyboard.row('Мужской', 'Женский')
		bot.send_message(message.chat.id, output, reply_markup=keyboard)
		bot.register_next_step_handler(message, get_choice)
	elif choiceToChange == u'Изменить имя' :
		bot.send_message(message.chat.id, output, reply_markup=telebot.types.ReplyKeyboardRemove())
		bot.register_next_step_handler(message, get_choice)
	elif choiceToChange == u'Изменить возраст' :
		bot.send_message(message.chat.id, output, reply_markup=telebot.types.ReplyKeyboardRemove())
		bot.register_next_step_handler(message, get_choice)
	else :
		bot.send_message(message.chat.id, 'Выберите с меню', reply_markup=keyboard1)
		bot.register_next_step_handler(message, get_menu)


def get_choice(message):
	global name
	global age
	global sex

	if choiceToChange == u'Изменить имя':
		name = message.text
	elif choiceToChange == u'Изменить пол':
		sex = message.text
	elif choiceToChange == u'Изменить возраст' :
			try:
				if age != int(message.text):
					age = int(message.text)
				else:
					bot.send_message(message.chat.id, 'Не повторять!')
					return bot.register_next_step_handler(message, get_choice)
			except Exception:
				bot.send_message(message.chat.id, "Некоректное значение, попробуйте ещё раз")
				return bot.register_next_step_handler(message, get_choice)
	
	keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
	keyboard2.row('Можно в меню?')
	
	bot.send_message(message.chat.id, u'Ваше имя: {} \nпол: {} \nвозраст: {}'
		.format(name, sex, age), reply_markup=keyboard2)
	bot.register_next_step_handler(message, get_infinity)

def get_infinity(message):
	keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
	keyboard1.row('Изменить имя', 'Изменить пол')
	keyboard1.row('Изменить возраст')
	
	bot.send_message(message.chat.id, 'да, пожалуйста', reply_markup=keyboard1)
	bot.register_next_step_handler(message, get_menu)

bot.polling(none_stop=True, interval=0)