from dataclasses import dataclass


@dataclass(frozen=True)
class Locale:
    greet: list[str] = ['']
    schedule: str = ''
    pp: str = ''
    command_unknown: str = ''
    newMemberSuccess: str = ''
    alreadyRegistred: str = ''
    emptyTop: str = ''
    goodPhoto: str = ''
    regProblem: str = ''
    commands: list[str] = ['']
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
    long_name: str = ''
    reg: str = ''
