import re
from typing import List, Optional

from bs4 import BeautifulSoup
from httpx import URL

from modules.wiki.base import Model, HONEY_HOST
from modules.wiki.base import WikiModel
from modules.wiki.other import Association, Element, WeaponType


class Birth(Model):
    """Birthday
    Attributes:
        day: day
        month: month
    """

    day: int
    month: int


class CharacterAscension(Model):
    """Breakthrough material for characters

    Attributes:
        level: level breakthrough material
        skill: Skill/talent training materials
    """

    level: List[str] = []
    skill: List[str] = []


class CharacterState(Model):
    """Role attribute value

    Attributes:
        level: level
        HP: life
        ATK: Attack Power
        DEF: Defense
        CR: Critical Strike Chance
        CD: Crit Damage
        bonus: Breakthrough attribute
    """

    level: str
    HP: int
    ATK: float
    DEF: float
    CR: str
    CD: str
    bonus: str


class CharacterIcon(Model):
    icon: str
    side: str
    gacha: str
    splash: Optional[str]


class Character(WikiModel):
    """Role
    Attributes:
        title: title
        occupation: belonging to
        association: region
        weapon_type: weapon type
        element: element
        birth: birthday
        constellation: the seat of fate
        cn_cv: Middle match
        jp_cv: Japanese match
        en_cv: British match
        kr_cv: Korean partner
        description: description
    """

    id: str
    title: str
    occupation: str
    association: Association
    weapon_type: WeaponType
    element: Element
    birth: Optional[Birth]
    constellation: str
    cn_cv: str
    jp_cv: str
    en_cv: str
    kr_cv: str
    description: str
    ascension: CharacterAscension

    stats: List[CharacterState]

    @classmethod
    def scrape_urls(cls) -> List[URL]:
        return [HONEY_HOST.join("fam_chars/?lang=CHS")]

    @classmethod
    async def _parse_soup(cls, soup: BeautifulSoup) -> "Character":
        """Analysis role page"""
        soup = soup.select(".wp-block-post-content")[0]
        tables = soup.find_all("table")
        table_rows = tables[0].find_all("tr")

        def get_table_text(row_num: int) -> str:
            """A shortcut function to return the text in the last cell of the corresponding row of the table"""
            return table_rows[row_num].find_all("td")[-1].text.replace("\xa0", "")

        id_ = re.findall(r"img/(.*?_\d+)_.*", table_rows[0].find("img").attrs["src"])[0]
        name = get_table_text(0)
        if name != "traveler": # if the character name is not a traveler
            title = get_table_text(1)
            occupation = get_table_text(2)
            association = Association.convert(get_table_text(3).lower().title())
            rarity = len(table_rows[4].find_all("img"))
            weapon_type = WeaponType[get_table_text(5)]
            element = Element[get_table_text(6)]
            birth = Birth(day=int(get_table_text(7)), month=int(get_table_text(8)))
            constellation = get_table_text(10)
            cn_cv = get_table_text(11)
            jp_cv = get_table_text(12)
            en_cv = get_table_text(13)
            kr_cv = get_table_text(14)
        else:
            name = "empty" if id_.endswith("5") else "fluorescence"
            title = get_table_text(0)
            occupation = get_table_text(1)
            association = Association.convert(get_table_text(2).lower().title())
            rarity = len(table_rows[3].find_all("img"))
            weapon_type = WeaponType[get_table_text(4)]
            element = Element[get_table_text(5)]
            birth = None
            constellation = get_table_text(7)
            cn_cv = get_table_text(8)
            jp_cv = get_table_text(9)
            en_cv = get_table_text(10)
            kr_cv = get_table_text(11)
        description = get_table_text(-3)
        ascension = CharacterAscension(
            level=[
                target[0]
                for i in table_rows[-2].find_all("a")
                if (target := re.findall(r"/(.*)/", i.attrs["href"])) # filter out wrong material (bug of honey web page)
            ],
            skill=[re.findall(r"/(.*)/", i.attrs["href"])[0] for i in table_rows[-1].find_all("a")],
        )
        stats = []
        for row in tables[2].find_all("tr")[1:]:
            cells = row.find_all("td")
            stats.append(
                CharacterState(
                    level=cells[0].text,
                    HP=cells[1].text,
                    ATK=cells[2].text,
                    DEF=cells[3].text,
                    CR=cells[4].text,
                    CD=cells[5].text,
                    bonus=cells[6].text,
                )
            )
        return Character(
            id=id_,
            name=name,
            title=title,
            occupation=occupation,
            association=association,
            weapon_type=weapon_type,
            element=element,
            birth=birth,
            constellation=constellation,
            cn_cv=cn_cv,
            jp_cv=jp_cv,
            rarity=rarity,
            en_cv=en_cv,
            kr_cv=kr_cv,
            description=description,
            ascension=ascension,
            stats=stats,
        )

     @classmethod
     async def get_url_by_name(cls, name: str) -> Optional[URL]:
         # The purpose of overriding this function is to handle the ID of the main character's name
         _map = {"Ying": "playergirl_007", "empty": "playerboy_005"}
         if (id_ := _map.get(name)) is not None:
             return await cls.get_url_by_id(id_)
         return await super(Character, cls).get_url_by_name(name)

     @property
     def icon(self) -> CharacterIcon:
         return CharacterIcon(
             icon=str(HONEY_HOST.join(f"/img/{self.id}_icon.webp")),
             side=str(HONEY_HOST.join(f"/img/{self.id}_side_icon.webp")),
             gacha=str(HONEY_HOST.join(f"/img/{self.id}_gacha_card.webp")),
             splash=str(HONEY_HOST.join(f"/img/{self.id}_gacha_splash.webp")),
         )
