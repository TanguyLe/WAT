import bottle

from api import index

app = application = bottle.default_app()
bottle.run(reloader=True)

if __name__ == '__main__':
    bottle.run(host='127.0.0.1', port=8000)
