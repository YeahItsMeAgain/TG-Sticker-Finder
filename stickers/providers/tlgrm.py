from typing import List
from urllib.parse import quote_plus
import requests
from stickers.providers.provider import Provider
from stickers.sticker_pack import StickerPack


class Tlgrm(Provider):
    @staticmethod
    def _is_valid_url(url) -> bool:
        return requests.get(url, headers=Tlgrm.headers(), timeout=10).status_code == 200

    @staticmethod
    def _get_sticker_pack_image_url(sticker_pack_id: str) -> str:
        url = f"https://tlgrm.eu/_/stickers/{sticker_pack_id[:3]}/{sticker_pack_id[3:6]}/{sticker_pack_id}"

        if Tlgrm._is_valid_url(f"{url}/thumb48.webp"):
            return f"{url}/thumb48.webp"
        elif Tlgrm._is_valid_url(f"{url}/thumb48.jpg"):
            return f"{url}/thumb48.jpg"
        else:
            return "https://www.iconsdb.com/icons/preview/red/x-mark-xxl.png"

    @staticmethod
    def headers():
        return Provider.headers() | {
            "X-Typesense-Api-Key": "RGhGeG1DWG1jTExUem14YVM0a2wrQ2xtMXdDUVBaYXdidU12dFVHVHpCcz1lUmE4eyJleGNsdWRlX2ZpZWxkcyI6InRhZ3MifQ=="
        }

    @staticmethod
    def get_stickers(sticker_pack_name: str) -> List[StickerPack]:
        hits = (
            requests.get(
                f"https://typesense.tlgrm.app/collections/stickers/documents/search?q={quote_plus(sticker_pack_name)}&query_by=tokenized_name,tags&per_page=10&page=1&query_by_weights=120,50&sort_by=_text_match:desc,installs:desc,external:desc&filter_by=lang:[na,en,he]&highlight_fields=_&min_len_1typo=5&min_len_2typo=8",
                headers=Tlgrm.headers(),
                timeout=5,
            )
            .json()
            .get("hits")
        )
        if not hits:
            return []

        packs = [hit.get("document") for hit in hits]
        return [
            StickerPack(
                link=f"https://t.me/addstickers/{pack.get('link')}",
                name=pack.get("name_en"),
                image_url=Tlgrm._get_sticker_pack_image_url(pack.get("id")),
                animated=pack.get("is_animated") if pack.get("is_animated") else False,
            )
            for pack in packs
        ]
