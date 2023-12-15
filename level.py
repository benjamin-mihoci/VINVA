import arcade
import arcade.gui
import constants


class Level():

    def __init__(self):

        self.tile_map = None
        self.impassable_list = []
        self.untouchable_list = []

        self.scene = None
        self.level_num = None
        self.map_name = None
        self.completed = False
        self.instructions = None


def level_setup(level_num):

    level = Level()
    level.level_num = level_num

    level.layer_options = {

            "Ground": {

                "use_spatial_hash": True,

            },

            "Wall": {

                "use_spatial_hash": True,
            },

            "Obstacles": {
                "use_spatial_hash": True,

            },

            "Keys": {
                "use_spatial_hash": True,
            },

            "BadVertical": {
                "use_spatial_hash": False,
            },

            "BadHorizontal": {
                "use_spatial_hash": False,
            },

            "Chest": {
                "use_spatial_hash": True,
            }

        }

    # Name of map file to load
    level.map_name = f"./Maps/map{level.level_num}.tmx"

    # Read in the tiled map
    level.tile_map = arcade.load_tilemap(level.map_name, constants.TILE_SCALING, level.layer_options)

    # Initialize Scene with our TileMap, this will automatically add all layers
    # from the map as SpriteLists in the scene in the proper order.

    level.scene = arcade.Scene.from_tilemap(level.tile_map)
    level.impassable_list.append(level.tile_map.sprite_lists["Obstacles"])
    level.impassable_list.append(level.tile_map.sprite_lists["Wall"])

    level.untouchable_list.append(level.tile_map.sprite_lists["BadHorizontal"])
    level.untouchable_list.append(level.tile_map.sprite_lists["BadVertical"])
    return level


def message(level_num):
    if level_num == 0:
        return ("Use the L key to move to the right and pick up the key! Press ESC to close this box.")
    if level_num == 1:
        return ("Use the H key to move to the left!")
    if level_num == 2:
        return ("Great! Now use K to go up!")
    if level_num == 3:
        return ("Excellent work! Now use J to go down!")
    if level_num == 4:
        return ("Now, beware of the skeletons!")
    if level_num == 5:
        return ("MORE SKELETONS! AVOID THEM!")
    if level_num == 6:
        return ("Alright, just one more time for good measure.")
    if level_num == 7:
        return ("Ok, hopefully, you now know the basic controls. Press E to jump in front of the next obstacle.")
    if level_num == 8:
        return ("Same, but different. Use E.")
    if level_num == 9:
        return("Now use W to go behind the next obstacle.")
    if level_num == 10:
        return("Now use B to go in front of the previous obstacle.")
    if level_num == 11:
        return("Use what you learned to avoid the skeletons.")
    if level_num == 12:
        return("Collect all three keys!")
    if level_num == 13:
        return("So far, so good. Now, press 4 while holding shift. "
               "The dollar sign will get you to the end of this row.")
    if level_num == 14:
        return("Now, use number 0 to get to the the beginning of this row.")
    if level_num == 15:
        return("Hold the shift key and the press G to go to the lower right corner.")
    if level_num == 16:
        return("Now press G two times to get to the upper right corner.")
    if level_num == 17:
        return("You're on your own.")
    if level_num == 18:
        return("This is kinda hard. Why don't you give up?")
    if level_num == 19:
        return("Wow. You actually did it. To end press :q and then ENTER, i.e. hold the SHIFT button, "
               "press the period and then ENTER. Thanks for playing!")