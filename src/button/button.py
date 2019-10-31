import enum
import pygame

from src.common.utils import Signal


# ============================================================================
# =
# = Enum
# =
# ============================================================================


class State(enum.Enum):
    normal = enum.auto()
    hover = enum.auto()
    pressed = enum.auto()


# =============================================================================
# =
# = Button
# =
# =============================================================================


class Button:
    """
    Set attributes to the button

    :param pygame.Surface window: surface where to blit the button
    :param 3-tuple bg_normal: color for normal background
    :param 3-tuple bg_hover: color for background when hover
    :param 3-tuple bg_pressed: color for background when pressed
    :param int bd: border size
    :param 3-tuple bd_color: color for the border
    :param str text: text to display on button
    :param dict text_font: {file: font family, size: font size}
    :param 3-tuple text_color: color for the text
    """

    def __init__(self, window: pygame.Surface=None, **kwargs):
        # Set attributes
        self.window = window
        self.state = State.normal
        self.enabled = True
        # Rectangle
        self.rect = pygame.Rect(0, 0, 100, 80)
        # Background
        self.bg = None
        self.bg_normal = None
        self.bg_hover = None
        self.bg_pressed = None
        # Border
        self.bd = 0
        self.bd_color = (0, 0, 0)
        # Text
        self.text = "Button"
        self.text_font = {"file": None, "size": 30}
        self.text_color = (0, 0, 0)
        # command
        self.signal = Signal()

        self.__setKwargs(**kwargs)
        self.text_core = pygame.font.Font(None, 30)
    
    def __setKwargs(self, **kwargs):
        """
        Set attributes to the button

        :param 3-tuple bg_normal: color for normal background
        :param 3-tuple bg_hover: color for background when hover
        :param 3-tuple bg_pressed: color for background when pressed
        :param int bd: border size
        :param 3-tuple bd_color: color for the border
        :param str text: text to display on button
        :param dict text_font: {file: font family, size: font size}
        :param 3-tuple text_color: color for the text
        """

        # Validate kwargs
        attr = [
            "bg_normal", "bg_hover", "bg_pressed",
            "bd", "bd_color",
            "text", "text_font", "text_color",
            "pos", "size"
        ]
        for kwarg in kwargs:
            if kwarg not in attr:
                raise ValueError(f"{kwarg} is not a valid attribute")

        # If a parameter has changed
        # Update rect
        if "pos" in kwargs:
            self.rect.x, self.rect.y = kwargs.pop("pos")
        if "size" in kwargs:
            self.rect.w, self.rect.h = kwargs.pop("size")

        self.__dict__.update(**kwargs)
        # Update text_core
        if "text_font" in kwargs:
            self.text_core = pygame.font.Font(**self.text_font)
    
    # =========================================================================
    # = Events
    # =========================================================================
    
    def __on_clic_down(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(*pos):
            self.state = State.pressed
            self.draw()

    def __on_clic_up(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(*pos):
            self.state = State.hover
            self.signal.emit()
        else:
            self.state = State.normal
        self.draw()
    
    def __on_hover(self):
        pos = pygame.mouse.get_pos()
        changed = False
        # If on button
        if self.rect.collidepoint(*pos):
            if self.state == State.normal:
                self.state = State.hover
                changed = True
        else:
            if self.state == State.hover:
                self.state = State.normal
                changed = True

        if changed:
            self.draw()
    
    # =========================================================================
    # = Public methods
    # =========================================================================

    def execute(self, *args, **kwargs):
        """
        Emit the signals attached to this button if it's not disabled
        """

        if self.enabled:
            self.signal.emit(*args, **kwargs)

    def enable(self):
        """
        Enable the button.
        """

        self.enabled = True
        self.draw()
    
    def disable(self):
        """
        Disable the button.
        """

        self.enabled = False
        self.draw()

    def collide(self, pos):
        """
        Return True if the position is on the button
        """

        return self.rect.collidepoint(pos)

    def set(self, **kwargs):
        """
        Set attributes to the button

        :param 3-tuple bg_normal: color for normal background
        :param 3-tuple bg_hover: color for background when hover
        :param 3-tuple bg_pressed: color for background when pressed
        :param int bd: border size
        :param 3-tuple bd_color: color for the border
        :param str text: text to display on button
        :param dict text_font: {file: font family, size: font size}
        :param 3-tuple text_color: color for the text
        """

        self.__setKwargs(**kwargs)

    def handle_event(self, event):
        """
        Handle the events used by the button

        :param pygame.event event: event generated by pygame
        """

        if not self.enabled:
            return

        if event.type == pygame.MOUSEMOTION:
            self.__on_hover()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.__on_clic_down()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.__on_clic_up()

    def draw(self):
        """
        Draw the button on window
        """

        core_text = self.text_core.render(self.text, 2, self.text_color)

        x_b, y_b = self.rect.x, self.rect.y
        w_b, h_b = self.rect.width, self.rect.height
        w_t, h_t = core_text.get_size()
        mid_x = x_b + (w_b - w_t) // 2
        mid_y = y_b + (h_b - h_t) // 2

        self.bg = {
            State.normal: self.bg_normal,
            State.hover: self.bg_hover,
            State.pressed: self.bg_pressed
        }.get(self.state, None)

        if self.bg:
            pygame.draw.rect(self.window, self.bg, self.rect)

        if self.bd > 0:
            points = (
                (x_b, y_b),
                (x_b, y_b + h_b),
                (x_b + w_b, y_b + h_b),
                (x_b + w_b, y_b)
            )
            pygame.draw.lines(self.window, self.bd_color, True, points, self.bd)

        self.window.blit(core_text, (mid_x, mid_y))

        if not self.enabled:
            s = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
            s.fill((0, 0, 0, 128))
            self.window.blit(s, (self.rect.x, self.rect.y))
        
        pygame.display.update(self.rect)
