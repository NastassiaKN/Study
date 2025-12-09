import telebot
import requests


TOKEN = ''

class TelegramBot:
    def __init__(self):
        self.bot = telebot.TeleBot(TOKEN)
        self.summa = ""
        self.client = ClientNBRB()


    def menu_value(self):
        curr = ("USD", "EUR", "RUB")
        self.kb_menu_value = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        self.kb_menu_value.add(*curr)

    def work_bot(self):
        self.menu_value()
        self.start_bot()
        self.bot.polling()

    def start_bot(self):
        @self.bot.message_handler(commands=['start'])
        def welcome(message):
            self.bot.send_message(message.chat.id, "Добро пожаловать в конвертер!")
            self.bot.send_message(message.chat.id, "Текущий курс:\n"
                                                   f"USD: {self.client.get_val(1, "USD")}\n"
                                                   f"EUR: {self.client.get_val(1, "EUR")}\n"
                                                   f"RUB: {self.client.get_val(100, "RUB")}\n")
            self.bot.send_message(message.chat.id,"Выберите валюту", reply_markup=self.kb_menu_value)

            self.bot.register_next_step_handler(message, enter_curr)

        def enter_curr(message):
            self.bot.send_message(message.chat.id, f"Вы выбрали: {message.text}\n"
                                                   "Введите сумму: ")
            self.summa = message.text
            self.bot.register_next_step_handler(message, enter_convert)

        def enter_convert(message):
            self.bot.send_message(message.chat.id, f"{message.text} {self.summa} в BYN = "
                                                   f"{self.client.get_val(float(message.text), self.summa)}")

class ClientNBRB:
    def __init__(self):
        self.usd_url = "https://api.nbrb.by/exrates/rates/USD?parammode=2"
        self.eur_url = "https://api.nbrb.by/exrates/rates/EUR?parammode=2"
        self.rub_url = "https://api.nbrb.by/exrates/rates/RUB?parammode=2"


    def get_val(self, valute, currency):
        if currency == "USD":
            currency_url = self.usd_url
        elif currency == "EUR":
            currency_url = self.eur_url
        elif currency == "RUB":
            currency_url = self.rub_url
        else:
            raise Exception("Доступно: USD, EUR, RUB")

        req = requests.get(currency_url)
        data = req.json()
        scale = data["Cur_Scale"]
        rate = data["Cur_OfficialRate"]
        byn_for1 = rate / scale
        rate_data = byn_for1 * valute
        return round(rate_data, 4)

if __name__ == '__main__':
    bot = TelegramBot()
    bot.work_bot()