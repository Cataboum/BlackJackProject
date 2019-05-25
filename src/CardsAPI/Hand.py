from .Card import Card
from typing import List, Tuple


class Hand(object):
    def __init__(self, card_list: List[Card]=None, is_dealer_hand: bool=False,
                 isSplit: bool = False):
        if card_list is None:
            card_list = []
        self.card_list = card_list
        self.is_split = isSplit
        self.is_dealer_hand = is_dealer_hand

    @property
    def value(self) -> int:
        # without this sort, aces are always counted as 11
        sorted_card_list = sorted(self.card_list, key=lambda x: x.value,
                                  reverse=True)
        return sum(sorted_card_list)

    @property
    def is_black_jack(self) -> bool:
        hand_sum = sum(self.card_list)
        if hand_sum == 21 and len(self.card_list) == 2 and not self.is_split:
            return True
        else:
            return False

    @property
    def is_burnt(self) -> bool:
        # without this sort, aces are always counted as 11
        sorted_card_list = sorted(self.card_list, key=lambda x: x.value,
                                  reverse=True)
        hand_sum = sum(sorted_card_list)
        if hand_sum > 21:
            return True
        else:
            return False

    def checkSplitIsPossible(self):
        """
        Check if the card are the same
        :return: True is split can be done False otherwise
        """
        if len(self.card_list) == 2 and \
           self.card_list[0].value == self.card_list[1].value:
           return True
        return False

    def split(self) -> Tuple['Hand', 'Hand']:
        """
        Performs a split action. Returns two instances of Hand.
        The methods checks for number of cards in the original Hand (which
        should be 2) and for equality of the two cards' values
        :return: The two resulting hands in a tuple
        :raise: AssertionError
        """
        if len(self.card_list) == 2 and \
           self.card_list[0].value == self.card_list[1].value:
            return (self.__class__([self.card_list[0]], isSplit=True),
                    self.__class__([self.card_list[1]], isSplit=True))
        return [None, None]

    """
    The following are comparison methods for comparing Hand objects. All
    standard comparison operators are defined and take into account the fact
    that a Hand can be a blackjack or not and that it can belong to the
    dealer or not
    """
    def __gt__(self, other: 'Hand') -> bool:
        if not isinstance(other, Hand):
            return NotImplemented
        if self.is_black_jack and not other.is_black_jack:
            return True
        elif other.is_burnt and not self.is_burnt:
            return True
        elif self.is_burnt and other.is_burnt and self.is_dealer_hand:
            return True
        elif self.value > other.value and not self.is_burnt:
            return True
        else:
            return False

    def __lt__(self, other: 'Hand') -> bool:
        if not isinstance(other, Hand):
            return NotImplemented
        return not self.__gt__(other) and not self.__eq__(other)

    def __eq__(self, other: 'Hand') -> bool:
        if not isinstance(other, Hand):
            return NotImplemented
        if self.is_black_jack and other.is_black_jack:
            return True
        elif self.is_burnt and other.is_burnt and not self.is_dealer_hand \
                and not other.is_dealer_hand:
            return True
        elif self.value == other.value and not \
                self.is_black_jack and not other.is_black_jack:
            return True
        else:
            return False

    def __ge__(self, other: 'Hand') -> bool:
        if not isinstance(other, Hand):
            return NotImplemented
        return not self.__lt__(other)

    def __le__(self, other: 'Hand') -> bool:
        if not isinstance(other, Hand):
            return NotImplemented
        return not self.__gt__(other)

    def __ne__(self, other: 'Hand') -> bool:
        if not isinstance(other, Hand):
            return NotImplemented
        return not self.__eq__(other)

    def __add__(self, card: Card) -> 'Hand':
        """
        Adds a card to the Hand, using "hand = hand + card" or "hand += card"
        :param card: a Card object to append to the Hand's card_list
        :return: The Hand itself
        """
        if not isinstance(card, Card):
            return NotImplemented
        self.card_list.append(card)
        return self

    def __repr__(self) -> str:
        return "Hand(card_list={}, is_dealer_hand={})".format(
            self.card_list, self.is_dealer_hand
        )

    def __str__(self) -> str:
        if self.is_dealer_hand:
            owner = "Dealer"
        else:
            owner = "Player"
        return "{} Hand : {}".format(owner, self.card_list)
