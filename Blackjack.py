import random
import colorama
from colorama import Fore


suits = ["❤", "♦", "♠", "♣"]
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
values = {"Two" : 2, "Three" : 3, "Four" : 4, "Five" : 5, "Six" : 6, "Seven" : 7, "Eight" : 8, "Nine" : 9, "Ten" : 10,
          "Jack" : 10, "Queen" : 10, "King" : 10, "Ace" : 11}
winner = ""


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    # String Presentation of each card
    def __str__(self):
        return f'Card : {self.rank} {self.suit}'



class Deck:
    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks :
                self.all_cards.append(Card(suit, rank))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.all_cards)

    def getCard(self):
        if len(self.all_cards) != 0:
            return self.all_cards.pop()
        else :
            print("Deck is empty")


    def __len__(self):
        return len(self.all_cards)

    def __str__(self):
        return f"Deck with {self.__len__()} Cards"




class HPlayer:

    def __init__(self, name, bankroll, _deck):
        self.name = name
        self.bankroll = bankroll
        self.deck = _deck
        self.open_cards = []
        self.bet = 0
        self.initialize()


    def initialize(self):
        print("Initializing Player Cards..")
        f_card = self.deck.all_cards.pop()
        s_card = self.deck.all_cards.pop()
        self.open_cards.append(f_card)
        self.open_cards.append(s_card)


    def enoughCoins(self, amt):
        if self.bankroll >= amt :
            self.bet = amt
            return True
        else :
            return False

    def hit(self):
        if len(self.deck) > 0 :
            new_card = self.deck.all_cards.pop()
            # The Value of Ace can be or 11 depending on Player Choice
            if new_card.rank == "Ace":
                ace_value = input("It is an Ace, do you want 1 or 11 as value ? ")
                if ace_value.isdigit() and int(ace_value) == 1 or int(ace_value) == 11:
                    ace_value = int(ace_value)
                    values["Ace"] = ace_value
                else :
                    print("Default value was token (1)")
                    values["Ace"] = 1
            self.open_cards.append(new_card)
        else:
            print("Deck is Empty")

    def getSum(self):
        result = 0
        for card in self.open_cards:
            result += values[card.rank]
        return result

    def checkBust(self):
        return self.getSum() > 21


    def play(self):
        print("Your Turn ")
        print(f"current value : {self.getSum()}")
        while not self.checkBust():
            player_choice = input("Do you want to hit or stand ?")
            if player_choice == "hit" :
                self.hit()
                print("Your Table :")
                for card in self.open_cards:
                    print(card)
                print(f"current value : {self.getSum()}")
            else :
                break
        if self.checkBust():
            global winner
            winner = "Dealer"
        elif self.getSum() == 21 :
            winner = "Player"



class CDealer:
    def __init__(self, _deck):
        self.deck = _deck
        self.cards = [] # contains all cards in the Dealer's hand
        self.open_cards = []
        self.initialize()

    def initialize(self):
        f_card = self.deck.all_cards.pop()
        s_card = self.deck.all_cards.pop()
        self.open_cards.append(f_card)
        self.cards.append(f_card)
        self.cards.append(s_card)


    def hit(self):
        if len(self.deck.all_cards) > 0 :
            new_card = self.deck.all_cards.pop()
            self.open_cards.append(new_card)
            self.cards.append(new_card)
        else:
            print("Deck is Empty")

    def getSum(self):
        result = 0
        for card in self.cards:
            result += values[card.rank]
        return result



    def checkBust(self):
        return self.getSum() > 21 # Player wins twice his bet

    def check17(self):
        return self.getSum() >= 17 # Player have to stay with his hands




    def play(self):
        print("Dealer's Turn ")
        print(f"current value : {self.getSum()}")
        while self.getSum() < 17 :
            print("Dealer's Table :")
            for card in self.cards :
                print(card)
            self.hit()
            print(f"current value : {self.getSum()}")
        print("Dealer's Table :")
        for card in self.cards:
            print(card)
        if self.checkBust():
            print(Fore.GREEN + "Dealer busted. You Won !")
            global winner
            winner = "Player"




class Game:
    def __init__(self, player, dealer):
        retry = True
        while retry :
            self.player = player
            self.dealer = dealer
            player_choice = input(f"{self.player.name}, How much do you want to bet ?")
            if player.enoughCoins(int(player_choice)): # Make sure player has enough coins
                player.play()
                if winner == "" : # winner still unknown
                    dealer.play()
                    if winner == "": # Player and dealer didn't busted
                        if 21 - player.getSum() < 21 - dealer.getSum():
                            print(Fore.GREEN + "You are closer to 21. You Won the game.")
                            player.bankroll += 2 * player.bet
                            print(f"Your Bankroll : {player.bankroll}")
                        elif 21 - player.getSum() > 21 - dealer.getSum():
                            print(Fore.RED + "Dealer is closer to 21. You lost !")
                            player.bankroll -= player.bet
                            print(f"Your Bankroll : {player.bankroll}")
                        else:
                            print(Fore.MAGENTA + "Tide")
                else :
                    if winner == "Player":
                        print(Fore.GREEN + "Dealer busted. You Won !")
                        player.bankroll += 2 * player.bet
                    elif winner == "Dealer":
                        print(Fore.RED + "You busted.You lost !")
                        player.bankroll -= player.bet
            else :
                print(f"Not enough money to bet. Current Bankroll : {player.bankroll}")

            retry_choice = input(Fore.WHITE + "Play again ? y or n : ")
            if retry_choice == "n":
                retry = False
            else :
                new_deck = Deck()
                new_p = HPlayer(player.name, player.bankroll, new_deck)
                new_d = CDealer(new_deck)
                Game(new_p, new_d)



deck = Deck()
p = HPlayer("Mohamad", 150, deck)

d = CDealer(deck)

Game(p, d)




