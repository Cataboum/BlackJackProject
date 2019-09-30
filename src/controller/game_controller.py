from src.views.view_game import ViewGame
from src.humans.dealer import Dealer
from src.humans.player import Player
from src.cards.deck import Deck
from src.common.constants import Decision

import pygame
from pygame.locals import (
    QUIT,
    KEYDOWN,
    K_ESCAPE,
    K_1,
    K_2,
    K_3,
    K_4,
    K_5,
    K_6,
    K_KP1,
    K_KP2,
    K_KP3,
    K_KP4,
    K_KP5,
    K_KP6,
)


class GameController:
    """
    A controller for all the game
    """
    def __init__(self, window):
        print("Enter in controller")
        self.window = window
        self.humans_list = []
        self.dealer = Dealer()
        self.view_game = None
        self.player_wallet = 500
        self.deck = Deck()
        # For loops purpose
        self.state = False
        self.human = None
        self.hand_idx = None
        # self.view_game = View_game(window, view_config)

    def game_launch(self):
        self.view_game = ViewGame(self.window)
        self.view_game.buttons["card"].signal.attach(self.btn_card)
        self.view_game.buttons["bet"].signal.attach(self.btn_bet)
        self.view_game.buttons["end_turn"].signal.attach(self.btn_end_turn)
        self.view_game.buttons["split"].signal.attach(self.btn_split)
        self.view_game.buttons["double"].signal.attach(self.btn_double)
        self.view_game.buttons["quit"].signal.attach(self.btn_quit)

    def initiate_players(self):
        """
        ask the player(s) how many they are and their name(s)

        :return: bool initialisation is done and OK
        """
        # ask the view to open a new window and ask the number of player
        number_of_player = 1

        for _ in range(number_of_player):
            # ask the name of the player and create the Player
            name_of_player = "Jesus"
            self.add_human(Player(name_of_player, self.player_wallet))

    def refresh(self):
        self.view_game.refresh()

    def add_human(self, human) -> bool:
        """
        Adding one player into the list of humans to handle at each round

        :param human: Player to add
        :type arg1: Player
        """
        if isinstance(human, Player):
            self.humans_list.append(human)
            return True
        else:
            # Given human isn't a player
            return False

    def remove_player(self, player_uuid) -> bool:
        """
        Removing one player

        :param player_uuid: Player's id to remove
        :type arg1: Player
        """
        if len(self.humans_list) > 2:
            for i in range(len(self.humans_list[:-1])):
                if self.humans_list[i].uuid == player_uuid :
                    self.humans_list = self.humans_list[:i] + self.humans_list[i+1:]
                    return True
        else:
            # No player to remove, player list is empty
            return False
        # Id not found
        return False

    def reset_all_humans(self):
        """Resetting all humans : no more player and new dealer"""
        self.humans_list = []
        self.dealer = Dealer()

    def first_round(self):
        """
        First round allow the players to bet them deal the card for everybody
        :return: bool : state of the round
        """

        for human in self.humans_list:
            human.clear_hands()
        self.dealer.clear_hand()

        # loop only for betting. Betting buttons should be the only one modifiable
        for human in self.humans_list:
            print(human.name + " is betting.")
            state = True
            while state:
                event = pygame.event.wait()
                if event.type == QUIT:
                    return False
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    return False
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if self.view_game.buttons["quit"].collide(pos):
                        return False
                else:
                    print(human.name + " is betting")
                    state = False
                for btn in self.view_game.buttons.values():
                    btn.handle_event(event)

        # loop to deal hands to everybody
        for human in self.humans_list:
            print(human.name + "is receiving cards.")
            # at initialization we only change the first hand of the player with 2 cards
            human.add_card(self.deck.getCard(), 0)
            human.add_card(self.deck.getCard(), 0)

        # giving the dealer a hand (with 2 card)
        self.dealer.add_card(self.deck.getCard())
        self.dealer.add_card(self.deck.getCard())

    def play_one_round(self):
        for self.human in self.humans_list:
            print(str(self.human) + " round")
            for self.hand_idx in range(len(self.human.hands)):
                print("Hand %i" % self.hand_idx)
                print(self.human.name + " is playing.")
                # Get list of possible actions
                # Manage interfaces
                # Let human choose
                self.state = True
                while self.state:
                    event = pygame.event.wait()
                    if event.type == QUIT:
                        return False
                    elif event.type == KEYDOWN :
                        if event.key == K_ESCAPE:
                            return False

                        elif event.key in [K_1, K_KP1]:
                            self.view_game.buttons["card"].execute()
                        elif event.key in [K_2, K_KP2]:
                            self.view_game.buttons["bet"].execute()
                        elif event.key in [K_3, K_KP3]:
                            self.view_game.buttons["end_turn"].execute()
                        elif event.key in [K_4, K_KP4]:
                            self.view_game.buttons["split"].execute()
                        elif event.key in [K_5, K_KP5]:
                            self.view_game.buttons["double"].execute()
                        elif event.key in [K_6, K_KP6]:
                            self.view_game.buttons["quit"].execute()
                            # TODO: find a way to use the button instead of the return
                            return False

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if self.view_game.buttons["quit"].collide(pos):
                            return False
                    
                    for btn in self.view_game.buttons.values():
                        btn.handle_event(event)

        dealer_decision = self.dealer.choose_action()
        print("Dealer hand : " + str(self.dealer.hand))

        while dealer_decision != Decision.stand:
            print(dealer_decision)
            if dealer_decision == Decision.hit:
                self.dealer.add_card(self.deck.getCard())
            print("Dealer hand : " + str(self.dealer.hand))
            dealer_decision = self.dealer.choose_action()

        print("Dealer decision : " + str(dealer_decision))

        # Win of loose ?
        if self.dealer.hand.is_burnt:
            print("Everyone win !")
        else:
            for human in self.humans_list:
                for hand in human.hands:
                    if hand.hand.is_burnt:
                        print("Player %s loose with hand %s." % (human, str(hand)))
                    elif hand.hand > self.dealer.hand:
                        print("Player %s win with hand %s." % (human, str(hand)))
                    elif hand.hand == self.dealer.hand:
                        print("Player %s with hand %s is even with the dealer." % (human, str(hand)))

        return True
    
    # =========================================================================
    # = Buttons
    # =========================================================================

    def btn_card(self):
        """
        Manage actions on card button
        """

        card = self.deck.getCard()
        self.human.add_card(card, self.hand_idx)
        print("You : " + str(self.human.hands[self.hand_idx].hand))
        if self.human.hands[self.hand_idx].hand.is_burnt or self.human.hands[self.hand_idx].hand.is_black_jack:
            print("Is burnt or black jack")
            self.state = False

        print("btn_card")
        self.view_game.buttons["card"].set(state="disabled")
        self.view_game.buttons["card"].draw()

    def btn_bet(self):
        """
        Manage actions on bet button
        """

        bet_amount = 5
        hand_id = 0
        if len(self.human.hands) >= 2:
            print("You have %i hands" % len(self.human.hands))
            hand_id = input("Hand number for bet : ")
        self.human.bet(int(bet_amount), int(hand_id))

        print("btn_bet")

    def btn_end_turn(self):
        """
        Manage actions on end turn button
        """

        self.state = False

        print("btn_end_turn")

    def btn_split(self):
        """
        Manage actions on split button
        """

        hand_id = 0
        if len(self.human.hands) >= 2:
            print("You have %i hands" % len(self.human.hands))
            hand_id = input("Hand number for bet : ")
        self.human.split(hand_id)

        print("btn_split")

    def btn_double(self):
        """
        Manage actions on double button
        """

        self.human.double(0)

        print("btn_double")

    def btn_quit(self):
        """
        Manage quit on quit button
        """

        print("btn_quit")
