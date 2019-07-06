from src.CardsAPI.Hand import Hand
from src.CardsAPI.Deck import Deck
from src.common.constants import Decision


class Dealer:
    def __init__(self):
        self.hand = Hand()
        self.name = "Hackiflette God"

    def chooseAction(self, mode=0) -> Decision:
        """
        Function to choose action, Hit or Stand, depending on the dealer's
        hand value. Usually 2 rules can be chosen regarding the dealer's
        decision making:
        - mode 0: dealer stands on all 17s and above (and hits below)
        - mode 1: dealer hits on soft 17 and below (and stands on hard 17 and
            above)
        :return: decision
        """
        if mode == 0:
            if self.hand.value < 17:  # Dealer stands on all 17s
                return Decision.hit

        elif mode == 1:
            if self.hand.value < 17:  # Dealer hits on soft 17
                return Decision.hit
            elif self.hand.value == 17:
                card_list = self.hand.card_list
                raw_sum = sum((card.value for card in card_list))
                if raw_sum != 17:
                    # if the raw sum (calculated without taking into account
                    # that an ace can count as 11) is not 17 (then it would
                    # be 7), we have a soft 17, thus we hit
                    return Decision.hit
        else:
            raise ValueError("'mode' parameter of class Dealer's "
                             "'chooseAction' method should be 0 or 1")
        return Decision.stand
