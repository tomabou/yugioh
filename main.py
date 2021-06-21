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
