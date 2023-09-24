from typing import List
from itertools import chain, zip_longest
import concurrent.futures


from stickers.sticker_pack import StickerPack

from .combot import Combot
from .tlgrm import Tlgrm


def find_sticker_packs(sticker_pack_name: str) -> List[StickerPack]:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(Tlgrm.get_stickers, sticker_pack_name),
            executor.submit(Combot.get_stickers, sticker_pack_name),
        ]

        return set(
            [
                sticker_pack
                for sticker_pack in list(
                    chain.from_iterable(
                        zip_longest(*[future.result() for future in futures])
                    )
                )
                if sticker_pack
            ]
        )
