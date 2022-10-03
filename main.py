import telebot
from telebot import types
import yaml


bot = telebot.TeleBot('5685870777:AAFxVf3llw8yij4ZmZdCfsrI3AbFTJi9kio')


@bot.message_handler(commands=['start'])
def choose_categories(message):
    with open('categories.yaml', 'r', encoding="utf-8") as categories_file:
        dict_names_of_buttons = yaml.load(categories_file, Loader=yaml.FullLoader)
        buttons = []
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        for button_name in dict_names_of_buttons.keys():
            buttons.append(types.KeyboardButton(button_name))
        markup.add(*buttons)
        bot.send_message(message.chat.id, 'Выберите категорию', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def choose_farmers(message):
    emoji = u"\U0001F39B"

    with open('categories.yaml', 'r', encoding="utf-8") as categories_file:
        dict_names_of_buttons = yaml.load(categories_file, Loader=yaml.FullLoader)
        if message.text not in dict_names_of_buttons.keys():
            return bot.send_message(
                message.chat.id,
                f'Друг, ты попал немного не туда. Чтобы вернуться к фермерам, нажми на четыре точки {emoji} в нижнем правом углу.'
            )
        chosen_category = dict_names_of_buttons[message.text]
    with open(f'farmers/{chosen_category}.yaml', 'r', encoding="utf-8") as farmers_file:
        dict_names_of_farmers = yaml.load(farmers_file, Loader=yaml.FullLoader)
        if dict_names_of_farmers is None:
            return bot.send_message(
                message.chat.id, f'Пока в этой категории нету фермеров. Если вы знаете таких, сообщите нам.'
            )
        buttons = []
        markup = types.InlineKeyboardMarkup(row_width=3)
        for name_of_button, info in dict_names_of_farmers.items():
            if 'url' in info:
                buttons.append(types.InlineKeyboardButton(name_of_button, info['url']))
            elif 'text' in info:
                buttons.append(types.InlineKeyboardButton(name_of_button, callback_data=f'{name_of_button}-{chosen_category}'))
        markup.add(*buttons)
        photo_1 = open(f'pictures/{chosen_category}.JPG', 'rb')
        bot.send_photo(message.chat.id, photo_1, 'Наши мастера в этой категории', reply_markup=markup)



@bot.callback_query_handler(func=lambda call:True)
def send_text(call):
    name_of_button, chosen_category = call.data.split('-')
    with open(f'farmers/{chosen_category}.yaml', 'r', encoding="utf-8") as farmers_file:
        dict_names_of_farmers = yaml.load(farmers_file, Loader=yaml.FullLoader)
        bot.send_message(call.message.chat.id, dict_names_of_farmers[name_of_button]['text'])


bot.polling(none_stop=True)