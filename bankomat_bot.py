import telebot
import time

TOKEN = ''

bot = telebot.TeleBot(TOKEN)

balance = 1000
history = []
pin = "1234"
autorization = False


operation = ("Проверить баланс", "Снять деньги", "Пополнить счет", "История операций")

kb_menu = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
kb_menu.add(*operation)

def save_log(operation, summ, balance):
    now_time = time.ctime()
    history_list = {
        "time": now_time,
        "operation": operation,
        "amount": summ,
        "balance": balance
    }
    history.append(history_list)

@bot.message_handler(commands=['start'])
def enter(message):
    global autorization
    autorization = False
    bot.send_message(message.chat.id, "Введите PIN")


@bot.message_handler(func=lambda message: message.text == "Проверить баланс")
def show_balance(message):
    if autorization:
        bot.send_message(message.chat.id, f"Ваш баланс: {balance}")
        save_log("Проверка текущего баланса", 0, balance)
    else:
        enter(message)

@bot.message_handler(func=lambda message: message.text == "Снять деньги")
def withdraw_money(message):
    bot.send_message(message.chat.id,"Введите сумму: ")
    bot.register_next_step_handler(message, minus)

def minus(message):
    global balance
    summ = float(message.text)
    if 0 < summ <= balance:
        balance -= summ
        bot.send_message(message.chat.id,f"Выдано: {summ}")
        save_log("Снятие средств: ", summ, balance)
    elif summ <= 0:
        bot.send_message(message.chat.id,"Проверьте введенную Вами сумму")
    else:
        bot.send_message(message.chat.id,"У Вас недостаточное количество средств")

@bot.message_handler(func=lambda message: message.text == "Пополнить счет")
def deposit_money(message):
    bot.send_message(message.chat.id,"Введите сумму для пополнения счета: ")
    bot.register_next_step_handler(message, plus)

def plus(message):
    global balance
    summ = float(message.text)
    if summ > 0:
        balance += summ
        bot.send_message(message.chat.id,"Пополнение счета успешно завершено")
        save_log("пополнение счета: ", summ, balance)
    else:
        bot.send_message(message.chat.id,"Проверьте введенную Вами сумму")

@bot.message_handler(func=lambda message: message.text == "История операций")
def show_history(message):
    global history
    bot.send_message(message.chat.id, str(history))
    if not history:
        bot.send_message(message.chat.id,"Операций нет")


@bot.message_handler(func=lambda message: True)
def initial(message):
    global autorization

    if message.text == pin:
        bot.send_message(message.chat.id,"PIN верный")
        autorization = True
        bot.send_message(message.chat.id, "Выберите команду:", reply_markup=kb_menu)
    else:
        bot.send_message(message.chat.id, "Введен неверный PIN. Попробуйте снова")
    return

bot.polling()















