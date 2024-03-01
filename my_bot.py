from poker_game_runner.state import Observation
from poker_game_runner.utils import Range, HandType
import time
import random

map_hand_to_pct = {9:[0.12, 7], 8:[0.1, 5]}#, 7:[0.1, 5], 6:[0.075, 5], 5:[0.05, 5], 4:[0.01, 2], 3:[0.005, 2], 2:[0.001, 1]}

class Bot:
  def get_name(self):
      return "Steven, the meek farmer"

  def act(self, obs: Observation):
    # Get Own hand and Board Hand
    current_bot_hand = obs.get_my_hand_type()
    current_board_hand = obs.get_board_hand_type()
    call_size = obs.get_call_size()
    me = obs.get_my_player_info() # Attributes: stack (how much left) & spent (how much spent so far)
    left_local = me.stack-me.spent

    if left_local == 0: ## Dont fold when you are already all-in
      return 1
    
    if obs.current_round == 0: ## Special handling for preflop
      if call_size <= obs.big_blind * 2:
        return 1
      else:
         return 0
    
    if current_bot_hand == current_board_hand:
      if (Range("77+, ATs+, KQs, AQo+").is_hand_in_range(obs.my_hand)):
         return 1
      elif current_bot_hand in [0, 1, 2, 3, 4] and call_size > 0 and obs.current_round < 3 and me.spent < call_size * 5:
        return 0
      elif call_size < 0.05 * left_local or call_size <= obs.small_blind:
         return 1 # Call
      elif call_size <= obs.small_blind and me.spent > 0.05 * left_local and call_size < 0.2 * left_local:
         return 1 # Call
      else:
         return 0
    # print(current_board_hand, current_bot_hand, call_size, me.stack, me.spent)
    # if current_bot_hand == 9:
    #    return obs.get_min_raise() + min(int(me.stack * 0.2), 10)
    # elif current_bot_hand == 8:
    #    return obs.get_min_raise() + min(int(me.stack * 0.1), 5)
    # elif current_bot_hand == 7:
    
    # elif current_bot_hand >= current_board_hand + 3:
    #    return obs.get_min_raise() + min(int(me.stack * 0.05), 2)
    if current_bot_hand in map_hand_to_pct:
      raising = min(int(left_local * map_hand_to_pct[current_bot_hand][0]), map_hand_to_pct[current_bot_hand][1])
    else:
      raising = 0

    # if current_bot_hand in [0, 1, 2, 3, 4] and call_size > obs.big_blind and me.spent < call_size * 4:
    #   return 0
    if (Range("66+, A8s+, KTs+, QTs+, ATo+, KQo").is_hand_in_range(obs.my_hand)):
      return min(obs.get_min_raise() + raising, obs.get_max_raise())
    elif obs.get_min_raise() < left_local * 0.2: 
      return obs.get_min_raise()
    else:
      return 1
  

