from dataclasses import dataclass
from enum import IntEnum

@dataclass
class PokemonPlan:
    Start_Active_priority: int
    Start_Bench_priority: int






pokemon_plan = {
    #Duskull
    131: PokemonPlan(3,2),
    #Dusclops = 132
    132: PokemonPlan(0,0),
    #Dusknoir = 133
    133: PokemonPlan(0,0),
    #Mega Diancie EX = 766
    766: PokemonPlan(1,0),
    #Latias EX = 184
    184: PokemonPlan(6,1),
    #Lillie’s Clefairy EX = 272
    272: PokemonPlan(2,1),
    #Meowth ex = 1071
    1071: PokemonPlan(4,1),
    #Frillish = 597
    597: PokemonPlan(5,1),
    #Judge = 1213
    1213: PokemonPlan(0,0),
    #Lillie's Determination = 1227
    1227: PokemonPlan(0,0),
    #Boss's orders = 1182
    1182: PokemonPlan(0,0),
    #Ultra ball = 1121
    1121: PokemonPlan(0,0),
    #Poke pad = 1152
    1152: PokemonPlan(0,0),
    #Wondrous patch = 1146
    1146: PokemonPlan(0,0),
    #Rare candy = 1079
    1079: PokemonPlan(0,0),
    #Night stretcher = 1097
    1097: PokemonPlan(0,0),
    #Secret box = 1092
    1092: PokemonPlan(0,0),
    #PowerGlass = 1163
    1163: PokemonPlan(0,0),
    #Lillie's pearl = 1172
    1172: PokemonPlan(0,0),
    #Mystery garden = 1263
    1263: PokemonPlan(0,0),
    #Basic Psychic energy = 5
    5: PokemonPlan(0,0),
    #Telepathis Psychic Energy = 19
    19: PokemonPlan(0,0),
}
    


class CARDS(IntEnum):
    # Duskull
    DUSKULL = 131

    # Dusclops
    DUSCLOPS = 132

    # Dusknoir
    DUSKNOIR = 133

    # Mega Diancie EX
    DIANCIE = 766

    # Latias EX
    LATIAS = 184

    # Lillie's Clefairy EX
    CLEFAIRY = 272

    # Meowth ex
    MEOWTH = 1071

    # Frillish
    FRILLISH = 597

    # Judge
    JUDGE = 1213

    # Lillie's Determination
    LILLIE_DETERMINATION = 1227

    # Boss's Orders
    BOSS = 1182

    # Ultra Ball
    ULTRA_BALL = 1121

    # Poké Pad
    POKE_PAD = 1152

    # Wondrous Patch
    WONDROUS_PATCH = 1146

    # Rare Candy
    RARE_CANDY = 1079

    # Night Stretcher
    NIGHT_STRETCHER = 1097

    # Secret Box
    SECRET_BOX = 1092

    # Powerglass
    POWERGLASS = 1163

    # Lillie's Pearl
    LILLIE_PEARL = 1172

    # Mystery Garden
    MYSTERY_GARDEN = 1263

    # Basic Psychic Energy
    PSYCHIC_ENERGY = 5

    # Telepathic Psychic Energy
    TELEPATHIC_ENERGY = 19