from src.game_info import Cards, Recipes
import flask

app = flask.Flask(__name__)
app.testing = True

cards = Cards()
recipes_loader = Recipes(cards)


def test_cards_names() -> None:
    for card in cards.iterate():
        name = cards._get_url_name(card['name'])
        recipes_loader.get_recipes(input=name)
        recipes_loader.get_recipes(output=name)
