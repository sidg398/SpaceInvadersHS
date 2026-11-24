import pygame
import random
import math
# Space Invaders Test Environment Sid Ghosh
# Features to include : Levels, Powerups, Music(?), Colour changes, Harder bosses/ Faster gameplay, Highscore tracker, Combo meter, and also fix issues with going out of frame
pygame.init()

# --- Setup ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders - test environment SG")
clock = pygame.time.Clock() #clock object keeping track of time
font = pygame.font.SysFont(None, 32)
big_font = pygame.font.SysFont(None, 72)
# --- Player (just a dot for now) ---
PLAYER_START_X = WIDTH // 2
PLAYER_START_Y = HEIGHT - 50
player_x = WIDTH // 2
player_y = HEIGHT - 50
player_radius = 10
player_speed = 6

# --- Lives, score and respawn --- NEW
START_LIVES = 3
lives = START_LIVES
score = 0
invulnerable_until = 0          # time (ms) until which the player can't be hit
INVULNERABLE_TIME = 2000        # ms of invulnerability after respawn

# --- Bullets ---
bullets = []            # each bullet is a [x, y] pair
bullet_speed = 10   # speed of each bullet
bullet_radius = 4 # radius of each bullet
shoot_cooldown = 250   # milliseconds between shots
last_shot = 0

# --- Invader bullets (I needed to complete this so I can test invader bullet vs player and lives) --- NEW
enemy_bullets = []      # each is a [x, y] pair, travels DOWN
enemy_bullet_speed = 5
enemy_bullet_radius = 4
enemy_shoot_delay = 800     # ms between invader shots
last_enemy_shot = 0

# --- Mobs --- NEW
# rectangular shape for now3
enemies = []            # each enemy is an [x, y] pair (top-left corner)
enemy_width = 40
enemy_height = 25
enemy_speed = 2         # sideways speed of the whole group
enemy_direction = 1     # 1 = moving right, -1 = moving left
enemy_drop = 20         # how far they drop when they hit the edge - fix?

# --- NEW (moved the enemy grid into a function so a restart can rebuild it)
def build_enemies():
    """Build a grid of enemies: 4 rows of 8"""
    grid = []
    for row in range(4):
        for col in range(8):
            grid.append([100 + col * 70, 50 + row * 45])
    return grid
enemies = build_enemies()


# --- NEW
def respawn_player():
    """Put the defender back at the start position and clear incoming fire."""
    global player_x, player_y, invulnerable_until
    player_x = PLAYER_START_X
    player_y = PLAYER_START_Y
    enemy_bullets.clear()
    invulnerable_until = pygame.time.get_ticks() + INVULNERABLE_TIME


# --- NEW
def reset_game():
    """Start a fresh game (press R on the game over screen)."""
    global lives, score, game_over, enemies, enemy_direction
    lives = START_LIVES
    score = 0
    game_over = False
    enemies = build_enemies()
    enemy_direction = 1
    bullets.clear()
    respawn_player()

# --- Game loop ---
running = True
while running:
    # Events (closing the window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Restart after game over --- NEW
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
            reset_game()
    now = pygame.time.get_ticks()

    if not game_over:  # --- NEW (everything below freezes when the game is over)
        # Input (hold left/right arrows or A/D)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed

    # Shoot with spacebar or W key
    now = pygame.time.get_ticks()
    if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and now - last_shot > shoot_cooldown:
        bullets.append([player_x, player_y - player_radius])
        last_shot = now

    # Keep the player on screen
    player_x = max(player_radius, min(WIDTH - player_radius, player_x))

    # Move bullets up, remove ones that leave the screen
    for bullet in bullets:
        bullet[1] -= bullet_speed
    bullets = [b for b in bullets if b[1] > 0]

    # Move enemies sideways, drop down and reverse at the screen edge --- NEW
    for enemy in enemies:
        enemy[0] += enemy_speed * enemy_direction
    if any(e[0] <= 0 or e[0] + enemy_width >= WIDTH for e in enemies):
        enemy_direction *= -1
        for enemy in enemies:
            enemy[1] += enemy_drop
            
    # --- Invader firing (PLACEHOLDER - Catherine's random firing replaces this) --- NEW
        if enemies and now - last_enemy_shot > enemy_shoot_delay:
            shooter = random.choice(enemies)
            enemy_bullets.append([shooter[0] + enemy_width // 2, shooter[1] + enemy_height])
            last_enemy_shot = now

        # Move invader bullets down, remove ones that leave the screen --- NEW
        for eb in enemy_bullets:
            eb[1] += enemy_bullet_speed
        enemy_bullets = [eb for eb in enemy_bullets if eb[1] < HEIGHT]

    # Bullet / enemy collision: both disappear on a hit --- NEW
    for bullet in bullets[:]:               # [:] loops over a copy so we can remove safely
        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
            if enemy_rect.collidepoint(bullet[0], bullet[1]):
                bullets.remove(bullet)
                enemies.remove(enemy)
                break                       # this bullet is used up, move to the next one
    # Invader bullet / player collision --- NEW
        # Ignored while the player is invulnerable after a respawn
        if now >= invulnerable_until:
            for eb in enemy_bullets[:]:
                distance = math.hypot(eb[0] - player_x, eb[1] - player_y)
                if distance < player_radius + enemy_bullet_radius:
                    enemy_bullets.remove(eb)
                    lives -= 1                  # reduce lives by 1
                    if lives <= 0:
                        game_over = True        # game over when lives reach 0
                    else:
                        respawn_player()        # back to start + brief invulnerability
                    break
    # Draw
    screen.fill((0, 0, 0))

    # Player blinks while invulnerable --- NEW
    blink_on = (now // 100) % 2 == 0
    if now >= invulnerable_until or blink_on:
        if not game_over:
            pygame.draw.circle(screen, (0, 255, 0), (player_x, player_y), player_radius)  # creates the circle that shoots
    for bullet in bullets:
        pygame.draw.circle(screen, (255, 255, 255), (bullet[0], bullet[1]), bullet_radius)
    for eb in enemy_bullets:  # NEW - invader bullets are orange
        pygame.draw.circle(screen, (255, 200, 0), (eb[0], eb[1]), enemy_bullet_radius)
    for enemy in enemies:  # NEW - enemy draw red rectangles
        pygame.draw.rect(screen, (255, 0, 0), (enemy[0], enemy[1], enemy_width, enemy_height))

    # HUD: lives and score --- NEW
    screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))
    lives_text = font.render(f"Lives: {max(lives, 0)}", True, (255, 255, 255))
    screen.blit(lives_text, (WIDTH - lives_text.get_width() - 10, 10))

    # Game over screen --- NEW
    if game_over:
        over = big_font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(over, (WIDTH // 2 - over.get_width() // 2, HEIGHT // 2 - 60))
        info = font.render(f"Final score: {score}  -  press R to restart", True, (255, 255, 255))
        screen.blit(info, (WIDTH // 2 - info.get_width() // 2, HEIGHT // 2 + 10))

    pygame.display.flip()

    clock.tick(60)  # 60 FPS

pygame.quit()
