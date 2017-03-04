import bottle

from api import index
from api.utils.logManager import LogManager

app = application = bottle.default_app()
app.install(LogManager.log_to_logger)
bottle.run(reloader=True)

if __name__ == '__main__':
    bottle.run(host='127.0.0.1', port=8000)
