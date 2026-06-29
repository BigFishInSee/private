import random
from typing import Optional
from cg.api import (
    Observation, Option, OptionType, SelectType, SelectContext,
    EnergyType, CardType, to_observation_class, Observation, Card, Option, all_card_data, all_attack
)
import os
from agent.weight_management.data import pokemon_plan, PokemonPlan, CARDS
from agent.computation.utils import has_card, has_card_count, get_Active


card_data = all_card_data()
card_table = {c.cardId:c for c in card_data}


def best_starting_active(hand: list[Card], legal: list[Option], first: bool):
    if len(legal) == 1:
        print("only 1 choice")
        return [0]
    
    best_option_idx = 0
    best_priority = -999999
    #agression, bump frillish for turn 1 disruption (REMAKE THIS SECTION LATER, FRILLISH FIRST DEFAULT FOR NOW)
    #can_I_frillish(first, hand)
    #can diancie drop someone?
    #turn_one_diancie(hand) #NEED UPDATE: make it go if 1 energy and potential to get 1 more
    for option_idx, option in enumerate(legal):

        card: Card = hand[option.index]

        priority = pokemon_plan[card.id].Start_Active_priority

        if priority > best_priority:
            best_priority = priority
            best_option_idx = option_idx

    return [best_option_idx]

def follow_up_bench(hand: list[Card], legal: list[Option], obs: Observation):
    
    options = []
    

    for option_idx,option in enumerate(legal):
       
        card: Card = hand[option.index]
        if pokemon_plan[card.id].Start_Bench_priority > 0:
            pokemon_plan[card.id].Start_Bench_priority -= 1
            options.append(option_idx)
            
    return options


#turn one garland ray
def turn_one_diancie(hand: list[Card]):
    #enough energy to boost a t1 attack
    if has_card_count(hand, CARDS.PSYCHIC_ENERGY) + has_card_count(hand, CARDS.TELEPATHIC_ENERGY) >= 2:
        pokemon_plan[CARDS.DIANCIE].Start_Active_priority += 10
    elif (has_card(hand,CARDS.PSYCHIC_ENERGY) or has_card(hand, CARDS.TELEPATHIC_ENERGY)) and (has_card(hand, CARDS.JUDGE) or has_card(hand, CARDS.LILLIE_DETERMINATION)):
        pokemon_plan[CARDS.DIANCIE].Start_Active_priority += 10
    
    
    



def can_I_frillish(first, hand: list[Card]):
    #no frillish
    if not has_card(hand, CARDS.FRILLISH):
        pass
    #going first and have a frillish
    elif first and has_card(hand, CARDS.FRILLISH):
        #has a psychic energy to charge it up
        if has_card(hand, CARDS.PSYCHIC_ENERGY) or has_card(hand, CARDS.TELEPATHIC_ENERGY):
            #bump frillish before latias
            pokemon_plan[CARDS.FRILLISH].Start_Active_priority += 2
            
        #no psychic energy, but have items to re-organize hand (judge and lillie's determination)
        elif has_card(hand, CARDS.JUDGE) or has_card(hand, CARDS.LILLIE_DETERMINATION):
            pokemon_plan[CARDS.FRILLISH].Start_Active_priority += 2
            
        #no energy, no re-organizer
        pass
    
    #Going 2nd with frillish
    elif not first and has_card(hand, CARDS.FRILLISH):
        #has energy to charge frillish, even if secondary hit, sure i guess
        if has_card(hand, CARDS.PSYCHIC_ENERGY) or has_card(hand, CARDS.TELEPATHIC_ENERGY) or has_card(hand, CARDS.SECRET_BOX):
            #bump frillish before latias
            pokemon_plan[CARDS.FRILLISH].Start_Active_priority += 2
            
        #has reshuffler and a latias for bench, so frillish can run in case gamble fails
        elif (has_card(hand, CARDS.JUDGE) or has_card(hand, CARDS.LILLIE_DETERMINATION)) and (has_card(hand, CARDS.LATIAS) or has_card(hand, CARDS.ULTRA_BALL)):
            pokemon_plan[CARDS.FRILLISH].Start_Active_priority += 2

        #can attatch energy, has diancie + energy-recovery if dies
        #SENARIO A: has telepathic energy, gets a diancie and latias
        #SENARIO B: 

    
            
        #f
        pass
        
    
