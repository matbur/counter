import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
from time import time

from flask import Flask, render_template, request

from moves_form import MovesForm
from parsers import create_files

app = Flask(__name__)
app.secret_key = 'very secret key'


def is_all_valid(data):
    values = data.values()

    def is_valid(item):
        return not item or item in map(str, range(8))

    return any(values) and all(is_valid(i) for i in values)


@app.route('/', methods=['GET', 'POST'])
def index():
    ip = 'static/' + request.remote_addr
    form = MovesForm(request.form)
    if request.method == 'POST' and form.validate():
        data = form.data
        if is_all_valid(data):
            create_files(data, ip)
    return render_template('index.html', form=form, ts='?{}'.format(time()))


@app.route('/file.tex')
def get_tex_file():
    file = request.remote_addr + '.tex'
    return app.send_static_file(file)


@app.route('/file.pdf')
def get_pdf_file():
    file = request.remote_addr + '.pdf'
    return app.send_static_file(file)


@app.route('/file.jpg')
def get_jpg_file():
    file = '{}.jpg'.format(request.remote_addr)
    return app.send_static_file(file)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        # debug=True
    )
