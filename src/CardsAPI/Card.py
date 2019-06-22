import re
from typing import Union, Pattern

card_names_and_values = {
    ("ACE", 1),
    ("TWO", 2),
    ("THREE", 3),
    ("FOUR", 4),
    ("FIVE", 5),
    ("SIX", 6),
    ("SEVEN", 7),
    ("EIGHT", 8),
    ("NINE", 9),
    ("TEN", 10),
    ("JACK", 11),
    ("QUEEN", 12),
    ("KING", 13),
}

card_to_value_dict = {
    key: min(10, value) for (key, value) in card_names_and_values
}
value_to_card_dict = {key: value for (value, key) in card_names_and_values}

colors = {"HEARTS", "SPADES", "CLUBS", "DIAMONDS"}


class Card(object):
    def __init__(self, value: Union[int, str], color: str = "hearts"):
        self._value = None
        self._color = None
        self.name = None

        # Calls color.setter
        self.color = color

        # Calls value.setter
        self.value = value
        try:
            self.value = value
        except KeyError:
            raise ValueError(
                "First argument 'value' should be a card name "
                "or integer between 1 and 13"
            )

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, color: str = "HEARTS"):
        color = color.upper()
        for c in colors:
            regexp = self.cardColorToRegexp(c).match(color)
            if regexp is None:
                # regexp.match returns None if nothing is matched,
                # which will raise a error if end method is used on the
                # matching result
                continue
            if regexp.end() == len(color):
                self._color = c
                break
        else:
            raise ValueError(
                'Invalid value for Card object\'s "color" member.\n'
                'Value should be either "HEARTS", "DIAMONDS", "CLUBS", '
                '"SPADES", their singular variant, or their first letter.\n'
                "Case is not relevant."
            )

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, arg):
        if isinstance(arg, str):
            self.name = arg.upper()
        elif isinstance(arg, int):
            self.name = value_to_card_dict[arg]
        self._value = card_to_value_dict[self.name]

    def __radd__(self, other: Union["Card", int]) -> int:
        if self.name == "ACE":
            if self._value + other <= 11:
                return self._value + other + 10
        return self._value + other

    def __add__(self, other: Union["Card", int]) -> int:
        if self.name == "ACE":
            if self._value + other <= 11:
                return self._value + other + 10
        return self._value + other

    def __int__(self) -> int:
        return self._value

    def __repr__(self) -> str:
        return "Card(value = %d, name = %s, color = %s)" % (
            self._value,
            self.name,
            self.color,
        )

    def __str__(self) -> str:
        return "%s of %s" % (self.name, self.color)

    @staticmethod
    def cardColorToRegexp(string: str) -> Pattern[str]:
        """
        Creates a regular expression to match user inputs for color parameter
        For example, replace "HEARTS" by "H(EART(S)?)?"
        Allows matching "H",  "HEART" and "HEARTS"
        :param str string: String to be changed to regular expression
        :return: a regular expression
        :rtype: Pattern[str]
        """
        string = string[0] + "(" + string[1:-1] + "(" + string[-1] + ")?)?"
        return re.compile(string)
