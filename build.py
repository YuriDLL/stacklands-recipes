from flask_frozen import Freezer
from app import app
import jinja2
from datetime import date

app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_STATIC_IGNORE'] = ['*.scss']

freezer = Freezer(app)

if __name__ == '__main__':
    urls_generator = freezer.freeze_yield()

    urls = [url[1] for url in urls_generator
            if url[0].split('/')[1] != 'static']
    HOME_PAGE = 'https://yuridll.github.io/stacklands-recipes/'
    edit_urls = [(HOME_PAGE + url.replace('\\', '/')) for url in urls]
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates/'))
    template = env.get_template("sitemap.xml")
    with open('build/sitemap.xml', 'w') as file:
        file.write(template.render(urls=edit_urls, date=date.today()))
