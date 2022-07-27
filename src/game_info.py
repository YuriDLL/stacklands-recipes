import csv
from dataclasses import dataclass
from typing import Any, Dict, List

from flask import url_for


class Cards:

    def __init__(self) -> None:
        self._prepare_cards()

    def get_card(self, name_key: str) -> Dict[str, Any]:
        return self.cards[name_key]

    def iterate(self):
        return self.cards.items()

    def _prepare_cards(self) -> None:
        self.cards: Dict[str, Dict[str, Any]] = {}
        with open('data/boosters.csv', 'r') as csv_file:
            boosters = csv.DictReader(csv_file)
            for card in boosters:
                name_key = self._get_url_name(card['name'])
                self.cards[name_key] = card
                self.cards[name_key]['category'] = 'Boosters'
                self.cards[name_key]['url'] = '/recipes/'+name_key
                self.cards[name_key]['png_url'] = url_for(
                    'static',
                    filename=f"img/{card['image_name']}.png"
                )
        with open('data/resources.csv', 'r') as csv_file:
            resources = csv.DictReader(csv_file)
            for card in resources:
                name_key = self._get_url_name(card['name'])
                self.cards[name_key] = card
                self.cards[name_key]['category'] = 'Resources'
                self.cards[name_key]['url'] = f'/recipes/{name_key}'
                self.cards[name_key]['png_url'] = url_for(
                    'static',
                    filename=f'img/{name_key}.png'
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
            'inputs': [cards.get_card(card) | {'count': count}
                       for card, count in self.inputs.items()],
            'outputs': [cards.get_card(card) | {'count': count}
                        for card, count in self.outputs.items()],
            'time': self.time,
            'place': self.place
        }


def get_recipes(
        cards: Cards,
        input: str = None,
        output: str = None) -> List[dict]:
    if input:
        recipes = [recipe.to_dict(cards) for recipe in recipes_list
                   if input in recipe.inputs]
    elif output:
        recipes = [recipe.to_dict(cards) for recipe in recipes_list
                   if output in recipe.outputs]
    return recipes


recipes_list = [
    Recipe(
        inputs={'stone': 1, 'wood': 2},
        outputs={'stick': 1},
        time=30,
        place='Desk'),
    Recipe(
        inputs={'wood': 3},
        outputs={'stick': 2},
        time=10,
        place='Desk')
]
