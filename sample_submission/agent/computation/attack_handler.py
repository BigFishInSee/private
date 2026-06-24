from cg.api import (
    Observation, Option, OptionType, SelectType, Pokemon, PlayerState,
    EnergyType, CardType, to_observation_class, Observation, Card, Option, all_attack, all_card_data
)

import agent.computation.utils as u
from agent.weight_management.data import CARDS
card_data = all_card_data()
card_table = {c.cardId:c for c in card_data}

attack_data = all_attack()
attack_table = {c.attackId:c for c in attack_data}


def handle_damage(attacker: Pokemon, attackId: int, opp: PlayerState, prizeTarget: int):
    damage = attack_table[attackId].damage
    return damage + u.attack_effectiveness_rebalance(attacker, opp)
    #Need handler for diancie too, ADD CONSIDERATION IF GAME DOSENT


def finishing_sequence(obs: Observation, opponent: PlayerState, prizeTarget: int) -> tuple[bool, list[int]]:
    #There is a eligible in active slot, enum options for a KO option
    if u.prize_card_drop(opponent.active[0].id) >= prizeTarget:
        for index, option in enumerate(obs.select.option):
            match option.type:
                case OptionType.ATTACK:
                    #TRY KILL WITH ATTACK
                    attacker = u.get_Active(obs, "me")
                    attacked = u.get_Active(obs, "opp")
                    if handle_damage(attacker, option.attackId, opponent) >= attacked.hp:
                        return True, [index]
                
                # WIN WITH A DUSKNOIR ABILITY 
                case OptionType.ABILITY:
                    if option.cardId == CARDS.DUSKNOIR and opponent.active[0].hp <= 130:
                        return True, [index]
                    elif option.cardId == CARDS.DUSCLOPS and opponent.active[0].hp <= 50:
                        return True, [index]
                case _:
                    pass
    #CHECK BENCH
    for card, Pokemon in enumerate(opponent.bench):
        if u.prize_card_drop(Pokemon.id) >= prizeTarget:
            #ELIGIBLE IN BENCH, 2 Ways. Boss-Order it out or DUSK it (Count boss order at 1 turn for simplicity, since it moves up to the above chain)
            for index, option in enumerate(obs.select.option):
                match option.type:
                    case OptionType.PLAY:
                        #TRY PLAY BOSS
                        if u.index_of_card(obs.current.players[obs.current.yourIndex].hand, CARDS.BOSS) != None:
                            is_at = u.index_of_card(obs.current.players[obs.current.yourIndex].hand, CARDS.BOSS)
                            if option.index == is_at: return True, [index]
            
                    #WIN WITH A DUSKNOIR ABILITY 
                    case OptionType.ABILITY:
                        if option.cardId == CARDS.DUSKNOIR and Pokemon.hp <= 130:
                            return True, [index]
                        elif option.cardId == CARDS.DUSCLOPS and Pokemon.hp <= 50:
                            return True, [index] 
                    case _:
                        pass
    return False, [999]


    

#(attack.damage+u.attack_effectiveness_rebalance(attacker, opponent, attack.damage))

















# def can_kill(obs: Observation, pokemon: Pokemon):
#     if obs.current.yourIndex == 0:
#         opp = 1
#     else:
#         opp = 0
#     opponent = obs.current.players[opp]


#     my_hand = obs.current.players[obs.current.yourIndex].hand
#     target_hp = pokemon.hp
#     my_active = u.get_Active(obs, "me")
#     my_bench = u.get_Bench(obs, "me")

#     if my_active.id == CARDS.FRILLISH:
#         #check if have energy and enemy HP low enough
#         if (len(my_active.energyCards)>0 or u.has_card(my_hand, CARDS.PSYCHIC_ENERGY) > 0 or u.has_card(my_hand, CARDS.TELEPATHIC_ENERGY) > 0)



