import subprocess

from flask import Flask, flash, render_template, request
from wtforms import Form, StringField

from latex import create_pdf_file, create_tex_file

app = Flask(__name__)
app.secret_key = 'very secret key'


class MovesForm(Form):
    move_0_0 = StringField('0 0')
    move_0_1 = StringField('0 1')
    move_0_2 = StringField('0 2')
    move_0_3 = StringField('0 3')
    move_0_4 = StringField('0 4')
    move_0_5 = StringField('0 5')
    move_0_6 = StringField('0 6')
    move_0_7 = StringField('0 7')
    move_1_0 = StringField('1 0')
    move_1_1 = StringField('1 1')
    move_1_2 = StringField('1 2')
    move_1_3 = StringField('1 3')
    move_1_4 = StringField('1 4')
    move_1_5 = StringField('1 5')
    move_1_6 = StringField('1 6')
    move_1_7 = StringField('1 7')


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
    file += '.tex'
    moves = parse_form(data)
    print(sorted(moves))
    create_tex_file(moves, file)
    create_pdf_file(file)


def convert_pdf(file):
    command = 'convert -density 300 {0}.pdf {0}.jpg'.format(file)
    subprocess.call(command, shell=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    ip = 'static/' + request.remote_addr
    form = MovesForm(request.form)
    if request.method == 'POST' and form.validate():
        data = form.data
        if any(data.values()):
            flash(parse_form(form.data))
            get_pdf(data, ip)
            convert_pdf(ip)
        else:
            flash('Serio?')
    return render_template('index.html', form=form)


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
    file = request.remote_addr + '.jpg'
    return app.send_static_file(file)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True
    )
