from flask_frozen import Freezer
from app import app


app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_STATIC_IGNORE'] = ['*.scss']

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()
