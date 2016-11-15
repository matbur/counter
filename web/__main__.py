import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')

from server import app


if __name__ == '__main__':
    app.run(host='0.0.0.0')
