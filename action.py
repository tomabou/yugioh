from card import Card
from typing import Union


class EffectAction0():
    def __init__(self, card: Card) -> None:
        self.card = card

    def __repr__(self) -> str:
        return "effect 0 {}".format(self.card.name)


class EffectAction1():
    def __init__(self, card: Card, target: Card) -> None:
        self.card = card
        self.target = target

    def __repr__(self) -> str:
        return "effect 1 {} {}".format(self.card.name, self.target.name)


class EffectAction2():
    def __init__(self, card: Card, t1: Card, t2: Card) -> None:
        self.card = card
        self.target1 = t1
        self.target2 = t2

    def __repr__(self) -> str:
        return "effect 2 {} {} {}".format(self.card.name,
                                          self.target1.name, self.target2.name)


class DrawAction():
    def __init__(self, n) -> None:
        self.num = n

    def __repr__(self) -> str:
        return "draw {}".format(self.num)


class ArmsHoleAction2():
    def __init__(self, card: Card) -> None:
        self.equip = card

    def __repr__(self) -> str:
        return "arms hole {}".format(self.equip.name)


# エアーマン　ヴァリー　ディスクガイ
class SummonAction0():
    def __init__(self, card) -> None:
        self.card = card

    def __repr__(self) -> str:
        return "Summon {}".format(self.card.name)

# クライス


class SummonAction1():
    def __init__(self, card: Card, tage: Card) -> None:
        self.card = card
        self.target = tage

    def __repr__(self) -> str:
        return "Summon {} {} ".format(self.card.name, self.target.name)


# こんくろ
class SummonAction2():
    def __init__(self, card: Card, tage1: Card, tage2: Card) -> None:
        self.card = card
        self.target1 = tage1
        self.target2 = tage2

    def __repr__(self) -> str:
        return "Summon kura {} {} ".format(self.target1.name,
                                           self.target2.name)


Action = Union[EffectAction0, EffectAction1,
               EffectAction2, DrawAction, ArmsHoleAction2,
               SummonAction0, SummonAction1, SummonAction2]
