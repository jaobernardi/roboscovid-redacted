from enum import Enum, auto

class CaseEvolution(Enum):
	RECOVERED = auto()
	DEAD = auto()
	ACTIVE = auto()


class PlaceType(Enum):
	STATE = auto()
	CITY = auto()
	STREETBLOCK = auto()
	HOSPITAL = auto()


class ActionType(Enum):
	SEND_MESSAGE = auto()