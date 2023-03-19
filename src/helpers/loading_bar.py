"""Helper prints loading bar."""

BAR_LENGTH = 50


def print_loading_bar(i: int, total: int, length: int = BAR_LENGTH):
    done, left = i, total - i
    loading_bar = '.' * ((length * done + total - 1) // total)
    loading_bar += ' ' * ((length * left) // total)
    loading_bar += f"\t{i / total * 100:.2f}%"
    print(f"\r{loading_bar}", end='', flush=True)


def print_finished_load_bar(length: int = BAR_LENGTH):
    print_loading_bar(1, 1)
    print()


def print_empty_load_bar(length: int = BAR_LENGTH):
    print_loading_bar(0, 1)
