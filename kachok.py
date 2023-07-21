import time
import json
from access import AccessLvl


class Kachok:
    """class for all club members"""
    # alias and name enough to initialize member, other information can be added later
    def __init__(self, alias, name):
        # If name include * at the end this member is female
        # Since there are very few women in the club, this is more convenient than adding methods
        if name[-1] == '*':
            self.female = True
            self.name = name[0, -1]
        else:
            self.female = False
            self.name = name

        # Telegram alias of club member
        self.alias = alias
        # Member's current access level
        self.access = AccessLvl.MEMBER
        # Member's current self weight
        self.selfWeight = 100
        # Member's max weight
        self.weight = 0
        # Member's max points
        self.proteinPoints = 0
        # Member's best grade
        self.mark = "(D)"
        # Dictionary of points in format date:points
        self.proteinPointsByDate = {}
        # Dictionary of weights in format date:points
        self.weightByDate = {}
        # Hardcoded owner
        if alias == '@kupamonke':
            self.access = AccessLvl.OWNER

    def make_female(self):
        """function that can be helpful if * forgotten while adding female member"""
        if not self.female:
            self.proteinPoints *= 1.64
            for i in self.proteinPointsByDate:
                self.proteinPointsByDate[i] *= 1.64
            self.female = True
            self.grade()

    def make_male(self):
        """function that can be helpful if extra * added while adding male member"""
        if self.female:
            self.proteinPoints /= 1.64
            for i in self.proteinPointsByDate:
                self.proteinPointsByDate[i] /= 1.64
            self.female = False
            self.grade()

    def grade(self):
        """function that update member grade"""
        if self.proteinPoints < 0.8:
            self.mark = "(D)"
        elif self.proteinPoints < 1:
            self.mark = "(C)"
        elif self.proteinPoints < 1.2:
            self.mark = "(B)"
        else:
            self.mark = "(A)"

    def set_self_weight(self, weight):
        """function that update member self weight"""
        # since new self weight not taken into account for previous results not so many actions needed
        self.selfWeight = float(weight)

    def set_weight(self, weight):
        """function that update member weight"""
        # Member's max weight updates if needed
        self.weight = max(float(weight), self.weight)
        # Member's max points updates if needed
        if self.female:
            self.proteinPoints = max(self.proteinPoints, float(weight)*1.64 / self.selfWeight)
        else:
            self.proteinPoints = max(self.proteinPoints, float(weight)/self.selfWeight)
        # the current date is taken
        date = time.strftime("%d/%m/%Y")
        if date not in self.weightByDate:
            self.weightByDate[date] = float(weight)
            self.proteinPointsByDate[date] = float(weight) / self.selfWeight
            if self.female:
                self.proteinPointsByDate[date] *= 1.64
        else:
            self.weightByDate[date] = max(float(weight), self.weightByDate[date])
            if not self.female:
                if float(weight) / self.selfWeight > self.proteinPointsByDate[date]:
                    self.proteinPointsByDate[date] = float(weight) / self.selfWeight
            else:
                if float(weight) * 1.64 / self.selfWeight > self.proteinPointsByDate[date]:
                    self.proteinPointsByDate[date] = float(weight) * 1.64 / self.selfWeight
        self.grade()

    def set_name(self, name):
        """function that change member name"""
        self.name = name

    def display(self):
        """function that display necessary information about member, using in displaying top"""
        information_1 = self.name + ' ' + self.alias + ' - ' + str(int(self.weight)) + ' kg - '
        information_2 = str(int(self.proteinPoints * 100)) + ' PP ' + self.mark
        information = information_1 + information_2
        return information
    def profile(self):
        info1 = self.name + ' ' + self.alias + '\n'
        info2 = ''
        for i in self.proteinPointsByDate:
            info2 += str(i) + ' ты пожал ' + str(self.weightByDate[i]) + ' и набрал ' + str(int(self.proteinPointsByDate[i]*100)) + 'PP\n'
        info = info1 + info2
        return info


class KachokEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Kachok):
            return obj.__dict__  # Convert Kachok object to a dictionary
        if isinstance(obj, list):
            return [self.default(item) for item in obj]  # Recursively encode list items
        if isinstance(obj, dict):
            return {k: self.default(v) for k, v in obj.items()}  # Recursively encode dictionary values
        return super().default(obj)


def kachok_decoder(jo) -> Kachok:
    member = Kachok(jo['alias'], jo['name'])
    member.access = jo['access'] if 'access' in jo else AccessLvl.MEMBER 
    member.female = jo['female'] if 'female' in jo else False
    member.selfWeight = jo['selfWeight'] if 'selfWeight' in jo else 100.0
    member.weight = jo['weight'] if 'weight' in jo else 0.0
    member.proteinPoints = jo['proteinPoints'] if 'proteinPoints' in jo else 0.0
    member.mark = jo['mark'] if 'mark' in jo else '(D)'
    member.proteinPointsByDate = jo['proteinPointsByDate'] if 'proteinPointsByDate' in jo else {}
    member.weightByDate = jo['weightByDate'] if 'weightByDate' in jo else {}
    return member
