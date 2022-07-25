from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, List

from flask import url_for


class Categories(Enum):
    Resources = auto()
    Enemies = auto()
    People = auto()


@dataclass
class Recipe:
    inputs: Dict[str, int]
    outputs: Dict[str, int]
    time: int  # sec
    place: str

    def to_dict(self) -> Dict:
        return {
            'inputs': [_card_info(card) | {'count': count}
                       for card, count in self.inputs.items()],
            'outputs': [_card_info(card) | {'count': count}
                        for card, count in self.outputs.items()],
            'time': self.time,
            'place': self.place
        }


cards_tem = {
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
        _get_url_name(card): _card_info(card)
        for card in cards_tem
    }


def _card_info(name: str) -> dict:
    card_url = '/recipes/' + _get_url_name(name)
    card_png_url = url_for('static', filename=_get_url_name(name) + '.png')
    return {
        'name': name,
        'url': card_url,
        'png_url': card_png_url,
        'category': cards_tem[name].name
    }


def _get_url_name(name: str) -> str:
    return name.lower().replace(' ', '_')


def _get_name(url_name: str) -> str:
    splits = url_name.split('_')
    name = ''
    for split in splits:
        name += split[0].upper() + split[1:] + ' '
    name = name[:-1]
    return name


def get_recipes(input: str = None, output: str = None) -> List[dict]:
    recipes = []
    if input:
        input = _get_name(input)
        recipes = [recipe.to_dict() for recipe in recipes_list
                   if input in recipe.inputs]
    elif output:
        output = _get_name(output)
        print(output)
        recipes = [recipe.to_dict() for recipe in recipes_list
                   if output in recipe.outputs]
    return recipes


recipes_list = [
    Recipe(
        inputs={'Villager': 1, 'Wood': 2},
        outputs={'Stick': 1},
        time=30,
        place='Desk'),
    Recipe(
        inputs={'Wood': 3},
        outputs={'Stick': 2},
        time=10,
        place='Desk')
]
