import json
import time
from typing import Any
from access import AccessLvl
from Locale import get_locale, Locale


class Kachok:
    """Class that represents club members"""

    def __init__(self, alias: str, name: str, chat_id: int) -> None:
        """Initializes the member record (Kachok object)

        alias and name enough to initialize member, other information can be added later

        If name include * at the end this member is female
        Since there are very few women in the club, this is more convenient than adding methods

        Parameters
        ----------
        alias : str
            member's alias
        name : str
            member's name
        """
        if name[-1] == '*':
            self.female = True
            self.name = name[0:-1]
            self.name = name[:19]
        else:
            self.female = False
            self.name = name[:19]
        self.alias: str = alias
        """Telegram alias of club member"""
        self.chat_id = chat_id
        """user chat id of club member"""
        self.access: AccessLvl = AccessLvl.MEMBER
        """Member's current access level"""
        self.selfWeight: float = 100
        """Member's current self weight"""
        self.weights: dict = {'bench press': 0, 'squat': 0, 'biceps curl': 0}
        """Member's max weights in format exercise: weight"""
        self.proteinPoints: dict = {'bench press': 0, 'squat': 0, 'biceps curl': 0}
        """Member's max points in format exercise: points"""
        self.mark: str = "D"
        """Member's best grade"""

        # Hardcoded owner
        if alias == '@kupamonke' or alias == '@nerag0n7':
            self.access = AccessLvl.OWNER

    def __eq__(self, __value: object) -> bool:
        """Standart equals (==) function implementation"""
        return isinstance(__value, Kachok) and \
            self.alias == __value.alias and \
            self.name == __value.name and \
            self.chat_id == __value.chat_id and \
            self.female == __value.female and \
            self.access == __value.access and \
            self.selfWeight == __value.selfWeight and \
            self.weight == __value.weight and \
            self.proteinPoints == __value.proteinPoints and \
            self.mark == __value.mark

    def __ne__(self, __value: object) -> bool:
        """Standart not equals (!=) function implementation"""
        return not self == __value

    def make_female(self):
        """Switches the member's sex"""
        if not self.female:
            self.proteinPoints *= 1.64
            self.female = True
            self.grade()
        else:
            self.proteinPoints /= 1.64
            self.female = False
            self.grade()

    def grade(self):
        """Updates member's grade"""
        if self.proteinPoints < 0.55:
            self.mark = "D"
        elif self.proteinPoints < 0.7:
            self.mark = "C"
        elif self.proteinPoints < 0.85:
            self.mark = "B"
        else:
            self.mark = "A"

    def set_self_weight(self, weight: float | str) -> None:
        """Updates the member's self weight records

        Parameters
        ----------
        weight : float
            the participant's weight
        """
        weight = float(weight)
        self.selfWeight = weight

    def set_weight(self, weight: float | str, exercise: str):
        """Updates member's lifted weight records

        Parameters
        ----------
        weight : float | str
            The lifted weight
        exercise: str
            'bench press', 'squat' or 'biceps curl'
        """
        weight = float(weight)
        # Member's result updates if needed
        this_points = weight * 1.64 / self.selfWeight if self.female else weight / self.selfWeight
        if self.proteinPoints[exercise] <= this_points:
            self.proteinPoints[exercise] = this_points
            self.weights[exercise] = max(weight, self.weights[exercise])
        self.grade()

    def display(self) -> str:
        """String representation of the member on the top
        
        Returns
        -------
        str
            formatted short info on member
        """
        return f'{self.name} {self.alias} - {str(int(self.weight))}kg - {str(int(self.proteinPoints * 100))}PP ({self.mark})'

    def info(self, locale: str) -> str:
        """String representation of the member's personal info

        Parameters
        ----------
        locale : str
            User's locale country code

        Returns
        -------
        str
            formatted and localized short info on member
        """
        result = ['{} {} - {}\n{}: {}kg - {}PP ({})'.format(
            self.name, self.alias, ('M' if (not self.female) else 'F'),
            get_locale(locale).personal_best, str(self.weight), str(int(self.proteinPoints*100)), self.mark)]
        if (not self.proteinPointsByDate):
            result.append(get_locale(locale).no_weight)
            return '\n'.join(result)

        for k, v in self.proteinPointsByDate.items():
            result.append('{} {} {}kg {} {}PP'.format(
                str(k), get_locale(locale).info_history[0], str(self.weightByDate[k]),
                get_locale(locale).info_history[1], str(int(v*100))))

        return '\n'.join(result)


class KachokEncoder(json.JSONEncoder):
    """Kachok JSON Encoder class"""
    def default(self, obj):
        if isinstance(obj, Kachok):
            return obj.__dict__  # Convert Kachok object to a dictionary
        if isinstance(obj, list):
            return [self.default(item) for item in obj]  # Recursively encode list items
        if isinstance(obj, dict):
            return {k: self.default(v) for k, v in obj.items()}  # Recursively encode dictionary values
        return super().default(obj)


def kachok_decoder(jo: dict[str, Any]) -> Kachok:
    """Kachok JSON Decoder

    Parameters
    ----------
    jo : dict[str, Any]
        Loaded JavaScript object

    Returns
    -------
    Kachok
        Member's record
    """
    member = Kachok(jo['alias'].lower(), jo['name'])
    member.access = jo['access'] if 'access' in jo else AccessLvl.MEMBER
    member.female = jo['female'] if 'female' in jo else False
    member.selfWeight = jo['selfWeight'] if 'selfWeight' in jo else 100.0
    member.weight = jo['weight'] if 'weight' in jo else 0.0
    member.proteinPoints = jo['proteinPoints'] if 'proteinPoints' in jo else 0.0
    member.mark = jo['mark'].strip('()') if 'mark' in jo else 'D'
    member.proteinPointsByDate = jo['proteinPointsByDate'] if 'proteinPointsByDate' in jo else {}
    member.weightByDate = jo['weightByDate'] if 'weightByDate' in jo else {}
    member.selfWeightByDate = jo['selfWeightByDate'] if 'selfWeightByDate' in jo else {}

    if member.alias == '@kupamonke':
        member.access = AccessLvl.OWNER

    return member
