import itertools
import re
from typing import List, Optional, Tuple, Union

from bs4 import BeautifulSoup
from httpx import URL

from modules.wiki.base import Model, HONEY_HOST, WikiModel
from modules.wiki.other import AttributeType, WeaponType

__all__ = ["Weapon", "WeaponAffix", "WeaponAttribute"]


class WeaponAttribute(Model):
    """Weapon entry"""

    type: AttributeType
    value: str


class WeaponAffix(Model):
    """Weapon Skills

    Attributes:
        name: skill name
        description: skill description

    """

    name: str
    description: List[str]


class WeaponState(Model):
    level: str
    ATK: float
    bonus: Optional[str]


class WeaponIcon(Model):
    icon: str
    awakened: str
    gacha: str


class Weapon(WikiModel):
    """arms

    Attributes:
        weapon_type: weapon type
        attack: base attack power
        attribute:
        affix: weapon skill
        description: description
        ascension: breakthrough material
        story: weapon story
    """

    weapon_type: WeaponType
    attack: float
    attribute: Optional[WeaponAttribute]
    affix: Optional[WeaponAffix]
    description: str
    ascension: List[str]
    story: Optional[str]

    stats: List[WeaponState]

    @staticmethod
    def scrape_urls() -> List[URL]:
        return [HONEY_HOST.join(f"fam_{i.lower()}/?lang=CHS") for i in WeaponType.__members__]

    @classmethod
    async def _parse_soup(cls, soup: BeautifulSoup) -> "Weapon":
        """Analysis weapon page"""
        soup = soup.select(".wp-block-post-content")[0]
        tables = soup.find_all("table")
        table_rows = tables[0].find_all("tr")

        def get_table_text(row_num: int) -> str:
            """A shortcut function to return the text in the last cell of the corresponding row of the table"""
            return table_rows[row_num].find_all("td")[-1].text.replace("\xa0", "")

        def find_table(select: str):
            """A shortcut function to find the table corresponding to the table header"""
            return list(filter(lambda x: select in " ".join(x.attrs["class"]), tables))

        id_ = re.findall(r"/img/(.*?)_gacha", str(table_rows[0]))[0]
        weapon_type = WeaponType[get_table_text(1).split(",")[-1].strip()]
        name = get_table_text(0)
        rarity = len(table_rows[2].find_all("img"))
        attack = float(get_table_text(4))
        ascension = [re.findall(r"/(.*)/", tag.attrs["href"])[0] for tag in table_rows[-1].find_all("a")]
        if rarity > 2: # if it is a weapon of 3 stars and above
            attribute = WeaponAttribute(
                type=AttributeType.convert(tables[2].find("thead").find("tr").find_all("td")[2].text.split(" ")[1]),
                value=get_table_text(6),
            )
            affix = WeaponAffix(
                name=get_table_text(7), description=[i.find_all("td")[1].text for i in tables[3].find_all("tr")[1:]]
            )
            description = get_table_text(-1) if len(tables) < 11 else get_table_text(9)
            if story_table := find_table("quotes"):
                story = story_table[0].text.strip()
            else:
                story = None
        else: # If it is a weapon of 2 stars and below
            attribute=affix=None
            description = get_table_text(5)
            story = tables[-1].text.strip()
        stats = []
        for row in tables[2].find_all("tr")[1:]:
            cells = row.find_all("td")
            if rarity > 2:
                stats.append(WeaponState(level=cells[0].text, ATK=cells[1].text, bonus=cells[2].text))
            else:
                stats.append(WeaponState(level=cells[0].text, ATK=cells[1].text))
        return Weapon(
            id=id_,
            name=name,
            rarity=rarity,
            attack=attack,
            attribute=attribute,
            affix=affix,
            weapon_type=weapon_type,
            story=story,
            stats=stats,
            description=description,
            ascension=ascension,
        )

    @classmethod
    async def get_name_list(cls, *, with_url: bool = False) -> List[Union[str, Tuple[str, URL]]]:
        # The purpose of rewriting this function is to de-duplicate the name. For example, there are three ""One Heart" Famous Swords in the one-handed sword page.
        name_list = [i async for i in cls._name_list_generator(with_url=with_url)]
        if with_url:
            return [(i[0], list(i[1])[0][1]) for i in itertools.groupby(name_list, lambda x: x[0])]
        else:
            return [i[0] for i in itertools.groupby(name_list, lambda x: x)]

    @property
    def icon(self) -> WeaponIcon:
        return WeaponIcon(
            icon=str(HONEY_HOST.join(f"/img/{self.id}.webp")),
            awakened=str(HONEY_HOST.join(f"/img/{self.id}_awaken_icon.webp")),
            gacha=str(HONEY_HOST.join(f"/img/{self.id}_gacha_icon.webp")),
        )
