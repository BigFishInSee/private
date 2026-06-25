import random
from typing import Optional
from cg.api import (
    Observation, Option, OptionType, SelectType, SelectContext,
    EnergyType, CardType, to_observation_class, Observation, Card, all_card_data, Pokemon, PlayerState,
    all_attack
)
import os
from agent.weight_management.data import CARDS


card_data = all_card_data()
card_table = {c.cardId:c for c in card_data}


attack_data = all_attack()
attack_table = {c.attackId:c for c in attack_data}


def has_card(jar: list[Card], ID: int):
    for index, card in enumerate(jar):
        if card.id == ID:
            return True
    
    return False

def has_card_count(jar: list[Card], ID: int):
    count = 0
    for index, card in enumerate(jar):
        if card.id == ID:
            count += 1
    return count

def index_of_card(hand: list[Card], ID: int):
    for index, card in enumerate(hand):
        if card.id == ID:
            return index
    return None

def has_Pokemon(jar: list[Pokemon], ID: int):
    for index, card in enumerate(jar):
        if card.id == ID:
            return True
    
    return False

def has_Pokemon_count(jar: list[Pokemon], ID: int):
    count = 0
    for index, card in enumerate(jar):
        if card.id == ID:
            count += 1
    return count

def index_of_pokemon(hand: list[Pokemon], ID: int):
    for index, card in enumerate(hand):
        if card.id == ID:
            return index
    return None

def get_Active(obs:Observation, player: str):
    if obs.current.yourIndex == 0:
        opp = 1
    else:
        opp = 0


    if player == "me":
        return obs.current.players[obs.current.yourIndex].active[0]
    if player == "opp":
        return obs.current.players[opp].active[0]
        

def has_pokemon(jar: list[Pokemon], id: int):
    for index, pokemon in enumerate(jar):
        if pokemon.id == id:
            return True
    return False

def get_Bench(obs:Observation, player: str):
    if obs.current.yourIndex == 0:
        opp = 1
    else:
        opp = 0


    if player == "me":
        return obs.current.players[obs.current.yourIndex].bench
    if player == "opp":
        return obs.current.players[opp].bench
    


def attack_effectiveness_rebalance(attacker: Pokemon, opp: PlayerState, damage: int):
    opponent_poke = opp.active[0].id
    weakness = card_table[opponent_poke].weakness
    resistance = card_table[opponent_poke].resistance
    my_type = card_table[attacker.id].energyType

    #edge case maybe? them passive abilities add here with dataset later manual search



    if my_type == weakness:
        return damage
    if my_type == resistance:
        return -20
    else: return 0
    

    

def is_Pokemon(id: int):
    if id is None:
        return False
    return card_data[id].cardType == CardType.POKEMON

def prize_card_drop(id: int):
    if card_data[id].ex: return 2
    if card_data[id].megaEx: return 3
    return 1

def is_under_count(jar: list[Pokemon], id: int):
    count = 0
    for index, pokemon in enumerate(jar):
        preEvs = pokemon.preEvolution
        for pre, preEvos in enumerate(preEvs):
            if preEvos.id == id: count += 1
    return count


    

def balance_energy_priorities(my_pokemon: list[Pokemon], hand: list[Card], obs: Observation):
    #does anyone need card?
    target = 67
    backup_target = 67
    for index, pokemon in enumerate(my_pokemon):
        match pokemon.id:
            case CARDS.FRILLISH:
                if obs.current.turn <=4 and len(pokemon.energyCards)==0:
                    target = index
                    break
            
            case CARDS.DIANCIE:
                if len(pokemon.energyCards)<3:
                    target = index
                    break
            
            case _:

                backup_target = index   

    #no valid targets found, go for auxillary to get telepathic energy to pull something needed
    if target == 67:
        if obs.current.turn <3 and has_card(hand, CARDS.TELEPATHIC_ENERGY) and backup_target != 67: 
            return backup_target, 19
        else:
            return 6767, 0
        
    #decide energy type
    if has_card(hand, CARDS.PSYCHIC_ENERGY) and has_card(hand, CARDS.TELEPATHIC_ENERGY):
        if has_Pokemon_count(my_pokemon, CARDS.DIANCIE) + has_card_count(hand, CARDS.DIANCIE) <2:
            return target, 19
        if not has_pokemon(my_pokemon, CARDS.FRILLISH) and not has_card(hand, CARDS.FRILLISH) and obs.current.turn <3:
            return target, 19
        if not has_pokemon(my_pokemon, CARDS.LATIAS) and not has_card(hand, CARDS.LATIAS):
            return target, 19
        if has_Pokemon_count(my_pokemon, CARDS.DUSKULL) + has_card_count(hand, CARDS.DUSKULL) + is_under_count(my_pokemon, CARDS.DUSKULL)<2:
            return target, 19
        
        return target, 5
    
    if has_card(hand, CARDS.PSYCHIC_ENERGY): return target, 5
    if has_card(hand, CARDS.TELEPATHIC_ENERGY): return target, 19
        
def get_discard_pile(obs: Observation):
    return obs.current.players[obs.current.yourIndex].discard
    