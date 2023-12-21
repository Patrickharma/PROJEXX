import pygame as pg
import sys
import os
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]


class Ship(pg.sprite.Sprite):
    """
    船作成
    """

    def __init__(self, num: int, xy: tuple[int, int], frame_count):
        super().__init__()
        self.spritesheet = pg.image.load(
            f"{MAIN_DIR}/fig/{num}.png").convert_alpha()
        self.frame_count = frame_count
        self.frames = self.load_frames(self.frame_count)
        self.current_frame = 0
        self.animation_speed = 0.2
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=xy)
        self.speed = 10
        self.dire = (0, 0)

        self.blinking = False
        self.blink_distance = 500  # Updated blink distance
        self.blink_direction = (1, 0)  # Default blink direction to the right

        self.last_direction = (+1, 0)

        self.blink_speed = 20  # How fast the ship blinks per frame

    def load_frames(self, frame_count):
        frames = []
        frame_width = self.spritesheet.get_width() // frame_count
        frame_height = self.spritesheet.get_height()
        for i in range(frame_count):
            frame = self.spritesheet.subsurface(
                (i * frame_width, 0, frame_width, frame_height))
            frames.append(frame)
        return frames

    def animate(self):
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]

    def update(self, key_lst: list[bool], ctrl_keys: dict, screen: pg.Surface):
        """
        押下キーに応じてこうかとんを移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        if not self.blinking:
            sum_mv = [0, 0]
            for k, mv in ctrl_keys.items():
                if key_lst[k]:
                    self.rect.move_ip(+self.speed*mv[0], +self.speed*mv[1])
                    sum_mv[0] += mv[0]
                    sum_mv[1] += mv[1]
                if sum_mv != [0, 0]:
                    # Update the last direction when moving
                    self.last_direction = (sum_mv[0], sum_mv[1])
        else:
            # Blinking movement code
            self.rect.x += self.blink_direction[0] * self.blink_speed
            self.blink_distance -= self.blink_speed
            if self.blink_distance <= 0:
                self.blinking = False
                self.blink_distance = 500  # Reset blink distance
                self.blink_direction = (1, 0)  # Reset blink direction
                # Trigger the stop_blink method of the Blink instance
                self.blink_instance.stop_blink()
        screen.blit(self.image, self.rect)

        self.animate()

