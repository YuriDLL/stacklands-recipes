from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, List

from flask import url_for


class Categories(Enum):
    Resources = auto()
    Enemies = auto()
    People = auto()


@dataclass
class Recepie:
    inputs: Dict[str, int]
    outputs: Dict[str, int]
    time: int  # sec
    palce: str


cards_templ = {
    'Wood': Categories.Resources,
    'Stone': Categories.Resources,
    'Bone': Categories.Resources,
    'Stick': Categories.Resources,

    'Villager': Categories.People,

    'Wolf': Categories.Enemies
}


def get_categories_names() -> List[str]:
    return [name.name for name in Categories]


def get_cards() -> Dict[str, dict]:
    return {
        _get_url_name(card): _card_info(card, cards_templ[card])
        for card in cards_templ
    }


def _card_info(name: str, catrgory: Categories) -> dict:
    card_url = '/recipes/' + _get_url_name(name)
    card_png_url = url_for('static', filename=_get_url_name(name) + '.png')
    return {
        'name': name,
        'url': card_url,
        'png_url': card_png_url,
        'category': catrgory.name
    }


def _get_url_name(name: str) -> str:
    return name.lower().replace(' ', '_')


recipes_list = [
    Recepie(
        inputs={'Villager': 2, 'Wood': 2},
        outputs={'Stick': 1},
        time=30,
        palce='Desc')
]
