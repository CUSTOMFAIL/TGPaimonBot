from enum import Enum
from typing import Optional

from typing_extensions import Self

from modules.wiki.base import HONEY_HOST

__all__ = [
    "Element",
    "WeaponType",
    "AttributeType",
    "Association",
]


class Element(Enum):
    """element"""

    Pyro = "fire"
    Hydro = "Water"
    Electro = "Thunder"
    Cryo = "ice"
    Dendro = "grass"
    Anemo = "Wind"
    Geo = "rock"
    Multi = "none" # main character


_WEAPON_ICON_MAP = {
    "Sword": HONEY_HOST.join("img/s_23101.png"),
    "Claymore": HONEY_HOST.join("img/s_163101.png"),
    "Polearm": HONEY_HOST.join("img/s_233101.png"),
    "Catalyst": HONEY_HOST.join("img/s_43101.png"),
    "Bow": HONEY_HOST.join("img/s_213101.png"),
}


class WeaponType(Enum):
    """Weapon Type"""

    Sword = "One-Handed Sword"
    Claymore = "two-handed sword"
    Polearm = "Polearm"
    Catalyst = "Magic"
    Bow = "Bow"

    def icon_url(self) -> str:
        return str(_WEAPON_ICON_MAP.get(self.name))


_ATTR_TYPE_MAP = {
    # This dictionary is used to convert the abbreviated characters of attributes encountered in Honey pages to characters of AttributeType
    # For example, HP% written on the Honey page corresponds to HP_p
    "HP": ["Health"],
    "HP_p": ["HP%", "Health %"],
    "ATK": ["Attack"],
    "ATK_p": ["Atk%", "Attack %"],
    "DEF": ["Defense"],
    "DEF_p": ["Def%", "Defense %"],
    "EM": ["Elemental Mastery"],
    "ER": ["ER%", "Energy Recharge %"],
    "CR": ["CrR%", "Critical Rate %", "CritRate%"],
    "CD": ["Crd%", "Critical Damage %", "CritDMG%"],
    "PD": ["Phys%", "Physical Damage %"],
    "HB": [],
    "Pyro": [],
    "Hydro": [],
    "Electro": [],
    "Cryo": [],
    "Dendro": [],
    "Anemo": [],
    "Geo": [],
}


class AttributeType(Enum):
    """Attribute enumeration class. Contains attributes of weapons and relics."""

    HP = "Life"
    HP_p = "Life %"
    ATK = "Attack Power"
    ATK_p = "Attack Power%"
    DEF = "Defense Strength"
    DEF_p = "Defense %"
    EM = "Elemental Mastery"
    ER = "Elemental Charge Efficiency"
    CR = "Crit Chance"
    CD = "Critical Damage"
    PD = "Physical Damage Bonus"
    HB = "Healing Bonus"
    Pyro = "Fire Elemental Damage Bonus"
    Hydro = "Water Elemental Damage Bonus"
    Electro = "Lightning Elemental Damage Bonus"
    Cryo = "Ice Elemental Damage Bonus"
    Dendro = "Grass Elemental Damage Bonus"
    Anemo = "Wind Elemental Damage Bonus"
    Geo = "Rock Elemental Damage Bonus"

    @classmethod
    def convert(cls, string: str) -> Optional[Self]:
        string = string.strip()
        for k, v in _ATTR_TYPE_MAP.items():
            if string == k or string in v or string.upper() == k:
                return cls[k]


_ASSOCIATION_MAP = {
    "Other": ["Mainactor", "Ranger", "Fatui"],
    "Snezhnaya": [],
    "Sumeru": [],
    "Inazuma": [],
    "Liyue": [],
    "Mondstadt": [],
}


class Association(Enum):
    """The region the character belongs to"""

    Other = "Other"
    Snezhnaya = "Winter"
    Sumeru = "Sumi"
    Inazuma = "Inazuma"
    Liyue = "Liyue"
    Mondstadt = "Mondstadt"

    @classmethod
    def convert(cls, string: str) -> Optional[Self]:
        string = string.strip()
        for k, v in _ASSOCIATION_MAP.items():
            if string == k or string in v:
                return cls[k]
            string = string.lower().title()
            if string == k or string in v:
                return cls[k]
        return cls[string]
