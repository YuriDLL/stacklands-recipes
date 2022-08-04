from flask import Flask, render_template
from src.game_info import Cards, get_recipes

app = Flask(__name__)

cards = Cards()


@app.route('/')
@app.route('/recipes')
def main_page():
    cards_by_category = {}
    for card in cards.iterate():
        category = card['category']
        if category in cards_by_category:
            cards_by_category[category].append(card)
        else:
            cards_by_category[category] = [card]
    return render_template('main_page.jinja', cards=cards_by_category)


@app.route('/recipes/<name>')
def recipes(name=None):
    return render_template(
        'card_templ.jinja',
        card=cards.get_card(name),
        create_recipes=get_recipes(cards, output=name),
        use_recipes=get_recipes(cards, input=name)
    )


if __name__ == '__main__':
    main_page()
