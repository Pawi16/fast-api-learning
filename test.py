from typing import Annotated


def double(x: Annotated[int, (0, 12)]) -> int:
    return x * 2


result = double(4)
print(result)
