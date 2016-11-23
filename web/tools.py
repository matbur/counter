import os
import random
import string
import sys
from time import time

from flask import flash

sys.path.append(os.path.dirname(__file__) + '/..')
from latex import create_jpg_file, create_pdf_file, create_tex_file


def random_filename():
    return ''.join(random.sample(string.ascii_lowercase, 6))


def get_time():
    return '?{}'.format(time())


def is_valid(data):
    values = data.values()

    def is_item_valid(item):
        return not item or item in map(str, range(8))

    return all(is_item_valid(i) for i in values)


def is_empty(data):
    return not any(data.values())


def decide(data, ff_type, ip):
    if is_empty(data):
        return flash('Tabela jest pusta!', category='warning')

    if not is_valid(data):
        return flash('Podano złe przejście!', category='warning')

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


def error(filetype):
    flash('Nastąpił problem z tworzeniem pliku {}'.format(filetype), category='error')


def create_files(data, ff_type, file):
    tex_file = file + '.tex'
    moves = parse_form(data)

    if create_tex_file(moves, ff_type, tex_file):
        print('Probably you run server from wrong directory')
        return error('TEX')
    if create_pdf_file(tex_file):
        return error('PDF')
    if create_jpg_file(file):
        return error('JPG')
