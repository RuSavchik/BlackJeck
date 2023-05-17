import cards, games


class BJ_Card(cards.Card):
    ACE_VALUE = 1
    @property
    def value(self):
        if self.is_face_up:
            v = BJ_Card.RANKS.index(self.rank) + 1
            if v > 10:
                v = 10   
        else:
            v = None
        return v



class BJ_Deck(cards.Deck):

    def populate(self):
        for suit in BJ_Card.SUITS:
            for rank in BJ_Card.RANKS:
                self.add(BJ_Card(rank, suit))

    def full_up(self):
        if self.rest() != 52:
            print("Залишок карт в колоді: ", self.rest())
            self.clear()
            self.populate()
            self.shuffle()
        else:
            print("Колода повна.")
            self.shuffle()



class BJ_Hand(cards.Hand):
    def __init__(self, name, count = 0):
        super(BJ_Hand, self).__init__()
        self.name = name
        self.bank = BJ_Bank(count)
    def __str__(self):
        rep = self.name + ":\t" + super(BJ_Hand, self).__str__()
        if self.total:
            rep += "(" + str(self.total) + ")"
        if self.bank.count != 0:
           rep += "\nБанк:\t" + str(self.bank) + "$"
        return rep
    @property
    def total(self):
        for card in self.cards:
            if not card.value:
                return None
        t = 0
        for card in self.cards:
            t += card.value
        contains_ace = False
        for card in self.cards:
            if card.value == BJ_Card.ACE_VALUE:
                contains_ace = True
        if contains_ace and t <= 11:
            t += 10
        return t

    def is_busted(self):
        return self.total > 21



class BJ_Player(BJ_Hand):

    def is_hitting(self):
        response = games.ask_yes_no("\n" + self.name + ", берете ще карту? (Y/N): ")
        return response == "y"

    def bust(self):
        print(self.name, "перебрав.")
        self.lose()

    def lose(self):
        print(self.name, "програв.")

    def win(self):
        print(self.name, "виграв.")

    def push(self):
        print(self.name, "зіграв нічию з компютером.")

    def new_bet(self, contragent, bet):
        self.bank.cash_out(bet, contragent)
        print("Прийнято ставку гравця ", self.name, ": ", bet, "$")




class BJ_Dealer(BJ_Hand):

    def is_hitting(self):
        return self.total < 17

    def bust(self):
        print(self.name, "перебрав.")

    def flip_first_card(self):
        first_card = self.cards[0]
        first_card.flip()




class BJ_Bank(object):
    def __init__(self, count = 0):
        self.count = count
    def __str__(self):
        rep = str(self.count)
        return rep

    def cash_in(self, null):
        self.count += null

    def cash_out(self, null, contr_bank):
        if self.count >= null:
            self.count -= null
            contr_bank.cash_in(null)
        else:
            print ("Не достатньо коштів!")
        


class BJ_Game(object):
    def __init__(self, names):
        self.players = []
        for name in names:
            player = BJ_Player(name, 100)
            self.players.append(player)
        self.bank = BJ_Bank(1000)
        self.dealer = BJ_Dealer("Dealer")
        self.deck = BJ_Deck()
        self.deck.populate()
        self.deck.shuffle()
    @property
    def still_playing(self):
        sp = []
        for player in self.players:
            if not player.is_busted():
                sp.append(player)
        return sp

    def __additional_cards(self, player):
        while not player.is_busted() and player.is_hitting():
            self.deck.deal([player])
            print(player)
            if player.is_busted():
                player.bust()

    def reward(self, player, bet, result):
        r = 0
        if result == "win":
            r = bet * 2
        elif result == "push":
            r = bet
        if r != 0:
            self.bank.cash_out(r, player.bank)
            print ("Виграш ", player.name,  "складає: ", r, "$")
    
    def play(self):
        con = {}
        bet = 10
        for player in self.players:
            player.new_bet(self.bank, bet)
            con[player.name] = [bet]
        self.deck.deal(self.players + [self.dealer], per_hand = 2)
        self.dealer.flip_first_card()
        for player in self.players:
            print(player)
        print(self.dealer)
        print("Банк казино: ", self.bank, "$")
        for player in self.players:
            self.__additional_cards(player)
        self.dealer.flip_first_card()
        if not self.still_playing:
            print(self.dealer)
        else:
            print(self.dealer)
            self.__additional_cards(self.dealer)
            if self.dealer.is_busted():
                for player in self.still_playing:
                    player.win()
                    con[player.name].append("win")
            else:
                for player in self.still_playing:
                    if player.total > self.dealer.total:
                        player.win()
                        con[player.name].append("win")
                    elif player.total < self.dealer.total:
                        player.lose()
                        con[player.name].append("lose")
                    else:
                        player.push()
                        con[player.name].append("push")
        for player in self.players:
            self.reward(player, con[player.name][0], con[player.name][1])
            player.clear()
            if player.bank.count < bet:
                self.players.remove(player)
        self.dealer.clear()
        self.deck.full_up()



def main():
    print:("\t\tВітаємо за ігровим столом Блек-джека!\n")
    names = []
    number = games.ask_number("Кількість учасників? (1-7): ", low = 1, high = 8)
    for i in range(number):
        name = input("Введіть ім'я гравця: ")
        names.append(name)
    game = BJ_Game(names)
    again = None
    while again != "n":
        game.play()
        again = games.ask_yes_no("\nХочете ще зіграти?")


main()
input("\n\nНатисніть 'Enter' для виходу.")
