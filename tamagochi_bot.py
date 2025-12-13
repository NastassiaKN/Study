import telebot
import time

TOKEN = ''

bot = telebot.TeleBot(TOKEN)

hunger = 100
energy = 100

def hunger_update():
    global hunger
    hunger = hunger - 5
    if hunger < 0:
        hunger = 0

def emotion(message):
    global hunger
    global energy

    if energy < 30 and hunger < 30:
        bot.send_message(message.chat.id, "Питомец очень устал и он голоден😞")
    elif 30 >= energy < 60 and 30 >= hunger < 70:
        bot.send_message(message.chat.id, "😺 Питомец чувствует себя нормально")
    elif energy >= 60 and hunger >= 70:
        bot.send_message(message.chat.id, "Питомец счастлив!😸✨")
    else:
        bot.send_message(message.chat.id, "😼")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет) Я твой виртуальный питомец 😸 Тамагочи!\n"
                                      "Я буду рад твоей заботе и вниманию!💛\n"
                                      "Вот что ты можешь сделать прямо сейчас:\n"
                                      "🍗 /feed - покормить меня, чтобы я был сытым\n"
                                      "⚾️ /play - поиграть со мной и поднять настроение\n"
                                      "😴 /sleep - дать мне отдохнуть и восстановить энергию\n"
                                      "📊 /status - узнать, как я себя чувствую\n"
                                      "Давай начнем наше приключение!🚀")

@bot.message_handler(commands=['feed'])
def send_feed(message):
    kb_feed = telebot.types.InlineKeyboardMarkup()
    but_1 = telebot.types.InlineKeyboardButton("🥩(+15⚡️)", callback_data="feed_15")
    but_2 = telebot.types.InlineKeyboardButton("🐟(+10⚡️)", callback_data="feed_10")
    but_3 = telebot.types.InlineKeyboardButton("🥕(+5⚡️)", callback_data="feed_5")
    kb_feed.add(but_1, but_2, but_3)

    bot.send_message(message.chat.id, "🍽️Выбери чем ты хочешь покормить питомца:", reply_markup=kb_feed)

@bot.callback_query_handler(func=lambda call: call.data.startswith("feed_"))
def callback_feed(call):
    global hunger
    global energy

    summa = int(call.data.split("_")[1])
    energy = energy + summa

    if energy > 100:
        energy = 100

    if summa == 15:
        product = "🥩 Мясо"
        hunger = hunger + 30
    elif summa == 10:
        product = "🐟 Рыба"
        hunger = hunger + 20
    else:
        product = "🥕 Морковка"
        hunger = hunger + 10

    if hunger > 100:
        hunger = 100

    if hunger == 100:
        reaction = "Я сыт до краев!😻🍖"
    else:
        reaction = "Вкусно!😺"

    bot.send_message(call.message.chat.id, reaction)
    bot.send_message(call.message.chat.id, f"{product} ...ммм! ⚡️Энергия: {energy}/100! Может поиграем?🪀")


@bot.message_handler(commands=['play'])
def send_play(message):
    kb_play = telebot.types.InlineKeyboardMarkup()
    but_1 = telebot.types.InlineKeyboardButton("🎾(-20⚡️)", callback_data="play_20")
    but_2 = telebot.types.InlineKeyboardButton("🎣(-15⚡️)", callback_data="play_15")
    but_3 = telebot.types.InlineKeyboardButton("🎮(-10⚡️)", callback_data="play_10")
    kb_play.add(but_1, but_2, but_3)

    bot.send_message(message.chat.id, "😸Выбери во что поиграем:", reply_markup=kb_play)


@bot.callback_query_handler(func=lambda call: call.data.startswith("play_"))
def callback_play(call):
    global hunger
    global energy

    summa = int(call.data.split("_")[1])
    if summa == 20:
        product = "🎾 Теннис"
    elif summa == 15:
        product = "🎣 Рыбалка"
    else:
        product = "🎮 PlayStation"

    if energy >= summa:
        energy = energy - summa
        bot.send_message(call.message.chat.id, f"{product}...было весело!⚡️Энергия:{energy}/100! Фух...я устал🥱")
    elif energy < summa:
        bot.send_message(call.message.chat.id,"У меня нет энергии для этой игры😿")

    hunger = hunger - 10
    if hunger < 0:
        hunger = 0
        bot.send_message(call.message.chat.id, "Я голоден😿")


@bot.message_handler(commands=['sleep'])
def send_sleep(message):
    bot.send_message(message.chat.id, "🌖✨Питомец засыпает")
    for i in range(3):
        time.sleep(1)
        bot.send_message(message.chat.id, "💤" * (i + 1))

    global hunger
    global energy

    summa = 25
    energy = energy + summa

    if energy > 100:
        energy = 100


    bot.send_message(message.chat.id, f"😻Я выспался! ⚡️Энергия: {energy}/100! Может поиграем?🪀")


@bot.message_handler(commands=['status'])
def send_status(message):
    global hunger
    global energy
    hunger_update()

    bot.send_message(message.chat.id, f"📊 Статус питомца:\n"
                                      f"️⚡️Энергия: {energy}/100\n"
                                      f"🍗Сытость: {hunger}/100\n")
    emotion(message)


@bot.message_handler(func=lambda message: message.text == "Привет")
def hello(message):
    bot.send_message(message.chat.id, "Привет👋 Виделись уже!)")


@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(message.chat.id, "Ха-ха😹...Я понял мы играем в повтори за мной!😼")
    bot.send_message(message.chat.id, message.text)

bot.polling()