import pgzrun
from pygame import Rect
import pygame

WIDTH, HEIGHT = 800, 500
GAME_MENU, GAME_PLAYING = "menu", "playing"
game_state = GAME_MENU
audio_on = True
music_playing = False

BTN_W, BTN_H = 300, 40

def btn_rect(cx, cy):
    return Rect(int(cx - BTN_W / 2), int(cy - BTN_H / 2), BTN_W, BTN_H)

def draw_button(text, center):
    r = btn_rect(*center)
    screen.draw.filled_rect(r, (120, 180, 255))
    screen.draw.rect(r, (255, 255, 255))
    screen.draw.text(text, center=center, fontsize=28, color="white")

def draw():
    screen.clear()
    if game_state == GAME_MENU:
        screen.fill((173, 230, 255))
        screen.draw.text("Jogo Plataforma de Brenda Mirelli", center=(WIDTH / 2, 140), fontsize=56, color=(255, 255, 255))
        draw_button("Start Game", (WIDTH / 2, 260))
        draw_button(f"Audio: {'ON' if audio_on else 'OFF'}", (WIDTH / 2, 320))
        draw_button("Quit", (WIDTH / 2, 380))
    elif game_state == GAME_PLAYING:
        screen.blit("background", (0, 0))

def toggle_music():
    global music_playing
    if audio_on:
        if not music_playing:
            pygame.mixer.music.load("sounds/music.mp3")
            pygame.mixer.music.play(-1)
            music_playing = True
    else:
        pygame.mixer.music.stop()
        music_playing = False



def on_mouse_down(pos, button):
    global game_state, audio_on

    if audio_on:
        sounds.click.play() 

    if game_state == GAME_MENU:
        if btn_rect(WIDTH / 2, 260).collidepoint(pos):
            game_state = GAME_PLAYING
            toggle_music()
        elif btn_rect(WIDTH / 2, 320).collidepoint(pos):
            audio_on = not audio_on
            toggle_music()
        elif btn_rect(WIDTH / 2, 380).collidepoint(pos):
            pygame.mixer.music.stop()
            exit()



if audio_on:
    toggle_music()

pgzrun.go()
