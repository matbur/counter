import subprocess

from flask import flash

from latex import create_pdf_file, create_tex_file


def is_valid(data):
    values = data.values()

    def is_item_valid(item):
        return not item or item in map(str, range(8))

    return all(is_item_valid(i) for i in values)


def is_empty(data):
    return not any(data.values())


def decide(data, ff_type, ip):
    if is_empty(data):
        return flash('Tabela jest pusta!')

    if not is_valid(data):
        return flash('Podano złe przejście!')

    create_files(data, ff_type, ip)


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


def create_files(data, ff_type, file):
    tex_file = file + '.tex'
    moves = parse_form(data)

    create_tex_file(moves, ff_type, tex_file)
    create_pdf_file(tex_file)

    command = 'convert -density 150 {0}.pdf -append {0}.jpg'.format(file)
    subprocess.call(command, shell=True)
