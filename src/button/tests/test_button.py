from src.button import Button


def testInitButton():
    try:
        button = Button(text="Test")
    except:
        assert False
    else:
        assert True


def testButtonPos():
    btn = Button(text="Test", pos=(10, 20))
    assert btn.rect.x == 10 and btn.rect.y == 20


def testButtonSize():
    btn = Button(text="Test", size=(10, 20))
    assert btn.rect.w == 10 and btn.rect.h == 20
