import random
import string

import gerador


def test_comprimento() -> None:
    comprimento: int = random.randint(4, 50)
    senha: str = gerador.gerar_senha(comprimento)
    assert comprimento == len(senha)


def test_duplicidade() -> None:
    senha_1: str = gerador.gerar_senha(10)
    senha_2: str = gerador.gerar_senha(10)
    assert senha_1 != senha_2


def checar_conteudo(amostra: str, universo: str) -> bool:
    for caractere in universo:
        if caractere in amostra:
            return True
    return False


def test_minusculas() -> None:
    senha_com_minusculas: str = gerador.gerar_senha(
        10, usar_minusculas=True, garantir_minusculas=True
    )
    senha_sem_minusculas: str = gerador.gerar_senha(10, usar_minusculas=False)

    resultado_com_minusculas: bool = checar_conteudo(
        senha_com_minusculas, string.ascii_lowercase
    )
    resultado_sem_minusculas: bool = checar_conteudo(
        senha_sem_minusculas, string.ascii_lowercase
    )

    assert resultado_com_minusculas is True
    assert resultado_sem_minusculas is False


def test_maiusculas() -> None:
    senha_com_maiusculas: str = gerador.gerar_senha(
        10, usar_maiusculas=True, garantir_maiusculas=True
    )
    senha_sem_maiusculas: str = gerador.gerar_senha(10, usar_maiusculas=False)

    resultado_com_maiusculas: bool = checar_conteudo(
        senha_com_maiusculas, string.ascii_uppercase
    )
    resultado_sem_maiusculas: bool = checar_conteudo(
        senha_sem_maiusculas, string.ascii_uppercase
    )

    assert resultado_com_maiusculas is True
    assert resultado_sem_maiusculas is False


def test_numeros() -> None:
    senha_com_numeros: str = gerador.gerar_senha(
        10, usar_numeros=True, garantir_numeros=True
    )
    senha_sem_numeros: str = gerador.gerar_senha(10, usar_numeros=False)

    resultado_com_numeros: bool = checar_conteudo(senha_com_numeros, string.digits)
    resultado_sem_numeros: bool = checar_conteudo(senha_sem_numeros, string.digits)

    assert resultado_com_numeros is True
    assert resultado_sem_numeros is False


def test_especiais() -> None:
    senha_com_especiais: str = gerador.gerar_senha(
        10, usar_especiais=True, garantir_especiais=True
    )
    senha_sem_especiais: str = gerador.gerar_senha(10, usar_especiais=False)

    resultado_com_especiais: bool = checar_conteudo(
        senha_com_especiais, string.punctuation
    )
    resultado_sem_especiais: bool = checar_conteudo(
        senha_sem_especiais, string.punctuation
    )

    assert resultado_com_especiais is True
    assert resultado_sem_especiais is False
