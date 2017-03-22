from api import index
from api.utils.index import LogManager
from geventwebsocket.handler import WebSocketHandler

import bottle

app = application = bottle.default_app()
app.install(LogManager.log_to_logger)

bottle.run(app=app,
           host='127.0.0.1',
           port=8080,
           reloader=True,
           server='gevent',
           handler_class=WebSocketHandler)
