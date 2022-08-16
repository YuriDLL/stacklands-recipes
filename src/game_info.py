import csv
from functools import cached_property
from typing import Any, Dict, Iterable, List

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
        return self._cards[name_key]

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
                card['name_key'] = name_key
                card['category'] = category_name
                if category_name == 'Boosters':
                    card['image_name'] += '_booster'
                    prepare_image(card['image_name'], 'black')
                    card['image_color'] = 'booster'
                else:
                    card['image_name'] = name_key
                    prepare_image(name_key, card['image_color'])
                cards[name_key] = card
        return cards

    def _get_url_name(self, name: str) -> str:
        return name.lower().replace(' ', '_')


class Recipes:

    def __init__(self, cards: Cards) -> None:
        self.cards = cards

    @cached_property
    def _recipes_yaml(self) -> List[dict]:
        recipes_yaml: List[dict] = []
        with open('data/recipes.yaml', 'r') as file:
            recipes_yaml.extend(YAML().load(file))

        with open('data/cards_drop.yaml', 'r') as file:
            drops_yaml: dict = YAML().load(file)
            recipes_yaml.extend(
                self._fill_drops_recipe(drops_yaml)
            )
        with open('data/harvestable.yaml', 'r') as file:
            harvestable_yaml: dict = YAML().load(file)
            recipes_yaml.extend(self._fill_recipe_work(harvestable_yaml))
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
            'chance': round(recipe['chance'] * 100)
            if 'chance' in recipe else None,
        }

    def _fill_drops_recipe(self, drops_yaml) -> list:
        result = []
        for main_card, drop_cards in drops_yaml.items():
            for drop, chance in drop_cards.items():
                result.append({
                    'inp': {main_card: 1},
                    'out': {drop: 1},
                    'chance': chance,
                })
        return result

    def _fill_recipe_work(self,
                          harvestable_yaml: Dict[str, Dict[str, Any]]) -> list:
        recipes: List[Dict] = []
        for harvestable, param in harvestable_yaml.items():
            for card in param['cards']:
                recipes.append({
                    'inp': {harvestable: 1, 'villager': 1},
                    'out': {card: 1},
                    'chance': param['cards'][card],
                    'time': param['time'],
                })

        return recipes
