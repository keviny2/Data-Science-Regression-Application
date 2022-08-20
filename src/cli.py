import click
import src.RegressionApp

@click.command(name='run')
def run(**kwargs):
    src.RegressionApp.run(**kwargs)

@click.group(name='regression-app')
def main():
    pass

main.add_command(run)
