import pygame as pg
import sys
from screen import *
from ship import *
from explosion import *
from blink import *
from bird import *
from shield import *
import os
import random
WIDTH, HEIGHT = 1400, 600
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]


def main():

    # Walk.pngを読み込み
    bird_image_path = os.path.join(MAIN_DIR, 'fig/Walk.png')
    birds = pg.sprite.Group()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load(f"{MAIN_DIR}/imgs/bg_ocean.png")
    bg_img_flipped = pg.transform.flip(bg_img, True, False)
    bg_x = 0
    bg_x_flipped = bg_img.get_width()
    ship1_frame_count = 8  # Update this if your sprite sheet has a different number of frames
    ship2_frame_count = 4  # Update this if your sprite sheet has a different number of frames
    explosions = pg.sprite.Group()

    ship1 = Ship(1, (100, 200), ship1_frame_count)
    ship2 = Ship(7, (1000, 500), ship2_frame_count)
    ships = pg.sprite.Group(ship1, ship2)

    ship1_controls = {
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, +1),
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (1, 0),
    }
    ship2_controls = {
        pg.K_w: (0, -1),
        pg.K_s: (0, +1),
        pg.K_a: (-1, 0),
        pg.K_d: (1, 0),
    }
    for _ in range(5):  # 鳥数が５に
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        # スピードをランダムに
        speed_x = random.choice([1, 2, 3])
        speed_y = random.choice([-3, -2, -1, 1, 2, 3])
        bird = Bird(WIDTH, HEIGHT, bird_image_path, (x, y), frame_count=6,
                    speed=(speed_x, speed_y))
        birds.add(bird)

    shield_sprite_path = os.path.join(MAIN_DIR, 'fig/shield1.png')
    shield_frame_count = 8  # Update with the correct number of frames.
    # Example size, you can adjust this to your preference.
    new_shield_size = (200, 200)

    ship1_shield = AnimatedShield(
        ship1, shield_sprite_path, shield_frame_count, new_size=new_shield_size)
    ship2_shield = AnimatedShield(
        ship2, shield_sprite_path, shield_frame_count, new_size=new_shield_size)

    # Update with your blink sprite sheet file name
    blink_image_path = os.path.join(MAIN_DIR, 'fig/blink.png')
    blink_frame_count = 8  # Update with the correct number of frames

    ship1_blink = Blink(ship1, blink_image_path, blink_frame_count)
    ship2_blink = Blink(ship2, blink_image_path, blink_frame_count)
    ship1.blink_instance = ship1_blink
    ship2.blink_instance = ship2_blink

    tmr = 0
    clock = pg.time.Clock()

    while True:
        bg_x -= 1
        bg_x_flipped -= 1
        # イベントハンドラー
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
         # 背景をブリット
        if bg_x < -bg_img.get_width():
            bg_x = bg_img.get_width()
        if bg_x_flipped < -bg_img.get_width():
            bg_x_flipped = bg_img.get_width()
        screen.blit(bg_img, (bg_x, 0))
        screen.blit(bg_img_flipped, (bg_x_flipped, 0))

        if key_lst[pg.K_RETURN]:
            ship1_shield.update(screen)
        if key_lst[pg.K_CAPSLOCK]:
            ship2_shield.update(screen)

        if key_lst[pg.K_LSHIFT]:
            direction = (-1, 0) if key_lst[pg.K_a] else (1, 0)
            if not ship2.blinking:
                ship2_blink.start_blink(direction)

        if key_lst[pg.K_RSHIFT]:
            direction = (-1, 0) if key_lst[pg.K_LEFT] else (1, 0)
            if not ship1.blinking:
                ship1_blink.start_blink(direction)

        # Inside the game loop
        collision = pg.sprite.collide_rect(ship1, ship2)

        if collision:
            # Create an explosion at the center of each ship
            explosion1 = Explosion(center=ship1.rect.center)
            explosion2 = Explosion(center=ship2.rect.center)
            # Add the explosions to the explosions group
            explosions.add(explosion1, explosion2)
            # Kill both ships to remove them from the game
            ship1.kill()
            ship2.kill()

        for explosion in explosions:
            explosion.update()
            if explosion.frame_count > explosion.total_frames:
                explosions.remove(explosion)

        ship1_blink.update(screen)
        ship2_blink.update(screen)

        birds.update()  # 鳥をアップデート
        birds.draw(screen)

        if ship1.alive():
            ship1.update(key_lst, ship1_controls, screen)
        if ship2.alive():
            ship2.update(key_lst, ship2_controls, screen)
        for ship in ships:
            if ship.alive():
                screen.blit(ship.image, ship.rect)
            else:
                ship.kill()

        ships.draw(screen)
        explosions.draw(screen)

        pg.display.update()
        tmr += 1
        clock.tick(50)
#


if __name__ == "__main__":

    pg.init()
    main()
    pg.quit()
    sys.exit()
