
import src.common.constants as cst
from src.views.view_game import View_game
from src.humans.Dealer import Dealer
from src.humans.Player import Player

import pygame
from pygame.locals import (
    QUIT,
    KEYDOWN,
    K_ESCAPE,
)
class Game_controller:
    """
    A controller for all the game
    """
    def __init__(self, window, view_config):

        print("Enter in controller")
        self.window = window
        self.view_config = view_config
        self.humans_list = [Dealer()]
        # self.view_game = View_game(window, view_config)

    def game_launch(self):
        self.view_game = View_game(self.window, self.view_config)

    def refresh(self):
        self.view_game.refresh()

    def addhuman(self,human) -> bool:
        """
        Adding one player into the list of humans to handle at each round

        :param human: Player to add
        :type arg1: Player
        """
        if isinstance(human,Player):    
            if len(self.humans_list) > 1: 
                self.humans_list = self.humans_list[:-1] + [human] + self.humans_list[:-1]
            else :
                self.humans_list = [human] + self.humans_list
            return True
        else:
            # Given human isn't a player
            return False

    def removeplayer(self, player_uuid) -> bool:
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

    def resetallhumans(self):
        """Reseting all humans : no more player and new dealer"""
        self.humans_list = [Dealer()]

    def playoneround(self):
        for human in self.humans_list :
            print(human.name+ " is playing.")
            #Get list of possible actions
            #Manage interfaces
            #Let human choose
            state =True
            while state == True:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        return False
                    elif event.type == KEYDOWN and event.key == K_ESCAPE:
                        return False
                    else:
                        human.chooseAction()
                        state = False
                        return


