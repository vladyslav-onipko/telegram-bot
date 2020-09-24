import telebot

from telebot import types
from link_parser import ParsBelok
from config import KEYWORDS, TOKEN, DB_NAME
from sqlighter import User

bot = telebot.TeleBot(TOKEN)
parser = ParsBelok()
db = User(db_name=DB_NAME)


@bot.message_handler(commands=['subscribe'])
def subscribe(message: types.Message):
    if not db.exist_user(message.from_user.id):
        db.add_user(message.from_user.id)
        bot.send_message(message.chat.id, 'You have just subscribe 😊 To unsubscribe enter /unsubscribe')
    else:
        bot.send_message(message.chat.id, 'You are already subscribed 😊')


@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message: types.Message):
    if not db.exist_user(message.from_user.id):
        bot.send_message(message.chat.id, 'You have not been subscribed yet! To subscribe enter /subscribe')
    else:
        db.delete_user(message.from_user.id)
        bot.send_message(message.chat.id, 'You have just unsubscribed 😢')


@bot.message_handler(commands=['start'])
def start_massage(message):
    stic = open('static/AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, stic)
   
    whey_button = types.KeyboardButton('Whey Protein')
    bcaa_button = types.KeyboardButton('BCAA')
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    keyboard.add(whey_button, bcaa_button)
   
    if not db.get_user():
        bot.send_message(message.chat.id, 'Welcome, my name is {0.first_name}!'
                                          ' I am checking sales bot.\n'
                                          'You can /subscribe to get information about sales.'.format(bot.get_me()),
                         parse_mode='html', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def start_massage(message):
    if db.get_user():
        if message.text == 'Whey Protein':
            products = parser.parse(keyword=KEYWORDS.get('whey protein'))
            if products:
                for product in products:
                    bot.send_message(
                        message.chat.id, 'Product name: {0}\nLink: {1}\nOld price: {2}\nNew price: {3}'.format(
                            product['title'], product['link'], product['price_old'], product['price_new']))
            else:
                bot.send_message(message.chat.id, 'Unfortunately we do not have sales now 😢')
        elif message.text == 'BCAA':
            products = parser.parse(keyword=KEYWORDS.get('bcaa'))
            if products:
                for product in products:
                    bot.send_message(
                        message.chat.id, 'Product name: {0}\nLink: {1}\nOld price: {2}\nNew price: {3}'.format(
                            product['title'], product['link'], product['price_old'], product['price_new']))
            else:
                bot.send_message(message.chat.id, 'Unfortunately we do not have sales now 😢')
    else:
        bot.send_message(message.chat.id, 'You have to /subscribe to check sales')


if __name__ == '__main__':
    bot.polling(none_stop=True)