import click

from . import main


class PlusCalculator(object):
    """
    The class which to compute `a + b`.

    We place the logic of `a + b` in this class, so as to demonstrate how we
    can separate the testing of the main functionality and the CLI interface
    by using the Mock framework in "tests/mlrun/test_plus_cmd.py".
    """

    def compute(self, a, b):
        return a + b


@main.command()
@click.option('-a', type=click.INT, required=True, help="The number a")
@click.option('-b', type=click.INT, required=True, help="The number b")
def plus(a, b):
    """Compute a + b"""
    click.echo('{}'.format(PlusCalculator().compute(a, b)))
