import random
import time
import string
import os
from colorama import Fore
import json
#{'0': {'cards': [], 'past_cards': []}, '1': {'cards': [], 'past_cards': []}, '2': {'cards': [], 'past_cards': []}, 'colour_codes': ['B', 'G', 'R', 'Y'], 'colours': {'B': 'Blue', 'G': 'Green', 'R': 'Red', 'Y': 'Yellow'}, 'cards': ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'wild_card', 'skip_turn', '+2_card', '+4_card', 'reverse_card']}

from colorama import init
init()

debug = False

class UNO:

    def __init__(self, card_amount=None):
        self.config = json.loads(open("config.json","r").read())
        self.sleep_time = self.config["sleep_time"]
        self.log = self.config["log"]
        self.game = {}
        self.deck = []
        self.reverse = False
        self.player_amount = self.config["players"]
        self.current_player = 0
        self.card_amount = 7 if card_amount == None else card_amount
        for player in range(self.player_amount):
            self.game[str(player)] = {
            "cards": [],
            "past_cards": [],
            "cards_used": 0,
            }
        self.game["colour_codes"] = ["B","G","R","Y"]
        self.game["colours"] = {"B": 34, "G": 32, "R": 31, "Y": 33}
        self.game["colours_full"] = {"B":"Blue","G":"Green","R":"Red","Y":"Yellow"}
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
        
        self.title()
        for player in range(self.player_amount):
            for i in range(self.card_amount):
                card_to_be_given = random.choice(self.deck)
                self.game[str(player)]["cards"].append(str(card_to_be_given))
                self.deck.remove(card_to_be_given)

    def time_sleep(self):
        x = int(random.randrange((self.sleep_time-0.5)*100,(self.sleep_time+0.5)*100))/100
        return x

    def save_game(self):
        f = open('win.json',"r")
        data = json.load(f)
        data["card_amount_on_win"].append(self.game["current_game"]["cards_used"])
        json_object = json.dumps(data, indent=4)

        with open("win.json", "w") as outfile:
            outfile.write(json_object)

    def title(self):
        colour_full = self.game["colours_full"][self.colour_current]
        try:
            c = self.game["current_game"]["used"][-1:][0]
        except Exception as e:
            print(e)
            os.system("title Colour: {} - Player: {} - Cards used: {} - Last Card: {}".format(colour_full, self.current_player,self.game["current_game"]["cards_used"], "None"))
            return
        name, pos, colour = self.card_format(c)
        colour = colour.lower().capitalize()
        if colour == "Black":
            os.system("title Colour: {} - Player: {} - Cards used: {} - Last Card: {}".format(colour_full, self.current_player,self.game["current_game"]["cards_used"], name))
        else:
            os.system("title Colour: {} - Player: {} - Cards used: {} - Last Card: {}".format(colour_full, self.current_player,self.game["current_game"]["cards_used"], "{} {}".format(colour,name)))
    

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


    def give_admin_card(self, player, card):
        self.game[str(player)]["cards"].append(str(card))
        return True

    def give_certain_person_cards(self, player,amount):
        try:
            if len(self.deck) > 0:
                for i in range(amount):
                    card_to_be_given = random.choice(self.deck)
                    if self.log:
                        print("Player {} has been given a card!".format(self.current_player))
                    self.game[str(player)]["cards"].append(str(card_to_be_given))
                    self.deck.remove(card_to_be_given)
                return True
            else:
                if self.log:
                    print("No cards left in the deck, using all used cards!")
                cards = self.game["current_game"]["used"]
                for card in cards:
                    self.deck.append(card)
                self.game["current_game"]["used"].clear()
                self.give_certain_person_cards(player,amount)
        except:
            return False

    def use_card(self,player, card, bot=True):
        deck = self.game[str(player)]["cards"]
        if card in deck:
            if "wild_card" in card:
                self.wild_card(card,bot)
            elif "+2_card" in card:
                self.plus2_card(card)
            elif "+4_card" in card:
                self.plus4_card(card)
            elif "reverse_card" in card:
                self.reverse_card(card)
            elif "skip_turn" in card:
                self.skip_turn(card)
            elif card[:1] == self.colour_current:
                self.normal_card(card)
            elif card[:1] != self.colour_current:
                
                print("That card is not the same colour as the current colour!")
                return False
            else:
                print("You have to use a card that is in your deck!")
                return False
        else:
            print("That card is not in your deck!")

    def wild_card(self,card,bot):
        if bot:
            x = True
            while x:
                new_colour = random.choice(self.game["colour_codes"])
                if new_colour != self.colour_current:
                    x = False
                else:
                    pass
        else:
            x = True
            while x:
                new_colour = input("What colour would you like to change the game to (R,G,B,Y): ")
                if new_colour != self.colour_current:
                    x = False
                else:
                    print("Please select a colour, that isnt the current colour!")

        self.colour_current = new_colour
        if self.log:
            print("Player {} has changed the colour to {}".format(self.current_player,new_colour))
        self.game[str(self.current_player)]["cards"].remove(card)
        self.game[str(self.current_player)]["past_cards"].append(card)
        self.count_update(self.current_player)
        self.game["current_game"]["used"].append(card)
        self.current_person_update()
        self.title()

    def plus2_card(self,card):
        colour = card[:1]
        if colour == self.colour_current:
            if self.reverse:
                player_affected = int(self.current_player)-1
                if player_affected < 0:
                    player_affected = player_affected + (self.player_amount)
            else:
                player_affected = int(self.current_player)+1
                if player_affected >= self.player_amount:
                    player_affected = player_affected-self.player_amount
            if player_affected > (self.player_amount)-1:
                player_affected = player_affected-self.player_amount
            self.game[str(self.current_player)]["cards"].remove(card)
            self.game[str(self.current_player)]["past_cards"].append(card)

            self.count_update(self.current_player)
            if self.log:
                print("+2 has been given to Player {} by {}".format(player_affected, self.current_player))
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

    def plus4_card(self,card):
        if self.reverse:
            player_affected = int(self.current_player)-1
            if player_affected < 0:
                player_affected = player_affected + (self.player_amount)
        else:
            player_affected = int(self.current_player)+1
            if player_affected >= self.player_amount:
                player_affected = player_affected-self.player_amount
        if self.log:
            print("+4 has been given to Player  {} by {}".format(player_affected, self.current_player))
        self.game[str(self.current_player)]["cards"].remove(card)
        self.game[str(self.current_player)]["past_cards"].append(card)
        self.count_update(self.current_player)
        self.give_certain_person_cards(player_affected, 4)
        self.game["current_game"]["used"].append(card)
        self.title()
        self.current_person_update()
        return True

    def reverse_card(self, card):
        if self.log:
            print("Reverse card has been used by {}!".format(self.current_player))
        self.game[str(self.current_player)]["cards"].remove(card)
        self.game[str(self.current_player)]["past_cards"].append(card)
        self.count_update(self.current_player)
        self.game["current_game"]["used"].append(card)
        if self.reverse:
            self.reverse = False
        else:
            self.reverse = True

        self.current_person_update()
        self.title()
        return True

    def skip_turn(self,card):
        x = self.current_player
        self.game[str(self.current_player)]["cards"].remove(card)
        self.game[str(self.current_player)]["past_cards"].append(card)
        self.game["current_game"]["used"].append(card)
        self.count_update(self.current_player)
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
        if self.log:
            print("Skip card has been used by {}!".format(x))
        self.title()
        return True

            
    def normal_card(self,card):
        ## add what card has been used, formatted
        if self.log:
            print("A card has been used by {}!".format(self.current_player))
        self.game[str(self.current_player)]["cards"].remove(card)
        self.game[str(self.current_player)]["past_cards"].append(card)
        self.count_update(self.current_player)
        self.game["current_game"]["used"].append(card)
        self.current_person_update()
        self.title()
        
        return True

    def bot_check(self):
        while True:
            time.sleep(self.time_sleep())
            random.shuffle(self.game[str(self.current_player)]["cards"])
            for card in self.game[str(self.current_player)]["cards"]:
                if self.colour_current in card or "wild" in card or "+4" in card:
                    return card
                else:
                    pass
            self.give_certain_person_cards(str(self.current_player),1)
            self.current_person_update()
            pass
            
    def card_format(self,card):

        ## R7
        try:
            colour_of_card = self.game["colours"][card[:1]]
        except:
            colour_of_card = "BLACK"
        try:
            pos_of_card = self.game[str(self.current_player)]["cards"].index(card)
        except:
            pos_of_card = "0"
        if "_" in card:
            card = card.replace("_"," ")
        card = card.strip(card[:1])
        if colour_of_card == 32:
            colour_of_card = "GREEN"
        elif colour_of_card == 33:
            colour_of_card = "YELLOW"
        elif colour_of_card == 34:
            colour_of_card = "BLUE"
        elif colour_of_card == 31:
            colour_of_card = "RED"
        if "reverse" in card:
            return "Reverse Card", pos_of_card, colour_of_card
        elif "+2" in card:
            return "+2 Card", pos_of_card, colour_of_card
        elif "skip" in card:
            return "Skip Turn", pos_of_card, colour_of_card
        elif "4 card" in card:
            return "+4 Card", pos_of_card, colour_of_card
        elif "ild card" in card:
            return "Wild Card", pos_of_card, colour_of_card 
        return card, pos_of_card, colour_of_card
    
    def run(self):
        self.my_player = random.randint(0,self.player_amount-1)
        print("You are Player {}!".format(self.my_player))
        print("\n")
        while True:
            time.sleep(self.time_sleep())
            if len(self.game[str(self.current_player)]["cards"]) == 1:
                print("{} is on UNO!".format(self.current_player))
            if len(self.game[str(self.current_player)]["cards"]) == 0:
                print("{} has won!".format(self.current_player))
                self.save_game()
                break
            if self.current_player == self.my_player:
                time.sleep(self.time_sleep())
                for card in self.game[str(self.current_player)]["cards"]:
                    c,pos,colour = self.card_format(card)
                    if colour == "GREEN":
                        print(Fore.GREEN + "({}) - {}".format(pos+1,c) + Fore.RESET)
                    elif colour == "YELLOW":
                        print(Fore.YELLOW + "({}) - {}".format(pos+1,c) + Fore.RESET)
                    elif colour == "BLUE":
                        print(Fore.BLUE + "({}) - {}".format(pos+1,c) + Fore.RESET)
                    elif colour == "RED":
                        print(Fore.RED + "({}) - {}".format(pos+1,c) + Fore.RESET)
                    elif colour== "BLACK":
                        print(Fore.MAGENTA + "({}) - {}".format(pos+1,c) + Fore.RESET)
                c = input("Enter a number to use (click enter to get a new card): ")
                if c:
                    if "give(" in c:
                        give_card = c.strip("give(").strip(")")
                        self.give_admin_card(self.current_player,give_card)
                    else:
                        c = int(c)-1
                        try:
                            card = self.game[str(self.current_player)]["cards"][c]
                            self.use_card(str(self.current_player),card, bot=False)
                        except:
                            self.give_certain_person_cards(str(self.current_player),1)
                            self.current_person_update()
                else:
                    self.give_certain_person_cards(str(self.current_player),1)
                    self.current_person_update()
                    pass
            else:
                card = self.bot_check()
                self.use_card(str(self.current_player),card)
                
    def bot_run(self):
        self.my_player = random.randint(0,self.player_amount-1)
        while True:
            if len(self.game[str(self.current_player)]["cards"]) == 0:
                print("{} HAS WON!".format(self.current_player))
                self.save_game()
                return True
            card = self.bot_check()
            self.use_card(str(self.current_player),card,bot=True)


if json.loads(open("config.json","r").read())["bot_game"]:
    UNO().bot_run()
else:
    UNO().run()