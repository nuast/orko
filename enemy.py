"""Enemy implementation for the dungeon crawler."""

from __future__ import annotations

import pygame

from entity import Entity
from settings import ENEMY_COLOR, ENEMY_MAX_HEALTH, ENEMY_SIZE, ENEMY_SPEED, SCREEN_HEIGHT, SCREEN_WIDTH


class Enemy(Entity):
    """Basic enemy that moves toward the player.

    Inheritance: Enemy extends Entity with simple chase AI.
    """

    def __init__(self, x: float, y: float) -> None:
        """Create the enemy with default stats."""
        super().__init__(x, y, ENEMY_SIZE, ENEMY_SPEED, ENEMY_MAX_HEALTH, ENEMY_COLOR)

        # Placeholder sprite for now.
        # Later load Piskel sprite, for example: assets/enemy.png

    def update(self, player: Entity, *_: object) -> None:
        """Move enemy toward the player each frame.

        Polymorphism: Enemy update uses AI targeting instead of keyboard input.
        """
        if not self.is_alive:
            return

        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        if dx != 0:
            self._x += self._speed if dx > 0 else -self._speed
        if dy != 0:
            self._y += self._speed if dy > 0 else -self._speed

        self._rect.x = int(self._x)
        self._rect.y = int(self._y)
        self._clamp_to_screen(SCREEN_WIDTH, SCREEN_HEIGHT)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw enemy only while alive."""
        if self.is_alive:
            super().draw(surface)
