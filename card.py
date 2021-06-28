from __future__ import annotations
from substate import SubState
from enum import Enum
from typing import Tuple


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
    dummy = 99


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
    CardName.dummy: 0,
}


def checkDeck():
    deckNum = 0
    for k in CardName:
        deckNum += Deck[k]

    print("number of cards in the deck is {}".format(deckNum))

    return


def id2name(index: int) -> CardName:
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
    MAGIC_SET = 6


class Card:
    id: int
    deckpos: int
    name: CardName
    pos: Position

    def __init__(self, index, deckpos) -> None:
        self.id: int = index
        self.deckpos: int = deckpos
        self.name = id2name(index)
        self.pos = Position.DECK

    def __repr__(self) -> str:
        return repr(self.name) + repr(self.pos)

    def SSutil(self, card) -> Tuple[SubState, int, int]:
        if card.name == CardName.k混沌の黒魔術師:
            return SubState.KonKuroSS, 0, 0
        elif card.name == CardName.eエアーマン:
            return SubState.AirManSS, 0, 0
        elif card.name == CardName.k光帝クライス:
            return SubState.KuraisuSS, 0, 0
        else:
            return SubState.Free, 0, 0

    def effect2(self,
                target1: Card, target2: Card) -> Tuple[SubState, int, int]:
        if self.name == CardName.fフェニブレ:
            target1.pos = Position.BANISHED
            target2.pos = Position.BANISHED
            self.pos = Position.HAND
            return SubState.Free, 0, 0
        elif self.name == CardName.DDR:
            target1.pos = Position.GRAVEYARD
            target2.pos = Position.MONSTER_FIELD
            self.pos = Position.MAGIC_FIELD
            return self.SSutil(target2)
        elif self.name == CardName.s死者転生:
            target1.pos = Position.GRAVEYARD
            target2.pos = Position.HAND
            self.pos = Position.GRAVEYARD
            return SubState.Free, 0, 0
        elif self.name == CardName.t手札断殺:
            target1.pos = Position.GRAVEYARD
            target2.pos = Position.GRAVEYARD
            self.pos = Position.GRAVEYARD
            return SubState.Draw, 2, 0
        elif self.name == CardName.k光帝クライス:
            target1.pos = Position.GRAVEYARD
            target2.pos = Position.GRAVEYARD
            return SubState.Draw, 2, 0
        assert False, "not implement"

    def effect1(self, card: Card) -> Tuple[SubState, int, int]:
        if self.name == CardName.dデステニードロー:
            assert self.pos == Position.HAND or Position.MAGIC_SET
            self.pos = Position.GRAVEYARD
            assert card.pos == Position.HAND
            assert card.isDhero()
            card.pos = Position.GRAVEYARD
            return SubState.Draw, 2, 0
        elif self.name == CardName.tトレードイン:
            assert self.pos == Position.HAND or Position.MAGIC_SET
            self.pos = Position.GRAVEYARD
            assert card.pos == Position.HAND
            assert card.isLevel8()
            card.pos = Position.GRAVEYARD
            return SubState.Draw, 2, 0
        elif self.name == CardName.aアームズホール:
            assert self.pos == Position.HAND or Position.MAGIC_SET
            self.pos = Position.GRAVEYARD
            assert card.pos == Position.DECK
            card.pos = Position.GRAVEYARD
            return SubState.ArmsHole, 0, 0
        elif self.name == CardName.h早すぎた埋葬:
            self.pos = Position.MAGIC_FIELD
            card.pos = Position.MONSTER_FIELD
            if card.name == CardName.k混沌の黒魔術師:
                return SubState.KonKuroSS, 0, -800
            elif card.name == CardName.eエアーマン:
                return SubState.AirManSS, 0, -800
            elif card.name == CardName.k光帝クライス:
                return SubState.KuraisuSS, 0, -800
            elif card.name == CardName.dディスクガイ:
                return SubState.Draw, 2, -800
            else:
                return SubState.Free, 0, -800
        elif self.name == CardName.s死者蘇生:
            self.pos = Position.GRAVEYARD
            card.pos = Position.MONSTER_FIELD
            if card.name == CardName.k混沌の黒魔術師:
                return SubState.KonKuroSS, 0, -800
            elif card.name == CardName.eエアーマン:
                return SubState.AirManSS, 0, -800
            elif card.name == CardName.k光帝クライス:
                return SubState.KuraisuSS, 0, -800
            elif card.name == CardName.dディスクガイ:
                return SubState.Draw, 2, -800
            else:
                return SubState.Free, 0, -800
        elif self.name == CardName.z増援:
            self.pos = Position.GRAVEYARD
            card.pos = Position.HAND
            return SubState.Free, 0, 0
        elif self.name == CardName.k光帝クライス:
            card.pos = Position.GRAVEYARD
            return SubState.Draw, 1, 0
        elif self.name == CardName.sサイバーヴァリー:
            self.pos = Position.BANISHED
            card.pos = Position.BANISHED
            return SubState.Draw, 2, 0
        elif self.name == CardName.eエアーマン:
            card.pos = Position.HAND
            return SubState.Free, 0, 0
        elif self.name == CardName.k混沌の黒魔術師:
            card.pos = Position.HAND
            return SubState.Free, 0, -2000

        assert False, "not implemented {}".format(self.name)
        return SubState.Free, 0

    def effect0(self) -> Tuple[SubState, int]:

        assert False, "not implemented"
        return SubState.Free, 0

    def setMagic(self) -> None:
        assert self.pos == Position.HAND
        self.pos = Position.MAGIC_SET

    def isDhero(self) -> bool:
        return self.name == CardName.dドグマガイ or self.name == CardName.dディスクガイ

    def isLevel8(self) -> bool:
        return self.name == CardName.dドグマガイ or self.name == CardName.k混沌の黒魔術師

    def isMagic(self) -> bool:
        v = self.name.value
        return v >= CardName.aアームズホール.value and v <= CardName.n成金ゴブリン.value

    def isMonster(self) -> bool:
        v = self.name.value
        return v <= CardName.dディスクガイ.value

    def isWarrior(self) -> bool:
        return self.name in [CardName.dディスクガイ, CardName.eエアーマン,
                             CardName.k光帝クライス, CardName.dドグマガイ]

    def isMonsterSSable(self) -> bool:
        return self.isMonster() and self.name != CardName.dドグマガイ

    def isEquipSpell(self) -> bool:
        return self.name in [CardName.fフェニブレ, CardName.DDR, CardName.h早すぎた埋葬]

    def numOfEffectTarget(self) -> int:
        if self.name in [CardName.dディスクガイ, CardName.m名推理,
                         CardName.n成金ゴブリン, CardName.mマジカルエクスプロージョン]:
            return 0
        elif self.name in [CardName.fフェニブレ, CardName.DDR,
                           CardName.t手札断殺, CardName.s死者転生]:
            return 2
        return 1

    # 召喚できないなら-1を返す

    def numOfSacrifice(self) -> int:
        if self.name in [CardName.dディスクガイ,
                         CardName.sサイバーヴァリー, CardName.eエアーマン]:
            return 0
        elif self.name == CardName.k光帝クライス:
            return 1
        elif self.name == CardName.k混沌の黒魔術師:
            return 2
        else:
            return -1


dummyCard = Card(99, 0)
