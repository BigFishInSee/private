from cg.api import (
    Observation, Option, OptionType, SelectType, AreaType,
    EnergyType, CardType, to_observation_class, Observation, Card, Option, all_attack, all_card_data
)

import agent.computation.utils as u
import agent.computation.attack_handler as atk
from agent.weight_management.data import CARDS, pokemon_plan
card_data = all_card_data()
card_table = {c.cardId:c for c in card_data}


def main_item(obs: Observation):
    #Core logic: Always try tool first (powerglass diancie only)
    #try support: (reshufle, disrupt or assasinate)
    #try item to better the hand
    bench = u.get_Bench(obs, "me")
    hand = obs.current.players[obs.current.yourIndex].hand


    #POWERGLASS FIRST
    can_powerglass, indicies = try_use_item(CARDS.POWERGLASS, obs.select.option, hand)
    if can_powerglass:
        best_bench = None
        best_energie_count = -1

        for option in indicies:
            checking = obs.select.option[option]
            
            if checking.inPlayArea == AreaType.ACTIVE:
                return True, [option]

            elif checking.inPlayArea == AreaType.BENCH:
                index_in_bench: int = checking.index
                energie_count = len(bench[index_in_bench].energies)
                if energie_count > best_energie_count:
                    best_energie_count = energie_count
                    best_bench = option

        if best_bench is not None:
            return True, [best_bench]

    #WONDEROUS PATCH
    can_Patch, indicies = try_use_item(CARDS.WONDROUS_PATCH, obs.select.option, hand)
    if can_Patch: return True, [indicies[0]]

    #NEEDS HANDLER
        

                



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
    has_powerglass = False
    isFirst = True
    #check if diancie and/or early frilish is well fed
    for index, pokemon in enumerate(my_pokemon):
        if card_table[pokemon.id].energyType == EnergyType.PSYCHIC:
            psychic_counter += 1
        if pokemon.id == CARDS.DIANCIE:
            if len(pokemon.energyCards)<=2 and isFirst:
                return False, [6767]
            isFirst = False
            tool = pokemon.tools[0]
            if tool.id == CARDS.POWERGLASS:
                has_powerglass = True

    if psychic_counter <= len(hand):
        return False, [6767]
    #check if theres too much energy in discard already
    if u.has_card_count(discard, CARDS.PSYCHIC_ENERGY) + u.has_card_count(discard, CARDS.TELEPATHIC_ENERGY)< 4:
        for index, option in enumerate(obs.select.option):
            if (option.area == 7 or option.inPlayArea == 7) and option.playerIndex == obs.current.yourIndex:
                return True, [index]
            
    #ignore that if diancie has powerglass
    elif has_powerglass and u.has_card_count(discard, CARDS.PSYCHIC_ENERGY) + u.has_card_count(discard, CARDS.TELEPATHIC_ENERGY)< 5:
        for index, option in enumerate(obs.select.option):
            if (option.area == 7 or option.inPlayArea == 7) and option.playerIndex == obs.current.yourIndex:
                return True, [index]
    
    return False, [6767]

#returns all the options that uses the "item". pick manually to avoid things like energy over-charge
def try_use_item(id: int, op_list: list[Option], hand: list[Card]):
    enndex = []
    for index, option in enumerate(op_list):
        card_id = hand[option.index].id
        if u.is_Pokemon(card_id):
            pass
        else:
            if (option.type == OptionType.PLAY or option.type == OptionType.ATTACH) and card_id == id:
                enndex.append(index)
    if len(enndex)!=0:
        return True, enndex
    return False, [6767]


def item_needs_handler(obs: Observation):
    hand = obs.current.players[obs.current.yourIndex].hand
    my_discard = u.get_discard_pile(obs)
    my_bench = u.get_Bench(obs, "me")
    my_active = u.get_Active(obs, "me")
    my_pokemon =[]
    my_pokemon.append(my_active)
    my_pokemon.append(my_bench)

    stadium = obs.current.stadium[0]
    turn = obs.current.turn

    opponent_bench = u.get_Bench(obs, "opp")
    opponent_active = u.get_Active(obs, "opp")
    opponent_pokemon = []
    opponent_pokemon.append(opponent_active)
    opponent_pokemon.append(opponent_bench)
    opponent_discard = u.get_discard_pile_opp(obs)

    

    