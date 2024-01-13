# TODO translate bot to English
from dataclasses import dataclass
from LocaleBase import Locale


@dataclass(frozen=True)
class LocaleEN(Locale):
    greet: str = ''
    schedule_: str = ''
    pp: str = ''
    empty: str = ''
    newMemberSuccess: str = ''
    newMemberFail: str = ''
    emptyTop: str = ''
    goodPhoto: str = ''
    regProblem: str = ''
    commands: str = ''
    nikulin: str = ''
    enter_alias: str = ''
    enter_name: str = ''
    enter_self_weight: str = ''
    enter_weight: str = ''
    not_registered: str = ''
    accessDenied: str = ''
    deleting: str = ''
    success: str = ''
    exception: str = ''
    weight_format: str = ''
    making_woman: str = ''
    no_spaces: str = ''
    long_name: str = ''
    reg: str = ''
