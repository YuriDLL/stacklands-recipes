from flask import Flask, render_template
from src.game_info import Cards, get_recipes

app = Flask(__name__)


@app.route('/')
@app.route('/recipes')
def main_page():
    cards = Cards()
    cards_by_category = {}
    for name_key, info in cards.iterate():
        category = info['category']
        if category in cards_by_category:
            cards_by_category[category].append(info)
        else:
            cards_by_category[category] = [info]
    return render_template('main_page.jinja', cards=cards_by_category)


@app.route('/recipes/<name>')
def recipes(name=None):
    cards = Cards()
    create_recipes = get_recipes(cards, output=name)
    return render_template(
        'card_templ.jinja',
        card=cards.get_card(name),
        create_recipes=create_recipes
    )


if __name__ == '__main__':
    main_page()
