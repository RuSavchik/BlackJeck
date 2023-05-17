class Player(object):
    def __init__(self, name, score = 0):
        self.name = name
        self.score = score
    def __str__(self):
        rep = self.name + "\t" + str(self.score)
        return rep
def ask_yes_no(question):
    response = None
    while response not in ("y", "n"):
        response = input(question).lower()
        if response not in ("y", "n"):
            print("Вкажіть коректну відповідь: 'Y' або 'N'.")
    return response
def ask_number(question, low, high):
    response = None
    while response not in range(low,high):
        try:
            response = int(input(question))
        except:
            print("Це не число!")
        else:
            if response not in range(low,high):
                print("Дане число виходить за межі допустимого діапазону.")
    return response
if __name__ == "__main__":
    print("Модуль відкрито напряму, його слід імпортувати")
    input("\n\nТисни 'Enter' для виходу")
