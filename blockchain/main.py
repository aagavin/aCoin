from sanic import Sanic
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic.request import Request

app = Sanic(__name__)


@app.route('/')
async def hello(request: Request) -> HTTPMethodView:
    return json({'success': True, 'request': request.ip})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
