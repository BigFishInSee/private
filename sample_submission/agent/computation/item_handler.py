from cg.api import (
    Observation, Option, OptionType, SelectType, SelectContext,
    EnergyType, CardType, to_observation_class, Observation, Card, Option, all_attack, all_card_data
)

import agent.computation.utils as u
import agent.computation.attack_handler as atk
from agent.weight_management.data import CARDS, pokemon_plan
card_data = all_card_data()
card_table = {c.cardId:c for c in card_data}


def main_item(obs: Observation):
    #Core logic: 


    pass # placeholder


def handle_garden(obs: Observation):
    need_arena = False
    hand = obs.current.players[obs.current.yourIndex].hand
    
    #if no stadium, use mustery garden
    if len(obs.current.stadium)>0:
        current_arena = obs.current.stadium[0]
        if current_arena.id != CARDS.MYSTERY_GARDEN:
            #play garden if not garden
            need_arena = True
        else:
            #try use garden if is garden
            return use_garden(obs)
    else:
        #no stadium, play garden
        need_arena = True

    
    #play the option with using mystery garden
    for index, option in enumerate(obs.select.option):
        if option.type == OptionType.PLAY and option.index == u.index_of_card(hand, CARDS.MYSTERY_GARDEN):
            return need_arena, [index]
    return False, [6767]
    
def use_garden(obs: Observation):
    hand = obs.current.players[obs.current.yourIndex].hand
    my_pokemon = u.get_Bench(obs, "me")
    my_pokemon.append(u.get_Active(obs, "me"))
    discard = u.get_discard_pile(obs)
    psychic_counter = 0

    #check if diancie and/or early frilish is well fed
    for index, pokemon in enumerate(my_pokemon):
        if card_table[pokemon.id].energyType == EnergyType.PSYCHIC:
            psychic_counter += 1

        if pokemon.id == CARDS.FRILLISH and obs.current.turn <= 4 and len(pokemon.energyCards)==0:
            return False, [6767]
        if pokemon.id == CARDS.DIANCIE and len(pokemon.energyCards)<3:
            return False, [6767]

    if psychic_counter <= len(hand):
        return False, [6767]
    #check if theres too much energy in discard already
    if u.has_card_count(discard, CARDS.PSYCHIC_ENERGY) < 3:
        for index, option in enumerate(obs.select.option):
            if option.area == 7 or option.inPlayArea == 7:
                return True, [index]
    
    return False, [6767]


