import random
from typing import Optional
from cg.api import (
    Observation, Option, OptionType, SelectType, SelectContext,
    EnergyType, CardType, to_observation_class
)
import os
from agent.computation.best_starting_play import best_starting_active, follow_up_bench
from agent.computation.analysis import analyse_setupBench

def choose_active(obs: Observation, first: bool):
    me = obs.current.players[obs.current.yourIndex]
    legal = obs.select.option
    
    return best_starting_active(me.hand, legal, first)


def choose_bench(obs: Observation):
    me = obs.current.players[obs.current.yourIndex]
    legal = obs.select.option

    return follow_up_bench(me.hand, legal)

def main_phase(obs):
    pass
def choose_attack(obs):
    pass
def choose_damage_target(obs):
    pass
def choose_attachment_target(obs):
    pass
def fallback(obs):
    pass

def decide(obs: Observation) -> list[int]:
    ctx = obs.select.context
    
    isFirst = (obs.current.firstPlayer == obs.current.yourIndex)

    if ctx == SelectContext.SETUP_ACTIVE_POKEMON:
        return choose_active(obs, isFirst)

    elif ctx == SelectContext.SETUP_BENCH_POKEMON:
        return choose_bench(obs)

    elif ctx == SelectContext.MAIN:
        return main_phase(obs)

    elif ctx == SelectContext.ATTACK:
        return choose_attack(obs)

    elif ctx == SelectContext.DAMAGE:
        return choose_damage_target(obs)

    elif ctx == SelectContext.ATTACH_TO:
        return choose_attachment_target(obs)

    else:
        return [0]
    

    