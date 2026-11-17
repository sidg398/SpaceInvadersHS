# SpaceInvadersHS
import pygame
# Space Invaders Test Environment Sid Ghosh
# Features to include : Levels, Powerups, Music(?), Colour changes, Harder bosses/ Faster gameplay, Highscore tracker, Combo meter, and also fix issues with going out of frame
pygame.init()

# --- Setup ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders - test environment SG")
clock = pygame.time.Clock() #clock object keeping track of time

# --- Player (just a dot for now) ---
player_x = WIDTH // 2
player_y = HEIGHT - 50
player_radius = 10
player_speed = 6

# --- Bullets ---
bullets = []            # each bullet is a [x, y] pair
bullet_speed = 10   # speed of each bullet
bullet_radius = 4 # radius of each bullet
shoot_cooldown = 250   # milliseconds between shots
last_shot = 0

# --- Mobs --- NEW
# rectangular shape for now3
enemies = []            # each enemy is an [x, y] pair (top-left corner)
enemy_width = 40
enemy_height = 25
enemy_speed = 2         # sideways speed of the whole group
enemy_direction = 1     # 1 = moving right, -1 = moving left
enemy_drop = 20         # how far they drop when they hit the edge - fix?

# build a grid of enemies: 4 rows of 8
for row in range(4):
    for col in range(8):
        enemies.append([100 + col * 70, 50 + row * 45])

# --- Game loop ---
running = True
while running:
    # Events (closing the window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    # Bullet / enemy collision: both disappear on a hit --- NEW
    for bullet in bullets[:]:               # [:] loops over a copy so we can remove safely
        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
            if enemy_rect.collidepoint(bullet[0], bullet[1]):
                bullets.remove(bullet)
                enemies.remove(enemy)
                break                       # this bullet is used up, move to the next one

    # Draw
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (0, 255, 0), (player_x, player_y), player_radius) # creates the circle that shoots
    for bullet in bullets:
        pygame.draw.circle(screen, (255, 255, 255), (bullet[0], bullet[1]), bullet_radius)
    for enemy in enemies:  # NEW - enemy draw red rectangles
        pygame.draw.rect(screen, (255, 0, 0), (enemy[0], enemy[1], enemy_width, enemy_height))
    pygame.display.flip()

    clock.tick(60)  # 60 FPS

pygame.quit()
