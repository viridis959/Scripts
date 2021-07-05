import sys
from typing import Union


def to_str(num: Union[int, float]) -> str:
    return '{:,}'.format(num)


def increment(value: int) -> int:
    return value + 1


def pipe(value: int, *args) -> int:
    for func in args:
        value = func(value)
    return value


def main():
    # 1.
    print(to_str(9527))
    print(to_str(3345678))
    print(to_str(-1234.45))

    # 2.
    print(pipe(5, increment))
    print(pipe(5, increment, increment, increment))

    # 3.
    """
    1.最簡單的方法就是幫伺服器加RAM，不過需要耗費設備成本。
    2.假如是讀取速度太慢的話，我會針對經常讀取的欄位加index，以增加讀取的速度，但由於每次寫入都需要
      再寫入index那個table，而導致寫入速度變慢。
    3.以batch的方式寫入資料，可以提升寫入的效率。
    """


if __name__ == "__main__":
    main()
