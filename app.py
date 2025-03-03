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

import generator


class PasswordGenerator(QWidget):
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
        root_layout: QHBoxLayout = QHBoxLayout()

        # Barra lateral
        sidebar: QGroupBox = QGroupBox('Opções')
        sidebar_layout: QVBoxLayout = QVBoxLayout()

        # Tamanho da senha
        self.length_label: QLabel = QLabel('Tamanho:')
        self.length_input: QSpinBox = QSpinBox()
        self.length_input.setRange(1, 100)
        self.length_input.setValue(8)

        # Checkboxes para as opções
        self.use_lowercase: QCheckBox = QCheckBox('Minúsculas')
        self.use_lowercase.setChecked(True)
        self.use_uppercase: QCheckBox = QCheckBox('Maiúsculas')
        self.use_uppercase.setChecked(True)
        self.use_numbers: QCheckBox = QCheckBox('Números')
        self.use_numbers.setChecked(True)
        self.use_symbols: QCheckBox = QCheckBox('Símbolos')
        self.use_symbols.setChecked(True)

        # Adiciona widgets à barra lateral
        sidebar_layout.addWidget(self.length_label)
        sidebar_layout.addWidget(self.length_input)
        sidebar_layout.addWidget(self.use_lowercase)
        sidebar_layout.addWidget(self.use_uppercase)
        sidebar_layout.addWidget(self.use_numbers)
        sidebar_layout.addWidget(self.use_symbols)
        sidebar_layout.addStretch()
        sidebar.setLayout(sidebar_layout)

        # Conteúdo principal
        main: QGroupBox = QGroupBox('Gerador de Senhas Seguras')
        main_layout: QVBoxLayout = QVBoxLayout()

        # Caixa horizontal para a senha e o botão de copiar
        password_display_layout: QHBoxLayout = QHBoxLayout()

        # A senha gerada
        self.password_display: QLineEdit = QLineEdit()
        self.password_display.setReadOnly(True)

        # Botão para copiar o texto
        self.copy_button: QPushButton = QPushButton(self)
        self.copy_button.setIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditCopy))
        self.copy_button.setIconSize(QSize(16, 16))
        self.copy_button.setFixedSize(24, 24)
        self.copy_button.setToolTip('Copiar')
        self.copy_button.clicked.connect(self.copy_password)

        # Adiciona widgets à linha da senha
        password_display_layout.addWidget(self.password_display)
        password_display_layout.addWidget(self.copy_button)

        # Espaço para feedbacks
        self.feedback_label = QLabel('', self)

        # Botão para gerar uma nova senha
        self.generate_button: QPushButton = QPushButton('Gerar Senha')
        self.generate_button.clicked.connect(self.generate_password)

        # Adiciona widgets ao layout principal
        main_layout.addLayout(password_display_layout)
        main_layout.addWidget(self.feedback_label)
        main_layout.addWidget(self.generate_button)
        main_layout.addStretch()
        main.setLayout(main_layout)

        # Adiciona a barra lateral e o conteúdo principal ao layout raiz
        root_layout.addWidget(sidebar)
        root_layout.addWidget(main)
        self.setLayout(root_layout)

    def generate_password(self) -> None:
        """Método da geração da senha."""
        try:
            password: str = generator.gerar_senha(
                self.length_input.value(),
                usar_minusculas=self.use_lowercase.isChecked(),
                usar_maiusculas=self.use_uppercase.isChecked(),
                usar_numeros=self.use_numbers.isChecked(),
                usar_especiais=self.use_symbols.isChecked(),
            )
            self.password_display.setText(password)
        except ValueError as e:
            self.feedback(e.__str__())

    def copy_password(self) -> None:
        """Método que copiar a senha para a área de transferência."""
        text_to_copy: str = self.password_display.text()

        if len(text_to_copy) == 0:
            self.feedback('Por favor, gere a senha antes de copiar.')
            return

        clipboard: QClipboard = cast(QClipboard, QApplication.clipboard())
        clipboard.setText(text_to_copy)

        self.feedback('Texto copiado!')

    def feedback(self, message: str) -> None:
        """
        Método que retorna uma mensagem para o usuário.

        Parameters
        ----------
        message : str
            A mensagem a ser exibida.
        """
        self.feedback_label.setText(message)
        self.opacity_effect: QGraphicsOpacityEffect = QGraphicsOpacityEffect()
        self.feedback_label.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)

        self.feedback_wait_timer = QTimer()
        self.feedback_wait_timer.setSingleShot(True)
        self.feedback_wait_timer.timeout.connect(self.start_feedback_fade_out)
        self.feedback_wait_timer.start(3000)

    def start_feedback_fade_out(self) -> None:
        """Método que inicia o apagamento do feedback."""
        self.fadeback_step_timer = QTimer()
        self.fadeback_step_timer.timeout.connect(self.feedback_fade_out)
        self.fadeback_step_timer.start(10)

    def feedback_fade_out(self) -> None:
        """Método que apaga gradualmente o feedback."""
        current_opacity: float = self.opacity_effect.opacity()

        if current_opacity > 0:
            self.opacity_effect.setOpacity(current_opacity - 0.02)
        else:
            self.fadeback_step_timer.stop()
            self.feedback_label.setText('')
            self.feedback_label.setGraphicsEffect(None)
