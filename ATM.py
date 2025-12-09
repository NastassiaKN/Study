import time


class ATM:
    def __init__(self):
        self.__balance = 1000
        self.__history = []
        self.__pin = "1111"
        self.__lock = False

    def initial(self):
        print("Введите PIN: ")
        for i in range(3):
            user_pin = str(input())
            if user_pin == self.__pin:
                print("PIN верный")
                return True
            else:
                print(f"Введен неверный PIN. Осталось попыток: {2 - i}")

        print("Ваша карта заблокирована. Обратитесь в банк.")
        self.__lock = True
        return False

    @property
    def lock(self):
        return self.__lock

    def __save_log(self, operation, summ, balance):
        now_time = time.ctime()
        history_list = {
            "time": now_time,
            "operation": operation,
            "amount": summ,
            "balance": balance
        }
        self.__history.append(history_list)


    def work(self):
        status_work = True
        while status_work:
            print(
                """
            1. Проверить баланс
            2. Снять деньги
            3. Пополнить счет
            4. История операций
            5. Выйти""")

            command = input("Введите команду: ")

            if command == "1":
                print(f"Ваш баланс: {self.__balance}")
                self.__save_log("Проверка текущего баланса", 0, self.__balance)

            elif command == "2":
                print("Введите сумму: ")
                summ = float(input())
                if 0 < summ <= self.__balance:
                    self.__balance -= summ
                    print(f"Выдано: {summ}")
                    self.__save_log("Снятие средств: ", summ, self.__balance)
                elif summ <= 0:
                    print("Проверьте введенную Вами сумму")
                else:
                    print("У Вас недостаточное количество средств")

            elif command == "3":
                print("Введите сумму для пополнения счета: ")
                summ = float(input())
                if summ > 0:
                    self.__balance += summ
                    print("Пополнение счета успешно завершено")
                    self.__save_log("пополнение счета: ", summ, self.__balance)
                else:
                    print("Проверьте введенную Вами сумму")

            elif command == "4":
                if not self.__history:
                    print("Операций нет")

                title_history = "История операций:\n"
                for history_list in self.__history:
                    title_history += f"{history_list}\n"
                print(title_history)

            elif command == "5":
                print("Операция успешно завершена. Заберите карту!")
                status_work = False

            else:
                print("Неверная команда. Попробуйте снова.")

atm = ATM()
status = True
while status:

    if atm.lock:
        break

    if not atm.initial():
        continue

    atm.work()
    status = False

















