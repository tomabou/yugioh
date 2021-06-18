from __future__ import annotations
from enum import Enum
from typing import List
import random

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
    "ドグマガイ": 2,
    "混沌の黒魔術師": 1,
    "光帝クライス": 1,
    "エアーマン": 1,
    "ディスクガイ": 1,
    "サイバーヴァリー": 2,
    "次元融合": 1,
    "増援": 1,
    "モンスターゲート": 2,
    "トレードイン": 2,
    "デステニードロー": 3,
    "アームズホール": 3,
    "名推理": 3,
    "手札抹殺": 1,
    "死者蘇生": 1,
    "魔法石の採掘": 2,
    "DDR": 2,
    "フェニブレ": 2,
    "早すぎた埋葬": 1,
    "手札断殺": 2,
    "死者転生": 2,
    "成金ゴブリン": 2,
    "魔法再生": 0,
    "マジカルエクスプロージョン": 2,
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
        return self.name + repr(self.pos)

    def effect(self, cards: List[Card]) -> None:
        if self.name == "デステニードロー":
            assert len(cards) == 1
            assert self.pos == Position.HAND
            self.pos = Position.GRAVEYARD
            assert cards[0].pos == Position.HAND
            cards[0].pos = Position.GRAVEYARD

    def isDhero(self) -> bool:
        return self.name == "ドグマガイ" or self.name == "ディスクガイ"


class GameState:
    def __init__(self, deckList) -> None:
        self.deck: List[Card] = []
        deckpos = 0
        for k in CardList:
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
        if card.name == "デステニードロー":
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
    d = gameState.getCardbyName("デステニードロー")
    disk = gameState.getCardbyName("ディスクガイ")
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
