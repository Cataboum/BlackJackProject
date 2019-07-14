from src.common.game_view_config import Coordinates
import pygame


class Signal:
    def __init__(self):
        self.__subscribers = []

    def emit(self, *args, **kwargs):
        for subscriber in self.__subscribers:
            subscriber(*args, **kwargs)

    def attach(self, subscriber):
        self.__subscribers.append(subscriber)

    def detach(self, subscriber):
        try:
            self.__subscribers.remove(subscriber)
        except ValueError:
            print('Warning: function %s not removed '
                  'from signal %s' % (subscriber, self))


class SurfaceWithPosition:
    def __init__(self, surface: pygame.Surface, position: Coordinates):
        self.surface = surface
        self.position = position
