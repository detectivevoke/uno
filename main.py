import random
import time
import string
import os
from colorama import Fore
import json

from colorama import init
init()

debug = False

class UNO:

    def __init__(self, card_amount=None):
        ##Loading config, setting variables
        self.config = json.loads(open("config.json","r").read())
        self.sleep = self.config["sleep"]
        self.sleep_time = self.config["sleep_time"]
        self.log = self.config["log"]
        self.game = {}
        self.deck = []
        self.reverse = False
        self.player_amount = self.config["players"]
        self.current_player = 0
        self.card_amount = 7 if card_amount == None else card_amount
        self.game_logged = {}
        
        ## Create player object
        for player in range(self.player_amount):
            self.game[str(player)] = {"cards": [],"past_cards": [],"cards_used": 0,}
        
        self.game_logged["player_amount"] = self.player_amount
        self.game_logged["card_amount"] = self.card_amount
        ## Setting colours for formatting the cards for console
        self.game["colour_codes"] = ["B","G","R","Y"]
        self.game["colours"] = {"B": 34, "G": 32, "R": 31, "Y": 33}
        self.game["colours_full"] = {"B":"Blue","G":"Green","R":"Red","Y":"Yellow"}
        self.game["cards"] = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "skip_turn","+2_card", "reverse_card"]
        self.game["special_cards"] = []
        self.game["current_game"] = {"cards_used": 0,"used": []}
        self.colour_current = random.choice(self.game["colour_codes"])
        ## Creating special cards
        for i in range(4):
            self.game["special_cards"].append("wild_card_{}".format(i))
            self.game["special_cards"].append("+4_card_{}".format(i))
        ## Creating all cards in the deck, to then be distributed
        for i in range(2):
            for colour in self.game["colour_codes"]:
                for card in self.game["cards"]:
                    self.deck.append(str(colour)+str(card))

        for card in self.game["special_cards"]:
            self.deck.append(card)
        
        self.title()

        ## Distributes the cards out to the amount of players
        for player in range(self.player_amount):
            for i in range(self.card_amount):
                card_to_be_given = random.choice(self.deck)
                self.game[str(player)]["cards"].append(str(card_to_be_given))
                self.deck.remove(card_to_be_given)

    ## Gets a random sleep time, within a certain range of the sleep time set in config.json
    def time_sleep(self):
        x = int(random.randrange((self.sleep_time-0.5)*100,(self.sleep_time+0.5)*100))/100
        return x


    ## Loads the game from game.json, giving the ability to save the game, and play it later
    ## It loads all the data, then replaces all the data in self.game with the newly imported data
    def load_game(self):
        game_loaded = json.loads(open('games/game.json',"r").read())
        self.player_amount = int(game_loaded[0]["player_amount"])
        self.card_amount = game_loaded[0]["card_amount"]
        self.my_player = game_loaded[0]["my_player"]
        self.game["current_game"]["used"] = list(eval(game_loaded[0]["cards_used"]))

        for player in range(self.player_amount):
            self.game[str(player)]["cards"] = game_loaded[0]["players"][str(player)]["deck"]
            self.game[str(player)]["past_cards"] = game_loaded[0]["players"][str(player)]["used_cards"]
            self.game[str(player)]["cards_used"] = int(len(game_loaded[0]["players"][str(player)]["used_cards"]))
       
    ## Saves the game data into game.json, to be loaded later
    def save_game(self):
        self.sv_gme = {
            "player_amount": "{}".format(self.player_amount),
            "card_amount": "{}".format(self.card_amount),
            "my_player": "{}".format(self.my_player),
            "cards_used": "{}".format(self.game["current_game"]["used"]),
            "cards_used_len": "{}".format(self.game["current_game"]["cards_used"]),}
        self.sv_gme["players"] = {}
        for player in range(self.player_amount):
            deck = self.game[str(player)]["cards"]
            used_cards = self.game[str(player)]["past_cards"]
            self.sv_gme["players"][str(player)] = {}
            self.sv_gme["players"][str(player)]["deck"] = deck
            self.sv_gme["players"][str(player)]["used_cards"] = used_cards
        open('games/game.json',"a")
        data = []
        data.append(self.sv_gme)
        json_object = json.dumps(data, indent=4)
        with open("games/game.json", "w") as outfile:
            outfile.write(json_object)


    ## Sets the title of the console, using os
    ## Gets the colour of the past card, and shows how many cards have been used, and what the previous card was
    def title(self):
        colour_full = self.game["colours_full"][self.colour_current]
        try:
            c = self.game["current_game"]["used"][-1:][0]
        except:
            os.system("title Colour: {} - Player: {} - Cards used: {} - Last Card: {}".format(colour_full, self.current_player,self.game["current_game"]["cards_used"], "None"))
            return
        name, pos, colour = self.card_format(c)
        colour = colour.lower().capitalize()
        if colour == "Black":
            os.system("title Colour: {} - Player: {} - Cards used: {} - Last Card: {}".format(colour_full, self.current_player,self.game["current_game"]["cards_used"], name))
        else:
            os.system("title Colour: {} - Player: {} - Cards used: {} - Last Card: {}".format(colour_full, self.current_player,self.game["current_game"]["cards_used"], "{} {}".format(colour,name)))
    

    ## Updates the cards_used count, for the title
    def count_update(self,player):
        self.game[str(player)]["cards_used"] += 1
        self.game["current_game"]["cards_used"] += 1
        return True


    ## Updates the player's used cards, and the current games cards
    def update(self):
        self.game_logged[self.game["current_game"]["cards_used"]] = {}
        self.game_logged[self.game["current_game"]["cards_used"]]["player"] = str(self.current_player)
        try:
            self.game_logged[self.game["current_game"]["cards_used"]]["card"] = self.game[str(self.current_player)]["past_cards"][-1]
        except:
            self.game_logged[self.game["current_game"]["cards_used"]]["card"] = "None"
        #self.game_logged[self.game["current_game"]["cards_used"]]["deck"] = self.game[str(self.current_player)]["cards"]
        #self.game_logged[self.game["current_game"]["cards_used"]]["deck_len"] = str(len(self.game[str(self.current_player)]["cards"]))
        #self.game_logged[self.game["current_game"]["cards_used"]]["cards_used"] = self.game[str(self.current_player)]["past_cards"]
        #self.game_logged[self.game["current_game"]["cards_used"]]["cards_used_len"] = str(len(self.game[str(self.current_player)]["past_cards"]))
        self.count_update(self.current_player)
        self.current_person_update()

    ## Changes the current person, and is able to check if the game is playing if reverse
    ## If the next player number becomes bigger than the player amount, it will take away the player amount, to make the player amount 0
    def current_person_update(self):
        if self.reverse:
            self.current_player -= 1
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

    ## Gives the player a certain card, bypassing the deck
    def give_admin_card(self, player, card):
        self.game[str(player)]["cards"].append(str(card))
        return True

    ## Returns the deck of the selected player
    def get_deck(self, player):
        return self.game[str(player)]["cards"]

    ## Gives the selected player a certain amount of cards from the deck
    def give_certain_person_cards(self, player,amount):
        try:
            if len(self.deck) > 0:
                for i in range(amount):
                    card_to_be_given = random.choice(self.deck)
                    if self.log:
                        print("Player {} has been given a card!".format(self.current_player))
                    self.game[str(player)]["cards"].append(str(card_to_be_given))
                    self.deck.remove(card_to_be_given)
                    if self.sleep:
                        time.sleep(self.time_sleep())
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

    ## Uses the card, central function to be able to use cards, without clogging the run function
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

    ## Checks if the user is a bot, if it isnt it asks for the colour, and then changes it, then updates the current player
    def wild_card(self,card,bot):
        if bot:
            x = True
            while x:
                new_colour = random.choice(self.game["colour_codes"])
                if new_colour != self.colour_current:
                    x = False
                else:
                    pass
        elif self.current_player == self.my_player:
            new_colour = input("What colour would you like to change the game to (R,G,B,Y): ")
        else:
            x = True
            while x:
                new_colour = random.choice(self.game["colour_codes"])
                if new_colour != self.colour_current:
                    x = False
                else:
                    pass

        self.colour_current = new_colour
        if self.log:
            print("Player {} has changed the colour to {}".format(self.current_player,new_colour))
        self.game[str(self.current_player)]["cards"].remove(card)
        self.game[str(self.current_player)]["past_cards"].append(card)
        self.game["current_game"]["used"].append(card)
        self.update()
        self.title()

    ## Finds which player the 2 cards have to be given to, and then gives them two cards from the deck and then updates the current player
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
            
            if self.log:
                print("+2 has been given to Player {} by {}".format(player_affected, self.current_player))
            if debug:
                print(self.game[str(player_affected)]["cards"])
            self.give_certain_person_cards(player_affected, 2)
            if debug:
                print(self.game[str(player_affected)]["cards"])
            self.game["current_game"]["used"].append(card)
            self.update()
            self.title()
            return True
        else:
            print("You have to use a {} card!".format(self.colour_current))
            return False

    ## Finds which player to give the 4 cards to, adds the cards, then asks the current player what colour to change the colour to, then updates the current player
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
            print("+4 has been given to Player {} by {}".format(player_affected, self.current_player))
        self.game[str(self.current_player)]["cards"].remove(card)
        self.game[str(self.current_player)]["past_cards"].append(card)
        self.give_certain_person_cards(player_affected, 4)
        if self.current_player == self.my_player:
            x = True
            while x:
                new_colour = input("What colour would you like to change the game to (R,G,B,Y): ")
                if new_colour != self.colour_current:
                    x = False
                else:
                    print("Please select a colour, that isnt the current colour!")
        else:
            x = True
            while x:
                new_colour = random.choice(self.game["colour_codes"])
                if new_colour != self.colour_current:
                    x = False
                else:
                    pass

        self.colour_current = new_colour
        if self.log:
            print("Player {} has changed the colour to {}".format(self.current_player,new_colour))
        self.update()
        self.game["current_game"]["used"].append(card)
        self.update()
        self.title()
        return True


    ## Sets the game into reverse, and updates current player
    def reverse_card(self, card):
        if self.log:
            print("Reverse card has been used by {}!".format(self.current_player))
        self.game[str(self.current_player)]["cards"].remove(card)
        self.game[str(self.current_player)]["past_cards"].append(card)
        
        self.game["current_game"]["used"].append(card)
        if self.reverse:
            self.reverse = False
        else:
            self.reverse = True
        self.update()
        self.title()
        return True

    ## Finds which player is next, and then skips their turn, by using "2" instead of "1"
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

    ## Removes the card from the players deck, and updates the current player
    def normal_card(self,card):
        c,pos,colour = self.card_format(card)
        if self.log:
            print("{} {} has been used by {}!".format(colour.capitalize(),c,self.current_player))
        self.game[str(self.current_player)]["cards"].remove(card)
        self.game[str(self.current_player)]["past_cards"].append(card)
        self.game["current_game"]["used"].append(card)
        self.update()
        self.title()
        return True

    ## Randomly picks a card in the bot's deck, as it isnt the current player's turn
    def bot_check(self):
        while True:
            if self.sleep:
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
    
    ## Formats the card so it is legible in the title
    def card_format(self,card):
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
    
    ## Main function for running the game
    def run(self):
        load = input("New game? (y/n): ")
        if load.lower() == "n":
            self.load_game()
        elif load.lower() == "y":

            self.my_player = random.randint(0,self.player_amount-1)
            self.game_logged["my_player"] = self.my_player
            print("You are Player {}!".format(self.my_player))
            print("\n")
        else:
            print("You didnt select an option, creating new game!")
            self.my_player = random.randint(0,self.player_amount-1)
            self.game_logged["my_player"] = self.my_player
            print("You are Player {}!".format(self.my_player))
            print("\n")
        while True:
            if self.sleep:
                time.sleep(self.time_sleep())
            if len(self.game[str(self.current_player)]["cards"]) == 1:
                print("{} is on UNO!".format(self.current_player))

            if len(self.game[str(self.current_player)]["cards"]) == 0:
                print("{} has won!".format(self.current_player))
                self.save_game()
                break
            if int(self.current_player) == int(self.my_player):
                if self.sleep:
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
                    elif "exit()" in c:
                        self.save_game()
                        return False
                    elif "deck(" in c:
                        find_deck = c.strip("deck(").strip(")")
                        r = self.get_deck(find_deck)
                        print(find_deck+"'s deck: {}".format(r))
                    else:
                        c = int(c)-1
                        try:
                            card = self.game[str(self.current_player)]["cards"][c]
                            self.use_card(str(self.current_player),card, bot=False)
                        except Exception:
                            self.give_certain_person_cards(str(self.current_player),1)
                            self.current_person_update()
                else:
                    self.give_certain_person_cards(str(self.current_player),1)
                    
                    self.current_person_update()
                    pass
            else:
                card = self.bot_check()
                self.use_card(str(self.current_player),card)
    
    ## Main function to run the game, but uses bots only, no player input
    def bot_run(self):
        self.my_player = self.player_amount +1
        while True:
            if len(self.game[str(self.current_player)]["cards"]) == 0:
                print("{} HAS WON!".format(self.current_player))
                self.save_game()
                return True
            card = self.bot_check()
            self.use_card(str(self.current_player),card,bot=True)

## Checks if to run via bots or not
if json.loads(open("config.json","r").read())["bot_game"]:
    UNO().bot_run()
else:
    UNO().run()