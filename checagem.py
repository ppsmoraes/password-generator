"""Módulo que executa as padronizações de código e testes de funcionalidades."""

from subprocess import run
from sys import argv, exit


def checar(target: str) -> None:
    """
    Executa isort, black, pydocstyle, mypy e pytest, nesta ordem, no alvo especificado.

    Parameters
    ----------
    target : str
        O arquivo ou diretório alvo.
    """
    comandos = [
        ['isort', '--only-modified', target],
        ['black', '--skip-string-normalization', target],
        ['pydocstyle', target],
        ['mypy', '--namespace-packages', '--explicit-package-bases', target],
        ['pytest', '--verbose'],
    ]

    for comando in comandos:
        resultado = run(comando)
        if resultado.returncode != 0:
            print(
                f'Command {' '.join(comando)} failed with exit code {resultado.returncode}'
            )
            exit(resultado.returncode)


if __name__ == '__main__':
    algo = argv[1] if len(argv) > 1 else '.'
    checar(algo)
