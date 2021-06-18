from __future__ import annotations
from enum import Enum
from typing import List
import random


class CardName(Enum):
    sサイバーヴァリー = 0
    dドグマガイ = 1
    eエアーマン = 2
    k光帝クライス = 3
    k混沌の黒魔術師 = 4
    dディスクガイ = 5
    aアームズホール = 6
    dデステニードロー = 7
    m名推理 = 8
    mモンスターゲート = 9
    fフェニブレ = 10
    DDR = 11
    t手札断殺 = 12
    tトレードイン = 13
    m魔法石の採掘 = 14
    s死者転生 = 15
    z次元融合 = 16
    s死者蘇生 = 17
    t手札抹殺 = 18
    h早すぎた埋葬 = 19
    m魔法再生 = 20
    z増援 = 21
    n成金ゴブリン = 22
    mマジカルエクスプロージョン = 23


Deck = {
    CardName.dドグマガイ: 2,
    CardName.k混沌の黒魔術師: 1,
    CardName.k光帝クライス: 1,
    CardName.eエアーマン: 1,
    CardName.dディスクガイ: 1,
    CardName.sサイバーヴァリー: 2,
    CardName.z次元融合: 1,
    CardName.z増援: 1,
    CardName.mモンスターゲート: 2,
    CardName.tトレードイン: 2,
    CardName.dデステニードロー: 3,
    CardName.aアームズホール: 3,
    CardName.m名推理: 3,
    CardName.t手札抹殺: 1,
    CardName.s死者蘇生: 1,
    CardName.m魔法石の採掘: 2,
    CardName.DDR: 2,
    CardName.fフェニブレ: 2,
    CardName.h早すぎた埋葬: 1,
    CardName.t手札断殺: 2,
    CardName.s死者転生: 2,
    CardName.n成金ゴブリン: 2,
    CardName.m魔法再生: 0,
    CardName.mマジカルエクスプロージョン: 2,
}


def checkDeck():
    deckNum = 0
    for k in CardName:
        deckNum += Deck[k]

    print("number of cards in the deck is {}".format(deckNum))

    return


def id2name(index: int):
    return CardName(index)


def name2id(name: CardName):
    return name


class Position(Enum):
    DECK = 0
    HAND = 1
    MAGIC_FIELD = 2
    MONSTER_FIELD = 3
    GRAVEYARD = 4
    BANISHED = 5


class Card:
    id: int
    deckpos: int
    name: str
    pos: Position

    def __init__(self, index, deckpos) -> None:
        self.id: int = index
        self.deckpos: int = deckpos
        self.name = id2name(index)
        self.pos = Position.DECK

    def __repr__(self) -> str:
        return repr(self.name) + repr(self.pos)

    def effect(self, cards: List[Card]) -> None:
        if self.name == CardName.dデステニードロー:
            assert len(cards) == 1
            assert self.pos == Position.HAND
            self.pos = Position.GRAVEYARD
            assert cards[0].pos == Position.HAND
            cards[0].pos = Position.GRAVEYARD

    def isDhero(self) -> bool:
        return self.name == CardName.dドグマガイ or self.name == CardName.dディスクガイ


class GameState:
    def __init__(self, deckList) -> None:
        self.deck: List[Card] = []
        deckpos = 0
        for k in CardName:
            for j in range(Deck[k]):
                self.deck.append(Card(name2id(k), deckpos))
                deckpos += 1
        self.life = 8000

    def __repr__(self):
        rep = ""
        for card in self.deck:
            rep += card.__repr__() + "\n"
        return rep

    def handCards(self) -> List[Card]:
        ret = []
        for c in self.deck:
            if c.pos == Position.HAND:
                ret.append(c)
        return ret

    def deckCards(self) -> List[Card]:
        ret = []
        for c in self.deck:
            if c.pos == Position.DECK:
                ret.append(c)
        return ret

    def canEffect(self, card) -> List[Card]:
        ret = []
        if card.name == CardName.dデステニードロー:
            if card.pos != Position.HAND:
                return []
            hands = self.handCards()
            for c in hands:
                if c.isDhero():
                    ret.append(c)

            return ret
        return ret

    def canDraw(self, number) -> bool:
        decks = self.deckCards()
        return len(decks) >= number

    def draw(self, number) -> None:
        decks = self.deckCards()
        cs = random.sample(population=decks, k=number)
        for c in cs:
            assert c.pos == Position.DECK, c.pos
            c.pos = Position.HAND

    def getCardbyName(self, name) -> Card:
        for c in self.deck:
            if c.name == name:
                return c


def test():
    gameState = GameState(Deck)
    d = gameState.getCardbyName(CardName.dデステニードロー)
    disk = gameState.getCardbyName(CardName.dディスクガイ)
    assert not gameState.canEffect(d)
    d.pos = Position.HAND
    disk.pos = Position.HAND
    cs = gameState.canEffect(d)
    assert cs == [disk], "canEffect is {}".format(cs)
    d.effect([disk])
    assert d.pos == Position.GRAVEYARD
    assert disk.pos == Position.GRAVEYARD
    print("run デステニードロー test")


def main():
    checkDeck()
    gameState = GameState(Deck)
    print(gameState)
    gameState.draw(6)
    print(gameState)

    test()


if __name__ == '__main__':
    main()
