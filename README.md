# uno

I remade UNO (the game) in python, not finished.

Currently uploaded:
  - UNO base
  - Smart Bots
  - More Controlled Console


 To do:
  - Add a panel/console (possibly).
  - Split the main.py into files that are easier to read.
  - Make the bots optional, can use all players.
  - Website possibly? (would be basic, I cant  make JS and animations)
 
 
Update 1:
  - Bots are now smarter, making the game harder
  - Printing of your deck is now using a function to get the colour, not in the run() function itself.

Update 2:
  - Split the use_card() function, to make it more legible for decoding.
  - Removed the give_cards() function, moved it into __init__().

Update 3:
  - Added "config.json" to edit the configs of the game easily.
  - Added option logging, making console cleaner
  - Made the logging easier to understand
  - Edited the title of the console to say the correct last card used ("R7" to "Red 7")
  - The sleep time has been randomised by 0.5 seconds each side of the set time
  - Added admin options, to give cards, Usage: give(card_name) 
  - Made it so it skips player, when they don't have the correct card (like in the actual UNO game, I didn't know the rules)
