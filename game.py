from enum import Enum

CardList = [
    "サイバーヴァリー",
    "ドグマガイ",
    "エアーマン",
    "光帝クライス",
    "混沌の黒魔術師",
    "ディスクガイ",
    "アームズホール",
    "デステニードロー",
    "名推理",
    "モンスターゲート",
    "フェニブレ",
    "DDR",
    "手札断殺",
    "トレードイン",
    "魔法石の採掘",
    "死者転生",
    "次元融合",
    "死者蘇生",
    "手札抹殺",
    "早すぎた埋葬",
    "魔法再生",
    "増援",
    "成金ゴブリン",
    "マジカルエクスプロージョン",
]

Deck = {
    "ドグマガイ":2,
    "混沌の黒魔術師":1,
    "光帝クライス":1,
    "エアーマン":1,
    "ディスクガイ" : 1,
    "サイバーヴァリー":2,
    "次元融合":1,
    "増援":1,
    "モンスターゲート":2,
    "トレードイン":2,
    "デステニードロー": 3,
    "アームズホール" :3,
    "名推理": 3,
    "手札抹殺":1,
    "死者蘇生":1,
    "魔法石の採掘":2,
    "DDR":2,
    "フェニブレ":2,
    "早すぎた埋葬":1,
    "手札断殺":2,
    "死者転生":2,
    "成金ゴブリン":2,
    "魔法再生":0,
    "マジカルエクスプロージョン":2,
}

def checkDeck():
    deckNum = 0
    for k in CardList:
        deckNum += Deck[k]

    print("number of cards in the deck is {}".format(deckNum))
    
    return 

def id2name(index):
    return CardList[index]

def name2id(index):
    return CardList.index(index)

class Position(Enum):
    DECK = 0
    HAND = 1
    MAGIC_FIELD = 2
    MONSTER_FIELD = 3
    GRAVEYARD = 4
    BANISHED = 5

class Card:
    def __init__(self,index) -> None:
        self.id = index        
        self.name = id2name(index)
        self.pos = Position.DECK

    def __repr__(self) -> str:
        return self.name + repr(self.pos)

class GameState:
    def __init__(self,deckList) -> None:
        deckNum = 0
        self.deck = []
        for k in CardList:
            for _ in range(Deck[k]):
                self.deck.append(Card(name2id(k)))
        self.life = 8000
    
    def __repr__(self):
        rep ="" 
        for card in self.deck:
            rep += card.__repr__() + "\n"
        return rep


            

def main():
    checkDeck()
    gameState = GameState(Deck)
    print(gameState)

if __name__ == '__main__':
    main()