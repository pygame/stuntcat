"""
Scenes module.
"""

from stuntcat.scenes.scene import Scene
from .gameover import GameOverScene
from .loading import LoadingScene
from .news import NewsScene
from .settings import SettingsScene
from .unisharklazer import CatUniScene
from .platformer.platformer import PlatformerScene

__all__ = [
    "Scene",
    "GameOverScene",
    "LoadingScene",
    "NewsScene",
    "SettingsScene",
    "CatUniScene",
    "PlatformerScene",
]
