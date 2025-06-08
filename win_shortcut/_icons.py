__all__ = [
    'pifmgr',
    'PIFMGR_DLL',
]

from pathlib import Path

PIFMGR_DLL = Path('pifmgr.dll')

class PifMgr:
    def __init__(self) -> None:
        self.dll = PIFMGR_DLL

        self.MS_DOS = (self.dll, 0)
        self.UMBRELLA = (self.dll, 1)
        self.TOY_BLOCK = (self.dll, 2)
        self.NEWSPAPER = (self.dll, 3)
        self.APPLE = (self.dll, 4)
        self.LIGHTNING = (self.dll, 5)
        self.EUPHONIUM = (self.dll, 6)
        self.BEACH_BALL = (self.dll, 7)
        self.LIGHTBULB = (self.dll, 8)
        self.COLUMN = (self.dll, 9)
        self.MONEY = (self.dll, 10)
        self.COMPUTER = (self.dll, 11)
        self.KEYBOARD = (self.dll, 12)
        self.FILING_CABINET = (self.dll, 13)
        self.BOOK = (self.dll, 14)
        self.PAPERS_WITH_CLIP = (self.dll, 15)
        self.PAPER_WITH_CRAYON = (self.dll, 16)
        self.PENCIL = (self.dll, 17)
        self.PAPER_WITH_PENCIL = (self.dll, 18)
        self.DICE = (self.dll, 19)
        self.WINDOWS = (self.dll, 20)
        self.SEARCH = (self.dll, 21)
        self.DOMINO = (self.dll, 22)
        self.CARDS = (self.dll, 23)
        self.FOOTBALL = (self.dll, 24)
        self.DOCTORS_BAG = (self.dll, 25)
        self.WIZARD_HAT = (self.dll, 26)
        self.RACECAR = (self.dll, 27)
        self.SHIP = (self.dll, 28)
        self.PLANE = (self.dll, 29)
        self.BOAT = (self.dll, 30)
        self.TRAFFIC_LIGHT = (self.dll, 31)
        self.RABBIT = (self.dll, 32)
        self.RADAR = (self.dll, 33)
        self.SWORDS = (self.dll, 34)
        self.SHIELD_WITHSWORD = (self.dll, 35)
        self.MACE = (self.dll, 36)
        self.DYNAMITE = (self.dll, 37)

pifmgr = PifMgr()
