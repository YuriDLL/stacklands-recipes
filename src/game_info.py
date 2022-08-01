import csv
from dataclasses import dataclass
from typing import Any, Dict, List

from flask import url_for
from ruamel.yaml import YAML


class Cards:

    def __init__(self) -> None:
        self._prepare_cards()

    def get_card(self, name_key: str) -> Dict[str, Any]:
        return self.cards[name_key]

    def iterate(self):
        return self.cards.items()

    def _prepare_cards(self) -> None:
        self.cards: Dict[str, Dict[str, Any]] = {}
        self._load_csv('Boosters', image_spec=True)
        self._load_csv('Mobs', image_spec=False)
        self._load_csv('Resources', image_spec=False)
        self._load_csv('Structures', image_spec=False)
        self._load_csv('Food', image_spec=False)
        self._load_csv('Locations', image_spec=False)

    def _load_csv(self, category_name: str, image_spec: bool) -> None:
        with open(f'data/{category_name.lower()}.csv', 'r') as csv_file:
            resources = csv.DictReader(csv_file)
            for card in resources:
                name_key = self._get_url_name(card['name'])
                self.cards[name_key] = card
                self.cards[name_key]['category'] = category_name
                self.cards[name_key]['url'] = url_for('recipes', name=name_key)
                if image_spec:
                    img_name = self.cards[name_key].pop('image_name')
                else:
                    img_name = name_key
                self.cards[name_key]['png_url'] = url_for(
                    'static',
                    filename=f'img/{img_name}.png'
                )
                self.cards[name_key]['ico_url'] = url_for(
                    'static',
                    filename=f'icon/{img_name}.ico'
                )

    def _get_url_name(self, name: str) -> str:
        return name.lower().replace(' ', '_')


@dataclass
class Recipe:
    inputs: Dict[str, int]
    outputs: Dict[str, int]
    time: int  # sec
    place: str

    def to_dict(self, cards: Cards) -> Dict:
        return {
            'inp': [cards.get_card(card) | {'count': count}
                    for card, count in self.inputs.items()],
            'out': [cards.get_card(card) | {'count': count}
                    for card, count in self.outputs.items()],
            'time': self.time,
            'place': self.place
        }


def get_recipes(
        cards: Cards,
        input: str = None,
        output: str = None) -> List[dict]:
    with open('data/recipes.yaml', 'r') as file:
        recipes = YAML().load(file)
        if input:
            find_key = 'inp'
            value = input
        elif output:
            find_key = 'out'
            value = output
        else:
            return []
        recipes = [_fill_recipe_cards(recipe, cards) for recipe in recipes
                   if value in recipe[find_key]]
        return recipes


def _fill_recipe_cards(recipe: dict, cards: Cards) -> dict:
    recipe.items
    return {
        'inputs': [cards.get_card(card) | {'count': count}
                   for card, count in recipe['inp'].items()],
        'outputs': [cards.get_card(card) | {'count': count}
                    for card, count in recipe['out'].items()],
        'time': recipe['time'] if 'time' in recipe else None,
        'place': recipe['place'] if 'place' in recipe else 'Desk'
    }