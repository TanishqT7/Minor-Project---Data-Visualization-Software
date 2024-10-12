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
    QComboBox,
    QInputDialog,
    QDialog,
    QFormLayout,
)
from data_handler import DataHandler


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Data Visualization Tool")
        self.setGeometry(100, 100, 1280, 720)

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

        self.clean_button = QPushButton("Data Cleaning Options", self)
        self.clean_button.clicked.connect(self.data_cleaning_options)
        layout.addWidget(self.clean_button)

        self.table_widget = QTableWidget(self)
        layout.addWidget(self.table_widget)

        # self.setLayout(layout)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_file(self):

        file_path = self.file_path_input.text()

        try:
            self.main_data_qt = self.handler.load_file(file_path)
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

            self.handler.disp_sel_var()

            self.display_text.append(f"Dependent variable: {dep_vars}")
            self.display_text.append(f"Independent variables: {indep_vars}")

            self.disp_sele_var()

        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))

    def disp_sele_var(self):

        if self.handler.usable_data is None or self.handler.usable_data.empty:
            QMessageBox.critical(self, "Error", "Usable Data is empty or None")
            return

        selec_var = [self.handler.dependent_variable] + \
            self.handler.independent_variable

        try:

            updated_vars = []

            for var in selec_var:
                if var in self.handler.usable_data.columns:
                    updated_vars.append(var)
                else:
                    dummy_vars = [col for col in self.handler.usable_data.columns if col.startswith(var + "_")]
                    updated_vars.extend(dummy_vars)

            self.usable_data_qt = self.handler.usable_data[updated_vars]

            print("Selected Variables: ", updated_vars)
            print("data Preview: \n", self.usable_data_qt.head())

            self.table_widget.clearContents()
            self.table_widget.setRowCount(0)

            self.table_widget.setRowCount(len(self.usable_data_qt))
            self.table_widget.setColumnCount(len(updated_vars))
            self.table_widget.setHorizontalHeaderLabels(updated_vars)

            for r_idx, r_data in self.usable_data_qt.iterrows():
                for c_idx, c_data in enumerate(updated_vars):
                    self.table_widget.setItem(
                        r_idx, c_idx, QTableWidgetItem(str(r_data[c_data])))

            self.table_widget.viewport().update()

            row_count = self.table_widget.rowCount()
            for row_idx in range(row_count - 1, -1, -1):
                empty = True
                for col_idx in range(self.table_widget.columnCount()):
                    item = self.table_widget.item(row_idx, col_idx)
                    if item and item.text().strip():
                        empty = False
                        break
                if empty:
                    self.table_widget.removeRow(row_idx)

        except KeyError as e:
            QMessageBox.critical(
                self, "Error", f"Error Displaying selected variables: {e}")

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Error Displaying selected variables: {e}")
            print(f"Error Refreshing Table: {e}")

    def data_cleaning_options(self):
        options = [
            "Handle Missing Data",
            "Remove Duplicates",
            "Normalize Data",
            "Standardize Data",
            "Encode Categorical Data",
            "Remove Outliers",
        ]

        choice, ok = QInputDialog.getItem(
            self, "Data Cleaning Options", "Select an Option: ", options, 0, False
        )

        if ok and choice:
            if choice == "Handle Missing Data":
                self.handle_missing_data()
            elif choice == "Remove Duplicates":
                self.remove_duplicates()
            elif choice == "Normalize Data":
                self.normalize_data()
            elif choice == "Standardize Data":
                self.standardize_data()
            elif choice == "Encode Categorical Data":
                self.encode_categorical_data()
            elif choice == "Remove Outliers":
                self.remove_outliers()

    def handle_missing_data(self):
        strat, ok = QInputDialog.getItem(
            self, "Handling Missing Data", "Choose Strategy: (Drop / Fill): ", [
                "drop", "fill"], 0, False
        )

        if ok:
            if strat == "fill":
                fill_value, ok_fill = QInputDialog.getText(
                    self, "Fill Value", "Enter Fill Value(mean / median / specific): "
                )
                if ok_fill:
                    self.handler.handle_missing_values(
                        strat="fill", fill_value=fill_value)
                    self.display_text.append(
                        f"Filled missing values using {fill_value}")
            elif strat == "drop":
                self.handler.handle_missing_values(strat="drop")
                self.display_text.append("Dropped missing values")

            print(self.handler.usable_data.head())
            self.disp_sele_var()

    def remove_duplicates(self):
        self.handler.remove_duplicates()
        self.display_text.append("Removed Duplicates")
        self.disp_sele_var()

    def normalize_data(self):

        norm_cols_qt, ok = QInputDialog.getText(
            self, "Normalize Data", "Enter columns to normalize (Comma-Separated): "
        )

        if ok:
            norm_cols_qt = norm_cols_qt.split(",") if norm_cols_qt else None
            norm_cols_qt = [cols.strip() for cols in norm_cols_qt]
            self.handler.normalize_data(columns=norm_cols_qt)
            self.display_text.append("Data Normalized")
            self.disp_sele_var()

    def standardize_data(self):
        stand_cols_qt, ok = QInputDialog.getText(
            self, "Standardize Data", "Enter columns to standardize (Comma-Separated): "
        )

        if ok:
            stand_cols_qt = stand_cols_qt.split(",") if stand_cols_qt else None
            stand_cols_qt = [cols.strip() for cols in stand_cols_qt]
            self.handler.standardize_data(columns=stand_cols_qt)
            self.display_text.append("Data Standardized")
            self.disp_sele_var()

    def encode_categorical_data(self):
        columns, ok = QInputDialog.getText(
            self, "Encode Categorical Data", "Enter columns to encode (Comma-Separated): "
        )

        if ok:
            columns = columns.split(",") if columns else None
            columns = [cols.strip() for cols in columns]
            self.handler.encode_cat_variables(columns=columns)
            self.display_text.append("Categorical Data Encoded")
            self.disp_sele_var()

    def remove_outliers(self):
        z_thresh, ok = QInputDialog.getDouble(
            self, "Remove Outliers", "Enter Z-Threshold for outliers: ", 3.0, 0.1, 10.0, 1
        )

        if ok:
            self.handler.remove_outliers(z_thresh=z_thresh)
            self.display_text.append("Outliers Removed")
            self.disp_sele_var()

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
