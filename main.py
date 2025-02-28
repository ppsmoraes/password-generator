"""Módulo para geração de senhas alatórias de forma segura."""

import secrets
import string


def gerar_senha(
    comprimento: int,
    usar_maiusculas: bool = True,
    usar_numeros: bool = True,
    usar_especiais: bool = True,
    garantir_miniscula: bool = True,
    garantir_maiuscula: bool = True,
    garantir_numeros: bool = True,
    garantir_especiais: bool = True,
) -> str:
    """
    Função que gera uma senha aletória.

    Parameters
    ----------
    comprimento : int
        Tamanho da senha.
    usar_maiusculas : bool, optional
        Se a senha pode conter letras maiúsculas, por padrão ``True``.
    usar_numeros : bool, optional
        Se a senha pode conter números, por padrão ``True``.
    usar_especiais : bool, optional
        Se a senha pode conter caracteres especiais, por padrão ``True``.
    garantir_miniscula : bool, optional
        Se a senha deve conter letras minúsculas, por padrão ``True``.
    garantir_maiuscula : bool, optional
        Se a senha deve conter letras maiuscúlas, por padrão ``True``.
    garantir_numeros : bool, optional
        Se a senha deve conter números, por padrão ``True``.
    garantir_especiais : bool, optional
        Se a senha deve conter caracteres especiais, por padrão ``True``.

    Returns
    -------
    str
        A senha gerada.
    """
    possiveis: str = string.ascii_lowercase
    escolhidos: list[str] = []
    if garantir_miniscula:
        escolhidos.append(secrets.choice(string.ascii_lowercase))

    if usar_maiusculas:
        possiveis += string.ascii_uppercase
        if garantir_maiuscula:
            escolhidos.append(secrets.choice(string.ascii_uppercase))
    if usar_numeros:
        possiveis += string.digits
        if garantir_numeros:
            escolhidos.append(secrets.choice(string.digits))
    if usar_especiais:
        possiveis += string.punctuation
        if garantir_especiais:
            escolhidos.append(secrets.choice(string.punctuation))

    escolhidos.extend(
        [secrets.choice(possiveis) for _ in range(comprimento - len(escolhidos))]
    )
    secrets.SystemRandom().shuffle(escolhidos)

    senha: str = ''.join(escolhidos)
    return senha


def teste() -> None:
    """Função de teste para utilização somente durante o desenvolvimento."""
    gerar_nova_senha: bool = True
    contador: int = 0
    while gerar_nova_senha:
        senha_segura: str = gerar_senha(
            comprimento=16, usar_especiais=True, garantir_especiais=False
        )
        contador += 1
        gerar_nova_senha = False

        for c in string.punctuation:
            if c in senha_segura:
                gerar_nova_senha = True
                break

    print('Senha geradas:', contador)
    print('Senha final:', senha_segura)


if __name__ == '__main__':
    teste()
