import os
import sys
from time import time

from flask import Flask, render_template, request

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
from form import MovesForm
from tools import decide

app = Flask(__name__)
app.secret_key = 'very secret key'


@app.route('/', methods=['GET', 'POST'])
def index():
    ip = 'static/' + request.remote_addr
    form = MovesForm(request.form)

    if request.method == 'POST' and form.validate():
        data = form.data
        ff_type = data.pop('ff_type')
        decide(data, ff_type, ip)
    return render_template('index.html', form=form, ts='?{}'.format(time()))


@app.route('/file.<ext>')
def get_file(ext):
    print(ext)
    file = '.'.join((request.remote_addr, ext))
    return app.send_static_file(file)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True
    )
