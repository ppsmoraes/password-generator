"""Módulo do design da aplicação."""

from typing import cast

from PyQt6.QtCore import QSize, QTimer
from PyQt6.QtGui import QClipboard, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QGraphicsOpacityEffect,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

import gerador


class GeradorDeSenhas(QWidget):
    """Classe da janela da aplicação."""

    def __init__(self) -> None:
        """Método de inicialização, agregando a classe pai."""
        super().__init__()
        self.init_UI()

    def init_UI(self) -> None:
        """Método de inicialização da classe."""
        self.setWindowIcon(QIcon.fromTheme(QIcon.ThemeIcon.SystemLockScreen))
        self.setWindowTitle('Gerador de Senhas')

        # Layout principal horizontal
        layout_raiz: QHBoxLayout = QHBoxLayout()

        # Barra lateral
        barra_lateral: QGroupBox = QGroupBox('Opções')
        layout_barra_lateral: QVBoxLayout = QVBoxLayout()

        # Comprimento da senha
        self.etiqueta_comprimento: QLabel = QLabel('Tamanho:')
        self.entrada_comprimento: QSpinBox = QSpinBox()
        self.entrada_comprimento.setRange(1, 100)
        self.entrada_comprimento.setValue(8)

        # Checkboxes para as opções
        self.usar_minusculas: QCheckBox = QCheckBox('Minúsculas')
        self.usar_minusculas.setChecked(True)
        self.usar_maiusculas: QCheckBox = QCheckBox('Maiúsculas')
        self.usar_maiusculas.setChecked(True)
        self.usar_numeros: QCheckBox = QCheckBox('Números')
        self.usar_numeros.setChecked(True)
        self.usar_simbolos: QCheckBox = QCheckBox('Símbolos')
        self.usar_simbolos.setChecked(True)

        # Adiciona widgets à barra lateral
        layout_barra_lateral.addWidget(self.etiqueta_comprimento)
        layout_barra_lateral.addWidget(self.entrada_comprimento)
        layout_barra_lateral.addWidget(self.usar_minusculas)
        layout_barra_lateral.addWidget(self.usar_maiusculas)
        layout_barra_lateral.addWidget(self.usar_numeros)
        layout_barra_lateral.addWidget(self.usar_simbolos)
        layout_barra_lateral.addStretch()
        barra_lateral.setLayout(layout_barra_lateral)

        # Conteúdo principal
        principal: QGroupBox = QGroupBox('Gerador de Senhas Seguras')
        layout_principal: QVBoxLayout = QVBoxLayout()

        # Caixa horizontal para a senha e o botão de copiar
        layout_senha: QHBoxLayout = QHBoxLayout()

        # A senha gerada
        self.local_senha: QLineEdit = QLineEdit()
        self.local_senha.setReadOnly(True)

        # Botão para copiar o texto
        self.botao_copiar: QPushButton = QPushButton(self)
        self.botao_copiar.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditCopy))
        self.botao_copiar.setIconSize(QSize(16, 16))
        self.botao_copiar.setFixedSize(24, 24)
        self.botao_copiar.setToolTip('Copiar')
        self.botao_copiar.clicked.connect(self.copiar_senha)

        # Adiciona widgets à linha da senha
        layout_senha.addWidget(self.local_senha)
        layout_senha.addWidget(self.botao_copiar)

        # Espaço para retornos ao usuário
        self.etiqueta_retorno = QLabel('', self)

        # Botão para gerar uma nova senha
        self.botao_gerar: QPushButton = QPushButton('Gerar Senha')
        self.botao_gerar.clicked.connect(self.gerar_senha)

        # Adiciona widgets ao layout principal
        layout_principal.addLayout(layout_senha)
        layout_principal.addWidget(self.etiqueta_retorno)
        layout_principal.addWidget(self.botao_gerar)
        layout_principal.addStretch()
        principal.setLayout(layout_principal)

        # Adiciona a barra lateral e o conteúdo principal ao layout raiz
        layout_raiz.addWidget(barra_lateral)
        layout_raiz.addWidget(principal)
        self.setLayout(layout_raiz)

    def gerar_senha(self) -> None:
        """Método da geração da senha."""
        try:
            senha: str = gerador.gerar_senha(
                self.entrada_comprimento.value(),
                usar_minusculas=self.usar_minusculas.isChecked(),
                usar_maiusculas=self.usar_maiusculas.isChecked(),
                usar_numeros=self.usar_numeros.isChecked(),
                usar_especiais=self.usar_simbolos.isChecked(),
            )
            self.local_senha.setText(senha)
        except ValueError as e:
            self.retorno(e.__str__())

    def copiar_senha(self) -> None:
        """Método que copiar a senha para a área de transferência."""
        texto_a_copiar: str = self.local_senha.text()

        if len(texto_a_copiar) == 0:
            self.retorno('Por favor, gere a senha antes de copiar.')
            return

        area_de_transferencia: QClipboard = cast(QClipboard, QApplication.clipboard())
        area_de_transferencia.setText(texto_a_copiar)

        self.retorno('Texto copiado!')

    def retorno(self, message: str) -> None:
        """
        Método que retorna uma mensagem para o usuário.

        Parameters
        ----------
        message : str
            A mensagem a ser exibida.
        """
        self.etiqueta_retorno.setText(message)
        self.efeito_de_opacidade: QGraphicsOpacityEffect = QGraphicsOpacityEffect()
        self.etiqueta_retorno.setGraphicsEffect(self.efeito_de_opacidade)
        self.efeito_de_opacidade.setOpacity(1.0)

        self.temporizador_apaga_retorno = QTimer()
        self.temporizador_apaga_retorno.setSingleShot(True)
        self.temporizador_apaga_retorno.timeout.connect(self.inicia_apagamento_retorno)
        self.temporizador_apaga_retorno.start(3000)

    def inicia_apagamento_retorno(self) -> None:
        """Método que inicia o apagamento do feedback."""
        self.temporizador_etapa_apaga_retono = QTimer()
        self.temporizador_etapa_apaga_retono.timeout.connect(self.apaga_retorno)
        self.temporizador_etapa_apaga_retono.start(10)

    def apaga_retorno(self) -> None:
        """Método que apaga gradualmente o feedback."""
        opacidade_atual: float = self.efeito_de_opacidade.opacity()

        if opacidade_atual > 0:
            self.efeito_de_opacidade.setOpacity(opacidade_atual - 0.02)
        else:
            self.temporizador_etapa_apaga_retono.stop()
            self.etiqueta_retorno.setText('')
            self.etiqueta_retorno.setGraphicsEffect(None)
