from flask import Flask, flash, redirect, render_template, request, url_for
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
    print(data)
    l = []
    for k, v in data.items():
        if v:
            kk = parse_key(k)
            kk.append(v)
            l.append(tuple(int(i) for i in kk))
    return l


def get_pdf(data):
    file = 'static/file.tex'
    moves = parse_form(data)
    create_tex_file(moves, file)
    create_pdf_file(file)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MovesForm(request.form)
    if request.method == 'POST' and form.validate():
        get_pdf(form.data)
        flash(sorted(form.data.items())[:8])
        flash(sorted(form.data.items())[8:])
        flash(parse_form(form.data))
        return redirect(url_for('index'))
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True
    )
