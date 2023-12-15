from typing import Optional
import time
import level
from arcade.gui import UIManager, UIEvent, UIMessageBox, UIKeyPressEvent
import arcade
import constants


class PlayerCharachter(arcade.Sprite):

    def __init__(self):
        super().__init__()
        self.player_animation = []
        self.cur_texture = 0
        self.scale = 1.5

        # load the sprites for player animation
        for i in range(1, 5):
            img = arcade.load_texture(f"./Sprites/Hero-outline{i}.png")
            self.player_animation.append(img)

        # set the texture to the first sprite
        self.texture = self.player_animation[0]

    def update_animation(self, delta_time: float = 1 / 60):
        self.cur_texture += 1
        if self.cur_texture > 3 * constants.UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // constants.UPDATES_PER_FRAME
        self.texture = self.player_animation[frame]


class MyPopup(UIMessageBox):
    def on_event(self, event: UIEvent) -> Optional[bool]:

        # For closing the instructions window with ESCAPE instead of clicking on it

        if isinstance(event, UIKeyPressEvent):
            if event.symbol == arcade.key.ESCAPE:
                self.close()
                return True
        return super().on_event(event)

    def close(self):
        if self.parent:
            self.parent.remove(self)


class MyGame(arcade.Window):

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)

        # enable the UIManager
        self.player_animation = []
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Number of keys collected and number needed to unlock the chest
        self.keys = 0
        self.needed = None

        # Sound related variables
        self.footsteps = []
        self.footstep_count = 0
        self.key_sound = None
        self.chest_sound = None
        self.death_sound = None
        self.music_list = []
        self.current_song_index = 0
        self.music = None
        self.current_player = None

        # Creating GUI boxes
        self.v_box = arcade.gui.UIBoxLayout()
        self.v_box2 = arcade.gui.UIBoxLayout()

        # GUI buttons, only one of them is clickable
        open_message_box_button = arcade.gui.UIFlatButton(text="Press BACKSPACE for help", width=200,
                                                          style={"bg_color": (169, 169, 169, 200), "font_size": 10})
        self.v_box.add(open_message_box_button)
        self.open_message_box_button2 = arcade.gui.UIFlatButton(text=f"Keys: {self.keys}", width=200,
                                                                style={"bg_color": (169, 169, 169, 200),
                                                                       "font_size": 10})
        self.v_box2.add(self.open_message_box_button2)

        # clickability of one button
        open_message_box_button.on_click = self.on_click_open
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="right",
                anchor_y="bottom",
                child=self.v_box)
        )
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="bottom",
                child=self.v_box2
            )
        )

        # level-related variables
        self.level_list = []
        self.num_of_lev = constants.NUMBER_OF_LEVELS
        self.current_level = 0
        self.new_level = None

        # tilemap object
        self.tile_map = None

        # lists for checking collisions, untouchables are enemies that
        # player_sprite may not collide with
        self.impassable_list = []
        self.untouchable_list = []

        # scene object
        self.scene = None

        self.player_sprite = None

        self.camera = None
        self.gui_camera = None

        # these are for a workaround until I figure out how to properly use a GUI for text-input
        self.key2 = None
        self.key3 = None

    def play_song(self):

        # There is only one song for now that keeps repeating

        self.music = arcade.Sound(self.music_list[0], streaming=True)
        self.current_player = self.music.play(1)
        time.sleep(0.03)

    def display_message(self, message):
        message_box = arcade.gui.UIMessageBox(
            width=300,
            height=200,
            message_text=message,
            buttons=["Ok"],
        )
        self.manager.add(message_box)

    def on_click_open(self, event):
        self.manager.add(MyPopup(message_text=level.message(self.current_level), width=300, height=200))

    def setup(self):

        self.music_list = [f"./Sounds/HWV56.ogg"]
        self.current_song_index = 0
        self.play_song()

        # Set up the Cameras
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        for i in range(0, 10):
            sound = arcade.load_sound(f"./Sounds/footstep0{i}.ogg")
            self.footsteps.append(sound)

        self.key_sound = arcade.load_sound(f"./Sounds/beltHandle1.ogg")
        self.death_sound = arcade.load_sound(f"./Sounds/death.wav")
        self.chest_sound = arcade.load_sound(f"./Sounds/doorClose_3.ogg")

        # Keep track of the collected keys
        self.keys = 0

        # create levels and add them to a list
        for x in range(0, self.num_of_lev):
            self.new_level = level.level_setup(x)
            self.level_list.append(self.new_level)

        # load the first level
        self.scene = self.level_list[self.current_level].scene
        self.tile_map = self.level_list[self.current_level].tile_map
        self.impassable_list = self.level_list[self.current_level].impassable_list
        self.untouchable_list = self.level_list[self.current_level].untouchable_list

        # adjust settings for each sprite in each level
        # this is needed because of different sizes of the sprites

        for leve in self.level_list:
            for sprite in leve.tile_map.sprite_lists["Keys"]:
                sprite.scale = 2
            for sprite in leve.tile_map.sprite_lists["Chest"]:
                sprite.scale = 1.5
            for sprite in leve.tile_map.sprite_lists["BadVertical"]:
                sprite.scale = 1.5
                sprite.change_x = 0
                sprite.change_y = 5
                sprite.center_x += 24
            for sprite in leve.tile_map.sprite_lists["BadHorizontal"]:
                sprite.scale = 1.5
                sprite.change_x = 5
                sprite.change_y = 0
                sprite.center_y += 24

        # the needed amount of keys to finish the level
        # is the same as the lenght of key sprites on generation
        self.needed = len(self.tile_map.sprite_lists["Keys"])

        # create a player sprite and add him to the scene
        self.player_sprite = PlayerCharachter()
        self.player_sprite.center_x, self.player_sprite.center_y = constants.STARTING_POSITIONS[self.current_level]
        self.player_sprite.previous_x, self.player_sprite.previous_y = constants.STARTING_POSITIONS[self.current_level]
        self.scene.add_sprite("Player", self.player_sprite)

        # add a popup message with instructions for the first level
        self.manager.add(MyPopup(message_text=level.message(self.current_level), width=300, height=200))
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()
        self.gui_camera.use()
        self.manager.draw()

    def sound_footstep(self):
        arcade.play_sound(self.footsteps[self.footstep_count], volume=0.2)

    def update_footsteps(self):
        self.footstep_count += 1
        if self.footstep_count == 10:
            self.footstep_count = 0

    def save_position(self):
        self.player_sprite.previous_y = self.player_sprite.center_y
        self.player_sprite.previous_x = self.player_sprite.center_x

    def colliding(self):
        # checks if player is colliding with lists he can't pass through
        return arcade.check_for_collision_with_lists(self.player_sprite, self.impassable_list)

    def update_level(self):
        # load the current level

        # reset the number of keys in case a player died during one level
        self.keys = 0

        # load the scene from the current level
        self.scene = self.level_list[self.current_level].scene
        self.tile_map = self.level_list[self.current_level].tile_map
        self.impassable_list = self.level_list[self.current_level].impassable_list
        self.untouchable_list = self.level_list[self.current_level].untouchable_list

        self.needed = len(self.tile_map.sprite_lists["Keys"])

        self.player_sprite = PlayerCharachter()
        self.player_sprite.center_x, self.player_sprite.center_y = constants.STARTING_POSITIONS[self.current_level]
        self.player_sprite.previous_x, self.player_sprite.previous_y = constants.STARTING_POSITIONS[self.current_level]
        self.scene.add_sprite("Player", self.player_sprite)
        self.manager.add(MyPopup(message_text=level.message(self.current_level), width=300, height=200))

    def on_key_press(self, key, modifiers):

        # a temporary workaround to close the game until I figure out the GUI
        if self.key2 == ':' and self.key3 == 'Q' and key != arcade.key.ENTER:
            self.key2 = '\0'
            self.key3 = '\0'
        elif self.key2 == ':' and self.key3 == 'Q' and key == arcade.key.ENTER:
            self.close()
        elif key == arcade.key.PERIOD and modifiers & arcade.key.MOD_SHIFT:
            self.key2 = ":"
        elif self.key2 == ":" and key == arcade.key.Q:
            self.key3 = "Q"
        elif self.key2 == ":" and key != arcade.key.Q:
            self.key2 = '\0'
            self.key3 = '\0'

        # for moving UP
        elif key == arcade.key.K:
            self.save_position()
            self.player_sprite.center_y += constants.PLAYER_MOVEMENT_SPEED
            if self.colliding():
                self.undo_movement()
            else:
                self.sound_footstep()
                self.update_footsteps()

        # for printing instructions
        elif key == arcade.key.BACKSPACE:
            self.manager.add(MyPopup(message_text=level.message(self.current_level), width=300, height=200))

        # for moving down
        elif key == arcade.key.J:
            self.save_position()
            self.player_sprite.center_y -= constants.PLAYER_MOVEMENT_SPEED
            if self.colliding():
                self.undo_movement()
            else:
                self.sound_footstep()
                self.update_footsteps()

        # for moving to the left
        elif key == arcade.key.H:
            self.save_position()
            self.player_sprite.center_x -= constants.PLAYER_MOVEMENT_SPEED
            if self.colliding():
                self.undo_movement()
            else:
                self.sound_footstep()
                self.update_footsteps()

        # for moving to the right
        elif key == arcade.key.L:
            self.save_position()
            self.player_sprite.center_x += constants.PLAYER_MOVEMENT_SPEED
            if self.colliding():
                self.undo_movement()
            else:
                self.sound_footstep()
                self.update_footsteps()
        # for moving to the end of the current 'word', i.e., in front of the next obstacle
        elif key == arcade.key.E:

            gen = (sprite for sprite in self.tile_map.sprite_lists["Obstacles"]
                   if sprite.center_y == self.player_sprite.center_y and sprite.center_x > self.player_sprite.center_x)
            min = 10000
            found = False
            for sprite in gen:
                if sprite.center_x == self.player_sprite.center_x + constants.PLAYER_MOVEMENT_SPEED:
                    continue
                if sprite.center_x < min:
                    min = sprite.center_x
                    found = True
            if found:
                self.save_position()
                self.player_sprite.center_x = min - constants.PLAYER_MOVEMENT_SPEED
                if self.colliding():
                    self.undo_movement()
            else:
                for i in range(1, 50):
                    gen = (sprite for sprite in self.tile_map.sprite_lists["Obstacles"]
                           if sprite.center_y == self.player_sprite.center_y - (constants.PLAYER_MOVEMENT_SPEED * i))
                    min = 1000
                    found_min = False
                    for sprite in gen:
                        if sprite.center_x < min:
                            min = sprite.center_x
                            found_min = True

                    if found_min:
                        self.save_position()
                        self.player_sprite.center_y -= constants.PLAYER_MOVEMENT_SPEED * i
                        self.player_sprite.center_x = min - constants.PLAYER_MOVEMENT_SPEED
                        if self.colliding():
                            self.undo_movement()
                        break

        # for moving behind the next obstacle, i.e., in front of the next 'word'
        elif key == arcade.key.W:
            gen = (sprite for sprite in self.tile_map.sprite_lists["Obstacles"] if
                   sprite.center_y == self.player_sprite.center_y and sprite.center_x > self.player_sprite.center_x)
            min = 10000
            found = False
            for sprite in gen:
                if sprite.center_x < min:
                    min = sprite.center_x
                    found = True
            if found:
                self.save_position()
                self.player_sprite.center_x = min + constants.PLAYER_MOVEMENT_SPEED
                if self.colliding():
                    self.undo_movement()
            else:
                for i in range(1, 50):
                    gen = (sprite for sprite in self.tile_map.sprite_lists["Obstacles"] if
                           sprite.center_y == self.player_sprite.center_y - (constants.PLAYER_MOVEMENT_SPEED * i))
                    min = 1000
                    found_min = False
                    for sprite in gen:
                        if sprite.center_x < min:
                            min = sprite.center_x
                            found_min = True
                    if found_min:
                        self.save_position()
                        self.player_sprite.center_y -= (constants.PLAYER_MOVEMENT_SPEED * i)
                        self.player_sprite.center_x = min + constants.PLAYER_MOVEMENT_SPEED
                        if self.colliding():
                            self.undo_movement()
        # for moving to the beginning of the previous 'word', i.e. in front of the previous obstacle
        elif key == arcade.key.B:
            gen = (sprite for sprite in self.tile_map.sprite_lists["Obstacles"] if
                   sprite.center_y == self.player_sprite.center_y and sprite.center_x < self.player_sprite.center_x)
            min = 0
            found = False
            for sprite in gen:
                if sprite.center_x == self.player_sprite.center_x - constants.PLAYER_MOVEMENT_SPEED:
                    continue
                if sprite.center_x > min:
                    min = sprite.center_x
                    found = True
            if found:
                self.player_sprite.center_x = min + constants.PLAYER_MOVEMENT_SPEED
                if self.colliding():
                    self.undo_movement()
            else:
                for i in range(1, 50):
                    gen = (sprite for sprite in self.tile_map.sprite_lists["Obstacles"] if
                           sprite.center_y == self.player_sprite.center_y + (constants.PLAYER_MOVEMENT_SPEED * i))
                    min = 0
                    found_min = False
                    for sprite in gen:
                        if sprite.center_x > min:
                            min = sprite.center_x
                            found_min = True
                    if found_min:
                        self.save_position()
                        self.player_sprite.center_y += (i * constants.PLAYER_MOVEMENT_SPEED)
                        self.player_sprite.center_x = min + constants.PLAYER_MOVEMENT_SPEED
                        if self.colliding():
                            self.undo_movement()
                        break

        # Go to the beginning of a line, i.e, in front of the first wall object in current line
        elif key == arcade.key.KEY_0:
            gen = (sprite for sprite in self.tile_map.sprite_lists["Wall"]
                   if sprite.center_y == self.player_sprite.center_y and sprite.center_x < self.player_sprite.center_x)
            max = 0
            found = False
            for sprite in gen:
                if sprite.center_x == self.player_sprite.center_x + constants.PLAYER_MOVEMENT_SPEED:
                    continue
                if sprite.center_x > max:
                    max = sprite.center_x
                    found = True
            if found:
                self.save_position()
                self.player_sprite.center_x = max + constants.PLAYER_MOVEMENT_SPEED
                if self.colliding():
                    self.undo_movement()

        # go to the lower right corner
        elif modifiers & arcade.key.MOD_SHIFT and key == arcade.key.G:
            self.key2 = '\0'
            gen = (sprite for sprite in self.tile_map.sprite_lists["Wall"]
                   if sprite.center_x == self.player_sprite.center_x and sprite.center_y < self.player_sprite.center_y)
            min = 5000
            for sprite in gen:
                if sprite.center_y < min:
                    min = sprite.center_y

            gen = (sprite for sprite in self.tile_map.sprite_lists["Wall"]
                   if sprite.center_y == min + constants.PLAYER_MOVEMENT_SPEED
                   and sprite.center_x > self.player_sprite.center_x)
            max = 0
            for sprite in gen:
                if sprite.center_x > max:
                    max = sprite.center_x
            self.save_position()
            self.player_sprite.center_y = min + constants.PLAYER_MOVEMENT_SPEED
            self.player_sprite.center_x = max - constants.PLAYER_MOVEMENT_SPEED

            if self.colliding():
                self.undo_movement()

        # if G is pressed two times in a row, go the upper left corner
        elif self.key2 != 'G' and key == arcade.key.G:
            self.key2 = 'G'
        elif self.key2 == 'G' and key != arcade.key.G:
            self.key2 == '0'
        elif self.key2 == 'G' and key == arcade.key.G:
            self.key2 == '0'
            # Now I see that I could have made my life so much easier
            # If every level had the same starting position in the upper left corner, but whatever
            gen = (sprite for sprite in self.tile_map.sprite_lists["Wall"]
                   if sprite.center_x == self.player_sprite.center_x and sprite.center_y > self.player_sprite.center_y)
            max = 0
            for sprite in gen:
                if sprite.center_y > max:
                    max = sprite.center_y

            gen = (sprite for sprite in self.tile_map.sprite_lists["Wall"]
                   if sprite.center_y == max - constants.PLAYER_MOVEMENT_SPEED
                   and sprite.center_x < self.player_sprite.center_x)
            min = 5000
            for sprite in gen:
                if sprite.center_x < min:
                    min = sprite.center_x

            self.save_position()
            self.player_sprite.center_y = max - constants.PLAYER_MOVEMENT_SPEED
            self.player_sprite.center_x = min + constants.PLAYER_MOVEMENT_SPEED

            if self.colliding():
                self.undo_movement()

        # dollar sign, go to the end of line, i.e., in front of the last wall object in current line
        if key == arcade.key.KEY_4 and modifiers & arcade.key.MOD_SHIFT:
            gen = (sprite for sprite in self.tile_map.sprite_lists["Wall"]
                   if sprite.center_y == self.player_sprite.center_y
                   and sprite.center_x > self.player_sprite.center_x)
            min = 5000
            found = False
            for sprite in gen:
                if sprite.center_x == self.player_sprite.center_x + constants.PLAYER_MOVEMENT_SPEED:
                    continue
                if sprite.center_x < min:
                    min = sprite.center_x
                    found = True

            if found:
                self.save_position()
                self.player_sprite.center_x = min - constants.PLAYER_MOVEMENT_SPEED
                if self.colliding():
                    self.undo_movement()



    def center_camera_to_player(self):
        # so that the camera follows the player
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def undo_movement(self):
        self.player_sprite.center_y = self.player_sprite.previous_y
        self.player_sprite.center_x = self.player_sprite.previous_x

    def on_update(self, delta_time):
        """Movement and game logic"""

        position = self.music.get_stream_position(self.current_player)
        if position == 0.0:
            # restarts the background music if it ended
            self.play_song()

        if arcade.check_for_collision_with_list(self.player_sprite, self.tile_map.sprite_lists["Chest"]):
            # check if enough keys has been collected to open the chest and advance
            if self.keys == self.needed:
                self.tile_map.sprite_lists["Chest"].clear()
                arcade.play_sound(self.chest_sound)
                self.current_level += 1
                self.update_level()
                time.sleep(0.1)

        if arcade.check_for_collision_with_lists(self.player_sprite, self.untouchable_list):
            # if we die, play the death sound and reload the level
            arcade.play_sound(self.death_sound)
            self.player_sprite.kill()
            self.new_level = level.level_setup(self.current_level)

            for sprite in self.new_level.tile_map.sprite_lists["Keys"]:
                sprite.scale = 2
            for sprite in self.new_level.tile_map.sprite_lists["Chest"]:
                sprite.scale = 1.5
            for sprite in self.new_level.tile_map.sprite_lists["BadVertical"]:
                sprite.scale = 1.5
                sprite.change_x = 0
                sprite.change_y = 5
                sprite.center_x += 24
            for sprite in self.new_level.tile_map.sprite_lists["BadHorizontal"]:
                sprite.scale = 1.5
                sprite.change_x = 5
                sprite.change_y = 0
                sprite.center_y += 24
            self.level_list[self.current_level] = self.new_level
            self.update_level()

        for sprite in self.tile_map.sprite_lists["BadVertical"]:
            sprite.center_y = sprite.center_y + sprite.change_y
            if arcade.check_for_collision_with_lists(sprite, self.impassable_list):
                sprite.change_y *= -1

        for sprite in self.tile_map.sprite_lists["BadHorizontal"]:
            sprite.center_x = sprite.center_x + sprite.change_x
            if arcade.check_for_collision_with_lists(sprite, self.impassable_list):
                sprite.change_x *= -1

        if arcade.check_for_collision_with_list(self.player_sprite, self.tile_map.sprite_lists["Keys"]):
            arcade.check_for_collision_with_list(self.player_sprite, self.tile_map.sprite_lists["Keys"])[0].kill()
            arcade.play_sound(self.key_sound)
            self.keys += 1

        # Position the camera
        self.center_camera_to_player()
        self.open_message_box_button2.text = f"Keys: {self.keys}/{self.needed}"

        self.tile_map.sprite_lists["Keys"].update_animation()
        self.tile_map.sprite_lists["BadHorizontal"].update_animation()
        self.tile_map.sprite_lists["BadVertical"].update_animation()
        self.tile_map.sprite_lists["Chest"].update_animation()
        self.player_sprite.update_animation()
