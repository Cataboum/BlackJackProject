from src.views.view_game import ViewGame
from src.humans.dealer import Dealer
from src.humans.player import Player
from src.cards.deck import Deck

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
        # self.view_game = View_game(window, view_config)

    def gameLaunch(self):
        self.view_game = ViewGame(self.window)

    def initiatePlayers(self):
        """
        ask the player(s) how many they are and their name(s)

        :return: bool initialisation is done and OK
        """
        # ask the view to open a new window and ask the number of player
        number_of_player = 1

        for i in range(number_of_player):
            #ask the name of the player and create the Player
            name_of_player = "Jesus"
            self.addHuman(Player(name_of_player, self.player_wallet))

    def refresh(self):
        self.view_game.refresh()

    def addHuman(self, human) -> bool:
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

    def removePlayer(self, player_uuid) -> bool:
        """
        Removing one player

        :param human: Player's id to remove
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

    def resetAllHumans(self):
        """Resetting all humans : no more player and new dealer"""
        self.humans_list = []
        self.dealer = Dealer()

    def firstRound(self):
        """
        First round allow the players to bet them deal the card for everybody
        :return: bool : state of the round
        """

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
                    if self.view_game.quit_btn.isClicked(pos):
                        return False
                else:
                    print(human.name + " is betting")
                    state = False

        #loop to deal hands to everybody
        for human in self.humans_list:
            print(human.name + "is receiving cards.")
            # at initialization we only change the first hand of the player with 2 cards
            human.addCard(self.deck.getCard(), 0)
            human.addCard(self.deck.getCard(), 0)

        #giving the dealer a hand (with 2 card)
        self.dealer.addCard(self.deck.getCard())
        self.dealer.addCard(self.deck.getCard())


    def playOneRound(self):
        for human in self.humans_list:
            for hand_idx in range(len(human.hands)):
                print(human.name + " is playing.")
                # Get list of possible actions
                # Manage interfaces
                # Let human choose
                state = True
                while state:
                    event = pygame.event.wait()
                    if event.type == QUIT:
                        return False

                    elif event.type == KEYDOWN :
                        if event.key == K_ESCAPE:
                            return False

                        elif event.key in [K_1, K_KP1] :
                            print(1)
                            card = self.deck.getCard()
                            human.addCard(card, hand_idx)
                            print("You : " + str(human.hands[hand_idx].hand))
                            if human.hands[hand_idx].hand.is_burnt or human.hands[hand_idx].hand.is_black_jack:
                                state = False

                        elif event.key in [K_2, K_KP2] :
                            print(2)
                            bet_amount = 5
                            hand_id = 0
                            if len(human.hands) >= 2:
                                print("You have " + len(human.hands) + "hands")
                                hand_id = input("Hand number for bet : ")
                            human.bet(int(bet_amount), int(hand_id))

                        elif event.key in [K_3, K_KP3] :
                            print(3)
                            state = False

                        elif event.key in [K_4, K_KP4] :
                            print(4)
                            hand_id = 0
                            if len(human.hands)>=2:
                                print("You have " + len(human.hands) + "hands")
                                hand_id = input("Hand number for bet : ")
                            human.split(hand_id)

                        elif event.key in [K_5, K_KP5] :
                            print(5)
                            human.double(0)

                        elif event.key in [K_6, K_KP6] :
                            return False

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        if self.view_game.quit_btn.isClicked(pos):
                            return False

        dealer_decision = self.dealer.chooseAction()
        # TODO: use dealer_decision if result is hit
        return True
