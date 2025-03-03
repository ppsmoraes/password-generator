"""Módulo principal do projeto."""

import sys

from PyQt6.QtWidgets import QApplication

from app import GeradorDeSenhas


def main() -> None:
    """Função que inicializa o projeto."""
    aplicativo = QApplication(sys.argv)
    janela = GeradorDeSenhas()
    janela.show()
    sys.exit(aplicativo.exec())


if __name__ == '__main__':
    main()
