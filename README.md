# VINVA
## VINVA stands for "VINVA is not Vim Adventures"
>This was my final project for the CS50 Introduction to Computer Science course. I am uploading it here to learn how to use git and hopefuly get some feedback.

### About the game
>The game is a top-down dungeon crawler with 20 levels and the idea behind is to teach the user basic commands in the Vim text editor and aims to serve as preparation for the vimtutor, which itself teaches basic commands while editing text. The game is inspired by the game Vim Adventures, which unfortunately is not freely available. That was also the main incentive for trying to make VINVA - so that people can get used to Vim commands for free.

### Resources
>The Python Arcade Library (https://api.arcade.academy/en/latest/)

> Tiled (https://www.mapeditor.org/)

> The soundtrack is attributed to AVGVSTA and it was downloaded from here: https://opengameart.org/content/generic-8-bit-jrpg-soundtrack (only one track is used: track number 03 - HWV 56 - Why do the nations so furiously rage together)

> Other sound effects were made by: RPG sounds by Kenney Vleugels (www.kenney.nl)

> Sprites were created by BUTTERHANDS and they can be found here:
https://butterhands.itch.io/doomland-kit
https://butterhands.itch.io/doomgeon-kit

### How to play the game
> Instead of using arrow keys for moving, you use L for going to the right, H for going to the left, J for going down, and K for going UP.

> Other controls are introduced while playing the game, but they all try to mimic the VIM commands. For instance, pressing the 0 key will move the player to the beginning of a row, i.e., in front of the first Wall object in the current row (just like the 0 key in VIM would move the cursor to the beginning of a line). The opposite would be the $ (dollar sign), which moves the player to the end of the row. Also, you can use 'gg' to go to the upper left corner of the map (beginning of a file) and 'G' (capital G) to go to the lower right corner of the map (end of a file). In the last level, the goal is to exit the game by typing :q (which is the command used for exiting vim)

> You are supposed to collect the keys in a level to open a chest so that you can advance to the next level. Also, you are supposed to avoid collision with skeletons, for it will restart the level and remove any keys you collected from your inventory.

### File structure
> level.py - handles loading levels from premade maps (created with Tiled) and specific instructions for each level

> constants.py - contains constants such as the player's movement speed, screen size, etc. Also, it contains starting positions for every level because the maps/levels and their instructions are different

> main.py - just the main function, nothing else

> mygame.py - contains the main Class of the game and handles all logic

### TODO
1) beautify existing levels and see to it that every one of them has the same starting positions
2) add 'delete' and 'replace' functionalities (like d and r in vim)
3) add a menu?
### SCREENSHOTS
![alt text](https://github.com/benjamin-mihoci/VINVA/blob/main/Screenshots/screen1.png)
![alt text](https://github.com/benjamin-mihoci/VINVA/blob/main/Screenshots/screen2.png)
![alt text](https://github.com/benjamin-mihoci/VINVA/blob/main/Screenshots/screen3.png)




