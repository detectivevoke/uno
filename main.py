import random
import time
import string
import os
from colorama import Fore
#{'0': {'cards': [], 'past_cards': []}, '1': {'cards': [], 'past_cards': []}, '2': {'cards': [], 'past_cards': []}, 'colour_codes': ['B', 'G', 'R', 'Y'], 'colours': {'B': 'Blue', 'G': 'Green', 'R': 'Red', 'Y': 'Yellow'}, 'cards': ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'wild_card', 'skip_turn', '+2_card', '+4_card', 'reverse_card']}

from colorama import init
init()

debug = False

class UNO:

    def __init__(self, players,card_amount=None):
        self.game = {}
        self.deck = []
        self.reverse = False
        self.player_amount = players
        self.current_player = 0
        self.card_amount = 7 if card_amount == None else card_amount
        for player in range(players):
            self.game[str(player)] = {
            "cards": [],
            "past_cards": [],
            "cards_used": 0,
            }
        self.game["colour_codes"] = ["B","G","R","Y"]
        self.game["colours"] = {"B": 34, "G": 32, "R": 31, "Y": 33}
        self.game["cards"] = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "skip_turn","+2_card", "reverse_card"]
        self.game["special_cards"] = []

        self.game["current_game"] = {
            "cards_used": 0,
            "used": []
        }

        self.colour_current = random.choice(self.game["colour_codes"])

        for i in range(4):
            self.game["special_cards"].append("wild_card_{}".format(i))
            self.game["special_cards"].append("+4_card_{}".format(i))

        for i in range(2):
            for colour in self.game["colour_codes"]:
                for card in self.game["cards"]:
                    self.deck.append(str(colour)+str(card))
        for card in self.game["special_cards"]:
            self.deck.append(card)
        

    def title(self):
        os.system("title Colour: {} - Player: {} - Cards used: {}".format(self.colour_current, self.current_player,self.game["current_game"]["cards_used"]))

    def count_update(self,player):
        self.game[str(player)]["cards_used"] += 1
        self.game["current_game"]["cards_used"] += 1
        return True

    def current_person_update(self):

        if self.reverse:
            self.current_player -= 1
            #-1
            if self.current_player < 0:
                if self.current_player == -1:
                    self.current_player += self.player_amount
                    return True
                n = self.player_amount
                self.current_player += n-1
                pass
            else:
                pass
            return True
        else:
            self.current_player +=1
            if self.current_player >= self.player_amount:
                n = self.player_amount
                self.current_player -= n
                pass
            else:
                pass
            return True
            

    def give_cards(self):
        self.title()
        for player in range(self.player_amount):
            for i in range(self.card_amount):
                card_to_be_given = random.choice(self.deck)
                self.game[str(player)]["cards"].append(str(card_to_be_given))
                self.deck.remove(card_to_be_given)


    def give_certain_person_cards(self, player,amount):
        try:
            if len(self.deck) > 0:
                for i in range(amount):
                    card_to_be_given = random.choice(self.deck)
                    print("{} has been given a card!".format(self.current_player))
                    self.game[str(player)]["cards"].append(str(card_to_be_given))
                    self.deck.remove(card_to_be_given)
                return True
            else:
                print("No cards left in the deck, using all used cards!")
                cards = self.game["current_game"]["used"]
                for card in cards:
                    self.deck.append(card)
                self.game["current_game"]["used"].clear()
                self.give_certain_person_cards(player,amount)
        except:
            return False




    def use_card(self,player, card):
        deck = self.game[str(player)]["cards"]
        if card in deck:
            
            if "wild_card" in card:
                new_colour = input("What colour would you like to change the game to: ")
                self.colour_current = new_colour

                self.game[str(player)]["cards"].remove(card)
                self.game[str(player)]["past_cards"].append(card)

                self.count_update(player)

                self.game["current_game"]["used"].append(card)
                self.current_person_update()
                self.title()
                
                return True

            elif "+2_card" in card:
                colour = card[:1]
                if colour == self.colour_current:
                    if self.reverse:
                        player_affected = int(player)-1
                        if player_affected < 0:
                            player_affected = player_affected + (self.player_amount)
                    else:
                        #2
                        player_affected = int(player)+1
                        #3
                        if player_affected >= self.player_amount:
                            player_affected = player_affected-self.player_amount
                    # if 3 > 2:
                    # p = 3 - 3
                    if player_affected > (self.player_amount)-1:
                        player_affected = player_affected-self.player_amount
                    self.game[str(player)]["cards"].remove(card)
                    self.game[str(player)]["past_cards"].append(card)

                    self.count_update(player)

                    print("+2 has been given to {} by {}".format(player_affected, self.current_player))
                    if debug:
                        print(self.game[str(player_affected)]["cards"])
                    self.give_certain_person_cards(player_affected, 2)
                    if debug:
                        print(self.game[str(player_affected)]["cards"])
                    self.game["current_game"]["used"].append(card)
                    self.current_person_update()
                    self.title()
                    return True
                else:
                    print("You have to use a {} card!".format(self.colour_current))
                    return False
            
            elif "+4_card" in card:
                if self.reverse:
                    player_affected = int(player)-1
                    if player_affected < 0:
                        player_affected = player_affected + (self.player_amount)
                else:
                    #2
                    player_affected = int(player)+1
                    #3
                    if player_affected >= self.player_amount:
                        player_affected = player_affected-self.player_amount
                print("+4 has been given to {} by {}".format(player_affected, self.current_player))

                self.game[str(player)]["cards"].remove(card)
                self.game[str(player)]["past_cards"].append(card)

                self.count_update(player)
                self.give_certain_person_cards(player_affected, 4)

                self.game["current_game"]["used"].append(card)
                self.title()
                self.current_person_update()
                return True

            elif "reverse_card" in card:
                print("Reverse card has been used by {}!".format(self.current_player))
                self.game[str(player)]["cards"].remove(card)
                self.game[str(player)]["past_cards"].append(card)

                self.count_update(player)

                self.game["current_game"]["used"].append(card)
                if self.reverse:
                    self.reverse = False
                else:
                    self.reverse = True

                self.current_person_update()
                self.title()
                return True

            elif "skip_turn" in card:
                x = self.current_player
                
                self.game[str(player)]["cards"].remove(card)
                self.game[str(player)]["past_cards"].append(card)
                self.game["current_game"]["used"].append(card)
                self.count_update(player)
                if self.reverse:
                    self.current_player -= 2
                    if self.current_player < 0:
                        self.current_player += (self.player_amount)
                        pass
                    else:
                        pass
                else:
                    self.current_player+=2
                    if self.current_player > (self.player_amount)-1:
                        self.current_player -= (self.player_amount)
                print("Skip card has been used by {}!".format(x))
                self.title()
                return True

            
            elif card[:1] == self.colour_current:
                print("A card has been used by {}!".format(self.current_player))
                self.game[str(player)]["cards"].remove(card)
                self.game[str(player)]["past_cards"].append(card)

                self.count_update(player)

                self.game["current_game"]["used"].append(card)

                self.current_person_update()
                self.title()
                
                return True
            
            elif card[:1] != self.colour_current:
                print("That card is not the same colour as the current colour!")
                return False
            else:
                print("You have to use a card that is in your deck!")
                return False
        else:
            print("That card is not in your deck!")

    


    def run(self):
        self.my_player = random.randint(0,self.player_amount-1)
        print("You are player {}!".format(self.my_player))
        print("\n")
        self.give_cards()
        while True:
            time.sleep(0.4)
            if len(self.game[str(self.current_player)]["cards"]) == 0:
                print("{} HAS WON!".format(self.current_player))
            if self.current_player == self.my_player:
                print("It is your turn, the last card used was {}".format(self.game["current_game"]["used"][-1:][0]))
                time.sleep(0.5)
                for card in self.game[str(self.current_player)]["cards"]:
                    pos_of_card = self.game[str(self.current_player)]["cards"].index(card)
                    if card in self.game["special_cards"]:
                        if "wild_card" in card:
                            card = "Wild Card"
                        elif "+4" in card:
                            card = "+4 Card"
                        print(Fore.MAGENTA + "({}) - {}".format(pos_of_card,card) + Fore.RESET)
                    try:
                        colour_of_card = self.game["colours"][card[:1]]
                        if "_" in card:
                            card = card.replace("_"," ")
                        card = card.strip(card[:1])
                        if "reverse" in card:
                            card = "Reverse Card"
                        elif "+2" in card:
                            card = "+2 Card"
                        elif "skip" in card:
                            card = "Skip Turn"
                        if colour_of_card == 32:
                            print(Fore.GREEN + "({}) - {}".format(pos_of_card,card) + Fore.RESET)
                        elif colour_of_card == 33:
                            print(Fore.YELLOW + "({}) - {}".format(pos_of_card,card) + Fore.RESET)
                        elif colour_of_card == 34:
                            print(Fore.BLUE + "({}) - {}".format(pos_of_card,card) + Fore.RESET)
                        elif colour_of_card == 31:
                            print(Fore.RED + "({}) - {}".format(pos_of_card,card) + Fore.RESET)
                    except:
                        pass
                c = input("Enter a number to use (click enter to get a new card): ")
                if c:
                    try:
                        card = self.game[str(self.current_player)]["cards"][int(c)]
                        self.use_card(str(self.current_player),card)
                    except:
                        self.give_certain_person_cards(str(self.current_player),1)
                else:
                    self.give_certain_person_cards(str(self.current_player),1)
            else:
                random.shuffle(self.game[str(self.current_player)]["cards"])
                if self.colour_current not in self.game[str(self.current_player)]["cards"]:
                    self.give_certain_person_cards(str(self.current_player),1)
                for card in self.game[str(self.current_player)]["cards"]:
                    if card[:1] == self.colour_current:
                        self.use_card(str(self.current_player),card)
                        break
                    else:
                        pass
                
    def bot_run(self):
        self.my_player = random.randint(0,self.player_amount-1)
        print("You are player {}!".format(self.my_player))
        print("\n")
        self.give_cards()
        while True:
            time.sleep(0.4)
            if len(self.game[str(self.current_player)]["cards"]) == 0:
                print("{} HAS WON!".format(self.current_player))
            else:
                print(len(self.game[str(self.current_player)]["cards"]))
            if len(self.game[str(self.current_player)]["cards"]) == 0:
                print("{} HAS WON!".format(self.current_player))
            time.sleep(0.5)
            random.shuffle(self.game[str(self.current_player)]["cards"])
            if self.colour_current not in self.game[str(self.current_player)]["cards"]:
                self.give_certain_person_cards(str(self.current_player),1)
            for card in self.game[str(self.current_player)]["cards"]:
                if card[:1] == self.colour_current:
                    self.use_card(str(self.current_player),card)
                    break
                else:
                    pass

    
num_of_players = 5
UNO(num_of_players).run()