from src.game_info import Cards, Recipes
import flask

app = flask.Flask(__name__)
app.testing = True

cards = Cards()
recipes_loader = Recipes(cards)


@app.route('/recipes/<name>')
def recipes(name=None):
    pass


def test_cards_names() -> None:
    with app.test_request_context('/recipes'):
        for card in cards.iterate():
            name = cards._get_url_name(card['name'])
            recipes_loader.get_recipes(input=name)
            recipes_loader.get_recipes(output=name)
