import enum


class Channel(enum.IntFlag):
    r = 0b0001
    g = 0b0010
    b = 0b0100
    a = 0b1000
    all = 0b1111
    hint = 0b0000
