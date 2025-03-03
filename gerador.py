"""Módulo para geração de senhas alatórias de forma segura."""

import secrets
import string


def gerar_senha(
    comprimento: int,
    *,
    usar_minusculas: bool = True,
    usar_maiusculas: bool = True,
    usar_numeros: bool = True,
    usar_especiais: bool = True,
    garantir_minusculas: bool = True,
    garantir_maiusculas: bool = True,
    garantir_numeros: bool = True,
    garantir_especiais: bool = True,
) -> str:
    """
    Função que gera uma senha aletória.

    Parameters
    ----------
    comprimento : int
        Tamanho da senha.
    usar_minusculas : bool, optional
        Se a senha pode conter letras minúsculas, por padrão ``True``.
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

    Raises
    ------
    ValueError
        Erro quando o tamanho da senha não pode garantir os tipos solicitados.
    """
    possiveis: str = ''
    escolhidos: list[str] = []

    if usar_minusculas:
        possiveis += string.ascii_lowercase
        if garantir_minusculas:
            escolhidos.append(secrets.choice(string.ascii_lowercase))
    if usar_maiusculas:
        possiveis += string.ascii_uppercase
        if garantir_maiusculas:
            escolhidos.append(secrets.choice(string.ascii_uppercase))
    if usar_numeros:
        possiveis += string.digits
        if garantir_numeros:
            escolhidos.append(secrets.choice(string.digits))
    if usar_especiais:
        possiveis += string.punctuation
        if garantir_especiais:
            escolhidos.append(secrets.choice(string.punctuation))

    if comprimento < len(escolhidos):
        raise ValueError(
            f'Não é possível garantir todos os tipos com uma senha de  tamanho {comprimento}.'
        )

    escolhidos.extend(
        [secrets.choice(possiveis) for _ in range(comprimento - len(escolhidos))]
    )
    secrets.SystemRandom().shuffle(escolhidos)

    senha: str = ''.join(escolhidos)
    return senha
