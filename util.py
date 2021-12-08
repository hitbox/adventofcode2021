from pathlib import Path

def input_filename(day_number):
    path = Path('inputs') / f'day{day_number:02d}.input.txt'
    return path
