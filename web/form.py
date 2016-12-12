from wtforms import BooleanField, Form, RadioField, SubmitField
from wtforms.fields.html5 import IntegerField, IntegerRangeField

MAX_MOVE = 16


class MovesForm(Form):
    is_z = BooleanField('Czy jest sygnał Z?')
    num = IntegerRangeField('Ile jest stanów?')
    ff_type = RadioField('Jaki jest typ przerzutnika?',
                         default='jk',
                         choices=(('jk', 'JK'), ('d', 'D'), ('t', 'T')))
    solve = SubmitField('SOLVE!')

    def get_field(self, x, y):
        field = 'move_{}_{}'.format(x, y)
        return vars(self)[field](min=0, max=MAX_MOVE - 1)


for i in range(2):
    for j in range(MAX_MOVE):
        move = 'move_{}_{}'.format(i, j)
        setattr(MovesForm, move, IntegerField())
