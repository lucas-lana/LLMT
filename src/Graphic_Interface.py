from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QLabel, QLineEdit, QPushButton, QFileDialog, QProgressBar
from PySide6.QtCore import QThread, Signal
import main as mn  # Importa o módulo com a função de transcrição

class TranscriptionWorker(QThread):
    """
    Thread para executar a tarefa demorada (transcrição).
    Emite sinais para indicar o progresso e a conclusão.
    """
    finished = Signal()  # Sinal emitido quando a tarefa é concluída
    canceled = Signal()  # Sinal emitido quando a tarefa é cancelada

    def __init__(self, folder1_path, folder2_path, modelos):
        super().__init__()
        self.folder1_path = folder1_path
        self.folder2_path = folder2_path
        self.modelos = modelos

    def run(self):
        # Executa a função de transcrição do módulo 'main'
        print("Iniciando transcrição...")
        print(f"Modelos selecionados: {self.modelos}")
        print(f"Pasta 1: {self.folder1_path}")
        print(f"Pasta 2: {self.folder2_path}")
        
        try:
            # Chama a função de transcrição do módulo 'main'
            mn.start(self.folder1_path, self.folder2_path, self.modelos)
            print("Transcrição concluída!")
            self.finished.emit()  # Emite o sinal de conclusão
        except Exception as e:
            print(f"Erro durante a transcrição: {e}")
            self.canceled.emit()  # Emite o sinal de cancelamento em caso de erro

    def cancel(self):
        print("Cancelando transcrição...")
        self.terminate()  # Interrompe a thread

class CheckBoxWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Configurações da janela
        self.setWindowTitle("Aplicação de Transcrição de Áudios")
        self.setGeometry(100, 100, 400, 500)
        # Layout principal
        layout = QVBoxLayout()
        # Label para exibir as seleções
        self.result_label = QLabel("Escolha os modelos a serem rodados:")
        layout.addWidget(self.result_label)
        # Criar os checkboxes
        self.checkbox1 = QCheckBox("Simple Vosk")
        self.checkbox2 = QCheckBox("Complete Vosk")
        self.checkbox3 = QCheckBox("Speech Recognition")
        
        self.checkbox1.setChecked(True)
        self.checkbox2.setChecked(True)
        self.checkbox3.setChecked(True)
        
        # Conectar os checkboxes a uma função que atualiza o label e verifica o botão
        self.checkbox1.stateChanged.connect(self.check_button_state)
        self.checkbox2.stateChanged.connect(self.check_button_state)
        self.checkbox3.stateChanged.connect(self.check_button_state)
        # Adicionar os checkboxes ao layout
        layout.addWidget(self.checkbox1)
        layout.addWidget(self.checkbox2)
        layout.addWidget(self.checkbox3)
        # Área para selecionar pastas
        self.folder1_line_edit = QLineEdit()
        self.folder1_line_edit.setReadOnly(True)
        self.folder1_button = QPushButton("Pasta Origem dos Áudios")
        self.folder1_button.clicked.connect(lambda: self.select_folder(self.folder1_line_edit))
        self.folder2_line_edit = QLineEdit()
        self.folder2_line_edit.setReadOnly(True)
        self.folder2_button = QPushButton("Pasta Destino das Transcrições")
        self.folder2_button.clicked.connect(lambda: self.select_folder(self.folder2_line_edit))
        # Adicionar os campos de seleção de pastas ao layout
        layout.addWidget(self.folder1_button)
        layout.addWidget(self.folder1_line_edit)
        layout.addWidget(self.folder2_button)
        layout.addWidget(self.folder2_line_edit)
        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(0)  # Indeterminada inicialmente
        self.progress_bar.hide()  # Inicialmente oculta
        layout.addWidget(self.progress_bar)
        # Label de status
        self.status_label = QLabel("Status: Escolha os modelos e as pastas...")
        layout.addWidget(self.status_label)
        # Botão "Gerar Transcrição"
        self.generate_button = QPushButton("Gerar Transcrição")
        self.generate_button.setEnabled(False)  # Inicialmente desabilitado
        self.generate_button.clicked.connect(self.start_transcription)
        layout.addWidget(self.generate_button)
        # Definir o layout para a janela
        self.setLayout(layout)
        # Chamar check_button_state para verificar o estado inicial do botão
        self.check_button_state()

    def update_selection(self):
        """Atualiza o label com base nas opções selecionadas."""
        selected_options = []
        if self.checkbox1.isChecked():
            selected_options.append("Simple Vosk")
        if self.checkbox2.isChecked():
            selected_options.append("Complete Vosk")
        if self.checkbox3.isChecked():
            selected_options.append("Speech Recognition")
        if selected_options:
            self.result_label.setText(f"Selecionado: {', '.join(selected_options)}")
        else:
            self.result_label.setText("Nenhuma opção selecionada.")

    def select_folder(self, line_edit):
        """Abre o diálogo de seleção de pasta e atualiza o campo correspondente."""
        folder = QFileDialog.getExistingDirectory(self, "Selecione uma Pasta")
        if folder:  # Se o usuário selecionou uma pasta
            line_edit.setText(folder)
            self.check_button_state()  # Verifica o estado do botão após selecionar a pasta

    def check_button_state(self):
        """Verifica se o botão 'Gerar Transcrição' deve ser habilitado."""
        at_least_one_checkbox_checked = (
            self.checkbox1.isChecked() or
            self.checkbox2.isChecked() or
            self.checkbox3.isChecked()
        )
        both_folders_selected = (
            bool(self.folder1_line_edit.text()) and
            bool(self.folder2_line_edit.text())
        )
        self.generate_button.setEnabled(at_least_one_checkbox_checked and both_folders_selected)

    def get_selected_data(self):
        """Coleta os dados dos modelos selecionados e os caminhos das pastas."""
        selected_models = []
        if self.checkbox1.isChecked():
            selected_models.append("Simple Vosk")
        if self.checkbox2.isChecked():
            selected_models.append("Complete Vosk")
        if self.checkbox3.isChecked():
            selected_models.append("Speech Recognition")
        folder1_path = self.folder1_line_edit.text()
        folder2_path = self.folder2_line_edit.text()
        return selected_models, folder1_path, folder2_path

    def start_transcription(self):
        """Inicia a transcrição e ativa a barra de progresso."""
        # Coleta os dados
        selected_models, folder1_path, folder2_path = self.get_selected_data()
        # Calcula o valor dos modelos
        modelos = 0
        for i in selected_models:
            if i == "Simple Vosk":
                modelos += 1
            elif i == "Complete Vosk":
                modelos += 2
            elif i == "Speech Recognition":
                modelos += 4
            else:
                print("Nenhum modelo selecionado")
        # Mostra a barra de progresso
        self.progress_bar.show()
        # Atualiza o status
        self.status_label.setText("Status: Gerando...")
        # Desabilita o botão de gerar transcrição
        self.generate_button.setEnabled(False)
        # Desabilita os botões de seleção de pastas
        self.folder1_button.setEnabled(False)
        self.folder2_button.setEnabled(False)
        # Desabilita os checkboxes
        self.checkbox1.setEnabled(False)
        self.checkbox2.setEnabled(False)
        self.checkbox3.setEnabled(False)
        # Inicia a thread de transcrição
        self.worker = TranscriptionWorker(folder1_path, folder2_path, str(modelos))
        self.worker.finished.connect(self.on_transcription_finished)
        self.worker.canceled.connect(self.on_transcription_canceled)
        self.worker.start()

    def on_transcription_finished(self):
        """Ação a ser tomada quando a transcrição é concluída."""
        self.progress_bar.hide()
        self.status_label.setText("Status: Transcrição concluída! Escolha novas pastas e modelos.")
        self.generate_button.setEnabled(True)
        self.folder1_button.setEnabled(True)
        self.folder2_button.setEnabled(True)
        self.checkbox1.setEnabled(True)
        self.checkbox2.setEnabled(True)
        self.checkbox3.setEnabled(True)

    def on_transcription_canceled(self):
        """Ação a ser tomada quando a transcrição é cancelada."""
        self.progress_bar.hide()
        self.status_label.setText("Status: Transcrição cancelada!")
        self.generate_button.setEnabled(True)
        self.folder1_button.setEnabled(True)
        self.folder2_button.setEnabled(True)
        self.checkbox1.setEnabled(True)
        self.checkbox2.setEnabled(True)
        self.checkbox3.setEnabled(True)

def interface():
    app = QApplication([])
    window = CheckBoxWindow()
    window.show()
    app.exec()