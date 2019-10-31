class Enum:
    """
    A C++ like enum

    :param args: a list of strings

    :Example:

        enum = Enum(
            "splash",
            "mainMenu",
            "quit"
        )

        state = enum.splash

        if state == enum.splash:
            state = enum.mainMenu
        else:
            state = enum.quit

        enum.print(state)
    """

    def __init__(self, *args):

        self.__i = 0
        self.__names = args

        for name in args:
            setattr(self, name, self.__i)
            self.__i += 1

    def print(self, i: int, **kwargs):
        """
        Print the name of the enum

        :param i: the value of the Enum
        :param kwargs: the common keyword arguments for the print function
        """

        print(self.__names[i], **kwargs)
