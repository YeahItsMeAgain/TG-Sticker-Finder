from typing import List
from urllib.parse import quote_plus
import requests
from bs4 import BeautifulSoup
from stickers.providers.provider import Provider

from stickers.sticker_pack import StickerPack


class Combot(Provider):
    @staticmethod
    def get_stickers(sticker_pack_name: str) -> List[StickerPack]:
        html = requests.get(
            f"https://combot.org/telegram/stickers?q={quote_plus(sticker_pack_name)}",
            headers=Combot.headers(),
            timeout=5
        )
        soup = BeautifulSoup(html.content, "html.parser")
        sticker_pack_list = soup.find(class_="sticker-packs-list")

        sticker_packs = []
        for sticker_pack in sticker_pack_list.find_all(
            class_="sticker-pack sticker-packs-list__item"
        ):
            sticker_packs.append(
                StickerPack(
                    name=sticker_pack.find(class_="sticker-pack__title").get_text(),
                    link=sticker_pack.find("a", class_="sticker-pack__btn").get("href"),
                    image_url=sticker_pack.find(class_="sticker-pack__sticker-img").get(
                        "data-src"
                    ),
                    animated=False,
                )
            )

        return sticker_packs
