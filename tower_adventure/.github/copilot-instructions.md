# Tower Adventure - AI Coding Instructions

## Project Overview

This is a **pure 2D platformer game** built with pygame featuring a mouse character ("起司小子") descending from a tower top to ground level. The game uses a continuous vertical level system with 5 distinct sections focused on **platforming challenges only** - **all enemies and cheese have been removed** from the level generator, making this a pacifist exploration experience.

## Architecture & Key Patterns

### Core Game Loop Structure

- **Event-driven input**: Main loop in `main.py` handles discrete events (jumps, slides) vs continuous input (movement)
- **Camera system**: Smooth following camera with 0.1 interpolation factor in `game.py`
- **State management**: Four game states: `playing`, `game_over`, `victory`, `upgrade`
- **Pure platformer**: No combat or collection mechanics - focus on movement and exploration

### Module Organization

```
config/settings.py    # All constants, colors (RGB tuples), physics values
src/game.py          # Main game logic, camera, state transitions
src/player.py        # Complex player mechanics (coyote time, multi-jump, charge attacks)
src/game_objects.py  # Platform, Enemy, Cheese classes (enemies/cheese unused)
src/ui.py           # UI rendering with Chinese font fallback system
levels/level_generator.py  # Procedural 5-section tower generation (platforms only)
```

### Critical Physics & Game Systems

#### Player Movement Mechanics

- **Coyote time**: 6-frame grace period after leaving platform (`PLAYER_MAX_COYOTE_TIME`)
- **Variable height jumping**: Hold spacebar for `PLAYER_MAX_JUMP_HOLD` frames
- **Multi-jump system**: Default 2 jumps, upgradeable to 3
- **Slide mechanic**: 20-frame slide with 60-frame cooldown, changes player color to pink

#### Collision Detection Pattern

All collision uses pygame.Rect with directional velocity checks:

```python
# From above (landing)
if self.vel_y > 0 and self.y < platform.rect.top - 5:
```

#### Level Generation System

- **Continuous tower**: Each section is `SECTION_HEIGHT` (1200px) tall
- **Safe spawn area**: Section 1 has starting platform at (500, 20)
- **Progress-based upgrades**: Triggered every `SECTION_HEIGHT` descent
- **Green safety platforms**: Healing platforms between sections (color == GREEN)

## Development Conventions

### Chinese Localization

- **UI text**: All in Traditional Chinese (`src/ui.py`)
- **Font system**: Primary font `msjh.ttc` with fallback to pygame default
- **Comments**: Mixed Chinese/English, Chinese for game logic explanations

### Color & Constants Management

- **All colors as RGB tuples** in `config/settings.py` (e.g., `WHITE = (255, 255, 255)`)
- **Physics constants centralized**: `GRAVITY = 0.6`, `JUMP_STRENGTH = -12`
- **Magic numbers avoided**: Use named constants like `PLAYER_MAX_COYOTE_TIME`

### Rendering Optimization

- **Screen culling**: Only draw objects within `[-50, WINDOW_HEIGHT + 50]` range
- **Camera offset pattern**: All draw methods accept `camera_offset_y` parameter
- **Surface reuse**: UI elements don't recreate surfaces unnecessarily

## Key Integration Points

### Game State Transitions

Progress rewards trigger in `game.py` based on `player.y / SECTION_HEIGHT`:

```python
if current_progress > self.last_progress:
    self.show_progress_reward()  # Shows upgrade menu
```

### Input System Architecture

- **Discrete actions**: Use `pygame.KEYDOWN` events (jumping, sliding)
- **Continuous actions**: Check key sets in main loop (movement)
- **Attack system**: Still implemented but unused (no enemies to attack)
- **Legacy features**: Charge attacks and combat exist but serve no purpose

### Legacy Systems (Currently Unused)

Enemy and cheese systems remain in codebase but are disabled:

- **Enemy AI**: Complete patrol system exists but no enemies spawn
- **Cheese collection**: Collection mechanics exist but no cheese spawns
- **Combat system**: Attack/defense mechanics functional but purposeless

## Testing & Debugging

### Quick Start Commands

```bash
python main.py              # Direct game start
start_game.bat             # Windows launcher with pause
pip install pygame>=2.0.0  # Minimal dependency
```

### Common Debugging Points

- **Collision issues**: Check 5-pixel buffer in platform collision detection
- **Camera jitter**: Verify 0.1 interpolation factor in camera update
- **Missing upgrades**: Ensure `last_progress` tracking in `reset_game()`
- **Font rendering**: Test Chinese text with fallback font system

### Performance Considerations

- **Object culling**: Verify screen bounds checking in all draw methods
- **Collision optimization**: Enemies only check collision when `health > 0`
- **Memory management**: No persistent surface creation in game loop

## Game Balance & Design

### Section Progression Design

1. **Section 1**: Safe tutorial area with starting platform at (500, 20)
2. **Section 2**: Basic platforming with varied platform sizes
3. **Section 3**: Combat platform layouts (enemies removed, platforms remain)
4. **Section 4**: Precision platforming with small platforms (60x15, 50x15)
5. **Section 5**: Final challenge area and victory condition (ground level)

### Upgrade System Balance

Three upgrade types per checkpoint: health restoration (+30), attack boost (+5), extra jump capability. Health/healing systems remain functional for safe platform interactions.
