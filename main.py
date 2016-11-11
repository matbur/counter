from latex import file_footer, file_header, gen_bin_moves, gen_flip_flop, gen_flip_flops, gen_moves, generate_function
from minimization import complete_moves


def main():
    # series = [int(i) for i in '0123654']
    # moves = [(v, series[(i + 1) % len(series)]) for i, v in enumerate(series)]

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

    full_moves = complete_moves(moves)

    to_write = '\n'.join([
        file_header,
        '',
        gen_moves(moves),
        gen_bin_moves(moves),
        gen_flip_flops(moves),
        '',
        gen_flip_flop(full_moves, 'J', 2),
        gen_flip_flop(full_moves, 'K', 2),
        '',
        generate_function(full_moves, 'J', 2),
        '',
        generate_function(full_moves, 'K', 2),
        '',
        gen_flip_flop(full_moves, 'J', 1),
        gen_flip_flop(full_moves, 'K', 1),
        '',
        generate_function(full_moves, 'J', 1),
        '',
        generate_function(full_moves, 'K', 1),
        '',
        gen_flip_flop(full_moves, 'J', 0),
        gen_flip_flop(full_moves, 'K', 0),
        '',
        generate_function(full_moves, 'J', 0),
        '',
        generate_function(full_moves, 'K', 0),
        '',
        file_footer
    ])

    with open('file.tex', 'w') as f:
        f.write(to_write)


if __name__ == '__main__':
    main()
    import subprocess

    subprocess.call('make -B && evince file.pdf', shell=True)
