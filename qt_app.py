import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
    QLineEdit,
    QMessageBox,
    QTextEdit,
    QTableWidget,
    QTableWidgetItem,
)
from data_handler import DataHandler


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Visualization Tool")
        self.setGeometry(100, 100, 600, 400)

        self.handler = DataHandler()

        self.load_stylesheet('style.qss')

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.file_path_input = QLineEdit(self)
        self.file_path_input.setPlaceholderText("Enter file path")
        layout.addWidget(self.file_path_input)

        self.load_button = QPushButton("Load File", self)
        self.load_button.clicked.connect(self.load_file)
        layout.addWidget(self.load_button)

        self.display_text = QTextEdit(self)
        layout.addWidget(self.display_text)

        self.dep_var_inp = QLineEdit(self)
        self.dep_var_inp.setPlaceholderText("Dependent Variable")
        layout.addWidget(self.dep_var_inp)

        self.indep_var_inp = QLineEdit(self)
        self.indep_var_inp.setPlaceholderText("Independent Variable")
        layout.addWidget(self.indep_var_inp)

        self.sub_vars_button = QPushButton("Submit Variables", self)
        self.sub_vars_button.clicked.connect(self.submit_variables)
        layout.addWidget(self.sub_vars_button)

        self.table_widget = QTableWidget(self)
        layout.addWidget(self.table_widget)

        # self.setLayout(layout)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_file(self):

        file_path = self.file_path_input.text()

        try:
            self.data = self.handler.load_file(file_path)
            self.display_text.append("Data Loaded Successfully!")
            self.display_columns()

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def display_columns(self):

        try:
            columns = self.handler.get_columns()
            self.display_text.append(f"Columns Available: {columns}")

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def submit_variables(self):

        try:

            dep_vars = self.dep_var_inp.text()
            indep_vars = self.indep_var_inp.text()

            self.handler.set_dependent_variable(dep_vars)
            self.handler.set_independent_variable(indep_vars)

            self.display_text.append(f"Dependent variable: {dep_vars}")
            self.display_text.append(f"Independent variables: {indep_vars}")

            self.disp_sele_var()

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def disp_sele_var(self):
        selec_var = [self.handler.dependent_variable] + \
            self.handler.independent_variable

        selec_data = self.data[selec_var]

        self.table_widget.setRowCount(len(selec_data))
        self.table_widget.setColumnCount(len(selec_var))
        self.table_widget.setHorizontalHeaderLabels(selec_var)

        for r_idx, r_data in selec_data.iterrows():
            for c_idx, c_data in enumerate(selec_var):
                self.table_widget.setItem(
                    r_idx, c_idx, QTableWidgetItem(str(r_data[c_data])))

    def load_stylesheet(self, file_name):
        try:
            with open(file_name, 'r') as file:
                self.setStyleSheet(file.read())
        except FileNotFoundError:
            print(f"Error: QSS file {file_name} not found!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = App()
    main_win.show()
    sys.exit(app.exec_())
