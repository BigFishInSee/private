import sys
sys.path.insert(0, '.')
from cg.game import battle_start, battle_select, battle_finish
from cg.api import to_observation_class
from main import agent



def read_deck():
    with open("deck.csv", encoding="utf-8") as f:
        return [int(l.strip()) for l in f if l.strip()]

deck = read_deck()
obs_dict, sd = battle_start(deck, deck)

if obs_dict is None:
    print(f'Deck error: player={sd.errorPlayer} type={sd.errorType}')
else:
    turns = 0
    while True:
        obs = to_observation_class(obs_dict)
        if obs.current and obs.current.result != -1:
            print(f'Game over in {turns} turns. Winner: Player {obs.current.result}')
            break
        if turns > 500:
            print('Turn limit hit')
            break
        
        

        print(f"TURN IS {turns} \n")

        print("TYPE")
        print(obs.select.type)
        print("CONTEXT")
        print(obs.select.context)
        print("MAX AND MIN")
        print(obs.select.maxCount)
        print(obs.select.minCount)
        

        print(f"CARDS_IN_HAND of agent {obs.current.yourIndex}")
        me = obs.current.players[obs.current.yourIndex]
        print(me.hand)

        print("optons IS HERE")
        print(obs.select.option)
        print(f"ACTIVE SLOT OF AGENT + {obs.current.yourIndex}")
        print(me.active)
        
       

        diddy = input("Enter smt to go on: ")
        action = agent(obs_dict)
        print(action)
        diddy2 = input("check action?:")
        obs_dict = battle_select(action)
        turns += 1

    battle_finish()