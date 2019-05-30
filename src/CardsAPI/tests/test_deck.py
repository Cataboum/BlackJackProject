from src.CardsAPI import Deck,Card


def test_init_deck():

    deck = Deck.Deck()
    assert deck.top_card_index == 0
    assert len(deck.cards) == 312
    # Check placement of the red Card
    assert ((3 / 4) * 312) - 30 <= deck.red_card_index <= ((3 / 4) * 312) + 30

    # Assert not shuffle
    deck = Deck.Deck(False)
    assert deck.top_card_index == 0
    assert len(deck.cards) == 312
    assert ((3 / 4) * 312) - 30 <= deck.red_card_index <= ((3 / 4) * 312) + 30


def test_deal_deck():

    deck = Deck.Deck()
    card = deck.getCard()
    assert type(card) == Card.Card
    assert deck.top_card_index == 1


def test_red_card_deck():

    deck = Deck.Deck()
    last_card = deck.cards[-1]
    deck.getCard()
    assert last_card == deck.cards[-1]

    for i in range(int(((3 / 4) * 312) + 35)):
        deck.getCard()

    assert deck.cards[-1] != last_card


def test_shuffle_deck():

    deck = Deck.Deck()
    try:
        for i in range(500):
            card = deck.getCard()
    except IndexError:
        assert True
    else:
        # This shouldn't work because the Deck is only 312 cards long
        assert False

    deck = Deck.Deck()

    for i in range(deck.red_card_index):
        assert not deck.needs_shuffling
        deck.getCard()

    assert deck.needs_shuffling

    deck.shuffle()

    assert not deck.needs_shuffling

    try:
        # This won't work if the deck has not been shuffled
        for i in range(
                (len(deck.cards) - deck.red_card_index) + 1
        ):
            deck.getCard()
    except IndexError:
        assert False


def test_init_shuffle_deck():

    deck1 = Deck.Deck(False)
    deck2 = Deck.Deck(False)
    assert deck1.cards[0] == deck2.cards[0]
