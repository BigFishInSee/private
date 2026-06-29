
from cg.api import (
    Observation, Option, OptionType, SelectType, SelectContext,
    EnergyType, CardType, to_observation_class, Observation, Card, Option, all_attack, all_card_data
)

import agent.computation.utils as u
import agent.computation.attack_handler as atk
from agent.weight_management.data import CARDS, pokemon_plan
from typing import Tuple, List
import agent.computation.item_handler as it


card_data = all_card_data()
card_table = {c.cardId:c for c in card_data}

attack_data = all_attack()
attack_table = {c.attackId:c for c in attack_data}
def main(obs: Observation):

    if obs.current.yourIndex == 0:
        opp = 1
    else:
        opp = 0

    
    if len(obs.current.players[opp].prize) <= 3:
        possible, index = try_win(obs)
        if possible: return index

    #bench anything i need
    #RISKY RUINS HANDLER
    skip_bench = False
    if obs.current.stadium[0].id == 1260:
        skip_bench = True
    can_bench, index = try_bench(obs)
    if can_bench and not skip_bench: return index

    #Evolve dusks if I can: Flat EVO or Candy
    can_evolve, index = try_evolve(obs)
    if can_evolve and not skip_bench: return index


    #handle energy 
    can_attatch, index = try_energy(obs)
    if can_attatch: return index

    ###TESTED TILL HERE###

    #need item-attacher, support player etc
    use_item, index = it.main_item(obs)
    if use_item: return index

    #handle arena (current garden safety is tuned to max, lower once threat assessment feeature is out, due to certain overly-tanky matchups and no confidence in the agent's handling of energy cycling)
    utilize_arena, index = it.handle_garden(obs)
    if utilize_arena: return index

    #need handler for abilities



    #cant do shit
    for index, options in enumerate(obs.select.option):
        if options.type == OptionType.END:
            return [index]

    


#ONLY code for win in next cycle
def try_win(obs: Observation):
    if obs.current.yourIndex == 0:
        opp = 1
    else:
        opp = 0
    opponent = obs.current.players[opp]
    #see if I can kill an mega_EX
    if len(opponent.prize) == 3:
        return atk.finishing_sequence(obs, opponent, 3)
    #see if I can kill a EX OR megaEX
    elif len(opponent.prize) == 2:
        return atk.finishing_sequence(obs, opponent, 2)
    #see if I can mug anything
    elif len(opponent.prize) == 1:
        return atk.finishing_sequence(obs, opponent, 1)
    else: 
        return False, [999]
        
        
def try_evolve(obs: Observation):

    hand = obs.current.players[obs.current.yourIndex].hand
    bench = u.get_Bench(obs, "me")
    #check if dusclops would get more value
    opponent_pokemon = u.get_Bench(obs, "opp")
    opponent_pokemon.append(u.get_Active(obs, "opp"))
    candy_first = False
    for index, pokemon in enumerate(opponent_pokemon):
        if pokemon.hp <= 50:
            candy_first = False

    for index, option in enumerate(obs.select.option):
        
        if candy_first:
            #check if rare candy
            if option.type == OptionType.PLAY and u.has_card(hand, CARDS.RARE_CANDY):
                if (option.index == u.index_of_card(hand, CARDS.RARE_CANDY)) and u.has_card(hand, CARDS.DUSKNOIR) and (u.get_Active(obs, "me").id == CARDS.DUSKULL or u.has_pokemon(bench, CARDS.DUSKULL)):
                    return True, [index]
                
                #evolving naturally 
            if option.type == OptionType.EVOLVE:
                return True, [index]
        else:   
            #evolving naturally 
            if option.type == OptionType.EVOLVE:
                return True, [index]
            #check if rare candy
            if option.type == OptionType.PLAY and u.has_card(hand, CARDS.RARE_CANDY):
                if (option.index == u.index_of_card(hand, CARDS.RARE_CANDY)) and u.has_card(hand, CARDS.DUSKNOIR) and (u.get_Active(obs, "me").id == CARDS.DUSKULL or u.has_pokemon(bench, CARDS.DUSKULL)):
                    return True, [index]
        
    
    return False, [67]

    
def try_bench(obs: Observation):
    current_bench = u.get_Bench(obs, "me")
    #make sure to save a slot for latias if none
    hand = obs.current.players[obs.current.yourIndex].hand
    if len(current_bench) >= 4 and not u.has_Pokemon(current_bench, CARDS.LATIAS):
        for index, option in enumerate(obs.select.option):
            if option.type == OptionType.PLAY and u.index_of_card(hand, CARDS.LATIAS) == option.index:
                return True, [index]
            
        return False, [6767]
    


    
    #normal benching (ADD BALACER FOR DANGEROUS MATCHUPS)
    for index, pokemon in enumerate(current_bench):
        pokemon_plan[pokemon.id].Start_Bench_priority -= 1
        if pokemon.id == CARDS.DUSCLOPS or pokemon.id == CARDS.DUSKNOIR:
            pokemon_plan[CARDS.DUSKULL].Start_Bench_priority -= 1
        if obs.current.turn >= 2:
            pokemon_plan[CARDS.FRILLISH].Start_Bench_priority -= 1
    
    for index, option in enumerate(obs.select.option):
        if option.type == OptionType.PLAY and u.is_Pokemon(u.id_from_option(option, obs)):
            if pokemon_plan[u.id_from_option(option, obs)].Start_Bench_priority > 0:
                return True, [index]
    
    return False, [6767]

def try_energy(obs: Observation):

    hand = obs.current.players[obs.current.yourIndex].hand
    my_pokemon = u.get_Bench(obs, "me")
    my_pokemon.append(u.get_Active(obs, "me"))
    if u.has_card_count(hand, CARDS.PSYCHIC_ENERGY) + u.has_card_count(hand, CARDS.TELEPATHIC_ENERGY) == 0: return False, [67] #no energy lol
    #find who needs energy
    id_needed, type = u.balance_energy_priorities(my_pokemon, hand, obs) #index = index of my_pokemon list, last means active slot
    if id_needed == 6767:
        return False, [6767]
    isActive = id_needed == len(my_pokemon)-1
    for index, option in enumerate(obs.select.option):
        if option.type == OptionType.ATTACH:
            #2 kinds of energy     
            card_id = hand[option.index].id
            
            match card_id:
                case CARDS.PSYCHIC_ENERGY:
                    #energy is needed in active slot
                    if isActive:
                        #check if option targets normal energy to active
                        if type==5 and option.inPlayArea == 4:
                            return True, [index]
                    #energy needed in bench
                    else:
                        #check if corret energy type, correct area to attatch and correct card
                        if type==5 and option.inPlayArea == 5 and option.inPlayIndex == id_needed:
                            return True, [index]

                case CARDS.TELEPATHIC_ENERGY:
                    #energy is needed in active slot
                    if isActive:
                        #check if option targets normal energy to active
                        if type==19 and option.inPlayArea == 4:
                            return True, [index]
                    #energy needed in bench
                    else:
                        #check if corret energy type, correct area to attatch and correct card
                        if type==19 and option.inPlayArea == 5 and option.inPlayIndex == id_needed:
                            return True, [index]

                
                case _:
                    pass
    
    return False, [6767]








