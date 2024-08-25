import math
import logging
import arcade
import pymunk

from game_object import Bird, ColumnV, ColumnH, Pig
from game_logic import get_impulse_vector, Point2D, get_distance
from game_object import Slingshot

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("arcade").setLevel(logging.WARNING)
logging.getLogger("pymunk").setLevel(logging.WARNING)
logging.getLogger("PIL").setLevel(logging.WARNING)

logger = logging.getLogger("main")

WIDTH = 1600
HEIGHT = 800
TITLE = "Angry birds"
GRAVITY = -900


class App(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        # self.background = arcade.load_texture("assets/img/background33.png")
        self.space = pymunk.Space()
        self.space.gravity = (0, GRAVITY)
        

        floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        floor_shape = pymunk.Segment(floor_body, [0, 12], [WIDTH, 12], 0.0)
        floor_shape.friction = 10
        self.space.add(floor_body, floor_shape)

        self.sprites = arcade.SpriteList()
        self.birds = arcade.SpriteList()
        self.world = arcade.SpriteList()
        self.score = 0 
        self.level = 1

        self.start_point = Point2D()
        self.end_point = Point2D()
        self.distance = 0
        self.draw_line = False

        self.handler = self.space.add_default_collision_handler()
        self.handler.post_solve = self.collision_handler
        
        self.setup_level()
        
        self.slingshot = Slingshot(300, 110)
        self.sprites.append(self.slingshot)

    def clear_level(self):
        for obj in self.world:
            obj.remove_from_sprite_lists()
            self.space.remove(obj.shape, obj.body)
        self.sprites = arcade.SpriteList()
        self.world = arcade.SpriteList()

    def collision_handler(self, arbiter, space, data):
        impulse_norm = arbiter.total_impulse.length
        if impulse_norm < 100:
            return True
        logger.debug(impulse_norm)
        if impulse_norm > 1200:
            for obj in self.world:
                if obj.shape in arbiter.shapes:
                    obj.remove_from_sprite_lists()
                    self.space.remove(obj.shape, obj.body)
        return True
    
    def update_collisions(self):
        pass
    
    def setup_level(self):
        self.clear_level()
        if self.level == 1:
            self.background = arcade.load_texture("assets/img/background31.png")
            self.add_columns(start_x=600, spacing=50, num_columns=20)
            self.add_pigs(start_x=600, spacing=50, num_pigs=6)
        elif self.level == 2:
            self.background = arcade.load_texture("assets/img/background32.png")
            self.add_columns(start_x=500, spacing=60, num_columns=15)
            self.add_pigs(start_x=550, spacing=55, num_pigs=5)
        else:
            self.background = arcade.load_texture("assets/img/background33.png")
            self.add_columns(start_x=500, spacing=60, num_columns=15)
            self.add_pigs(start_x=550, spacing=55, num_pigs=15)
            
    def add_columns(self, start_x, spacing, num_columns):
        for i in range(num_columns):
            x_position = start_x + i * spacing
            column = ColumnV(x_position, 50, self.space)
            self.sprites.append(column)
            self.world.append(column)

    def add_pigs(self, start_x, spacing, num_pigs):
        for i in range(num_pigs):
            x_position = start_x + i * spacing
            pig = Pig(x_position, 100, self.space)
            self.sprites.append(pig)
            self.world.append(pig)

    def on_update(self, delta_time: float):
        self.space.step(1 / 60.0)
        self.sprites.update()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.start_point = Point2D(x, y)
            self.end_point = Point2D(x, y)
            self.draw_line = True
            logger.debug(f"Start Point: {self.start_point}")

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        if buttons == arcade.MOUSE_BUTTON_LEFT:
            self.end_point = Point2D(x, y)
            logger.debug(f"Dragging to: {self.end_point}")

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            logger.debug(f"Releasing from: {self.end_point}")
            self.draw_line = False
            impulse_vector = get_impulse_vector(self.start_point, self.end_point)
            bird = Bird("assets/img/red-bird3.png", impulse_vector, x, y, self.space)
            self.sprites.append(bird)
            self.birds.append(bird)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, WIDTH, HEIGHT, self.background)
        self.sprites.draw()
        if self.draw_line:
            arcade.draw_line(300, 170, self.end_point.x, self.end_point.y,
                             arcade.color.BLACK, 3)
            
        arcade.draw_text(f"Score: {self.score}", 10, HEIGHT - 30, arcade.color.RED, 24)


def main():
    app = App()
    arcade.run()


if __name__ == "__main__":
    main()
