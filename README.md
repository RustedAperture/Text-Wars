# Text Wars

Created by: Cameron Varley

Description: A fun text game where you can battle a enemy, gamble, or become a millionaire

Requirement: Python3

## Change Log
#### Version 2.2.0 (latest)
major changes to the base code. spring cleaning as well
1. Player class introduced to make the code easier to read
2. player values are now accessed by the player.value instead of userVal[value]
3. removed duplicate code or unnecessary
4. change menu() to return True to prevent loops in loops
5. changed transport() to slim down code, makes more sense now
6. casino/gamble now uses the loot system for prizes

#### Version 2.1.0
Created a few helper scripts that will allow for future proofing
1. created pymenu which will help in speedy menu creation
2. created pystore which is a simple store helper to create items
3. default items are stored in store.config

#### Version 2.0.2
this update is just a few simple changes
1. comments were added for confusing/difficult parts of the script
2. store items are now stored in a single location
3. added some comments regarding what future plans might entail
   
#### Version 2.0.0
1. Complete Overhaul of script
   1. this includes the menu
   2. validation of inputs
   3. sanitization
   4. variable
   5. almost 400 lines have been removed

## TODO
1. add hints for the user
2. create another script to add items
3. create different troop types - this might be too hard...
4. convert pygame and pymenu to full crud helper scripts
5. create a way to make hidden menu items 