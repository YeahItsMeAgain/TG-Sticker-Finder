from abc import abstractmethod


from typing import List

from stickers.sticker_pack import StickerPack
from fake_useragent import UserAgent


class Provider:
    @staticmethod
    @abstractmethod
    def get_stickers(sticker_pack_name: str) -> List[StickerPack]:
        ...

    @staticmethod
    def headers():
        return {
            "User-Agent": UserAgent(browsers=['chrome'], os=["windows"]).random
        }
