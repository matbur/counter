from wtforms import Form, RadioField, StringField


class MovesForm(Form):
    move_0_0 = StringField()
    move_0_1 = StringField()
    move_0_2 = StringField()
    move_0_3 = StringField()
    move_0_4 = StringField()
    move_0_5 = StringField()
    move_0_6 = StringField()
    move_0_7 = StringField()
    move_1_0 = StringField()
    move_1_1 = StringField()
    move_1_2 = StringField()
    move_1_3 = StringField()
    move_1_4 = StringField()
    move_1_5 = StringField()
    move_1_6 = StringField()
    move_1_7 = StringField()
    ff_type = RadioField(default='jk',
                         choices=(('jk', 'JK'), ('d', 'D'), ('t', 'T')))
