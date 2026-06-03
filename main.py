"""Entry point for the retro dungeon crawler project."""

from game import Game


def main() -> None:
    """Create and run the game manager."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
