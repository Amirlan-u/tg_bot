import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup
import fake_useragent

def imdb_anime():
    fake = fake_useragent.UserAgent()
    useragent = {"User-Agent": fake.random}
    url = ('https://www.imdb.com/search/keyword/?keywords=anime&sort=user_rating,desc&mode=detail&page=1')
    response = requests.get(url, headers = useragent)
    soup = BeautifulSoup(response.text, 'lxml')

    name = []

    items = soup.find_all('div', class_="lister-item mode-detail")
    for i in items:
        names = i.h3.a.text
        name.append(names)
    stars = []
    for n, i in enumerate(items, start=1):
        rating = i.find("div", class_ = "inline-block ratings-imdb-rating").text.replace('\n', '')
        stars.append(rating)
    return name, stars
def imdb_films():
    url = ('https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    name = []

    items = soup.find_all('div', class_="lister-item mode-advanced")
    for n, i in enumerate(items, start=1):
        names = i.h3.a.text
        name.append(names)
    stars = []
    for n, i in enumerate(items, start=1):
        rating = i.find("div", class_ = "inline-block ratings-imdb-rating").text.replace('\n', '')
        stars.append(rating)
    return name, stars
def imdb_shows():
    url = ('https://www.imdb.com/search/title/?count=100&languages=en&num_votes=1000,&sort=num_votes,desc&title_type=')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    name = []

    items = soup.find_all('div', class_="lister-item mode-advanced")
    for n, i in enumerate(items, start=1):
        names = i.h3.a.text
        name.append(names)
    stars = []
    for n, i in enumerate(items, start=1):
        rating = i.find("div", class_="inline-block ratings-imdb-rating").text.replace('\n', '')
        stars.append(rating)
    stars.sort(reverse=True)
    return name, stars

bot = telebot.TeleBot('5907647190:AAGUaTMwl_ON3M9zfQfc2i86xCumL-Ky0PQ')
@bot.message_handler(commands=['start'])

def start_message(message):
    bot.send_message(message.chat.id, 'Привет, что хочеш узнать рейтинг аниме, фильмов или может сериалов?')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Рейтинг аниме")
    markup.add("Рейтинг сериалов")
    markup.add("Рейтинг фильмов")
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

name = list()
stars = list()
@bot.message_handler(content_types = 'text')

def message_reply(message):
    if message.text.lower() == "рейтинг аниме":
        anime, raiting_anime = imdb_anime()
        bot.send_message(message.chat.id, "1 - " + anime[0] + " " + raiting_anime[0])
        bot.send_message(message.chat.id, "2 - " + anime[1] + " " + raiting_anime[1])
        bot.send_message(message.chat.id, "3 - " + anime[2] + " " + raiting_anime[2])


        if len(name) >= 1:
            name.clear()
            stars.clear()
        name.append(anime)
        stars.append(raiting_anime)


    elif message.text.lower() == "рейтинг фильмов":
        films, raiting_films = imdb_films()
        bot.send_message(message.chat.id, "1 - " + films[0] + " " + raiting_films[0])
        bot.send_message(message.chat.id, "2 - " + films[1] + " " + raiting_films[1])
        bot.send_message(message.chat.id, "3 - " + films[2] + " " + raiting_films[2])

        if len(name) >= 1:
            name.clear()
            stars.clear()
        name.append(films)
        stars.append(raiting_films)

    elif message.text.lower() == "рейтинг сериалов":
        shows, raiting_shows = imdb_shows()
        bot.send_message(message.chat.id, "1 - " + shows[0] + " " + raiting_shows[0])
        bot.send_message(message.chat.id, "2 - " + shows[1] + " " + raiting_shows[1])
        bot.send_message(message.chat.id, "3 - " + shows[2] + " " + raiting_shows[2])


        if len(name) >= 1:
            name.clear()
            stars.clear()
        name.append(shows)
        stars.append(raiting_shows)

    else:
        bot.send_message(message.chat.id, 'Попробуй снова')
    try:
        msg = bot.reply_to(message, "Введите нужную цифру. Всего " + str(len(name[0])))
        bot.register_next_step_handler(msg, print_place)
    except Exception as e:
        bot.reply_to(message, 'Попробуй снова')

def print_place(message):
    if message.text.isdigit():
        msg = message.text
        msg = int(msg)
        if msg <= 0:
            bot.send_message(message.chat.id, "Нужно ввести от 1 до " + str(len(name[0])))
        elif msg > len(name[0]):
            bot.send_message(message.chat.id, "Нужно ввести от 1 до " + str(len(name[0])))
        else:
            bot.send_message(message.chat.id, name[0][msg - 1] + " " + stars[0][msg - 1])
    if not message.text.isdigit():
        bot.send_message(message.chat.id, "Попробуй снова")
bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

bot.infinity_polling()