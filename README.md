## Space Invaders: Prototype Files

This repository holds the early work on a Space Invaders game built with Pygame. It currently contains two scripts: a small timing experiment and a playable test environment. Both open an 800x600 window and run a main loop at 60 FPS, but they focus on different parts of the game.

### Timing test (`timing_test.py`)

This script is where the game loop itself was worked out before any gameplay existed. A green rectangle stands in for the player and moves across the screen at 300 pixels per second. The important part is how that movement is calculated. `clock.tick(60)` caps the frame rate and returns the milliseconds since the last frame, which is converted to seconds and stored as `dt` (delta time). The rectangle's position is then advanced by `speed * dt` each frame, so it covers the same distance in the same real-world time whether the game runs at 30 FPS or 144.

The rectangle has no input handling and no screen boundary, so it simply drifts off the right-hand side of the window. That is deliberate: the script exists to check that the timing logic behaves correctly, and it is not meant to be played. The window setup, the 60 FPS cap and the structure of the loop (handle events, update, draw, flip) are the same ones the test environment is built on.

### Test environment (`space_invaders_test.py`)

This is the playable version, and it adds everything the timing test leaves out. The player is a green dot at the bottom of the screen, moved left and right with the arrow keys or A and D. Holding space or W fires white bullets upwards, limited by a 250 millisecond cooldown so shots can't be spammed. The player's position is clamped to the window edges, which fixes the out-of-frame problem the timing test has.

Above the player is a grid of 32 red rectangles (4 rows of 8) that move sideways as a group. When any enemy reaches the edge of the window, the whole group reverses direction and drops down by 20 pixels. Each frame, every bullet is checked against every enemy using a rectangle collision test, and when one hits, both the bullet and the enemy are removed. Bullets that leave the top of the screen are also cleaned up.

One difference between the two files is worth knowing about. The test environment moves things by a fixed number of pixels per frame (for example `player_speed = 6`) rather than using `dt`, so its speeds are tied to the 60 FPS cap. The timing test shows the frame-rate-independent approach that this version has not adopted yet.

The comment at the top of the test environment lists the features planned for it: levels, powerups, music, colour changes, harder bosses and faster gameplay, a highscore tracker, a combo meter, and a fix for the enemy drop behaviour.

### Running the scripts

Both scripts need Python 3.8 or later and Pygame:

```bash
pip install pygame
```

Then run whichever one you want:

```bash
python timing_test.py
python space_invaders_test.py
```
