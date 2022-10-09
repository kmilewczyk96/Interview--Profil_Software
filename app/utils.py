import typer
from time import time


def count_time_execution(func_to_time):
    def wrapper(*args, **kwargs):
        typer.secho('Starting the timer.')
        start = time()
        res = func_to_time(*args, **kwargs)
        finish = time()
        typer.secho(f'Finished in: {(finish - start):.4f}seconds', fg=typer.colors.GREEN)
        return res
    return wrapper
