from wtforms import Form, RadioField, StringField


class MovesForm(Form):
    ff_type = RadioField(default='jk',
                         choices=(('jk', 'JK'), ('d', 'D'), ('t', 'T')))

    def get_field(self, x, y):
        field = 'move_{}_{}'.format(x, y)
        return vars(self)[field](maxlength=2)


for i in range(2):
    for j in range(16):
        move = 'move_{}_{}'.format(i, j)
        setattr(MovesForm, move, StringField())
