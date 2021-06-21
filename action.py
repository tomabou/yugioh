from card import Card
from typing import Union


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
