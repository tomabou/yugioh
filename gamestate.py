from typing import List, Sequence, Iterable, Tuple
from substate import SubState
from card import (Card, CardName, Deck, name2id, Position,
                  dummyCard)
from action import (Action, DrawAction, EffectAction1,
                    EffectAction0, ArmsHoleAction2, EffectAction2,
                    MahousekiAction,
                    SummonAction0, SummonAction1, SummonAction2)

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

    def getSSMonster(self) -> List[Card]:
        ret = []
        for c in self.deck:
            if c.isMonsterSSable():
                ret.append(c)
        return ret

    def getSenshis(self) -> List[Card]:
        ret = []
        for c in self.deck:
            if c.name == CardName.eエアーマン or c.name == CardName.dディスクガイ:
                ret.append(c)
        return ret

    def getHeros(self) -> List[Card]:
        ret = []
        for c in self.deck:
            if c.name in [CardName.eエアーマン, CardName.dディスクガイ, CardName.dドグマガイ]:
                ret.append(c)
        return ret

    def getEquipSpell(self) -> List[Card]:
        ret = []
        for c in self.deck:
            if c.isEquipSpell():
                ret.append(c)
        return ret

    def _validActionsFree(self) -> Sequence[Action]:
        acs: List[Action] = []
        hands = self.getCardByPos(Position.HAND)
        phoenix = self.getCardsbyName(CardName.fフェニブレ)
        for c in (hands+phoenix):
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
            elif target_num == 2:
                target12s = self.getTarget2(c)
                for t1, t2 in target12s:
                    acs.append(EffectAction2(c, t1, t2))
        for c in hands:
            if self.hasNormalSummon:
                break
            sacNum = c.numOfSacrifice()
            if sacNum == 0:
                acs.append(SummonAction0(c))
            elif sacNum == 1:
                sacs = self.getSac1()
                for sac in sacs:
                    acs.append(SummonAction1(c, sac))
            elif sacNum == 2:
                sacabs = self.getSac2()
                for sac1, sac2 in sacabs:
                    acs.append(SummonAction2(c, sac1, sac2))
        return acs

    def _validActionsArms(self) -> Sequence[Action]:
        acs: List[Action] = []
        cards = filter(
            lambda c: (c.pos in [Position.DECK, Position.GRAVEYARD]),
            self.getEquipSpell())
        for c in cards:
            acs.append(ArmsHoleAction2(c))
        return acs

    def _validActionsAirMan(self) -> Sequence[Action]:
        acs: List[Action] = []
        c = self.getCardbyName(CardName.eエアーマン)
        targets = self.getTarget1(c)
        for t in targets:
            acs.append(EffectAction1(c, t))
        return acs

    def _validActionsKonKuro(self) -> Sequence[Action]:
        acs: List[Action] = []
        c = self.getCardbyName(CardName.k混沌の黒魔術師)
        targets = self.getTarget1(c)
        for t in targets:
            acs.append(EffectAction1(c, t))
        return acs

    def _validActionsKuraisu(self) -> Sequence[Action]:
        acs: List[Action] = []
        c = self.getCardbyName(CardName.k光帝クライス)
        targets1 = self.getTarget1(c)
        targets2 = self.getTarget2(c)
        for t in targets1:
            acs.append(EffectAction1(c, t))
        for t1, t2 in targets2:
            acs.append(EffectAction2(c, t1, t2))
        return acs

    def _validActionsMahouseki(self) -> Sequence[Action]:
        acs: List[Action] = []
        cards = self.getCardByPos(Position.TMP)
        assert len(cards) == 3
        if cards[0].name == CardName.m魔法石の採掘:
            c, t1, t2 = cards[0], cards[1], cards[2]
        elif cards[1].name == CardName.m魔法石の採掘:
            c, t1, t2 = cards[1], cards[0], cards[2]
        elif cards[2].name == CardName.m魔法石の採掘:
            c, t1, t2 = cards[2], cards[0], cards[1]
        targets = self.getTarget1(c)
        for t3 in targets:
            acs.append(MahousekiAction(c, t1, t2, t3))
        return acs

    def vaildActions(self) -> Sequence[Action]:
        if self.subState == SubState.Draw:
            return [DrawAction(self.drawNum)]
        elif self.subState == SubState.Free:
            return self._validActionsFree()
        elif self.subState == SubState.ArmsHole:
            return self._validActionsArms()
        elif self.subState == SubState.AirManSS:
            return self._validActionsAirMan()
        elif self.subState == SubState.KonKuroSS:
            return self._validActionsKonKuro()
        elif self.subState == SubState.KuraisuSS:
            return self._validActionsKuraisu()
        elif self.subState == SubState.Mahouseki:
            return self._validActionsMahouseki()
        return []

    def runAction(self, action: Action) -> None:
        if type(action) == DrawAction:
            self.draw(action.num)
        elif type(action) == ArmsHoleAction2:
            assert action.equip.pos in [Position.GRAVEYARD, Position.DECK]
            action.equip.pos = Position.HAND
        elif type(action) == EffectAction0:
            self.effect0(action.card)
        elif type(action) == EffectAction1:
            self.effect1(action.card, action.target)
        elif type(action) == EffectAction2:
            self.effect2(action.card, action.target1, action.target2)
        elif type(action) == SummonAction0:
            self.summon0(action.card)
        elif type(action) == SummonAction1:
            self.summon1(action.card, action.target)
        elif type(action) == SummonAction2:
            self.summon2(action.card, action.target1, action.target2)
        elif type(action) == MahousekiAction:
            self.effect3(action.card, action.t1,
                         action.t2, action.t3)
        else:
            assert False, "not implemented"

    def summon0(self, card: Card):
        card.pos = Position.MONSTER_FIELD
        if card.name == CardName.eエアーマン:
            self.subState = SubState.AirManSS

    def summon1(self, card, tag):
        card.pos = Position.MONSTER_FIELD
        tag.pos = Position.GRAVEYARD
        if card.name == CardName.k光帝クライス:
            self.subState = SubState.KuraisuSS

    def summon2(self, card, tag1, tag2):
        card.pos = Position.MONSTER_FIELD
        tag1.pos = Position.GRAVEYARD
        tag2.pos = Position.GRAVEYARD
        if card.name == CardName.k混沌の黒魔術師:
            self.subState = SubState.KonKuroSS

    def effect1(self, card: Card, target: Card) -> None:
        sub, num, lifedif = card.effect1(target)
        self.subState = sub
        self.drawNum = num
        self.life += lifedif

    def effect2(self, card: Card, target1: Card, target2: Card) -> None:
        sub, num, lifedif = card.effect2(target1, target2)
        self.subState = sub
        self.drawNum = num
        self.life += lifedif

    def effect3(self, card: Card, target1: Card,
                target2: Card, target3: Card) -> None:
        sub, num, lifedif = card.effect3(target1, target2, target3)
        self.subState = sub
        self.drawNum = num
        self.life += lifedif

    def effect0(self, card: Card) -> None:
        if card.name == CardName.t手札抹殺:
            card.pos = Position.GRAVEYARD
            self.effectMassatsu()
            return
        sub, num = card.effect0()
        self.subState = sub
        self.drawNum = num

# 対象を取らないのでgameState objectの外に出せなかった
    def effectMassatsu(self) -> None:
        num = 0
        for c in self.getCardByPos(Position.HAND):
            num += 1
            c.pos = Position.GRAVEYARD
        self.subState = SubState.Draw
        self.drawNum = num

    def getSac1(self) -> Iterable[Card]:
        mons = self.getCardByPos(Position.MONSTER_FIELD)
        return self.select1Util(mons)

    def getSac2(self) -> Iterable[Tuple[Card, Card]]:
        mons = self.getCardByPos(Position.MONSTER_FIELD)
        return self.select2Util(mons)

    def getTarget1(self, card: Card) -> Iterable[Card]:
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
        elif card.name == CardName.s死者蘇生 or card.name == CardName.h早すぎた埋葬:
            cs = self.getSSMonster()
            return filter(lambda c: c.pos == Position.GRAVEYARD, cs)
        elif card.name == CardName.z増援:
            cs = self.getSenshis()
            return filter(lambda c: c.pos == Position.DECK, cs)
        elif card.name == CardName.k光帝クライス:
            monsters = self.getCardByPos(Position.MONSTER_FIELD)
            return self.select1Util(monsters)
        elif card.name == CardName.sサイバーヴァリー:
            monsters = list(filter(lambda x: x != card,
                            self.getCardByPos(Position.MONSTER_FIELD)))
            return self.select1Util(monsters)
        elif card.name == CardName.eエアーマン:
            hearos = self.getHeros()
            targets = list(filter(lambda c: c.pos == Position.DECK, hearos))
            return self.select1Util(targets)
            # assert False, "not implemented"
        elif card.name in [CardName.k混沌の黒魔術師, CardName.m魔法石の採掘]:
            return self.select1Util(list(filter(
                lambda c: c.isMagic(),
                self.getCardByPos(Position.GRAVEYARD))))
        return ret

    def select2Util(self, cs: List[Card]) -> Iterable[Tuple[Card, Card]]:
        ret = []
        if len(cs) < 2:
            return []
        a = dummyCard
        b = dummyCard
        for i in range(len(cs)):
            if a.name == cs[i].name:
                continue
            for j in range(i+1, len(cs)):
                if b.name == cs[j].name:
                    continue
                a = cs[i]
                b = cs[j]
                ret.append((a, b))
        return ret

    def select1Util(self, cs: List[Card]) -> Iterable[Card]:
        ret = []
        if len(cs) < 1:
            return []
        a = dummyCard
        for i in range(len(cs)):
            if a.name == cs[i].name:
                continue
            a = cs[i]
            ret.append(a)
        return ret

    def getTarget2(self, card) -> Iterable[Tuple[Card, Card]]:
        ret: List[Tuple[Card, Card]] = []
        if card.name == CardName.fフェニブレ:
            cs = self.getCardByPos(Position.GRAVEYARD)
            tmp = list(filter(lambda c: c.isWarrior(), cs))
            return self.select2Util(tmp)
        elif card.name == CardName.t手札断殺:
            hands = self.getCardByPos(Position.HAND)
            tmp = list(filter(lambda x: x != card, hands))
            return self.select2Util(tmp)
        elif card.name == CardName.DDR:
            hands = self.getCardByPos(Position.HAND)
            tmp = list(filter(lambda x: x != card, hands))
            handcosts = self.select1Util(tmp)
            banishmonster = list(filter(lambda x: x.isMonsterSSable(),
                                        self.getCardByPos(Position.BANISHED)))
            target2 = self.select1Util(banishmonster)
            for a in handcosts:
                for b in target2:
                    ret.append((a, b))
            return ret
        elif card.name == CardName.s死者転生:
            hands = self.getCardByPos(Position.HAND)
            tmp = list(filter(lambda x: x != card, hands))
            handcosts = self.select1Util(tmp)
            gravemonster = list(filter(lambda x: x.isMonster(),
                                       self.getCardByPos(Position.GRAVEYARD)))
            target2 = self.select1Util(gravemonster)
            for a in handcosts:
                for b in target2:
                    ret.append((a, b))
            return ret
        elif card.name == CardName.k光帝クライス:
            monsters = self.getCardByPos(Position.MONSTER_FIELD)
            return self.select2Util(monsters)
        elif card.name == CardName.m魔法石の採掘:
            hands = self.getCardByPos(Position.HAND)
            tmp = list(filter(lambda x: x != card, hands))
            hand2costs = self.select2Util(tmp)
            return hand2costs
        return ret

    def canEffectMagic(self, card) -> bool:
        if card.pos != Position.HAND and card.pos != Position.MAGIC_SET:
            return False
        if card.pos == Position.HAND and self.getMagicFieldNum() >= 5:
            return False
        return True

    def canHandCost(self, card: Card, num: int) -> bool:
        hands = self.getCardByPos(Position.HAND)
        count = 0
        for h in hands:
            if h != card:
                count += 1
        return count >= num

    def canEffect(self, card: Card) -> bool:
        if self.subState != SubState.Free:
            return False

        # 魔法カードだったら一律に手札にあるか、魔法カードゾーンが空いているかチェック
        if card.isMagic() and card.name != CardName.fフェニブレ:
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
        elif card.name == CardName.s死者蘇生 or card.name == CardName.h早すぎた埋葬:
            cs = self.getSSMonster()
            for c in cs:
                if c.pos == Position.GRAVEYARD:
                    return True
            return False
        elif card.name == CardName.z増援:
            cs = self.getSenshis()
            for c in cs:
                if c.pos == Position.DECK:
                    return True
            return False
        elif card.name == CardName.fフェニブレ:
            if card.pos != Position.GRAVEYARD:
                return False
            cs = self.getCardByPos(Position.GRAVEYARD)
            tmp = list(filter(lambda c: c.isWarrior(), cs))
            if len(tmp) < 2:
                return False
            return True
        elif card.name == CardName.DDR:
            if not self.canHandCost(card, 1):
                return False
            cs = self.getSSMonster()
            for c in cs:
                if c.pos == Position.BANISHED:
                    return True
            return False
        elif card.name == CardName.t手札断殺:
            return self.canHandCost(card, 2)
        elif card.name == CardName.s死者転生:
            if not self.canHandCost(card, 1):
                return False
            cs = self.getCardByPos(Position.GRAVEYARD)
            for c in cs:
                if c.isMonster():
                    return True
            return False
        elif card.name == CardName.n成金ゴブリン:
            return True
        elif card.name == CardName.m名推理:
            cs = self.getCardByPos(Position.DECK)
            for c in cs:
                if c.isMonsterNSable():
                    return True
            return False
        elif card.name == CardName.mモンスターゲート:
            cs = self.getCardByPos(Position.DECK)
            for c in cs:
                if c.isMonsterNSable():
                    return True
            return False
        elif card.name == CardName.t手札抹殺:
            hand = self.getCardByPos(Position.HAND)
            deck = self.getCardByPos(Position.DECK)
            numHand = len(hand)-1 if card.pos == Position.HAND else len(hand)
            return numHand <= len(deck)
        elif card.name == CardName.m魔法石の採掘:
            if not self.canHandCost(card, 2):
                return False
            bs = self.getCardByPos(Position.GRAVEYARD)
            for c in bs:
                if c.isMagic():
                    return True
            return False

        return False
        # assert False, "encont not implemented card{}".format(card)

    def canSet(self, card) -> bool:
        if self.getMagicFieldNum() >= 5:
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

    def getCardsbyName(self, name) -> List[Card]:
        ret = []
        for c in self.deck:
            if c.name == name:
                ret.append(c)
        return ret
