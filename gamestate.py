from typing import List, Sequence, Iterable
from substate import SubState
from card import Card, CardName, Deck, name2id, Position
from action import (Action, DrawAction, EffectAction1,
                    EffectAction0, ArmsHoleAction2)

import random


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
