import pygame as pg
import sys
import os
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]


class Explosion(pg.sprite.Sprite):
    def __init__(self, center, size=(100, 100)):
        super().__init__()
        self.images = []
        self.load_images()
        self.current_frame = 0
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect(center=center)
        self.frame_count = 0
        # Total frames for the explosion animation
        self.total_frames = 10*5  # Number of images times desired frames per image

    def load_images(self):
        for i in range(1, 11):  # Assuming you have 10 images for the explosion
            img = pg.image.load(
                f'{MAIN_DIR}/fig/Explosion_{i}.png').convert_alpha()
            img = pg.transform.scale(img, (100, 100))  # Scale to desired size
            self.images.append(img)

    def update(self):
        if self.frame_count < self.total_frames:
            self.current_frame = (self.frame_count // 5) % len(self.images)
            self.image = self.images[self.current_frame]
            self.frame_count += 1
        else:
            self.kill()  # Kill the sprite after the animation
