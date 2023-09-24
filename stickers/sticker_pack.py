from dataclasses import dataclass


@dataclass
class StickerPack:
    link: str
    image_url: str
    description: str
    name: str

    def __init__(self, link: str, image_url: str, name: str, animated: bool):
        self.link = link
        self.image_url = image_url
        self.name = name
        self.description = f"Animated: {animated}"

    def __hash__(self):
        return hash(self.link)

    def __eq__(self, other):
        return self.link == other.link
