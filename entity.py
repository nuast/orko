"""Base entity classes used by all moving game characters."""

from __future__ import annotations

from abc import ABC, abstractmethod

import pygame


class Entity(ABC):
    """Abstract base class for all game entities.

    Abstraction: this class defines a simple interface (update, draw)
    that child classes must provide.
    """

    def __init__(self, x: float, y: float, size: int, speed: float, max_health: int, color: tuple[int, int, int]) -> None:
        """Create an entity with position, movement speed, and health."""
        # Encapsulation: these protected attributes are shared and managed by the class hierarchy.
        self._x = x
        self._y = y
        self._speed = speed

        # Encapsulation: private health state is only changed through methods.
        self.__health = max_health
        self._max_health = max_health

        self._rect = pygame.Rect(int(self._x), int(self._y), size, size)

        # Placeholder graphics surface for now.
        # Later this can load a Piskel PNG sprite from assets/.
        # Example: pygame.image.load("assets/entity.png").convert_alpha()
        self._sprite = pygame.Surface((size, size))
        self._sprite.fill(color)

    @property
    def rect(self) -> pygame.Rect:
        """Return the collision rectangle for this entity."""
        return self._rect

    @property
    def health(self) -> int:
        """Return current health value."""
        return self.__health

    @property
    def is_alive(self) -> bool:
        """Return True if the entity still has health remaining."""
        return self.__health > 0

    def take_damage(self, amount: int) -> None:
        """Reduce health by a positive damage amount."""
        self.__health = max(0, self.__health - max(0, amount))

    def heal(self, amount: int) -> None:
        """Increase health by a positive amount up to max health."""
        self.__health = min(self._max_health, self.__health + max(0, amount))

    def _clamp_to_screen(self, screen_width: int, screen_height: int) -> None:
        """Keep the entity rectangle inside the screen boundaries."""
        self._rect.left = max(0, self._rect.left)
        self._rect.top = max(0, self._rect.top)
        self._rect.right = min(screen_width, self._rect.right)
        self._rect.bottom = min(screen_height, self._rect.bottom)
        self._x = float(self._rect.x)
        self._y = float(self._rect.y)

    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        """Update entity state each frame.

        Polymorphism: each subclass implements update differently.
        """

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the entity sprite onto the screen surface."""
        surface.blit(self._sprite, self._rect)
