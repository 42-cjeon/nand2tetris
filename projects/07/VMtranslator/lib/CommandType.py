from enum import Enum
class COMMANDTYPE(Enum):
    ARITHMETIC=0,
    PUSH=1,
    POP=2,
    LABEL=3,
    GOTO=4,
    IF=5,
    FUNCTION=6,
    RETURN=7,
    CALL=8