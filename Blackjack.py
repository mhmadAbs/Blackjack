import random
import sys

from colorama import Fore, Style

suits = ["❤", "♦", "♠", "♣"]
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
values = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10,
          "Jack": 10, "Queen": 10, "King": 10, "Ace": 11}
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
            for rank in ranks:
                self.all_cards.append(Card(suit, rank))
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.all_cards)

    def getCard(self):
        if len(self.all_cards) != 0:
            return self.all_cards.pop()
        else:
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
        print(Fore.YELLOW + f"Bankroll : {self.bankroll}" + Style.RESET_ALL)


    '''
        Gives the Dealer the start-cards
    '''

    def initialize(self):
        print("Initializing Player Cards..")
        f_card = self.deck.all_cards.pop()
        s_card = self.deck.all_cards.pop()
        self.open_cards.append(f_card)
        self.open_cards.append(s_card)


    '''
        checks if Player has enough Coins to bet
    '''

    def enoughCoins(self, amt):
        if self.bankroll >= amt:
            self.bet = amt
            return True
        else:
            return False

    '''
    Takes a card and checks if it is a ACE card. 
    if so, the Value of Ace can be or 11 depending on Player Choice.
    '''
    @staticmethod
    def deal_with_ace(new_card):
        if new_card.rank == "Ace":
            ace_value = input("It is an Ace, do you want 1 or 11 as value ? ")
            if ace_value.isdigit() and int(ace_value) == 1 or int(ace_value) == 11:
                ace_value = int(ace_value)
                values["Ace"] = ace_value
            else:
                print("Default value was token (1)")
                values["Ace"] = 1

    '''
        Takes a card from the Deck and give it to the Player(in case the Deck is not empty)
    '''
    def hit(self):
        if len(self.deck) > 0:
            new_card = self.deck.all_cards.pop()
            # The Value of Ace can be or 11 depending on Player Choice
            self.deal_with_ace(new_card)
            self.open_cards.append(new_card)
        else:
            print("Deck is Empty")

    '''
        returns the sum of the values of all cards in Player hand
        
    '''

    def getSum(self):
        result = 0
        for card in self.open_cards:
            result += values[card.rank]
        return result

    def checkBust(self):
        return self.getSum() > 21

    '''
        Controls the play of the Player.
        The Player get to choose between hitting(take new Card) and staying(stop taking cards)
        
        IF the player entered another a non valid Option he/she will be asked again to provide a new one.
    '''

    def play(self):
        print("Your Turn ")
        print("Your Table :")
        for card in self.open_cards:
            print(card)
        print(Fore.BLUE + Style.BRIGHT + f"Your Sum : {self.getSum()}" + Style.RESET_ALL)
        not_valid_opt = True
        while not_valid_opt or not self.checkBust():
            player_choice = input("Do you want to hit or stand ? h or s : ")
            if player_choice == "hit" or player_choice == "h":
                not_valid_opt = False
                self.hit()
                print("Your Table :")
                for card in self.open_cards:
                    print(card)
                print(Fore.BLUE + Style.BRIGHT + f"Your Sum : {self.getSum()}" + Style.RESET_ALL)
            elif player_choice == "stand" or player_choice == "s":
                not_valid_opt = False
                break
            else:
                print("Non-valid Option was given ! Exiting the game..")

        if self.checkBust():  # player busted
            global winner
            winner = "Dealer"


class CDealer:
    def __init__(self, _deck):
        self.deck = _deck
        self.cards = []  # contains all cards in the Dealer's hand
        self.open_cards = []
        self.initialize()

    '''
        Gives the Dealer the start-cards
    '''

    def initialize(self):
        f_card = self.deck.all_cards.pop()
        s_card = self.deck.all_cards.pop()
        self.open_cards.append(f_card)
        self.cards.append(f_card)
        self.cards.append(s_card)


    '''
        Takes a new Card from the Deck and give it to the Dealer's .
    '''
    def hit(self):
        if len(self.deck.all_cards) > 0:
            new_card = self.deck.all_cards.pop()
            self.open_cards.append(new_card)
            self.cards.append(new_card)
        else:
            print("Deck is Empty")

    '''
    Returns the sum of the Values of all cards
    '''
    def getSum(self):
        result = 0
        for card in self.cards:
            result += values[card.rank]
        return result

    def checkBust(self):
        return self.getSum() > 21  # Player wins twice his bet

    def check17(self):
        return self.getSum() >= 17

    '''
    Shows one of the two start-cards of the Dealer and hide the second one
    '''
    def showCards(self):
        print("Dealer's Table : ")
        print(self.cards[0])
        print("Card : Hidden")



    '''
    Controls the play of the Dealer
    Note : As long as the sum of Dealer's hand is smaller than 17, Dealer hits
    '''

    def play(self):
        print("Dealer's Turn ")
        while self.getSum() < 17:
            print("Dealer's Table :")
            for card in self.cards:
                print(card)
            print(Fore.CYAN + Style.BRIGHT + f"Dealer's Sum : {self.getSum()}" + Style.RESET_ALL)
            self.hit()
        print("Dealer's Table :")
        for card in self.cards:
            print(card)
        print(Fore.CYAN + Style.BRIGHT + f"Dealer's Sum : {self.getSum()}" + Style.RESET_ALL)
        if self.checkBust():
            print(Fore.GREEN + "Dealer busted. You Won !" + Style.RESET_ALL)
            global winner
            winner = "Player"


class Game:
    def __init__(self, player, dealer):
        want_retry = True
        while want_retry:
            self.player = player
            self.dealer = dealer
            player_choice = input(f"{self.player.name}, How many coins do you want to bet ? ")
            not_enough_coins = True
            while not_enough_coins:
                if player.enoughCoins(int(player_choice)):  # Make sure player has enough coins
                    not_enough_coins = False
                    dealer.showCards()
                    player.play()
                    if winner == "":  # winner still unknown
                        dealer.play()
                        if winner == "":  # Player and dealer didn't busted
                            if 21 - player.getSum() < 21 - dealer.getSum():
                                print(Fore.GREEN + "You are closer to 21. You Won the game." + Style.RESET_ALL)
                                player.bankroll += 2 * player.bet
                                print(f"Your Bankroll : {player.bankroll}")
                            elif 21 - player.getSum() > 21 - dealer.getSum():
                                print(Fore.RED + "Dealer is closer to 21. You lost !" + Style.RESET_ALL)
                                player.bankroll -= player.bet
                                print(f"Your Bankroll : {player.bankroll}")
                            else:
                                print(Fore.MAGENTA + "Tide" + Style.RESET_ALL)
                    else:
                        if winner == "Player":
                            print(Fore.GREEN + "Dealer busted. You Won !" + Style.RESET_ALL)
                            player.bankroll += 2 * player.bet
                            print(f"Your Bankroll : {player.bankroll}")
                        elif winner == "Dealer":
                            print(Fore.RED + "You busted.You lost !" + Style.RESET_ALL)
                            player.bankroll -= player.bet
                            print(f"Your Bankroll : {player.bankroll}")
                else:
                    print(f"Not enough money to bet. Current Bankroll : {player.bankroll}")

            retry_choice = input(Fore.WHITE + "Play again ? y or n : " + Style.RESET_ALL)
            if retry_choice == "n":
                sys.exit()
            else:
                new_deck = Deck()
                new_p = HPlayer(player.name, player.bankroll, new_deck)
                new_d = CDealer(new_deck)
                Game(new_p, new_d)


deck = Deck()
p = HPlayer("Mohamad", 150, deck)

d = CDealer(deck)

Game(p, d)
