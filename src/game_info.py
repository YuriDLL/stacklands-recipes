import csv
from dataclasses import dataclass
from functools import cached_property
from typing import Any, Dict, Iterable, List

from flask import url_for
from ruamel.yaml import YAML

from src.image_processing import prepare_image


class Cards(object):

    @cached_property
    def _cards(self) -> Dict[str, Dict[str, Any]]:
        cards: Dict[str, Dict[str, Any]] = {}
        cards = cards | self._load_csv('Boosters')
        cards = cards | self._load_csv('Mobs')
        cards = cards | self._load_csv('Resources')
        cards = cards | self._load_csv('Structures')
        cards = cards | self._load_csv('Food')
        cards = cards | self._load_csv('Locations')
        return cards

    def get_card(self, name_key: str) -> Dict[str, Any]:
        card = self._cards[name_key].copy()
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
        return (self.get_card(key_name) for key_name in self._cards.keys())

    def _load_csv(
            self,
            category_name: str) -> Dict[str, Dict[str, Any]]:
        cards: Dict[str, Dict[str, Any]] = {}
        with open(f'data/{category_name.lower()}.csv', 'r') as csv_file:
            resources = csv.DictReader(csv_file)
            for card in resources:
                name_key = self._get_url_name(card['name'])
                cards[name_key] = card
                cards[name_key]['category'] = category_name
                if 'image_name' in card:
                    BOOSTER_SUFFIX = '_booster'
                    prepare_image(card['image_name'], 'black', BOOSTER_SUFFIX)
                    card['image_name'] += BOOSTER_SUFFIX
                    card['image_color'] = 'booster'
                else:
                    prepare_image(name_key, card['image_color'])
        return cards

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


class Recipes:

    def __init__(self, cards: Cards) -> None:
        self.cards = cards

    @cached_property
    def _recipes_yaml(self) -> List[dict]:
        recipes_yaml: List[dict] = []
        with open('data/recipes.yaml', 'r') as file:
            recipes_yaml.extend(YAML().load(file))

        with open('data/boosters_drop.yaml', 'r') as file:
            booster_out_yaml: dict = YAML().load(file)
            for booster in booster_out_yaml:
                recipes_yaml.extend(
                    self._fill_recipe_booster(booster, card)
                    for card in booster_out_yaml[booster]
                )
        with open('data/works.yaml', 'r') as file:
            works_out_yaml: dict = YAML().load(file)
            for factory in works_out_yaml:
                recipes_yaml.extend(
                    self._fill_recipe_work(factory, card)
                    for card in works_out_yaml[factory]
                )
        return recipes_yaml

    def get_recipes(
            self,
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
        recipes = [self._fill_recipe_cards(recipe)
                   for recipe in self._recipes_yaml
                   if value in recipe[find_key]]
        return recipes

    def _fill_recipe_cards(self, recipe: dict) -> dict:
        return {
            'inputs': [self.cards.get_card(card) | {'count': count}
                       for card, count in recipe['inp'].items()],
            'outputs': [self.cards.get_card(card) | {'count': count}
                        for card, count in recipe['out'].items()],
            'time': recipe['time'] if 'time' in recipe else None,
        }

    def _fill_recipe_booster(self, booster: str, card: str) -> dict:
        return {
            'inp': {booster: 1},
            'out': {card: 1}
        }

    def _fill_recipe_work(self, factory: str, card: str) -> dict:
        return {
            'inp': {factory: 1, 'villager': 1},
            'out': {card: 1}
        }
