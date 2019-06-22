import itertools
import random

from src.CardsAPI.Card import Card, card_to_value_dict, colors


class Deck:
    def __init__(self, SHUFFLE: bool = True):
        # boolean flag to tell the controller if the deck needs to be shuffled
        # should be checked at the end of every turn by the controller
        self.needs_shuffling = False

        self.cards = (
            list(itertools.product(card_to_value_dict.keys(), colors)) * 6
        )

        if SHUFFLE:
            self.shuffle()

        # index of the card on the top of the deck
        self.top_card_index = 0

        # index of the red card, when the dealer finds this card, he shuffles
        # the deck. Usually placed around 3/4 of the deck
        # self.needs_shuffling is set to True when this index is reached
        self.red_card_index = self.computeRedCardIndex(len(self.cards))

    def shuffle(self):
        # shuffle deck
        random.shuffle(self.cards)
        # reset counter
        self.top_card_index = 0
        # recalculate red card index, not really necessary but more realistic
        self.red_card_index = self.computeRedCardIndex(len(self.cards))
        # reset shuffling flag to False
        self.needs_shuffling = False

    def getCard(self) -> Card:
        self.top_card_index += 1
        if self.top_card_index == self.red_card_index:
            # The deck needs to be shuffled
            self.needs_shuffling = True

        return Card(*self.cards[self.top_card_index])

    @staticmethod
    def computeRedCardIndex(deck_length):
        """
        Utility function to choose a random index at 3/4th of the deck's
        length += 30
        :param deck_length:
        :return: red card index
        """
        return random.randint(
            (3 / 4) * deck_length - 30, (3 / 4) * deck_length + 30
        )
