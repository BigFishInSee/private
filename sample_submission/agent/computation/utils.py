import random
from typing import Optional
from cg.api import (
    Observation, Option, OptionType, SelectType, SelectContext,
    EnergyType, CardType, to_observation_class, Observation, Card, Option
)
import os

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