from sanic import Sanic
from sanic import response
from jinja2 import Environment, PackageLoader, select_autoescape

import sys

# Enabling async template execution which allows you to take advantage
# of newer Python features requires Python 3.6 or later.
enable_async = sys.version_info >= (3, 6)

app = Sanic(__name__)

# Load the template environment with async support
template_env = Environment(
    loader=PackageLoader('jinja_example', 'templates', 'index'),  # 所需文件
    autoescape=select_autoescape(['html', 'xml']),
    enable_async=enable_async
)

# Load the template from file
template = template_env.get_template("example_template.html")


@app.route('/')
async def test(request):
    rendered_template = await template.render_async(
        knights='YuanJie')
    return response.html(rendered_template)


app.run(host="0.0.0.0", port=8000, debug=True)
