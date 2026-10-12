import pygame
import random
from .fruit import Fruit
from .sounds import Sounds

# Game Engine

WHITE = (255, 255, 255)
BOMB_BLACK = (30, 30, 30)
FRUIT_COLORS = [(220, 60, 60), (230, 140, 40), (230, 200, 40), (90, 180, 90)]

# spawn_interval = frames between spawns (lower = more fruit)
DIFFICULTIES = {
    "Easy":   {"spawn_interval": 75, "bomb_chance": 0.08},
    "Medium": {"spawn_interval": 55, "bomb_chance": 0.15},
    "Hard":   {"spawn_interval": 35, "bomb_chance": 0.25},
}
DIFFICULTY_ORDER = ["Easy", "Medium", "Hard"]
GAME_OVER_SOUND_DELAY = 25  # frames, so the bomb blast is heard first


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.font = pygame.font.SysFont("Arial", 28)
        self.big_font = pygame.font.SysFont("Arial", 64, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 22)
        self.sounds = Sounds()

        self.quit_requested = False
        self.difficulty = "Medium"
        self.speed_scale = 1.0

        # Clickable buttons on the game-over screen: (label, rect)
        self.buttons = self._build_buttons()

        self.reset(self.difficulty)

    # ---------- setup / reset ----------
    def _build_buttons(self):
        btn_w, btn_h, gap = 160, 50, 20
        total = 3 * btn_w + 2 * gap
        x0 = (self.width - total) // 2
        y = int(self.height * 0.58)
        buttons = []
        for i, name in enumerate(DIFFICULTY_ORDER):
            buttons.append((name, pygame.Rect(x0 + i * (btn_w + gap), y, btn_w, btn_h)))
        quit_rect = pygame.Rect((self.width - 200) // 2, y + btn_h + 30, 200, btn_h)
        buttons.append(("Quit", quit_rect))
        return buttons

    def reset(self, difficulty):
        self.difficulty = difficulty
        settings = DIFFICULTIES[difficulty]
        self.spawn_interval = settings["spawn_interval"]
        self.bomb_chance = settings["bomb_chance"]

        self.fruits = []
        self.trail = []  # recent mouse positions, drawn as the "blade"
        self._spawn_timer = 0
        self.lives = 3
        self.score = 0
        self.game_over = False
        self.game_over_reason = ""
        self._game_over_sound_timer = None

    # ---------- spawning ----------
    def spawn_fruit(self):
        x = random.randint(60, self.width - 60)
        vy = -random.uniform(13, 16) * self.speed_scale
        vx = random.uniform(-2, 2)
        gravity = 0.35
        kind = "bomb" if random.random() < self.bomb_chance else "fruit"

        fruit = Fruit(x, self.height + 30, vx, vy, gravity, kind=kind)
        fruit.color = BOMB_BLACK if kind == "bomb" else random.choice(FRUIT_COLORS)
        self.fruits.append(fruit)

    # ---------- input ----------
    def handle_event(self, event):
        if self.game_over:
            self._handle_game_over_event(event)
            return
        if event.type == pygame.MOUSEMOTION:
            self._handle_motion(event.pos)

    def _handle_game_over_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.reset("Easy")
            elif event.key == pygame.K_2:
                self.reset("Medium")
            elif event.key == pygame.K_3:
                self.reset("Hard")
            elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                self.quit_requested = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for label, rect in self.buttons:
                if rect.collidepoint(event.pos):
                    if label == "Quit":
                        self.quit_requested = True
                    else:
                        self.reset(label)
                    break

    def _handle_motion(self, pos):
        # Test the whole blade segment since the previous point, not just the
        # new point, so fast swipes can't skip over a fruit.
        prev = self.trail[-1] if self.trail else pos
        for fruit in self.fruits:
            if not fruit.sliced and fruit.intersects_segment(prev[0], prev[1], pos[0], pos[1]):
                self._slice(fruit)
                if self.game_over:
                    break

        self.trail.append(pos)
        if len(self.trail) > 15:
            self.trail.pop(0)

    def _slice(self, fruit):
        fruit.sliced = True
        if fruit.kind == "bomb":
            self.sounds.play("bomb")
            self._end_game("You sliced a bomb!")
        else:
            self.score += 1
            self.sounds.play("slice")

    def _end_game(self, reason):
        self.game_over = True
        self.game_over_reason = reason
        self._game_over_sound_timer = GAME_OVER_SOUND_DELAY

    def handle_input(self):
        # Reserved for continuously-held-key input; this game is
        # entirely mouse-driven, so there's nothing to poll here.
        pass

    # ---------- update ----------
    def update(self):
        if self.game_over:
            if self._game_over_sound_timer is not None:
                self._game_over_sound_timer -= 1
                if self._game_over_sound_timer <= 0:
                    self.sounds.play("game_over")
                    self._game_over_sound_timer = None
            return

        # Let the blade trail fade out when the mouse stops moving
        if self.trail:
            self.trail.pop(0)

        self._spawn_timer += 1
        if self._spawn_timer >= self.spawn_interval:
            self._spawn_timer = 0
            self.spawn_fruit()

        still_alive = []
        for fruit in self.fruits:
            fruit.update()
            if fruit.sliced:
                continue
            if fruit.off_screen(self.height):
                if fruit.kind == "fruit":
                    self.lives -= 1
                continue
            still_alive.append(fruit)
        self.fruits = still_alive

        if self.lives <= 0:
            self.lives = 0
            self._end_game("You ran out of lives!")

    # ---------- drawing ----------
    def render(self, screen):
        for fruit in self.fruits:
            if fruit.sliced:
                continue
            color = getattr(fruit, "color", WHITE)
            pygame.draw.circle(screen, color, (int(fruit.x), int(fruit.y)), fruit.radius)

        if len(self.trail) >= 2:
            pygame.draw.lines(screen, WHITE, False, self.trail, 3)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        screen.blit(lives_text, (self.width - 130, 10))
        diff_text = self.small_font.render(self.difficulty, True, (170, 170, 190))
        screen.blit(diff_text, (10, 45))

        if self.game_over:
            self._render_game_over(screen)

    def _centered(self, screen, surf, y):
        screen.blit(surf, ((self.width - surf.get_width()) // 2, y))

    def _render_game_over(self, screen):
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        self._centered(screen, self.big_font.render("GAME OVER", True, (230, 70, 70)), int(self.height * 0.15))
        self._centered(screen, self.small_font.render(self.game_over_reason, True, (200, 200, 210)), int(self.height * 0.15) + 80)
        self._centered(screen, self.font.render(f"Final Score: {self.score}", True, WHITE), int(self.height * 0.15) + 120)
        self._centered(screen, self.small_font.render("Play again - choose a difficulty:", True, WHITE), int(self.height * 0.58) - 40)

        mouse = pygame.mouse.get_pos()
        hints = {"Easy": "1", "Medium": "2", "Hard": "3", "Quit": "Q"}
        for label, rect in self.buttons:
            hovered = rect.collidepoint(mouse)
            fill = (80, 90, 140) if hovered else (50, 58, 95)
            pygame.draw.rect(screen, fill, rect, border_radius=8)
            pygame.draw.rect(screen, WHITE, rect, 2, border_radius=8)
            text = self.small_font.render(f"{label} ({hints[label]})", True, WHITE)
            screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))
