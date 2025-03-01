"""Módulo que executa as padronizações de código e testes de funcionalidades."""

from subprocess import run
from sys import argv, exit


def run_checks(target: str) -> None:
    """
    Executa isort, black, pydocstyle, mypy e pytest, nesta ordem, no alvo especificado.

    Parameters
    ----------
    target : str
        O arquivo ou diretório alvo.
    """
    commands = [
        ['isort', '--only-modified', target],
        ['black', '--skip-string-normalization', target],
        ['pydocstyle', target],
        ['mypy', '--namespace-packages', '--explicit-package-bases', target],
        ['pytest', '--verbose'],
    ]

    for command in commands:
        result = run(command)
        if result.returncode != 0:
            print(
                f'Command {' '.join(command)} failed with exit code {result.returncode}'
            )
            exit(result.returncode)


if __name__ == '__main__':
    target = argv[1] if len(argv) > 1 else '.'
    run_checks(target)
