import csv
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List

from flask import url_for
from ruamel.yaml import YAML

from src.image_processing import prepare_image


class Cards(object):

    def __init__(self) -> None:
        self._prepare_cards()

    def get_card(self, name_key: str) -> Dict[str, Any]:
        card = self.cards[name_key].copy()
        card['url'] = url_for('recipes', name=name_key)
        if 'image_name' in card:
            img_name = card.pop('image_name')
        else:
            img_name = name_key
        card['png_url'] = url_for('static',
                                  filename=f'generate/img/{img_name}.png')
        card['ico_url'] = url_for('static',
                                  filename=f'generate/icon/{img_name}.ico')
        return card

    def iterate(self) -> Iterable[Dict[str, Any]]:
        return (self.get_card(key_name) for key_name in self.cards.keys())

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
                if 'image_name' in card:
                    BOOSTER_SUFFIX = '_booster'
                    prepare_image(card['image_name'], 'black', BOOSTER_SUFFIX)
                    card['image_name'] += BOOSTER_SUFFIX
                else:
                    prepare_image(name_key, card['image_color'])

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
    if input:
        find_key = 'inp'
        value = input
    elif output:
        find_key = 'out'
        value = output
    else:
        return []
    recipes: List[dict] = []
    with open('data/recipes.yaml', 'r') as file:
        recipes_yaml: list = YAML().load(file)

        with open('data/boosters_drop.yaml', 'r') as file:
            booster_out_yaml: dict = YAML().load(file)
            for booster in booster_out_yaml:
                recipes_yaml.extend(_fill_recipe_booster(booster, card)
                                    for card in booster_out_yaml[booster])

        recipes.extend(_fill_recipe_cards(recipe, cards)
                       for recipe in recipes_yaml
                       if value in recipe[find_key])
    return recipes


def _fill_recipe_cards(recipe: dict, cards: Cards) -> dict:
    return {
        'inputs': [cards.get_card(card) | {'count': count}
                   for card, count in recipe['inp'].items()],
        'outputs': [cards.get_card(card) | {'count': count}
                    for card, count in recipe['out'].items()],
        'time': recipe['time'] if 'time' in recipe else None,
    }


def _fill_recipe_booster(booster: str, card: str) -> dict:
    return {
        'inp': {booster: 1},
        'out': {card: 1}
    }
