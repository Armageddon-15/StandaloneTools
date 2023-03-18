import enum


class Channel(enum.IntFlag):
    r = 0b0001
    g = 0b0010
    b = 0b0100
    a = 0b1000
    all = 0b1111
    hint = 0b0000


class Bit(enum.IntFlag):
    U8 = 0b001
    U16 = 0b010
    U16_1 = 0b011
    F32 = 0b100
    hint = 0


class Format(enum.IntFlag):
    jpg = 1
    png = 2
    tga = 3
    webp = 4
    hint = 0
