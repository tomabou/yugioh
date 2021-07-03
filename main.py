from action import DrawAction
from substate import SubState
from gamestate import GameState
from card import Deck, CardName, Position, checkDeck


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
    # print(gameState)

    print("run arums test")


def test5():
    gameState = GameState(Deck)
    a = gameState.getCardbyName(CardName.s死者蘇生)
    a.pos = Position.HAND
    b = gameState.getCardbyName(CardName.dディスクガイ)
    b.pos = Position.GRAVEYARD
    assert gameState.canEffect(a)
    acs = gameState.vaildActions()
    assert len(acs) == 1
    gameState.runAction(acs[0])
    assert a.pos == Position.GRAVEYARD
    assert b.pos == Position.MONSTER_FIELD

    print("run sosei test")


def test6():
    gameState = GameState(Deck)
    a = gameState.getCardbyName(CardName.h早すぎた埋葬)
    a.pos = Position.HAND
    b = gameState.getCardbyName(CardName.dディスクガイ)
    b.pos = Position.GRAVEYARD
    assert gameState.canEffect(a)
    acs = gameState.vaildActions()
    assert len(acs) == 1
    gameState.runAction(acs[0])
    assert a.pos == Position.MAGIC_FIELD
    assert b.pos == Position.MONSTER_FIELD

    print("run hayamai test")


def test7():
    gameState = GameState(Deck)
    a = gameState.getCardbyName(CardName.z増援)
    a.pos = Position.HAND
    assert gameState.canEffect(a)
    acs = gameState.vaildActions()
    gameState.runAction(acs[0])
    assert a.pos == Position.GRAVEYARD
    assert len(gameState.getCardByPos(Position.HAND)) == 1

    print("run zoen test")


def test8():
    gameState = GameState(Deck)
    cs = gameState.getEquipSpell()
    tmp = gameState.select2Util(cs)
    assert len(tmp) == 5

    print("run select2 test")


def test9():
    gameState = GameState(Deck)
    a = gameState.getCardbyName(CardName.fフェニブレ)
    a.pos = Position.GRAVEYARD
    assert not gameState.canEffect(a)
    b = gameState.getCardbyName(CardName.dディスクガイ)
    b.pos = Position.GRAVEYARD
    assert not gameState.canEffect(a)
    c = gameState.getCardbyName(CardName.k光帝クライス)
    c.pos = Position.GRAVEYARD
    assert gameState.canEffect(a)
    acs = gameState.vaildActions()
    gameState.runAction(acs[0])
    assert a.pos == Position.HAND
    assert b.pos == Position.BANISHED
    assert c.pos == Position.BANISHED

    print("run feni test")


def test10():
    gameState = GameState(Deck)
    a = gameState.getCardbyName(CardName.DDR)
    a.pos = Position.HAND
    assert not gameState.canEffect(a)
    b = gameState.getCardbyName(CardName.s死者蘇生)
    b.pos = Position.HAND
    assert not gameState.canEffect(a)
    c = gameState.getCardbyName(CardName.k光帝クライス)
    c.pos = Position.BANISHED
    assert gameState.canEffect(a)
    acs = gameState.vaildActions()
    gameState.runAction(acs[0])
    assert a.pos == Position.MAGIC_FIELD, "pos is {}".format(a.pos)
    assert b.pos == Position.GRAVEYARD
    assert c.pos == Position.MONSTER_FIELD

    print("run DDR test")


def test11():
    gameState = GameState(Deck)
    a = gameState.getCardbyName(CardName.s死者転生)
    a.pos = Position.HAND
    assert not gameState.canEffect(a)
    b = gameState.getCardbyName(CardName.s死者蘇生)
    b.pos = Position.HAND
    assert not gameState.canEffect(a)
    c = gameState.getCardbyName(CardName.k光帝クライス)
    c.pos = Position.GRAVEYARD
    assert gameState.canEffect(a)
    acs = gameState.vaildActions()
    gameState.runAction(acs[0])
    assert a.pos == Position.GRAVEYARD, "pos is {}".format(a.pos)
    assert b.pos == Position.GRAVEYARD
    assert c.pos == Position.HAND

    print("run tensei test")


def test12():
    gameState = GameState(Deck)
    a = gameState.getCardbyName(CardName.t手札断殺)
    a.pos = Position.HAND
    assert not gameState.canEffect(a)
    b = gameState.getCardbyName(CardName.s死者蘇生)
    b.pos = Position.HAND
    assert not gameState.canEffect(a)
    c = gameState.getCardbyName(CardName.DDR)
    c.pos = Position.HAND
    assert gameState.canEffect(a)
    acs = gameState.vaildActions()
    gameState.runAction(acs[0])
    assert gameState.subState == SubState.Draw, "state is {}".format(
        gameState.subState)
    acs = gameState.vaildActions()
    gameState.runAction(acs[0])
    assert a.pos == Position.GRAVEYARD, "pos is {}".format(a.pos)
    assert b.pos == Position.GRAVEYARD
    assert c.pos == Position.GRAVEYARD
    assert len(gameState.getCardByPos(Position.HAND)) == 2

    print("run dansatsu test")


def test13():
    gs = GameState(Deck)
    a = gs.getCardbyName(CardName.dディスクガイ)
    a.pos = Position.HAND
    acs = gs.vaildActions()
    assert len(acs) == 1, "{}".format(len(acs))
    gs.runAction(acs[0])
    assert a.pos == Position.MONSTER_FIELD
    print("disc summon test")


def test14():
    gs = GameState(Deck)
    a = gs.getCardbyName(CardName.k混沌の黒魔術師)
    a.pos = Position.HAND
    acs = gs.vaildActions()
    assert len(acs) == 0, "{}".format(len(acs))
    b = gs.getCardbyName(CardName.eエアーマン)
    b.pos = Position.MONSTER_FIELD
    acs = gs.vaildActions()
    assert len(acs) == 0, "{}".format(len(acs))
    c = gs.getCardbyName(CardName.k光帝クライス)
    c.pos = Position.MONSTER_FIELD
    acs = gs.vaildActions()
    assert len(acs) == 1, "{}".format(len(acs))

    gs.runAction(acs[0])
    assert a.pos == Position.MONSTER_FIELD
    assert b.pos == Position.GRAVEYARD
    assert c.pos == Position.GRAVEYARD
    print("kon summon test")


def test15():
    gs = GameState(Deck)
    b = gs.getCardbyName(CardName.k光帝クライス)
    b.pos = Position.HAND
    acs = gs.vaildActions()
    assert len(acs) == 0, "{}".format(len(acs))
    c = gs.getCardbyName(CardName.eエアーマン)
    c.pos = Position.MONSTER_FIELD
    acs = gs.vaildActions()
    assert len(acs) == 1, "{}".format(len(acs))

    gs.runAction(acs[0])
    assert b.pos == Position.MONSTER_FIELD
    assert c.pos == Position.GRAVEYARD
    print("kura summon test")


def test16():
    gameState = GameState(Deck)
    a = gameState.getCardbyName(CardName.s死者蘇生)
    a.pos = Position.HAND
    b = gameState.getCardbyName(CardName.dディスクガイ)
    b.pos = Position.GRAVEYARD
    assert gameState.canEffect(a)
    acs = gameState.vaildActions()
    assert len(acs) == 1
    gameState.runAction(acs[0])
    assert a.pos == Position.GRAVEYARD
    assert b.pos == Position.MONSTER_FIELD
    assert len(gameState.vaildActions()) == 1
    assert type(gameState.vaildActions()[0]) == DrawAction

    print("run disk sosei test")


def test17():
    gs = GameState(Deck)
    b = gs.getCardbyName(CardName.k光帝クライス)
    b.pos = Position.HAND
    acs = gs.vaildActions()
    assert len(acs) == 0, "{}".format(len(acs))
    c = gs.getCardbyName(CardName.eエアーマン)
    c.pos = Position.MONSTER_FIELD
    acs = gs.vaildActions()
    assert len(acs) == 1, "{}".format(len(acs))

    gs.runAction(acs[0])
    assert b.pos == Position.MONSTER_FIELD
    assert c.pos == Position.GRAVEYARD
    c.pos = Position.MONSTER_FIELD
    assert gs.subState == SubState.KuraisuSS
    assert len(gs.vaildActions()) == 3

    print("run kuraisu test")


def test18():
    gs = GameState(Deck)
    a = gs.getCardbyName(CardName.t手札抹殺)
    b = gs.getCardbyName(CardName.dドグマガイ)
    c = gs.getCardbyName(CardName.k光帝クライス)
    a.pos = Position.HAND
    b.pos = Position.HAND
    c.pos = Position.HAND
    acs = gs.vaildActions()
    assert len(acs) == 1
    gs.runAction(acs[0])
    assert a.pos == Position.GRAVEYARD
    assert len(gs.getCardByPos(Position.GRAVEYARD)) == 3
    assert gs.subState == SubState.Draw
    assert gs.drawNum == 2
    print("run massatsu test")


def test19():
    gs = GameState(Deck)
    x = gs.getCardbyName(CardName.m魔法石の採掘)
    a = gs.getCardbyName(CardName.t手札抹殺)
    b = gs.getCardbyName(CardName.dドグマガイ)
    c = gs.getCardbyName(CardName.k光帝クライス)
    x.pos = Position.HAND
    a.pos = Position.GRAVEYARD
    b.pos = Position.HAND
    c.pos = Position.HAND
    acs = gs.vaildActions()
    assert len(acs) == 1
    gs.runAction(acs[0])
    assert gs.subState == SubState.Mahouseki
    acs = gs.vaildActions()
    assert len(acs) == 1
    gs.runAction(acs[0])
    assert gs.subState == SubState.Free
    assert x.pos == Position.GRAVEYARD
    assert a.pos == Position.HAND
    assert b.pos == Position.GRAVEYARD
    assert c.pos == Position.GRAVEYARD
    print("run mahouseki test")


def test():
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()
    test8()
    test9()
    test10()
    test11()
    test12()
    test13()
    test14()
    test15()
    test16()
    test17()
    test18()
    test19()


def main():
    checkDeck()
    gameState = GameState(Deck)
    gameState.draw(6)
    print(gameState)

    test()


if __name__ == '__main__':
    main()
