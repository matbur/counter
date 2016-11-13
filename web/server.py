import subprocess
from time import time

from flask import Flask, flash, render_template, request

from latex import create_pdf_file, create_tex_file
from moves_form import MovesForm

app = Flask(__name__)
app.secret_key = 'very secret key'


def parse_key(key):
    return key.split('_')[1:]


def parse_form(data):
    parsed = []
    for key, value in data.items():
        if not value:
            continue
        parsed_key = parse_key(key) + [value]
        parsed.append(tuple(int(i) for i in parsed_key))
    return parsed


def get_pdf(data, file):
    tex_file = file + '.tex'
    moves = parse_form(data)
    print(sorted(moves))
    create_tex_file(moves, tex_file)
    create_pdf_file(tex_file)
    command = 'convert -density 150 {0}.pdf {0}.jpg'.format(file)
    subprocess.call(command, shell=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    ip = 'static/' + request.remote_addr
    form = MovesForm(request.form)
    if request.method == 'POST' and form.validate():
        data = form.data

        if any(data.values()) and all(not i or i.isdigit() for i in data.values()):
            flash(parse_form(form.data))
            get_pdf(data, ip)
        else:
            flash('Serio?')
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
    file = '{}.jpg'.format(request.remote_addr, time())
    return app.send_static_file(file)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        # debug=True
    )
