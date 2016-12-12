from flask import Flask, make_response, render_template, request

from form import MovesForm
from tools import decide, get_time, pop_ff, random_filename, remove_items

app = Flask(__name__)
app.secret_key = 'very secret key'


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MovesForm(request.form)
    fields = {'form': form, 'ts': get_time()}
    resp = make_response(render_template('index.html', **fields))

    # resp.set_cookie('file', expires=0)
    filename = request.cookies.get('file')

    print(request.remote_addr, filename)
    if filename is None:
        filename = random_filename()
        resp.set_cookie('file', filename)

    filename = 'static/generated/' + filename
    if request.method == 'POST':
        data = form.data
        ff_type = pop_ff(data)
        remove_items(data)
        err = decide(data, ff_type, filename)
        if err is not None:
            return err

    return resp


@app.route('/file.<ext>')
def get_file(ext):
    print(ext)
    file = 'generated/{}.{}'.format(request.cookies.get('file'), ext)
    return app.send_static_file(file)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True
    )
