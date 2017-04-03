from bottle import request, abort
from gevent import monkey
from geventwebsocket import WebSocketError
from api.utils.index import LogManager
from api.constants.index import LOG_WEBSOCKETS

monkey.patch_all()


class WebsocketWrapper:
    Error = WebSocketError

    @staticmethod
    def create_service():
        websocket = request.environ.get('wsgi.websocket')
        LogManager.info_log(LOG_WEBSOCKETS + "Connection to a WebSocket")

        if not websocket:
            LogManager.error_log(LOG_WEBSOCKETS + "Connection Failed")
            abort(400, 'Expected WebSocket request.')

        return WebsocketWrapper(websocket)

    def __init__(self, websocket):
        self._websocket = websocket

    def receive(self):
        return self._websocket.receive()

    def send(self, data):
        self._websocket.send(data)

    def __del__(self):
        LogManager.info_log(LOG_WEBSOCKETS + "Closing WebSocket Connection")
