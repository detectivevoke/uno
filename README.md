# uno

I remade UNO (the game) in python, not finished.

Currently uploaded:
  - UNO base
  - Smart Bots
  - More Controlled Console


 To do:
  - Add a panel/console (possibly).
  - Split the main.py into files that are easier to read.
  - Add option log for the game (all print functions, that aren't important).
  - Make the bots optional, can use all players.
  - Update title (last card used).
 
Update 1:
  - Bots are now smarter, making the game harder
  - Printing of your deck is now using a function to get the colour, not in the run() function itself.

Update 2:
  - Split the use_card() function, to make it more legible for decoding.
  - Removed the give_cards() function, moved it into __init__().
