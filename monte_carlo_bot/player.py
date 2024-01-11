'''
Simple example pokerbot, written in Python.
'''
import math
import random

import eval7

from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction
from skeleton.states import GameState, TerminalState, RoundState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot


class Player(Bot):
    '''
    A pokerbot.
    '''

    def __init__(self):
        '''
        Called when a new game starts. Called exactly once.

        Arguments:
        Nothing.

        Returns:
        Nothing.
        '''
        pass

    def handle_new_round(self, game_state, round_state, active):
        '''
        Called when a new round starts. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        #my_bankroll = game_state.bankroll  # the total number of chips you've gained or lost from the beginning of the game to the start of this round
        #game_clock = game_state.game_clock  # the total number of seconds your bot has left to play this game
        #round_num = game_state.round_num  # the round number from 1 to NUM_ROUNDS
        #my_cards = round_state.hands[active]  # your cards
        #big_blind = bool(active)  # True if you are the big blind
        pass

    def handle_round_over(self, game_state, terminal_state, active):
        '''
        Called when a round ends. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        terminal_state: the TerminalState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        #my_delta = terminal_state.deltas[active]  # your bankroll change from this round
        #previous_state = terminal_state.previous_state  # RoundState before payoffs
        #street = previous_state.street  # 0, 3, 4, or 5 representing when this round ended
        #my_cards = previous_state.hands[active]  # your cards
        #opp_cards = previous_state.hands[1-active]  # opponent's cards or [] if not revealed
        pass

    def get_action(self, game_state, round_state, active):
        """
        Takes current hand, computes the value of many random hands starting with the current hand to get an estimated
        of the current hand's value

        """


        legal_actions = round_state.legal_actions()  # the actions you are allowed to take
        
        cards = round_state.hands[active]
        street = round_state.street
        board_cards = round_state.deck[:street]
        chips = round_state.stacks[active]

        deck = eval7.Deck()
        sims = 1000
        avg_eval = 0
        for i in range(0, sims):
            deck.shuffle()
            total_cards = list(map(eval7.Card, cards + board_cards)) + deck.sample(7 - street)
            evaluation = eval7.evaluate(total_cards)
            avg_eval += evaluation
        avg_eval /= sims

        abs_max_eval = 135004160  # Value of royal flush, max value
        
        # Arbitrary numbers to decide when to do each action
        min_eval = 10000
        max_eval = 50000000

        if avg_eval < min_eval:
            if CheckAction in legal_actions:
                return CheckAction()
            else:
                return FoldAction()
        elif avg_eval > max_eval and RaiseAction in legal_actions:
            min_raise, max_raise = round_state.raise_bounds()
            bet_amt = math.ceil(min_raise + (max_raise - min_raise) * (avg_eval / abs_max_eval))
            return RaiseAction(bet_amt)
        else:
            if CheckAction in legal_actions:
                return CheckAction()
            return CallAction()


if __name__ == '__main__':
    run_bot(Player(), parse_args())
