from dataclasses import dataclass
from enum import IntEnum

@dataclass
class PokemonPlan:
    Start_Active_priority: int
    Start_Bench_priority: int
    Need_This_Item: bool






pokemon_plan = {
    #Duskull
    131: PokemonPlan(3,2, False),
    #Dusclops = 132
    132: PokemonPlan(0,0, False),
    #Dusknoir = 133
    133: PokemonPlan(0,0, False),
    #Mega Diancie EX = 766
    766: PokemonPlan(4,2, False),
    #Latias EX = 184
    184: PokemonPlan(6,1, False),
    #Lillie’s Clefairy EX = 272
    272: PokemonPlan(2,1, False),
    #Meowth ex = 1071
    1071: PokemonPlan(1,0, False),
    #Frillish = 597
    597: PokemonPlan(5,1, False),
    #Judge = 1213
    1213: PokemonPlan(0,0, False),
    #Lillie's Determination = 1227
    1227: PokemonPlan(0,0, False),
    #Boss's orders = 1182
    1182: PokemonPlan(0,0, False),
    #Ultra ball = 1121
    1121: PokemonPlan(0,0, False),
    #Poke pad = 1152
    1152: PokemonPlan(0,0, False),
    #Wondrous patch = 1146
    1146: PokemonPlan(0,0, False),
    #Rare candy = 1079
    1079: PokemonPlan(0,0, False),
    #Night stretcher = 1097
    1097: PokemonPlan(0,0, False),
    #Secret box = 1092
    1092: PokemonPlan(0,0, False),
    #PowerGlass = 1163
    1163: PokemonPlan(0,0, False),
    #Lillie's pearl = 1172
    1172: PokemonPlan(0,0, False),
    #Mystery garden = 1263
    1263: PokemonPlan(0,0, False),
    #Basic Psychic energy = 5
    5: PokemonPlan(0,0, False),
    #Telepathis Psychic Energy = 19
    19: PokemonPlan(0,0, False),
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