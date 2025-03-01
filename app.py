import sys

from PyQt6.QtCore import QSize, QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QGraphicsOpacityEffect,
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
    def __init__(self) -> None:
        super().__init__()

        self.initUI()

    def initUI(self) -> None:
        # Aparência geral
        main_layout: QVBoxLayout = QVBoxLayout()
        self.setWindowTitle('Gerador de Senhas')

        # Título
        self.label: QLabel = QLabel('Gerador de Senhas Seguras')
        main_layout.addWidget(self.label)

        # Entrada para o tamanho da senha
        self.length_input: QSpinBox = QSpinBox()
        self.length_input.setRange(0, 100)
        self.length_input.setValue(8)
        main_layout.addWidget(self.length_input)

        # Caixa horizontal para a senha e o botão de copiar
        h_layout = QHBoxLayout()

        # A senha gerada
        self.password_display: QLineEdit = QLineEdit()
        self.password_display.setReadOnly(True)
        h_layout.addWidget(self.password_display)

        # Botão para copiar o texto
        self.copyButton: QPushButton = QPushButton(self)
        self.copyButton.setIcon(QIcon.fromTheme('edit-copy'))
        self.copyButton.setIconSize(QSize(16, 16))
        self.copyButton.setFixedSize(24, 24)
        self.copyButton.clicked.connect(self.copy_password)
        h_layout.addWidget(self.copyButton)

        # Adiciona o layout horizontal ao layout principal
        main_layout.addLayout(h_layout)

        # Título para feedback
        self.feedbackLabel = QLabel('', self)
        self.feedbackLabel.setStyleSheet('color: white; opacity: 1.0;')
        main_layout.addWidget(self.feedbackLabel)

        # Botão para gerar uma nova senha
        self.generate_button: QPushButton = QPushButton('Gerar Senha')
        self.generate_button.clicked.connect(self.generate_password)
        main_layout.addWidget(self.generate_button)

        self.setLayout(main_layout)

    def generate_password(self) -> None:
        try:
            length: int = int(self.length_input.text())
        except ValueError:
            self.feedbackLabel.setText('Por favor, insira um tamanho de senha válido.')
            return

        password: str = generator.gerar_senha(length)
        self.password_display.setText(password)

    def copy_password(self) -> None:
        text_to_copy: str = self.password_display.text()

        if len(text_to_copy) == 0:
            self.feedbackLabel.setText('Por favor, gere a senha antes de copiar.')
            return

        clipboard = QApplication.clipboard()
        clipboard.setText(text_to_copy)

        # Exibe um feedback ao usuário
        self.feedbackLabel.setText('Texto copiado!')
        self.opacity_effect: QGraphicsOpacityEffect = QGraphicsOpacityEffect()
        self.feedbackLabel.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)

        self.wait_timer = QTimer()
        self.wait_timer.setSingleShot(True)
        self.wait_timer.timeout.connect(self.start_fade_out)
        self.wait_timer.start(2000)

    def start_fade_out(self):
        self.fade_timer = QTimer()
        self.fade_timer.timeout.connect(self.fade_out)
        self.fade_timer.start(10)

    def fade_out(self):
        current_opacity = self.opacity_effect.opacity()

        if current_opacity > 0:
            new_opacity = current_opacity - 0.02
            self.opacity_effect.setOpacity(new_opacity)
        else:
            self.fade_timer.stop()
            self.feedbackLabel.setText('')
            self.feedbackLabel.setGraphicsEffect(None)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PasswordGenerator()
    window.show()
    sys.exit(app.exec())
