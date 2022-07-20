from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/recipes')
def main_page():
    categories = {
        'Resources': [
            'Wood', 'Stone', 'Bone'
        ],
        'Enemies': [
            'Wolf'
        ]
    }
    cards = {}
    for category in categories:
        cards[category] = {}
        for card in categories[category]:
            card_url = card.lower().replace(' ', '_')
            card_png_url = url_for('static', filename=card_url + '.png')
            cards[category][card] = {
                'url': card_url,
                'png_url': card_png_url
            }
    return render_template('main_page.html', cards=cards)


@app.route('/recipes/<name>')
def recipes(name=None):
    return render_template('hello.html', name=name)
