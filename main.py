#Сгенерировано с помощью https://chat.openai.com/chat

import telebot
import random

with open('pas.txt', 'r') as file:
    TOKEN = file.read()

bot = telebot.TeleBot(TOKEN)

used_cities = []

with open('cities.txt', 'r', encoding='utf-8') as file:
    cities = [line.strip().lower() for line in file]

@bot.message_handler(commands=['start'])
def start_message(message):
    used_cities.clear()
    bot.send_message(message.chat.id, 'Привет! Давай сыграем в игру в города. Начни первым!')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_word = message.text.lower()

    if user_word in used_cities:
        bot.send_message(message.chat.id, "Этот город уже был назван. Попробуй другой.")
        return

    if user_word not in cities:
        bot.send_message(message.chat.id, "Я не знаю такого города. Попробуй другой.")
        return

    if len(used_cities) > 0 and user_word[0] != used_cities[-1][-1]:
        bot.send_message(message.chat.id, "Этот город не подходит. Попробуй другой.")
        return
    
    last_letter = user_word[-1]
    if last_letter in ['й', 'ъ', 'ь', 'ы']:
        last_letter = user_word[-2]

    used_cities.append(user_word)

    bot.send_message(message.chat.id, f"Отлично! Твой город - {user_word.capitalize()}. Теперь мой ход.")

    possible_cities = [city for city in cities if city[0] == last_letter and city not in used_cities]

    if not possible_cities:
        bot.send_message(message.chat.id, "Я не знаю больше городов на эту букву. Вы выиграли!")
        return

    computer_choice = random.choice(possible_cities)
    used_cities.append(computer_choice)

    bot.send_message(message.chat.id, f"Мой город - {computer_choice.capitalize()}. Теперь твой ход.")

bot.polling()
