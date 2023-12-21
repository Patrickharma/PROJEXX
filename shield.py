import pygame as pg
import sys
import os
from ship import *
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]


class Shield(pg.sprite.Sprite):
    # シールドのクラスを作成
    def __init__(self, ship: Ship, radius: int = 75, color=(0, 0, 255), width=2):
        super().__init__()
        # ship自体、半径、色、幅を設定
        self.ship = ship
        self.radius = radius
        self.color = color
        self.width = width

    def update(self, screen: pg.Surface):
        # 円を描く
        pg.draw.circle(screen, self.color, self.ship.rect.center,
                       self.radius, self.width)


class AnimatedShield(pg.sprite.Sprite):
    def __init__(self, ship: Ship, image_path, frame_count, new_size=None):
        super().__init__()
        self.ship = ship
        self.spritesheet = pg.image.load(image_path).convert_alpha()
        self.frame_count = frame_count
        # Pass the new_size argument to the load_frames method.
        self.frames = self.load_frames(self.frame_count, new_size)
        self.current_frame = 0
        self.animation_speed = 0.2

    def load_frames(self, frame_count, new_size):
        # Split the spritesheet into frames and resize if new_size is provided.
        frames = []
        frame_width = self.spritesheet.get_width() // frame_count
        frame_height = self.spritesheet.get_height()
        for i in range(frame_count):
            frame = self.spritesheet.subsurface(
                (i * frame_width, 0, frame_width, frame_height))
            if new_size:
                # Scale the frame to the new_size.
                frame = pg.transform.scale(frame, new_size)
            frames.append(frame)
        return frames
