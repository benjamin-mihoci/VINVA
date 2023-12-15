# VINVA
## VINVA stands for "VINVA is not Vim Adventures"
>This was my final project for the CS50 Introduction to Computer Science course.

### About the game
>The game is a top-down dungeon crawler with 20 levels and the idea behind is to teach the user basic commands in the text editor Vim and serves as preparation for the vimtutor, which itself teaches basic commands while editing text. The game tries to imitate an already existing game called Vim Adventures (https://vim-adventures.com/), which is unfortunately not freely available. That was also the main incentive for making VINVA - so that people can get used to Vim commands without having to pay money for it.

### Resources
>The Python Arcade Library was used in making the game.

> Maps were made in the map editor "Tiled". Tiled was also used for animating most of the sprites. (Player's sprite was loaded and animated with the Arcade library in Python.)

> Soundtrack was made by AVGVSTA and it was downloaded from here: https://opengameart.org/content/generic-8-bit-jrpg-soundtrack (only one track is used: track number 03 - HWV 56 - Why do the nations so furiously rage together)

> Other sound effects were made by: RPG sounds by Kenney Vleugels (www.kenney.nl)

> Sprites were made by BUTTERHANDS and they can be found here:
https://butterhands.itch.io/doomland-kit
https://butterhands.itch.io/doomgeon-kit

### How to play the game
> Instead of using arrow keys, you are supposed to use L for going to the right, H for going to the left, J for going down, and K for going UP.

>Other controls are introduced while playing the game, but they all try to mimic the VIM commands. For instance, pressing the 0 key will move the player to the beginning of a row, i.e, in front of the first Wall object in the current row (just like the 0 key in VIM would move the cursor to the beginning of a line). The opposite would be the $ (dollar sign), which moves the player to the end of the row. Also, you can use 'gg' to go to the upper left corner of the map (beginning of a file) and 'G' (capital G) to go to the lower right corner of the map (end of a file). In the last level, the goal is to exit the game by typing :q (which is the command used for exiting vim)

> You are supposed to collect the keys in a level in order to open a chest so that you can advance to the next level. Also, you are supposed to avoid collision with skeletons, for it will restart the level and remove any keys you collected from your inventory.

### File structure
> level.py - handles loading leveles from premade maps (created with Tiled) and specific instructions for each level

> constants.py - contains constants such as player's movement speed, screen size, etc. also, it contains starting positions for every level because the maps/levels and their instructions are different

> main.py - just the main function, nothing else

> mygame.py - contains the main Class of the game and handles all logic
