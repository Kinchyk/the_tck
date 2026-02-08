from pygame import *
from random import randint
import sys

init()
window_size = 1200, 800
window = display.set_mode(window_size)
clock = time.Clock()

try:
    pipe_texture = image.load("celinder.png").convert_alpha()
except:
    pipe_texture = Surface((150, 300), SRCALPHA)
    pipe_texture.fill((34, 139, 34))
try:
    bird_texture = image.load("bird.png").convert_alpha()
except:
    bird_texture = Surface((100, 100), SRCALPHA)
    bird_texture.fill((255, 215, 0))

player_rect = Rect(150, window_size[1] // 2 - 100, 100, 100)
bird_texture = transform.scale(bird_texture, (player_rect.width, player_rect.height))


def generate_pipes(count, pipe_width=150, gap=280, min_height=50, max_height=440, distance=650):
    pipes = []
    x = window_size[0]
    for _ in range(count):
        h = randint(min_height, max_height)
        top = Rect(x, 0, pipe_width, h)
        bottom = Rect(x, h + gap, pipe_width, window_size[1] - (h + gap))
        pipes.append((top, True))
        pipes.append((bottom, False))
        x += distance
    return pipes


main_font = font.Font(None, 100)
small_font = font.Font(None, 50)
title_font = font.Font(None, 120)

score = 0
lose = False
y_vel = 2

game_state = "menu"
base_pipe_speed = 10
selected_multiplier = 1
pipe_speed = base_pipe_speed * selected_multiplier


start_button = Rect(300, 160, 600, 100)
button_easy = Rect(300, 300, 600, 80)
button_medium = Rect(300, 400, 600, 80)
button_hard = Rect(300, 500, 600, 80)
button_retry = Rect(400, 380, 400, 80)
button_menu = Rect(400, 480, 400, 80)

pies = generate_pipes(150)


def reset_game():
    global pies, score, lose, y_vel, player_rect
    pies = generate_pipes(150)
    score = 0
    lose = False
    y_vel = 2
    player_rect.y = window_size[1] // 2 - 100


def draw_menu():
    window.fill((135, 206, 235))
    title = title_font.render("FLAPPY BIRD", True, (0, 0, 0))
    window.blit(title, title.get_rect(center=(window_size[0] // 2, 100)))
    draw.rect(window, (144, 238, 144), start_button)
    draw.rect(window, (0, 100, 0), start_button, 3)
    start_text = main_font.render("СТАРТ", True, (0, 0, 0))
    window.blit(start_text, start_text.get_rect(center=start_button.center))
    color_e = (144, 238, 144) if selected_multiplier == 1 else (211, 211, 211)
    color_m = (255, 255, 0) if selected_multiplier == 2 else (211, 211, 211)
    color_h = (240, 128, 128) if selected_multiplier == 4 else (211, 211, 211)
    draw.rect(window, color_e, button_easy)
    draw.rect(window, (0, 0, 0), button_easy, 2)
    easy_text = small_font.render("ЛЕГКА", True, (0, 0, 0))
    window.blit(easy_text, easy_text.get_rect(center=button_easy.center))
    draw.rect(window, color_m, button_medium)
    draw.rect(window, (0, 0, 0), button_medium, 2)
    medium_text = small_font.render("СЕРЕДНЯ", True, (0, 0, 0))
    window.blit(medium_text, medium_text.get_rect(center=button_medium.center))
    draw.rect(window, color_h, button_hard)
    draw.rect(window, (0, 0, 0), button_hard, 2)
    hard_text = small_font.render("СКЛАДНА", True, (0, 0, 0))
    window.blit(hard_text, hard_text.get_rect(center=button_hard.center))


def draw_game_over():
    window.fill((135, 206, 235))
    go_text = title_font.render("ВИ ПРОГРАЛИ", True, (255, 0, 0))
    window.blit(go_text, go_text.get_rect(center=(window_size[0] // 2, 120)))
    score_text = main_font.render(f"Очки: {int(score)}", True, (0, 0, 0))
    window.blit(score_text, score_text.get_rect(center=(window_size[0] // 2, 260)))
    draw.rect(window, (173, 216, 230), button_retry)
    draw.rect(window, (0, 0, 139), button_retry, 3)
    retry_text = small_font.render("ГРАТИ ЗНОВУ", True, (0, 0, 0))
    window.blit(retry_text, retry_text.get_rect(center=button_retry.center))
    draw.rect(window, (211, 211, 211), button_menu)
    draw.rect(window, (105, 105, 105), button_menu, 3)
    menu_text = small_font.render("ГОЛОВНЕ МЕНЮ", True, (0, 0, 0))
    window.blit(menu_text, menu_text.get_rect(center=button_menu.center))


while True:
    for e in event.get():
        if e.type == QUIT:
            sys.exit()
        if e.type == MOUSEBUTTONDOWN:
            mouse_pos = e.pos
            if game_state == "menu":
                if button_easy.collidepoint(mouse_pos):
                    selected_multiplier = 1
                elif button_medium.collidepoint(mouse_pos):
                    selected_multiplier = 2
                elif button_hard.collidepoint(mouse_pos):
                    selected_multiplier = 4
                if start_button.collidepoint(mouse_pos):
                    pipe_speed = base_pipe_speed * selected_multiplier
                    reset_game()
                    game_state = "playing"
            elif game_state == "game_over":
                if button_retry.collidepoint(mouse_pos):
                    pipe_speed = base_pipe_speed * selected_multiplier
                    reset_game()
                    game_state = "playing"
                elif button_menu.collidepoint(mouse_pos):
                    game_state = "menu"

    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        window.fill((135, 206, 235))
        window.blit(bird_texture, player_rect)
        for pie, is_top in pies[:]:
            if not lose:
                pie.x -= pipe_speed
            pipe_img = transform.scale(pipe_texture, (pie.width, pie.height))
            if is_top:
                pipe_img = transform.flip(pipe_img, False, True)
            window.blit(pipe_img, pie)
            if pie.x <= -pie.width:
                try:
                    pies.remove((pie, is_top))
                except ValueError:
                    pass
                score += 0.5
            if player_rect.colliderect(pie):
                lose = True
                game_state = "game_over"
        if len(pies) < 20:
            pies += generate_pipes(20)
        score_text = main_font.render(f"{int(score)}", True, (0, 0, 0))
        window.blit(score_text, (window_size[0] // 2 - score_text.get_rect().w // 2, 40))
        keys = key.get_pressed()
        if keys[K_w] and not lose:
            player_rect.y -= 15
        if keys[K_s] and not lose:
            player_rect.y += 15
        if player_rect.y >= window_size[1] - player_rect.height:
            lose = True
            game_state = "game_over"
        if lose:
            player_rect.y += y_vel
            y_vel *= 1.1
            if y_vel > 50:
                y_vel = 50
    elif game_state == "game_over":
        draw_game_over()
    display.update()
    clock.tick(60)
