import pgzrun
from pygame import Rect

WIDTH, HEIGHT = 800, 500
GAME_MENU, GAME_PLAYING = "menu", "playing"
game_state = GAME_MENU
audio_on = True
music_playing = False
BTN_W, BTN_H = 300, 40

# Plataformas com tamanhos reais
platforms = [
    {"image": "platform_large", "rect": Rect(0, 390, 250, 62)},
    {"image": "platform_small", "rect": Rect(350, 360, 100, 50)},
    {"image": "platform_large", "rect": Rect(550, 290, 250, 62)},
    {"image": "platform_large", "rect": Rect(220, 180, 250, 62)},
    {"image": "platform_small", "rect": Rect(40, 110, 100, 50)}
]

class Player:
    def __init__(self, x, y):
        self.image = "player_idle1"
        self.rect = Rect(x, y, 50, 84)
        self.vy = 0
        self.on_ground = False
        self.walk_images = ["player_walk1", "player_walk2"]
        self.walk_index = 0
        self.walk_timer = 0

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

        # Animação de pulo
        if not self.on_ground:
            self.image = "player_jump1"
        else:
            # Animação de caminhada
            if keyboard.left or keyboard.right or keyboard.a or keyboard.d:
                self.walk_timer += 1
                if self.walk_timer % 10 == 0:
                    self.walk_index = (self.walk_index + 1) % len(self.walk_images)
                self.image = self.walk_images[self.walk_index]
            else:
                self.image = "player_idle1"

    def jump(self):
        if self.on_ground:
            self.vy = -18  # pulo mais forte
            if audio_on:
                sounds.jump.play()

player = Player(100, 300)



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
            screen.draw.rect(plat["rect"], (0, 255, 0))  # verde: colisão da plataforma

        player.draw()
        screen.draw.rect(player.rect, (255, 0, 0))  # vermelho: colisão do jogador

        feet = Rect(player.rect.x, player.rect.bottom - 4, player.rect.width, 4)
        screen.draw.rect(feet, (0, 0, 255))  # azul: área dos pés

def update():
    if game_state == GAME_PLAYING:
        # Movimento lateral
        if keyboard.left or keyboard.a:
            player.rect.x -= 5
        if keyboard.right or keyboard.d:
            player.rect.x += 5

        # Limite da tela
        player.rect.x = max(0, min(player.rect.x, WIDTH - player.rect.width))

        player.update()

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