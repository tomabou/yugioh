from __future__ import annotations
from collections.abc import Iterable, Sequence
from enum import Enum
from typing import List, Tuple, Union
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

    def effect1(self, card) -> Tuple[SubState, int]:
        if self.name == CardName.dデステニードロー:
            assert self.pos == Position.HAND or Position.MAGIC_SET
            self.pos = Position.GRAVEYARD
            assert card.pos == Position.HAND
            assert card.isDhero()
            card.pos = Position.GRAVEYARD
            return SubState.Draw, 2
        elif self.name == CardName.tトレードイン:
            assert self.pos == Position.HAND or Position.MAGIC_SET
            self.pos = Position.GRAVEYARD
            assert card.pos == Position.HAND
            assert card.isLevel8()
            card.pos = Position.GRAVEYARD
            return SubState.Draw, 2
        elif self.name == CardName.aアームズホール:
            assert self.pos == Position.HAND or Position.MAGIC_SET
            self.pos = Position.GRAVEYARD
            assert card.pos == Position.DECK
            card.pos = Position.GRAVEYARD
            return SubState.ArmsHole, 0

        assert False, "not implemented"
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

    def isEquipSpell(self) -> bool:
        return self.name in [CardName.fフェニブレ, CardName.DDR, CardName.h早すぎた埋葬]

    def numOfEffectTarget(self) -> int:
        if self.name in [CardName.dディスクガイ, CardName.m名推理,
                         CardName.n成金ゴブリン, CardName.mマジカルエクスプロージョン]:
            return 0
        elif self.name in [CardName.fフェニブレ, CardName.DDR,
                           CardName.t手札抹殺, CardName.s死者転生]:
            return 2
        return 1


class EffectAction0():
    def __init__(self, card: Card) -> None:
        self.card = card


class EffectAction1():
    def __init__(self, card: Card, target: Card) -> None:
        self.card = card
        self.target = target


class EffectAction2():
    def __init__(self, card: Card, t1: Card, t2: Card) -> None:
        self.card = card
        self.target1 = t1
        self.target2 = t2


class DrawAction():
    def __init__(self, n) -> None:
        self.num = n


class ArmsHoleAction2():
    def __init__(self, card) -> None:
        self.equip = card


Action = Union[EffectAction0, EffectAction1,
               EffectAction2, DrawAction, ArmsHoleAction2]


class SubState(Enum):
    Free = 0
    ArmsHole = 1
    Draw = 2


class GameState:
    def __init__(self, deckList) -> None:
        self.deck: List[Card] = []
        self.subState: SubState = SubState.Free
        self.drawNum: int = 0
        deckpos = 0
        for k in CardName:
            for j in range(Deck[k]):
                self.deck.append(Card(name2id(k), deckpos))
                deckpos += 1
        self.life: int = 8000
        self.hasNormalSummon: bool = False

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

    def getCardByPos(self, pos: Position) -> List[Card]:
        ret = []
        for c in self.deck:
            if c.pos == pos:
                ret.append(c)
        return ret

    def getMagicFieldNum(self) -> int:
        a = len(self.getCardByPos(Position.MAGIC_FIELD))
        b = len(self.getCardByPos(Position.MAGIC_SET))
        return a + b

    def getEquipSpell(self) -> List[Card]:
        ret = []
        for c in self.deck:
            if c.isEquipSpell():
                ret.append(c)
        return ret

    def vaildActions(self) -> Sequence[Action]:
        if self.subState == SubState.Draw:
            return [DrawAction(self.drawNum)]
        elif self.subState == SubState.Free:
            acs: List[Action] = []
            hands = self.getCardByPos(Position.HAND)
            for c in hands:
                flag = self.canEffect(c)
                if not flag:
                    continue
                target_num = c.numOfEffectTarget()
                if target_num == 0:
                    acs.append(EffectAction0(c))
                elif target_num == 1:
                    targets = self.getTarget1(c)
                    for tag in targets:
                        acs.append(EffectAction1(c, tag))

            return acs
        elif self.subState == SubState.ArmsHole:
            acs = []
            cards = filter(
                lambda c: (c.pos in [Position.DECK, Position.GRAVEYARD]),
                self.getEquipSpell())
            for c in cards:
                acs.append(ArmsHoleAction2(c))
            return acs
        return []

    def runAction(self, action: Action) -> None:
        if type(action) == DrawAction:
            self.draw(action.num)
        elif type(action) == ArmsHoleAction2:
            card = action.equip
            assert card.pos in [Position.GRAVEYARD, Position.DECK]
            card.pos = Position.HAND
        elif type(action) == EffectAction0:
            card = action.card
            self.effect0(card)
        elif type(action) == EffectAction1:
            card = action.card
            target = action.target
            self.effect1(card, target)

    def effect1(self, card: Card, target: Card) -> None:
        sub, num = card.effect1(target)
        self.subState = sub
        self.drawNum = num

    def effect0(self, card: Card) -> None:
        sub, num = card.effect0()
        self.subState = sub
        self.drawNum = num

    def getTarget1(self, card) -> Iterable[Card]:
        ret = []
        if card.name == CardName.dデステニードロー:
            if card.pos != Position.HAND and card.pos != Position.MAGIC_SET:
                return []
            hands = self.handCards()
            for c in hands:
                if c.isDhero():
                    ret.append(c)
            return ret
        elif card.name == CardName.tトレードイン:
            if card.pos != Position.HAND and card.pos != Position.MAGIC_SET:
                return []
            hands = self.handCards()
            for c in hands:
                if c.isLevel8():
                    ret.append(c)
            return ret
        elif card.name == CardName.aアームズホール:
            target = random.choice(self.getCardByPos(Position.DECK))
            ret = [target]
        return ret

    def canEffectMagic(self, card) -> bool:
        if card.pos != Position.HAND and card.pos != Position.MAGIC_SET:
            return False
        if card.pos == Position.HAND and self.getMagicFieldNum() >= 5:
            return False
        return True

    def canEffect(self, card) -> bool:
        if self.subState != SubState.Free:
            return False
        if card.isMagic():
            if not self.canEffectMagic(card):
                return False

        if card.name == CardName.dデステニードロー:
            hands = self.handCards()
            for c in hands:
                if c.isDhero():
                    return True
            return False
        elif card.name == CardName.tトレードイン:
            hands = self.handCards()
            for c in hands:
                if c.isLevel8():
                    return True
            return False
        elif card.name == CardName.aアームズホール:
            if len(self.deckCards()) == 0:
                return False
            return any(map(
                lambda c: (c.pos in [Position.DECK, Position.GRAVEYARD]),
                self.getEquipSpell()))

        assert False, "encont not implemented card"

    def canSet(self, card) -> bool:
        fieldCards = self.getCardByPos(Position.MAGIC_SET)
        assert len(fieldCards) <= 5
        if len(fieldCards) == 5:
            return False
        if card.pos != Position.HAND:
            return False
        return True

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
        assert False, "getCardERROR"


def test1():
    gameState = GameState(Deck)
    d = gameState.getCardbyName(CardName.dデステニードロー)
    disk = gameState.getCardbyName(CardName.dディスクガイ)
    assert not gameState.canEffect(d)
    d.pos = Position.HAND
    disk.pos = Position.HAND
    cs = gameState.canEffect(d)
    assert cs, "canEffect is {}".format(cs)
    d.effect1(disk)
    assert d.pos == Position.GRAVEYARD
    assert disk.pos == Position.GRAVEYARD
    print("run デステニードロー test")


def test2():
    gameState = GameState(Deck)
    d = gameState.getCardbyName(CardName.tトレードイン)
    disk = gameState.getCardbyName(CardName.k混沌の黒魔術師)
    assert not gameState.canEffect(d)
    d.pos = Position.HAND
    disk.pos = Position.HAND
    cs = gameState.canEffect(d)
    assert cs, "canEffect is {}".format(cs)
    d.effect1(disk)
    assert d.pos == Position.GRAVEYARD
    assert disk.pos == Position.GRAVEYARD
    print("run トレードイン test")


def test3():
    gameState = GameState(Deck)
    d = gameState.getCardbyName(CardName.dデステニードロー)
    disk = gameState.getCardbyName(CardName.dディスクガイ)
    d.pos = Position.HAND
    disk.pos = Position.HAND
    d.setMagic()
    assert d.pos == Position.MAGIC_SET
    assert gameState.canEffect(d)
    d.effect1(disk)
    assert d.pos == Position.GRAVEYARD
    assert disk.pos == Position.GRAVEYARD
    print("run set test")


def test4():
    gameState = GameState(Deck)
    a = gameState.getCardbyName(CardName.aアームズホール)
    a.pos = Position.HAND
    acs = gameState.vaildActions()
    assert gameState.canEffect(a)
    assert len(acs) == 1
    gameState.runAction(acs[0])
    acs = gameState.vaildActions()
    gameState.runAction(acs[0])
    assert a.pos == Position.GRAVEYARD
    print(gameState)

    print("run arums test")


def test():
    test1()
    test2()
    test3()
    test4()


def main():
    checkDeck()
    gameState = GameState(Deck)
    gameState.draw(6)
    print(gameState)

    test()


if __name__ == '__main__':
    main()
