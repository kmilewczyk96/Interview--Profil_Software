from app import __app_name__
from app.cli import CommandLineInterface
from app.model import Model


if __name__ == '__main__':
    model = Model(requests_limiter=30)
    controller = CommandLineInterface(model=model)
    controller(prog_name=__app_name__)
