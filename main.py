from latex import create_pdf_file, create_tex_file


def main():
    moves = [
        (0, 0, 1),
        (0, 1, 2),
        (0, 2, 3),
        (0, 3, 6),
        (0, 4, 0),
        (0, 5, 4),
        (0, 6, 5),

        (1, 0, 4),
        (1, 1, 0),
        (1, 2, 1),
        (1, 3, 2),
        (1, 4, 5),
        (1, 5, 6),
        (1, 6, 3),
    ]

    file = 'file.tex'
    create_tex_file(moves, file)
    create_pdf_file(file)


if __name__ == '__main__':
    main()
