from enum import IntEnum, auto


class AccessLvl(IntEnum):
    MEMBER = 0
    VIP = auto()
    OWNER = auto()
    

def access_from_str(s) -> AccessLvl:
    match s.upper():
        case AccessLvl.MEMBER.name:
            return AccessLvl.MEMBER
        case AccessLvl.VIP.name:
            return AccessLvl.VIP
        case AccessLvl.OWNER.name:
            return AccessLvl.OWNER
        case _:
            return AccessLvl.MEMBER


def has_access(memebers, alias, lvl) -> bool:
    if lvl == AccessLvl.MEMBER:
        return True
    if alias[0] != '@':
        alias = '@' + alias
    if alias not in memebers:
        return False
    return memebers[alias].access >= lvl
