import pygame

# ============================================================================
# =
# = Button
# =
# ============================================================================


class Button:
    """
    A button to be displayed on screen

    :param pos: position of the button
    :type pos: 2-tuple
    :param width: width of the button
    :type width: int
    :param height: height of the button
    :type height: int
    :param text: text to display on the button
    :type text: str
    :param command: function to execute when clicked
    :type command: function
    :param state: ["disabled", "enabled"]
    :type state: str
    :param background: background of the Button
    :type background: 3-tuple
    :param color: text color
    :type color: 3-tuple
    :param border: border size
    :type border: int
    :param border_color: border color
    :type border_color: 3-tuple
    """

    def __init__(self, **kwargs):

        self.__validKwargs = {"pos", "width", "height", "text", "color", "background",
                              "command", "value", "state", "border", "border_color"}
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.text = "Button"
        self.color = (0, 0, 0)
        self.background = None
        self.command = self.__emptyFunc
        self.value = None
        self.state = "enabled"
        self.border = 0
        self.border_color = (0, 0, 0)
        self.__setFromKwargs(kwargs)

    def set(self, **kwargs):
        """
        Set the values

        :param pos: position of the button
        :type pos: 2-tuple
        :param width: width of the button
        :type width: int
        :param height: height of the button
        :type height: int
        :param text: text to display on the button
        :type text: str
        :param command: function to execute when clicked
        :type command: function
        :param state: ["disabled", "enabled"]
        :type state: str
        :param background: background of the Button
        :type background: 3-tuple
        """

        self.__setFromKwargs(kwargs)

    def execute(self):
        """
        Execute the command if it was given
        """

        if self.state == "enabled":
            self.command()

    def isClicked(self, pos):
        """
        Return True is the pos is in the Button
        """

        return self.rect.collidepoint(pos)

    def display(self, window):
        """
        Display the button on the window
        """

        core_font = pygame.font.Font(None, 30)
        core_text = core_font.render(self.text, 2, self.color)

        x_b, y_b = self.rect.x, self.rect.y
        w_b, h_b = self.rect.width, self.rect.height
        w_t, h_t = core_text.get_size()

        mid_x = x_b + (w_b - w_t) // 2
        mid_y = y_b + (h_b - h_t) // 2

        if self.background is not None:
            pygame.draw.rect(window, self.background, self.rect)

        if self.border > 0:
            points = (
                (x_b, y_b),
                (x_b, y_b + h_b),
                (x_b + w_b, y_b + h_b),
                (x_b + w_b, y_b)
            )
            pygame.draw.lines(window, self.border_color, True, points, self.border)

        window.blit(core_text, (mid_x, mid_y))

    def __setFromKwargs(self, kwargs: dict):
        """
        Set the values from the kwargs
        """

        self.__validateKwargs(kwargs.keys())

        if "pos" in kwargs:
            self.rect.x, self.rect.y = kwargs["pos"]

        if "width" in kwargs:
            self.rect.width = kwargs["width"]

        if "height" in kwargs:
            self.rect.height = kwargs["height"]

        if "text" in kwargs:
            self.text = kwargs["text"]

        if "color" in kwargs:
            self.color = kwargs["color"]

        if "background" in kwargs:
            self.background = kwargs["background"]

        if "command" in kwargs:
            self.command = kwargs["command"]
            self.state = "enabled"

        if "value" in kwargs:
            self.value = kwargs["value"]

        if "state" in kwargs:
            self.state = kwargs["state"]

        if "border" in kwargs:
            self.border = kwargs["border"]

        if "border_color" in kwargs:
            self.border_color = kwargs["border_color"]

    def __validateKwargs(self, kwargs: dict):
        """
        Parse all the kwargs and raise an error if one isn't correct
        """

        for key in kwargs:
            if key not in self.__validKwargs:
                err = "%s is not a valid argument : [%s]"
                args = ", ".join(self.__validKwargs)
                raise AttributeError(err % (key, args))

    def __emptyFunc(self):
        pass

    def __str__(self):
        """
        To print the caracteristics of the Button
        """

        txt = "Button:\n"
        txt += "- pos (%d, %d)\n" % (self.rect.x, self.rect.y)
        txt += "- width %d\n" % self.rect.width
        txt += "- height %d\n" % self.rect.height
        txt += "- text %s\n" % self.text

        return txt


if __name__ == '__main__':
    btn = Button(text="Ok")
    btn.set(pos=(200, 200), width=200, height=50, command=lambda: ...)
