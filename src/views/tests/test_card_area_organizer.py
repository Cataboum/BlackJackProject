from src.cards.card import Card
from src.common.game_view_config import game_view_config
from src.views.card_area_organizer import CardAreaOrganizer

# override method so we don't have to initialize a pygame window
CardAreaOrganizer._create_card_tile = lambda _, __: None


class SignalTriggerCounter:
    signal_trigger_count = 0

    def signal_triggered(self):
        self.signal_trigger_count += 1


def test_dealer_cards():
    card_1 = Card(1)
    card_2 = Card(2)
    dealer_card_area_config = game_view_config.card_areas.dealer
    extra_card_offset = game_view_config.card_areas.extra_card_offset

    signal_triggered = SignalTriggerCounter()

    organizer = CardAreaOrganizer()
    organizer.areas_updated.attach(signal_triggered.signal_triggered)

    assert not organizer.dealer_area

    organizer.add_card(card_1, "dealer")

    assert signal_triggered.signal_trigger_count == 1
    assert len(organizer.dealer_area) == 1
    assert organizer.dealer_area[0].position.as_tuple == (
        dealer_card_area_config.x,
        dealer_card_area_config.y,
    )

    organizer.add_card(card_2, "dealer")

    # Check signal trigger
    assert signal_triggered.signal_trigger_count == 2

    assert len(organizer.dealer_area) == 2

    # Check if adding new card didn't change first card position
    assert organizer.dealer_area[0].position.as_tuple == (
        dealer_card_area_config.x,
        dealer_card_area_config.y,
    )

    # Checking new card position, with offset
    assert organizer.dealer_area[1].position.as_tuple == (
        dealer_card_area_config.x + extra_card_offset.x,
        dealer_card_area_config.y + extra_card_offset.y,
    )


def test_player_cards_single_hand():
    card_1 = Card(1)
    card_2 = Card(2)
    player_card_area_config = game_view_config.card_areas.player
    extra_card_offset = game_view_config.card_areas.extra_card_offset

    signal_triggered = SignalTriggerCounter()

    organizer = CardAreaOrganizer()
    organizer.areas_updated.attach(signal_triggered.signal_triggered)

    assert not organizer.player_areas

    organizer.add_card(card_1, "player", 0)

    assert signal_triggered.signal_trigger_count == 1
    assert len(organizer.player_areas) == 1
    assert len(organizer.player_areas[0]) == 1
    assert organizer.player_areas[0][0].position.as_tuple == (
        player_card_area_config.x + player_card_area_config.width / 2,
        player_card_area_config.y,
    )

    organizer.add_card(card_2, "player", 0)

    # Check signal trigger
    assert signal_triggered.signal_trigger_count == 2

    assert len(organizer.player_areas) == 1
    assert len(organizer.player_areas[0]) == 2

    # Check if adding new card didn't change first card position
    assert organizer.player_areas[0][0].position.as_tuple == (
        player_card_area_config.x + player_card_area_config.width / 2,
        player_card_area_config.y,
    )

    # Checking new card position, with offset
    assert organizer.player_areas[0][1].position.as_tuple == (
        player_card_area_config.x
        + player_card_area_config.width / 2
        + extra_card_offset.x,
        player_card_area_config.y + extra_card_offset.y,
    )


def test_player_cards_multi_hand():
    card_1 = Card(1)
    card_2 = Card(2)
    player_card_area_config = game_view_config.card_areas.player

    signal_triggered = SignalTriggerCounter()

    organizer = CardAreaOrganizer()
    organizer.areas_updated.attach(signal_triggered.signal_triggered)

    organizer.add_card(card_1, "player", 0)
    organizer.add_card(card_2, "player", 1)

    # Check signal trigger
    assert signal_triggered.signal_trigger_count == 2

    assert len(organizer.player_areas) == 2
    assert len(organizer.player_areas[0]) == 1
    assert len(organizer.player_areas[1]) == 1

    # Check the old card's position (it should have changed)
    assert organizer.player_areas[0][0].position.as_tuple == (
        round(player_card_area_config.x
              + player_card_area_config.width / 3),
        player_card_area_config.y,
    )

    # Checking new card position
    assert organizer.player_areas[1][0].position.as_tuple == (
        round(player_card_area_config.x
              + 2 * player_card_area_config.width / 3),
        player_card_area_config.y,
    )


def test_player_cards_split():
    card_1 = Card("QUEEN")
    card_2 = Card("KING")
    card_3 = Card(1)
    player_card_area_config = game_view_config.card_areas.player

    signal_triggered = SignalTriggerCounter()

    organizer = CardAreaOrganizer()
    organizer.areas_updated.attach(signal_triggered.signal_triggered)

    organizer.add_card(card_1, "player", 0)
    organizer.add_card(card_2, "player", 0)
    organizer.add_card(card_3, "player", 1)
    organizer.split_hand(0)

    assert len(organizer.player_areas) == 3
    assert len(organizer.player_areas[0]) == 1
    assert len(organizer.player_areas[1]) == 1
    assert len(organizer.player_areas[2]) == 1
    assert organizer.player_areas[0][0].position.as_tuple == (
        round(player_card_area_config.x + player_card_area_config.width / 4),
        player_card_area_config.y,
    )
    assert organizer.player_areas[1][0].position.as_tuple == (
        round(player_card_area_config.x
              + 2 * player_card_area_config.width / 4),
        player_card_area_config.y,
    )
    assert organizer.player_areas[2][0].position.as_tuple == (
        round(player_card_area_config.x
              + 3 * player_card_area_config.width / 4),
        player_card_area_config.y,
    )

    # Check signal trigger
    assert signal_triggered.signal_trigger_count == 4


def test_clear_areas():
    card_1 = Card(1)
    card_2 = Card(2)

    signal_triggered = SignalTriggerCounter()

    organizer = CardAreaOrganizer()
    organizer.areas_updated.attach(signal_triggered.signal_triggered)

    organizer.add_card(card_1, "dealer")
    organizer.add_card(card_2, "player", 0)
    organizer.clear_areas()

    assert signal_triggered.signal_trigger_count == 3
    assert len(organizer.dealer_area) == 0
    assert len(organizer.player_areas) == 0
