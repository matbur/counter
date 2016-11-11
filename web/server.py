from flask import Flask, redirect, render_template
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index(r=''):
    if request.method == 'POST':
        return str(dir(request))

    form = MyForm(csrf_enabled=False)
    if form.validate_on_submit():
        return redirect('/')

    return render_template('index.html', form=form)


@app.route('/success', methods=['GET'])
def success():
    return 'success'


if __name__ == '__main__':
    app.run(
        debug=True
    )
