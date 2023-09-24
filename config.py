from dataclasses import dataclass
from typing import List, Optional
import json

from dacite import from_dict

@dataclass
class Bot:
    token: str
    allowed_usernames: List[str]

@dataclass
class Config:
    bot: Bot

with open("config.json", encoding="ascii") as json_data_file:
    config = from_dict(data_class=Config, data=json.load(json_data_file))
