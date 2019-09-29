from src.cards.exceptions import CardsAPIError
import uuid
from typing import List
from src.common.constants import PlayerHand


class Player:
    def __init__(self, name, wallet, uid=None):
        self.uuid: uuid.UUID = self.create_uuid(uid)
        # hands are list of Hand, money bet and if the hand is lock
        self.hands: List[PlayerHand] = [PlayerHand()]
        self.wallet: int = wallet
        self.name = name

    @staticmethod
    def create_uuid(uid):
        if uid is None:
            return uuid.uuid4()
        else:
            return uid

    def bet(self, amount, index_of_the_hand) -> bool:
        """
        Check wallet value and substract the amount or take all the wallet
        :return: boolean value :
                 - True : amount betted can be bet
                 - False : amount is too high bet only what left in the wallet
        """

        if amount <= self.wallet :
            # subtract amount from wallet and add it the the pot
            self.wallet -= amount
            # increasing the amount of money bet for this hand
            self.hands[index_of_the_hand].hand_bet += amount
            return True
        else:
            # amount is higher than wallet put wallet at zero and put it into
            # the money bet on hand
            self.hands[index_of_the_hand].hand_bet += self.wallet
            self.wallet = 0

        return False

    def check_split_is_possible(self, index_of_hand_to_split) -> bool:
        """
        Check if a split is possible according to the money bet on the hand and
        the value of the wallet.
        :return: boolean
           - True : split can be done
           - False: split can't be done
        """
        if (
                self.check_double_bet_is_possible(index_of_hand_to_split)
                and self.hands[index_of_hand_to_split].hand.checkSplitIsPossible()):
            return True

        return False

    def check_double_bet_is_possible(self, index_of_the_bet_to_double) -> bool:
        """
        Check if player can bet again what he has already bet on his hands
        :return: True if double is possible False if not
        """
        if self.hands[index_of_the_bet_to_double].hand_bet <= self.wallet:
            return True

        return False

    def double(self, index_of_the_hand_to_double):
        """
        Double the money spend by the player
        """
        if self.check_double_bet_is_possible(index_of_the_hand_to_double):
            # ---- Double the bet ----
            # 3 - lock the hand
            self.hands[index_of_the_hand_to_double].is_lock = True

            # 1 - removing the bet in the wallet
            self.wallet -= self.hands[index_of_the_hand_to_double].hand_bet

            # 2 - adding the new bet value
            self.hands[index_of_the_hand_to_double].hand_bet *= 2
        else:
            print("<class Player>[double] double bet on Player", self.uuid, "is impossible")

    def split(self, index_of_hand_to_split):
        """
        Check if the hand can be split if so it split it
        """

        if self.check_split_is_possible(index_of_hand_to_split):
            # if check is ok cards are good and wallet have enough money
            splitted_hand = self.hands[index_of_hand_to_split].hand.split()
            bet_of_the_hand = self.hands[index_of_hand_to_split].hand_bet

            # remove bet of the second hand just created
            self.wallet -= bet_of_the_hand

            if len(splitted_hand) == 2:
                # ---- Creating the new hands ---
                # 1 - reinitialize hands of the player
                self.clear_hands()
                self.hands.pop()

                # 2 - adding first hand with the associated bet
                self.hands.append(PlayerHand(splitted_hand[0],
                                             bet_of_the_hand, False))

                # 3 - adding second hand with it associated bet
                self.hands.append(PlayerHand(splitted_hand[1],
                                             bet_of_the_hand, False))
            else:
                raise CardsAPIError(
                    f"Split does not return exactly two hands for "
                    f"Player: {self!r}"
                )

    def add_card(self, card_to_add, index_of_the_hand_to_change):
        self.hands[index_of_the_hand_to_change].hand += card_to_add

    def clear_hands(self):
        self.hands = [PlayerHand()]

    def __repr__(self):
        return f"Player(name = {self.name}, uuid = {self.uuid},\n" \
            f"hands = {self.hands})"

    def __str__(self) -> str:
        return f"Player: {self.name}"
