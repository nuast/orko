"""Core game manager and loop support for the dungeon crawler."""

from __future__ import annotations

import pygame

from enemy import Enemy
from player import Player
from settings import BACKGROUND_COLOR, FPS, SCREEN_HEIGHT, SCREEN_WIDTH, TEXT_COLOR


class Game:
    """Manages setup, update, and drawing of the game.

    Abstraction: this class gives main.py a simple interface (run).
    """

    def __init__(self) -> None:
        """Initialise pygame systems and game objects."""
        pygame.init()
        self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Retro Dungeon Crawler")
        self._clock = pygame.time.Clock()
        self._font = pygame.font.Font(None, 28)

        self._player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self._enemies = [Enemy(80, 80), Enemy(680, 500)]
        self._running = True

    def _handle_events(self) -> None:
        """Handle window and keyboard events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self._player.cast_spell(self._enemies)

    def _update(self) -> None:
        """Update all entities for the current frame."""
        keys = pygame.key.get_pressed()
        self._player.update(keys, self._enemies)

        for enemy in self._enemies:
            enemy.update(self._player)
            if enemy.is_alive and enemy.rect.colliderect(self._player.rect):
                self._player.take_damage(1)

        if not self._player.is_alive:
            self._running = False

    def _draw_ui(self) -> None:
        """Draw simple health and mana text."""
        health_text = self._font.render(f"Health: {self._player.health}", True, TEXT_COLOR)
        mana_text = self._font.render(f"Mana: {self._player.mana}", True, TEXT_COLOR)
        spell_text = self._font.render("Space: cast spell", True, TEXT_COLOR)

        self._screen.blit(health_text, (10, 10))
        self._screen.blit(mana_text, (10, 35))
        self._screen.blit(spell_text, (10, 60))

    def _draw(self) -> None:
        """Render all game visuals."""
        self._screen.fill(BACKGROUND_COLOR)

        self._player.draw(self._screen)
        for enemy in self._enemies:
            enemy.draw(self._screen)

        self._draw_ui()
        pygame.display.flip()

    def run(self) -> None:
        """Run the main game loop until the game ends."""
        while self._running:
            self._handle_events()
            self._update()
            self._draw()
            self._clock.tick(FPS)

        pygame.quit()
