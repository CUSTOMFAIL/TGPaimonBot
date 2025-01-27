import re
from typing import List, Optional, Tuple, Union

from bs4 import BeautifulSoup
from httpx import URL

from modules.wiki.base import HONEY_HOST, WikiModel

all = ["Material"]

WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


class Material(WikiModel):
    # noinspection PyUnresolvedReferences
    """Weapons, character training materials

    Attributes:
        type: type
        weekdays: Weekly opening hours
        source: method of obtaining
        description: describe
    """
    type: str
    source: Optional[List[str]] = None
    weekdays: Optional[List[int]] = None
    description: str

    @staticmethod
    def scrape_urls() -> List[URL]:
        weapon = [HONEY_HOST.join(f"fam_wep_{i}/?lang=CHS") for i in ["primary", "secondary", "common"]]
        talent = [HONEY_HOST.join(f"fam_talent_{i}/?lang=CHS") for i in ["book", "boss", "common", "reward"]]
        return weapon + talent

    @classmethod
    async def get_name_list(cls, *, with_url: bool = False) -> List[Union[str, Tuple[str, URL]]]:
        return list(sorted(set(await super(Material, cls).get_name_list(with_url=with_url)), key=lambda x: x[0]))

    @classmethod
    async def _parse_soup(cls, soup: BeautifulSoup) -> "Material":
        """Parse the breakthrough material page"""
        soup = soup.select(".wp-block-post-content")[0]
        tables = soup.find_all("table")
        table_rows = tables[0].find_all("tr")

        def get_table_row(target: str):
            """A convenience function that returns the text in the last cell of the corresponding row of the corresponding table header"""
            for row in table_rows:
                if target in row.find("td").text:
                    return row.find_all("td")[-1]

        def get_table_text(row_num: int) -> str:
            """A convenience function that returns the text in the last cell of the corresponding row of the table"""
            return table_rows[row_num].find_all("td")[-1].text.replace("\xa0", "")

        id_ = re.findall(r"/img/(.*?)\.webp", str(table_rows[0]))[0]
        name = get_table_text(0)
        rarity = len(table_rows[3].find_all("img"))
        type_ = get_table_text(1)
        if (item_source := get_table_row("Item Source")) is not None:
            item_source = list(
                # filter The role here is to filter out empty data
                filter(lambda x: x, item_source.encode_contents().decode().split(""))
            )
        if (alter_source := get_table_row("Alternative Item")) is not None:
            alter_source = list(
                # filter The role here is to filter out empty data
                filter(lambda x: x, alter_source.encode_contents().decode().split(""))
            )
        source = list(sorted(set((item_source or []) + (alter_source or []))))
        if (weekdays := get_table_row("Weekday")) is not None:
            weekdays = [*(WEEKDAYS.index(weekdays.text.replace("\xa0", "").split(",")[0]) + 3 * i for i in range(2)), 6]
        description = get_table_text(-1)
        return Material(
            id=id_, name=name, rarity=rarity, type=type_, description=description, source=source, weekdays=weekdays
        )

    @property
    def icon(self) -> str:
        return str(HONEY_HOST.join(f"/img/{self.id}.webp"))
