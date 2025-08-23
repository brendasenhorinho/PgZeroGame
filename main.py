import pgzrun
from pygame import Rect

WIDTH, HEIGHT = 800, 500
GAME_MENU, GAME_PLAYING = "menu", "playing"
game_state = GAME_MENU
audio_on = True
music_playing = False
BTN_W, BTN_H = 300, 40

# Plataformas
platforms = [
    {"image": "platform_large", "rect": Rect(0, 390, 250, 62)},
    {"image": "platform_small", "rect": Rect(350, 360, 100, 50)},
    {"image": "platform_large", "rect": Rect(550, 290, 250, 62)},  # Terceira
    {"image": "platform_large", "rect": Rect(220, 180, 250, 62)},  # Quarta
    {"image": "platform_small", "rect": Rect(40, 110, 100, 50)}
]

class Player:
    def __init__(self, x, y):
        self.image = "player_idle1"
        self.rect = Rect(x, y, 50, 82)
        self.vy = 0
        self.on_ground = False
        self.walk_images_right = ["player_walk1_right", "player_walk2_right"]
        self.walk_images_left = ["player_walk1_left", "player_walk2_left"]
        self.walk_index = 0
        self.walk_timer = 0
        self.facing_right = True
        self.idle_images = ["player_idle1", "player_idle2"]
        self.idle_index = 0
        self.idle_timer = 0

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.vy += 1
        self.on_ground = False

        next_rect = self.rect.copy()
        next_rect.y += self.vy

        collided = False
        for plat in platforms:
            if next_rect.colliderect(plat["rect"]) and self.vy > 0:
                if self.rect.bottom <= plat["rect"].top + 10:
                    self.rect.bottom = plat["rect"].top
                    self.vy = 0
                    self.on_ground = True
                    collided = True
                    break

        if not collided:
            self.rect.y += self.vy

        if not self.on_ground:
            self.image = "player_jump1"
        else:
            if keyboard.left or keyboard.a:
                self.facing_right = False
            elif keyboard.right or keyboard.d:
                self.facing_right = True

            if keyboard.left or keyboard.right or keyboard.a or keyboard.d:
                self.walk_timer += 1
                if self.walk_timer % 10 == 0:
                    self.walk_index = (self.walk_index + 1) % 2
                self.image = self.walk_images_right[self.walk_index] if self.facing_right else self.walk_images_left[self.walk_index]
            else:
                self.idle_timer += 1
                if self.idle_timer % 60 == 0:
                    self.idle_index = (self.idle_index + 1) % len(self.idle_images)
                self.image = self.idle_images[self.idle_index]

    def jump(self):
        if self.on_ground:
            self.vy = -18
            if audio_on:
                sounds.jump.play()

class Enemy:
    def __init__(self, x, y):
        self.rect = Rect(x, y, 50, 82)
        self.walk_images_right = ["enemy_walk1_right", "enemy_walk2_right"]
        self.walk_images_left = ["enemy_walk1_left", "enemy_walk2_left"]
        self.walk_index = 0
        self.walk_timer = 0
        self.facing_right = True
        self.image = self.walk_images_right[0]
        self.speed = 2

        self.on_platform = None
        for plat in platforms:
            if self.rect.bottom <= plat["rect"].top + 10 and \
               self.rect.centerx >= plat["rect"].x and \
               self.rect.centerx <= plat["rect"].x + plat["rect"].width:
                self.rect.bottom = plat["rect"].top
                self.on_platform = plat["rect"]
                break

        if self.on_platform:
            self.left_limit = self.on_platform.x
            self.right_limit = self.on_platform.x + self.on_platform.width
        else:
            self.left_limit = 0
            self.right_limit = WIDTH

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        if self.facing_right:
            self.rect.x += self.speed
            if self.rect.x + self.rect.width >= self.right_limit:
                self.facing_right = False
        else:
            self.rect.x -= self.speed
            if self.rect.x <= self.left_limit:
                self.facing_right = True

        self.walk_timer += 1
        if self.walk_timer % 15 == 0:
            self.walk_index = (self.walk_index + 1) % 2
        self.image = self.walk_images_right[self.walk_index] if self.facing_right else self.walk_images_left[self.walk_index]

# Criação dos personagens
player = Player(100, 300)
enemy1 = Enemy(550 + (250 - 50) // 2, 290 - 82)  # Terceira plataforma
enemy2 = Enemy(220 + (250 - 50) // 2, 180 - 82)  # Quarta plataforma

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
        for plat in platforms:
            screen.blit(plat["image"], (plat["rect"].x, plat["rect"].y))
            screen.draw.rect(plat["rect"], (0, 255, 0))

        player.draw()
        screen.draw.rect(player.rect, (255, 0, 0))
        feet = Rect(player.rect.x, player.rect.bottom - 4, player.rect.width, 4)
        screen.draw.rect(feet, (0, 0, 255))

        enemy1.draw()
        enemy2.draw()

def update():
    if game_state == GAME_PLAYING:
        if keyboard.left or keyboard.a:
            player.rect.x -= 5
        if keyboard.right or keyboard.d:
            player.rect.x += 5

        player.rect.x = max(0, min(player.rect.x, WIDTH - player.rect.width))
        player.update()
        enemy1.update()
        enemy2.update()

def on_key_down(key):
    if game_state == GAME_PLAYING:
        if key == keys.SPACE or key == keys.UP:
            player.jump()

def btn_rect(cx, cy):
    return Rect(int(cx - BTN_W / 2), int(cy - BTN_H / 2), BTN_W, BTN_H)

def draw_button(text, center):
    r = btn_rect(*center)
    screen.draw.filled_rect(r, (120, 180, 255))
    screen.draw.rect(r, (255, 255, 255))
    screen.draw.text(text, center=center, fontsize=28, color="white")

def toggle_music():
    sounds.music.stop()
    if audio_on:
        sounds.music.play()

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
            sounds.music.stop()
            exit()

if audio_on:
    toggle_music()

pgzrun.go()