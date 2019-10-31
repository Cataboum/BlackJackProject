import pygame


class Star(pygame.sprite.Sprite):
    """
    A shooting star

    kwargs is used to define where the rect is placed
    """

    speed = 2
    images = list()
    screenRect = None

    def __init__(self, **kwargs):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.image = self.images[0]
        self.rect = self.image.get_rect(**kwargs)

    def update(self):
        """
        Update the star at each iteration
        """

        self.rect.move_ip(self.speed, 0)
        if not self.screenRect.contains(self.rect):
            self.kill()
