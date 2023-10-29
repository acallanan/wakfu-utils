import base2048
import enum
import struct
from typing import NamedTuple


class Slots(enum.IntEnum):
    R = 0
    W = 1
    G = 2
    B = 3
    RW = 4
    GR = 5
    BR = 6
    GW = 7
    BW = 8
    BG = 9
    GRW = 10
    BRW = 11
    BGR = 12
    BGW = 13
    BGRW = 14
    unset = 15


class Elements(enum.IntEnum):
    A = 0
    E = 1
    F = 2
    W = 3
    AW = 4
    EA = 5
    EW = 6
    FA = 7
    FE = 8
    FW = 9
    EAW = 10
    FAW = 11
    FEA = 12
    FEW = 13
    unset = 15


class ClassName(enum.IntEnum):
    Feca = 0
    Osa = 1
    Enu = 2
    Sram = 3
    Xel = 4
    Eca = 5
    Eni = 6
    Iop = 7
    Cra = 8
    Sadi = 9
    Sac = 10
    Panda = 11
    Rogue = 12
    Masq = 13
    Ougi = 14
    Fog = 15
    Elio = 16
    Hupper = 17


class Stats(NamedTuple):
    percent_hp: int
    res: int
    barrier: int
    heals_rec: int
    armor: int
    elemental_mastery: int
    melee_mastery: int
    distance_mastery: int
    hp: int
    lock: int
    dodge: int
    initiative: int
    lockdodge: int
    fow: int
    crit: int
    block: int
    crit_mastery: int
    rear_mastery: int
    berserk_mastery: int
    healing_mastery: int
    rear_resistence: int
    critical_resistence: int
    ap: bool
    mp: bool
    ra: bool
    wp: bool
    control: bool
    di: bool
    major_res: bool


class Item(NamedTuple):
    item_id: int
    slots: Slots
    sublimation: int
    assigned_mastery: Elements
    assigned_res: Elements
    ...  # todo, slot stats


class Build(NamedTuple):
    classname: ClassName
    level: int
    stats: Stats
    relic_sub: int
    epic_sub: int
    items: list[Item]


def v1_pack_build(build: Build) -> bytes:

    return struct.pack(
        "!bbb22b7?HH%s" % ("HBHBB" * len(build.items)), 1, build.classname, build.level, *build.stats, build.relic_sub, build.epic_sub, *build.items
    )

def v1_encode_build(build: Build) -> str:
    packed = v1_pack_build(build)
    return base2048.encode(packed)


def decode_build(build_str: str) -> Build:

    decoded = base2048.decode(build_str)
    
    offset = 36
    version, cl, lv, *stats, rs, es, item_len = struct.unpack_from("!bbb22b7?HH", decoded)
    if version != 1:  # expand as needed
        msg = "Unknown build version."
        raise RuntimeError(msg)
    # split per version later, as needed.
    items: list[Item] = []
    for _ in range(item_len):
        iid, slts, sub, am, ar = struct.unpack_from("!HBHBB", decoded, offset)
        items.append(Item(iid, Slots(slts), sub, Elements(am), Elements(ar)))
        offset += 7

    return Build(ClassName(cl), lv, Stats(*stats), rs, es, items)