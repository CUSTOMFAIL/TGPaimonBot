import enum

class FightProp(enum.Enum):

    BASE_HP = "Base HP"

    FIGHT_PROP_BASE_ATTACK = "Base Attack Power"

    FIGHT_PROP_BASE_DEFENSE = "Base Defense"

    FIGHT_PROP_BASE_HP = "Base HP"

    FIGHT_PROP_ATTACK = "Attack Power"

    FIGHT_PROP_ATTACK_PERCENT = "Attack Power Percentage"

    FIGHT_PROP_HP = "HP"

    FIGHT_PROP_HP_PERCENT = "Percent Health"

    FIGHT_PROP_DEFENSE = "Defense"

    FIGHT_PROP_DEFENSE_PERCENT = "Defense Percentage"

    FIGHT_PROP_ELEMENT_MASTERY = "Elemental Mastery"

    FIGHT_PROP_CRITICAL = "Critical Chance"

    FIGHT_PROP_CRITICAL_HURT = "Critical Damage"

    FIGHT_PROP_CHARGE_EFFICIENCY = "Elemental Charge Efficiency"

    FIGHT_PROP_FIRE_SUB_HURT = "Fire Resistance"

    FIGHT_PROP_ELEC_SUB_HURT = "Lightning Resistance"

    FIGHT_PROP_ICE_SUB_HURT = "Ice Elemental Resistance"

    FIGHT_PROP_WATER_SUB_HURT = "Water Resistance"

    FIGHT_PROP_WIND_SUB_HURT = "Wind Resistance"

    FIGHT_PROP_ROCK_SUB_HURT = "Rock Resistance"

    FIGHT_PROP_GRASS_SUB_HURT = "Grass Elemental Resistance"

    FIGHT_PROP_FIRE_ADD_HURT = "Fire Elemental Damage Bonus"

    FIGHT_PROP_ELEC_ADD_HURT = "Lightning Elemental Damage Bonus"

    FIGHT_PROP_ICE_ADD_HURT = "Ice Elemental Damage Bonus"

    FIGHT_PROP_WATER_ADD_HURT = "Water Elemental Damage Bonus"

    FIGHT_PROP_WIND_ADD_HURT = "Wind Elemental Damage Bonus"

    FIGHT_PROP_ROCK_ADD_HURT = "Rock Elemental Damage Bonus"

    FIGHT_PROP_GRASS_ADD_HURT = "Grass Elemental Damage Bonus"

    FIGHT_PROP_PHYSICAL_ADD_HURT = "Physical Damage Bonus"

    FIGHT_PROP_HEAL_ADD = "Healing Bonus"

class FightPropScore(enum.Enum):

    _value_: float

    value: float

    FIGHT_PROP_BASE_ATTACK = 1

    FIGHT_PROP_BASE_DEFENSE = 1

    FIGHT_PROP_BASE_HP = 1

    FIGHT_PROP_ATTACK = 662 / 3110 # attack power

    FIGHT_PROP_ATTACK_PERCENT = 4 / 3 # attack power percentage

    FIGHT_PROP_HP = 662 / 47800 # health

    FIGHT_PROP_HP_PERCENT = 4 / 3 # health percentage

    FIGHT_PROP_DEFENSE = 662 / 3890 # Defense

    FIGHT_PROP_DEFENSE_PERCENT = 662 / 583 # Defense percentage

    FIGHT_PROP_ELEMENT_MASTERY = 1 / 3 # Elemental Mastery

    FIGHT_PROP_CRITICAL = 2 # crit chance

    FIGHT_PROP_CRITICAL_HURT = 1 # crit damage

    FIGHT_PROP_CHARGE_EFFICIENCY = 662 / 518 # Elemental charge efficiency

    FIGHT_PROP_FIRE_SUB_HURT = 1

    FIGHT_PROP_ELEC_SUB_HURT = 1

    FIGHT_PROP_ICE_SUB_HURT = 1

    FIGHT_PROP_WATER_SUB_HURT = 1

    FIGHT_PROP_WIND_SUB_HURT = 1

    FIGHT_PROP_ROCK_SUB_HURT = 1

    FIGHT_PROP_GRASS_SUB_HURT = 1

    FIGHT_PROP_FIRE_ADD_HURT = 1

    FIGHT_PROP_ELEC_ADD_HURT = 1

    FIGHT_PROP_ICE_ADD_HURT = 1

    FIGHT_PROP_WATER_ADD_HURT = 1

    FIGHT_PROP_WIND_ADD_HURT = 1

    FIGHT_PROP_ROCK_ADD_HURT = 1

    FIGHT_PROP_GRASS_ADD_HURT = 1

    FIGHT_PROP_PHYSICAL_ADD_HURT = 1

    FIGHT_PROP_HEAL_ADD = 1
