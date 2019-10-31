from src.cards.hand import Hand
from src.cards.card import Card

# To launch test in console :
# ... $ python -m pytest tests/
from src.cards.exceptions import CardsAPIError


def test_init_hand():

    hand = Hand()
    assert len(hand.card_list) == 0

    hand = Hand([Card(2)])
    assert hand.value == 2


def test_add_card():

    hand = Hand()
    card = Card(2)
    hand = hand + card
    card = Card(5)
    hand = hand + card
    assert len(hand.card_list) == 2
    assert hand.value == 7


def test_iadd_card():

    hand = Hand([Card(5)])
    hand_list = [hand]
    hand += Card(2)
    assert len(hand_list[0].card_list) == 2
    assert hand_list[0].value == 7


def test_comparison_hand():

    hand_1 = Hand([Card(5),
                   Card(7)])
    hand_2 = Hand([Card(3)])
    assert hand_1 > hand_2


def test_split_hand():

    hand = Hand([Card(3, 'heart'),
                 Card(3, 'spades')])
    [hand_1, hand_2] = hand.split()
    assert hand_1.value == 3 and hand_2.value == 3
    assert hand_1 == hand_2

    hand2 = Hand([Card(3), Card(4)])
    try:
        hand2.split()
    except CardsAPIError:
        assert True
    else:
        assert False

    # testing too many cards in hand
    hand += Card(3)
    try:
        hand.split()
    except CardsAPIError:
        assert True
    else:
        assert False
