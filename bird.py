import pygame as pg
import sys
import os
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]


class Bird(pg.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT, image_path, xy, frame_count, speed):
        super().__init__()
        self.spritesheet = pg.image.load(
            image_path).convert_alpha()  # ファイル読み込み
        self.frame_count = frame_count
        self.frames = self.load_frames(self.frame_count)
        self.current_frame = 0
        self.animation_speed = 0.2
        # 最初のフレームから
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=xy)
        self.speed = speed
        self.BGWIDTH = WIDTH
        self.BGHEIGHT = HEIGHT

    def load_frames(self, frame_count):
        # spritesheetからフレームを取得
        frames = []
        frame_width = self.spritesheet.get_width() // frame_count
        frame_height = self.spritesheet.get_height()

        for i in range(frame_count):
            frame = self.spritesheet.subsurface(
                (i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)
        return frames
    
    def animate(self):
        # Sprite動かし
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0

        self.image = self.frames[int(self.current_frame)]

    def update(self):
        # アップデート
        self.animate()  # sprite動かし
        self.rect.x += self.speed[0]
        #self.rect.y += self.speed[1]

        if self.rect.right < 0:
            self.rect.left = self.BGWIDTH
        if self.rect.left > self. BGWIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = self.BGHEIGHT
        if self.rect.top > self.BGHEIGHT:
            self.rect.bottom = 0
