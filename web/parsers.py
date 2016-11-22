import subprocess

from latex import create_pdf_file, create_tex_file


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
