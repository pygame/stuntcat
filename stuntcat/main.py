"""
Main module
"""
from stuntcat.game import Game


def main():
    """
    Main function.
    """
    try:
        game_main()
    except KeyboardInterrupt:
        print("Keyboard Interrupt...")
        print("Exiting")


def game_main():
    """
    Game main function.
    """
    Game().mainloop()
