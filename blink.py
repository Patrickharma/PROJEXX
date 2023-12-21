import pygame as pg
import sys
import os
from ship import *
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]


class Blink(pg.sprite.Sprite):
    def __init__(self, ship: Ship, image_path, frame_count):
        super().__init__()
        self.ship = ship
        self.spritesheet = pg.image.load(image_path).convert_alpha()
        self.frame_count = frame_count
        self.frames = self.load_frames(self.frame_count)
        self.current_frame = 0
        self.animation_speed = 1
        self.active = False  # Indicates if the blink is active

    def animate(self):
        if self.active:
            self.current_frame += self.animation_speed
            if self.current_frame >= len(self.frames):
                self.current_frame = 0
            self.image = self.frames[int(self.current_frame)]
            self.rect = self.image.get_rect(center=self.ship.rect.center)

    def start_blink(self, direction):
        self.active = True
        self.ship.blinking = True  # Tell the ship it's blinking
        self.ship.blink_direction = direction
        self.current_frame = 0  # Reset animation frame

        # Flip the animation frames if the blink direction is to the left
        self.frames = [pg.transform.flip(
            frame, True, False) if direction[0] < 0 else frame for frame in self.original_frames]

    def stop_blink(self):
        self.active = False
        self.ship.blinking = False  # Tell the ship it's done blinking

    def load_frames(self, frame_count):
        # Split the spritesheet into frames and resize if new_size is provided.
        frames = []
        frame_width = self.spritesheet.get_width() // frame_count
        frame_height = self.spritesheet.get_height()
        for i in range(frame_count):
            frame = self.spritesheet.subsurface(
                (i * frame_width, 0, frame_width, frame_height))
            frame = pg.transform.rotozoom(frame, 225, 1.0)
            frames.append(frame)
        # Store the original frames for flipping
        self.original_frames = list(frames)
        return frames

    def update(self, screen: pg.Surface):
        self.animate()
        if self.active:
            # Position the animation on the edge of the ship's rect based on direction
            if self.ship.blink_direction[0] > 0:  # If moving left
                self.rect.right = self.ship.rect.left
            else:  # If moving right
                self.rect.left = self.ship.rect.right
            screen.blit(self.image, self.rect)
