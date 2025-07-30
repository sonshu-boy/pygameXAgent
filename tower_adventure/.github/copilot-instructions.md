# Tower Adventure - AI Coding Instructions

## Project Overview

This is a 2D platform game built with pygame featuring a mouse character ("起司小子") descending from a tower top to ground level. The game uses a continuous vertical level system with 5 distinct sections, each offering different challenges and upgrade opportunities.

## Architecture & Key Patterns

### Core Game Loop Structure

- **Event-driven input**: Main loop in `main.py` handles discrete events (jumps, slides) vs continuous input (movement, charge attacks)
- **Camera system**: Smooth following camera with 0.1 interpolation factor in `game.py`
- **State management**: Four game states: `playing`, `game_over`, `victory`, `upgrade`

### Module Organization

```
config/settings.py    # All constants, colors (RGB tuples), physics values
src/game.py          # Main game logic, camera, state transitions
src/player.py        # Complex player mechanics (coyote time, multi-jump, charge attacks)
src/game_objects.py  # Platform, Enemy, Cheese classes with collision detection
src/ui.py           # UI rendering with Chinese font fallback system
levels/level_generator.py  # Procedural 5-section tower generation
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
- **Safe spawn area**: Section 1 has enemy-free starting platform at (500, 20)
- **Progress-based upgrades**: Triggered every `SECTION_HEIGHT` descent

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
- **Continuous actions**: Check key sets in main loop (movement, charging)
- **Charge attacks**: Track time in main loop, apply damage on `MOUSEBUTTONUP`

### Enemy AI Pattern

Simple but effective: patrol within `ENEMY_PATROL_RANGE` of spawn point, reverse direction at platform edges or range limits.

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

1. **Section 0**: Safe tutorial area with welcome cheese
2. **Sections 1-2**: Basic platforming with sparse enemies
3. **Section 3**: Combat-heavy with boss enemies
4. **Section 4**: Precision platforming with small platforms
5. **Section 5**: Final boss area and victory condition

### Upgrade System Balance

Three upgrade types per checkpoint: health restoration (+30), attack boost (+5), extra jump capability. System prevents overpowered combinations through section-gated progression.
