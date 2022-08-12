from flask import Flask, render_template
from src.game_info import Cards, Recipes
from flask_assets import Environment, Bundle

app = Flask(__name__)

assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('scss/index.scss', filters='pyscss')

css = Bundle(
    scss, 
    # 'css/anim_main.css',
    # 'css/style_main_page.css',
    filters='cssmin', 
    output='generate/index.css')

assets.register('css_all', css)

cards = Cards()
recipes_list = Recipes(cards)


@app.route('/')
@app.route('/recipes')
def home_page():
    cards_by_category = {}
    for card in cards.iterate():
        category = card['category']
        if category in cards_by_category:
            cards_by_category[category].append(card)
        else:
            cards_by_category[category] = [card]
    return render_template('home.jinja', cards=cards_by_category)


@app.route('/recipes/<name>')
def recipes(name=None):
    return render_template(
        'card_templ.jinja',
        card=cards.get_card(name),
        create_recipes=recipes_list.get_recipes(output=name),
        use_recipes=recipes_list.get_recipes(input=name)
    )


if __name__ == '__main__':
    home_page()
