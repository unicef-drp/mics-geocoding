from ast import Return
from enum import Enum, auto


class ErrorCode(Enum):
    SUCCESS = 0

    # TEST
    ERROR_1 = auto()


ErrorDisplayString = {
    ErrorCode.SUCCESS: "",
    ErrorCode.ERROR_1: "This is case 1"
}
